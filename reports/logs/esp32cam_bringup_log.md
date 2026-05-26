# ESP32-CAM Bring-Up Log

## 2026-05-26 - HW-409 Flash And GPIO4 Smoke Test

| Field | Value |
| --- | --- |
| Board | ESP32-CAM bare module |
| USB serial adapter | HW-409 / CP210x on COM4 |
| Firmware path | `firmware/esp32cam_cc1101/src/main.cpp` |
| Framework | PlatformIO, Arduino framework, `board = esp32cam` |
| Upload command | `python -m platformio run --target upload` |
| Monitor command | `python -m platformio device monitor` |
| Serial baud | 115200 |
| Smoke-test output | GPIO4 flash LED blink plus serial heartbeat |
| Result | Pass |

## Wiring Used

| HW-409 | ESP32-CAM |
| --- | --- |
| 5V | 5V |
| GND | GND |
| TXD | U0R / RX / GPIO3 |
| RXD | U0T / TX / GPIO1 |

For flashing only:

```text
ESP32-CAM GPIO0 -> GND
```

After upload, GPIO0 was disconnected from GND and the board was reset/power-cycled to run the sketch.

## Observed Serial Output

```text
heartbeat 18 millis=10008 led=off
heartbeat 19 millis=10508 led=on
heartbeat 20 millis=11008 led=off
heartbeat 21 millis=11508 led=on
heartbeat 22 millis=12008 led=off
heartbeat 23 millis=12508 led=on
heartbeat 24 millis=13008 led=off
heartbeat 25 millis=13508 led=on
heartbeat 26 millis=14008 led=off
heartbeat 27 millis=14508 led=on
heartbeat 28 millis=15008 led=off
heartbeat 29 millis=15508 led=on
heartbeat 30 millis=16008 led=off
heartbeat 31 millis=16508 led=on
heartbeat 32 millis=17008 led=off
heartbeat 33 millis=17508 led=on
heartbeat 34 millis=18008 led=off
heartbeat 35 millis=18508 led=on
heartbeat 36 millis=19008 led=off
heartbeat 37 millis=19508 led=on
heartbeat 38 millis=20008 led=off
heartbeat 39 millis=20508 led=on
heartbeat 40 millis=21008 led=off
heartbeat 41 millis=21508 led=on
heartbeat 42 millis=22008 led=off
heartbeat 43 millis=22508 led=on
heartbeat 44 millis=23008 led=off
heartbeat 45 millis=23508 led=on
heartbeat 46 millis=24008 led=off
heartbeat 47 millis=24508 led=on
heartbeat 48 millis=25008 led=off
```

## Notes

- GPIO0 is a boot strapping pin on ESP32. If GPIO0 is held low during reset/power-up, the ROM bootloader enters serial download mode instead of booting the existing application from flash.
- The first failed upload was consistent with the board booting the existing application instead of entering the bootloader.
- Seeing old MQTT logs before the smoke-test upload confirmed that ESP32 TX to HW-409 RX was working.
- The successful heartbeat confirms that flashing, serial monitoring, basic power, and GPIO4 flash LED control are working.

