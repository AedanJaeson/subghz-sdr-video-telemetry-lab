# CC1101 Bring-Up Log

## 2026-05-26 - ESP32-CAM To CC1101 SPI/Register Check

| Field | Value |
| --- | --- |
| Controller | ESP32-CAM bare module |
| USB serial adapter | HW-409 / CP210x on COM4 |
| Radio module | CC1101 module |
| Firmware path | `firmware/esp32cam_cc1101/src/main.cpp` |
| Framework | PlatformIO, Arduino framework, RadioLib |
| Frequency configured in firmware | 433.920 MHz |
| TX enabled? | No, `CC1101_TRANSMIT_ENABLED=0` |
| Result | Pass: SPI/register access and RadioLib init succeeded |

## Wiring Used

| CC1101 | ESP32-CAM |
| --- | --- |
| GND | GND |
| VCC | 3V3 |
| SCK | GPIO14 |
| MISO / SO | GPIO12 |
| MOSI / SI | GPIO13 |
| CSN | GPIO15 |
| GDO0 | GPIO2 |
| GDO2 | Disconnected |

## Observed Serial Output

```text
ESP32-CAM CC1101 staged bring-up
Flash LED: GPIO4
Safety: confirm local rules, legal band, verified module variant, low power, and antenna before TX.

CC1101 bring-up
Mode: SPI/register check first; RF TX gated by build flag.
Configured frequency MHz: 433.920
Transmit enabled: NO
CC1101 PARTNUM read OK
CC1101 PARTNUM=0x0
CC1101 VERSION read OK
CC1101 VERSION=0x14
RadioLib CC1101 init ... success
CC1101 SPI OK
heartbeat 1 millis=2235 led=on
```

## Notes

- `VERSION=0x14` and `RadioLib CC1101 init ... success` confirm the ESP32-CAM can talk to the CC1101 over SPI.
- Transmit remains disabled in firmware. The next RF step requires the safety/legal checklist, antenna connection, verified module band, and deliberate build flag change.
- `PARTNUM=0x0` is expected for CC1101 on many modules; the successful RadioLib init is the stronger check.

