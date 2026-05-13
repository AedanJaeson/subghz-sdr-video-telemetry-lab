# ESP32-CAM And CC1101 Design

## Current Status

No firmware implementation yet. Hardware variant verification comes first.

## CC1101 Checks

- Verify frequency variant from module marking, seller listing, or measurement.
- Confirm pinout.
- Confirm 3.3 V operation only.
- Record antenna connector and matching network assumptions if known.

## ESP32-CAM Checks

- Record exact board type.
- Record flashing method.
- Identify available SPI pins that do not conflict with camera, SD card, flash, boot strapping, or serial upload.

## Frame Budget Table

| Resolution | JPEG quality | Average size | Estimated packets | Estimated transmit time | Rough FPS ceiling |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

