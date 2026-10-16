#!/usr/bin/env python3
"""Read-only structural validation for experimental Makerdiary nRF52840 UF2.

Verifies family ID, complete block set, application-only addresses, and
the initial ARM vector table. This does NOT prove the firmware works or that
it is safe to flash on a particular physical board.
"""
import struct
import sys
from pathlib import Path

MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30
FAMILY_FLAG = 0x00002000
NRF52840_FAMILY = 0xADA52840
APP_START = 0x1000
SETTINGS_START = 0xEC000
RAM_START = 0x20000000
RAM_END = 0x20040000


def main(path):
    data = Path(path).read_bytes()
    if not data or len(data) % 512:
        raise ValueError("UF2 size is not a nonzero multiple of 512")
    expected_blocks = len(data) // 512
    seen = set()
    first_block = None
    lowest = 1 << 32
    highest = 0

    for index in range(expected_blocks):
        block = data[index * 512 : (index + 1) * 512]
        magic0, magic1, flags, addr, payload_size, block_no, num_blocks, family = struct.unpack_from("<8I", block)
        final_magic = struct.unpack_from("<I", block, 508)[0]
        if (magic0, magic1, final_magic) != (MAGIC_START0, MAGIC_START1, MAGIC_END):
            raise ValueError(f"Invalid UF2 magic in block {index}")
        if not flags & FAMILY_FLAG or family != NRF52840_FAMILY:
            raise ValueError(f"Wrong or missing family ID in block {index}: flags={flags:#x}, family={family:#x}")
        if num_blocks != expected_blocks or block_no in seen or block_no >= expected_blocks:
            raise ValueError(f"Duplicate/missing/invalid block numbering at {index}")
        if payload_size != 256 or addr % 256:
            raise ValueError(f"Unexpected block payload or alignment at {index}")
        if addr < APP_START or addr + payload_size > SETTINGS_START:
            raise ValueError(f"UF2 block {index} writes outside application area at {addr:#x}")
        seen.add(block_no)
        lowest = min(lowest, addr)
        highest = max(highest, addr + payload_size)
        if addr == APP_START:
            first_block = block[32 : 32 + payload_size]

    if len(seen) != expected_blocks or lowest != APP_START or first_block is None:
        raise ValueError("Incomplete UF2 block sequence or application start mismatch")
    stack_ptr, reset_vector = struct.unpack_from("<II", first_block)
    if not (RAM_START < stack_ptr <= RAM_END and stack_ptr % 8 == 0):
        raise ValueError(f"Invalid initial stack pointer: {stack_ptr:#x}")
    if not ((reset_vector & 1) and APP_START <= (reset_vector & ~1) < SETTINGS_START):
        raise ValueError(f"Invalid reset vector: {reset_vector:#x}")

    print(f"UF2 block count: {expected_blocks}")
    print(f"UF2 family: {NRF52840_FAMILY:#010x} (nRF52840)")
    print(f"Application address range: {lowest:#010x} - {highest - 1:#010x}")
    print(f"Initial stack pointer: {stack_ptr:#010x}")
    print(f"Reset vector: {reset_vector:#010x}")
    print(f"Protected settings: {SETTINGS_START:#010x} onward")
    print("PASS: UF2 structural checks. NOT a physical-device safety certification.")


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except (IndexError, ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
