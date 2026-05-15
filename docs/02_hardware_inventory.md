# Hardware Inventory

Use this file to record verified hardware. Unknowns should stay marked `TBD` until checked from silkscreen, receipts, datasheets, or direct testing. Items not yet purchased should be marked `To Buy`.

| Item | Status | Notes |
| --- | --- | --- |
| Nooelec NESDR SMArt v5 | Owned | RTL2832U + R820T2/R860 style RTL-SDR, approx. 100 kHz to 1.75 GHz, 0.5 ppm TCXO. Standard SMArt v5 does not have an always-on bias tee. |
| Antennas in Nooelec kit | Owned | Telescopic Whip, 433 Mhz Antenna, UHF Antenna |
| ESP32-CAM with OV2640 | TBD | Record exact board variant and flash method. |
| CC1101 module | Ordered / blocked | Ordered from AliExpress. Expected delivery: 2026-05-27. Verify frequency variant before any transmit work. Do not assume 433/868/915 MHz. |
| USB data cable | TBD | Confirm data-capable cable, not charge-only. |
| Powered USB hub | Optional/TBD | Useful if laptop USB power is unstable. |
| Second CC1101 | Optional/TBD | Useful for standalone packet-link debugging. |
| Attenuators / dummy load / shielding | Optional/TBD | Preferred for controlled bench tests. |
| SMA adapters | Optional/TBD | Record connector chain and losses if known. |

## Current Hardware Blockers

As of 2026-05-15, CC1101 RF transmit/receive tasks are blocked until the module arrives. AliExpress currently lists expected delivery by 2026-05-27.

Do not wait on the module for the rest of the project. Work that can continue now:

- SDR receive-only bring-up and IQ capture workflow.
- Python packet framing, CRC, and file reconstruction tests.
- JPEG/image chunking simulation.
- ESP32-CAM still-image capture and frame-size budget, if the ESP32-CAM is available.
- Serial or file-loopback packet tests that prove image serialization before any RF transmission.

## Nooelec Kit Antennas

| Antenna | Type | Frequency Range | Gain | Best Use / Notes | Which one in your photo |
| --- | --- | --- | --- | --- | --- |
| Telescopic Whip | Adjustable-length whip | ~100–800 MHz (depends on length) | Not specified (broadband) | General VHF/UHF scanning, most versatile starter antenna | Left (with spring/coil base) |
| 433 MHz Antenna | Fixed-length (long black) | 433 MHz ISM band | ~3 dBi | Useful if the CC1101 module is a 433 MHz variant and the test is legal for the location. | Right (straight, longer one) |
| UHF Antenna | Fixed-length (short black) | 800–2200 MHz | ~5 dBi | UHF / 3G / higher frequencies (e.g. ADS-B at 1090 MHz) | The remaining one (often right-angle in some kits) |

## Provisional ESP32-CAM to CC1101 Wiring Plan

This wiring plan is provisional until the ordered CC1101 module arrives and its exact pinout/frequency variant are verified. Do not treat this as final build wiring yet.

| CC1101 Pin | ESP32-CAM Pin | Notes |
| --- | --- | --- |
| VCC | 3V3 | 3.3 V only – never 5 V |
| GND | GND | Any ground pad |
| SCK | IO14 | HSPI clock |
| MOSI | IO13 | SPI data in to CC1101 |
| MISO | IO12 | SPI data out (boot pin – must be LOW at reset, which it normally is) |
| CSn | IO15 | Chip Select |
| GDO0 | IO2 | Main interrupt / packet ready (important) |
| GDO2 | IO16 | Optional second interrupt (can leave unconnected for first tests) |

### Important Board Notes

- **MicroSD Card Slot:** You will lose the microSD card slot (pins IO12–15 are shared). That’s fine — we’re streaming over RF instead of saving to card.
- **Flash LED:** The white flash LED is on IO4 — we are not using IO4, so ignore it (or desolder the LED later if you want the pin back).
- **Power Supply:** Power the whole thing from a good 5 V / 1 A+ USB supply (the onboard USB connector is fine). The CC1101 draws extra current when transmitting.

### Physical Connection (Step-by-Step)

**1. Solder headers to the ESP32-CAM (one-time job):**
- Get a strip of 2.54 mm male pin headers (cheap on AliExpress / Jaycar / etc.).
- Snap off two rows of ~8–10 pins each.
- Insert from the bottom of the board so the long pins stick out downward.
- Solder from the top side. Tack one pin first, make sure the header is straight, then do the rest.

**2. Connect with jumper wires:**
- Use female-to-female Dupont wires (or male-to-female if you soldered male headers).
- Match the table above exactly.

**3. Antenna:**
- Screw the black rubber-duck antenna (the long one from your Nooelec kit) onto the gold SMA connector on the CC1101.
- **Never transmit without an antenna — it can damage the chip.**
