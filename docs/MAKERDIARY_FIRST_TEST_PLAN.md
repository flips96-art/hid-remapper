# Makerdiary nRF52840 / Flipper Momentum — preflight and first-test plan

**Status (2026-10-18): NOT FLASHED. Experimental. Do not bypass browser malware blocking.**

## Verified before this checklist

- Dongle identification from INFO_UF2.TXT: `nRF52840-MDK-USB-DONGLE`; UF2 bootloader 0.7.1, Jul 20 2023; reports `SoftDevice: S132 5.1.0`.
- Firmware branch: `makerdiary-uf2-experiment` (do not merge into master while testing).
- Latest firmware build #9: https://github.com/flips96-art/hid-remapper/actions/runs/39096517313
- Latest build #9 artifact ID 12124618016, name `makerdiary-uf2-EXPERIMENTAL-DO-NOT-FLASH`. Do not confuse with older builds.
- Build #9 passes UF2 block/flash region checks and Kconfig checks that avoid UICR reset-pin reconfiguration. This is **not** a guarantee of correct runtime behavior or reliable recovery.
- ClamAV scanned the exact build #9 firmware in https://github.com/flips96-art/hid-remapper/actions/runs/39096868117; no known malware detected. This does **not** clear Firefox's separate explicit malware warning.
- Makerdiary vendor docs: https://wiki.makerdiary.com/nrf52840-mdk-usb-dongle/programming/uf2boot/
- Reports of firmware updates not taking effect on some dongles with matching INFO_UF2 fields: https://github.com/makerdiary/nrf52840-mdk-usb-dongle/issues/120 and https://github.com/makerdiary/nrf52840-mdk-usb-dongle/issues/114 . One report identified wrong `0x2000` conversion offset; our build uses vendor-documented `0x1000`.
- Firefox blocked the GitHub-hosted ZIP as malware. The precise detection or URL reputation reason remains **unknown**.

## Next session: preflight before ANY flash

1. Confirm we are on a **personal**, non-school Windows PC. A spare PC is optional, not required.
2. Confirm the original Makerdiary application backup `connectivity_4.1.4_usb_with_s132_5.1.0.uf2` remains available. This is only an **application** recovery option if UF2 bootloader remains accessible; it does not reinstall a damaged bootloader.
3. Investigate / resolve Firefox's security warning through a legitimate review/report or clearly documented, authorized trusted distribution route. **Do not disable browser protections, force-allow a malware-blocked file, rename archives to evade scanning, or put a blocked file on a work/school machine.**
4. Before touching the hardware, review the button's two functions: entering UF2 mode while plugging it in, and application pairing. The source currently aliases the single Makerdiary button to remapper `sw0`. Ensure returning to UF2 mode remains possible independently of the running application.
5. Plan rollback: if app won't enumerate, try unplugging and (while holding button) reinserting it to get `UF2BOOT`. If `UF2BOOT` doesn't return, the original application backup alone may be insufficient; recovery might require SWD programmer.
6. **Do not proceed to flashing until user explicitly decides to accept the experiment's recovery risk.**

## Only after resolved security warning and go-ahead

1. Keep Flipper disconnected / do not run Bluetooth keyboard scripts; close sensitive documents.
2. Verify correct, trusted build #9 `.uf2`, file fingerprint, and board ID. Do not use previous builds.
3. Follow Makerdiary's documented UF2 application installation in its hardware documentation, observing any write errors.
4. On reconnection, check whether Windows sees `HID Remapper Bluetooth` as a USB HID device. Use a benign text-only test, not DuckyScript / BadUSB.
5. If USB works, test Bluetooth pairing separately, then a simple harmless typed string with a user-approved Flipper keyboard mode.
6. If anything unexpected occurs, unplug the dongle and reassess before further flashes.

## What we do NOT yet know

- Whether the custom firmware boots and enumerates on this specific physical dongle.
- Whether Bluetooth keyboard pairing works with the currently installed Flipper Momentum firmware.
- Why Firefox blocked the GitHub Actions ZIP.
- Whether USB DFU recovery remains operational after an unsuccessful application flash on this hardware revision.
