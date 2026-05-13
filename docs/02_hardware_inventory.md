# Hardware Inventory

Use this file to record verified hardware. Unknowns should stay marked `TBD` until checked from silkscreen, receipts, datasheets, or direct testing.

| Item | Status | Notes |
| --- | --- | --- |
| Nooelec NESDR SMArt v5 | Owned/TBD | RTL2832U + R820T2/R860 style RTL-SDR, approx. 100 kHz to 1.75 GHz, 0.5 ppm TCXO. Standard SMArt v5 does not have an always-on bias tee. |
| Antennas in Nooelec kit | TBD | Record antenna types and connector/adapters. |
| ESP32-CAM with OV2640 | TBD | Record exact board variant and flash method. |
| CC1101 module | TBD | Verify frequency variant before any transmit work. Do not assume 433/868/915 MHz. |
| USB data cable | TBD | Confirm data-capable cable, not charge-only. |
| Powered USB hub | Optional/TBD | Useful if laptop USB power is unstable. |
| Second CC1101 | Optional/TBD | Useful for standalone packet-link debugging. |
| Attenuators / dummy load / shielding | Optional/TBD | Preferred for controlled bench tests. |
| SMA adapters | Optional/TBD | Record connector chain and losses if known. |

## Wiring Assumptions To Verify

- CC1101 logic is 3.3 V only.
- ESP32-CAM GPIO availability varies by board and camera wiring.
- SPI pins must be chosen around camera, SD card, flash, boot strapping, and serial upload constraints.

