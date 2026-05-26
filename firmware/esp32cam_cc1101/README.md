# ESP32-CAM CC1101 Firmware

Firmware starts with a hardware smoke test before camera or CC1101 work.

Initial goals:

1. Compile and flash a minimal ESP32-CAM sketch.
2. Prove HW-409 programming/serial wiring with a GPIO4 flash LED blink.
3. Capture a still JPEG and log size.
4. Send known CC1101 text packets.
5. Add packetised frame transport only after the protocol is tested on the host.

## Current Smoke Test

`src/main.cpp` blinks the ESP32-CAM flash LED on GPIO4 and prints a serial heartbeat at 115200 baud.

Status: passed on 2026-05-26 using HW-409 on COM4. See `reports/logs/esp32cam_bringup_log.md`.

Expected serial output:

```text
ESP32-CAM HW-409 smoke test
Flash LED: GPIO4
Expected: LED blinks and serial heartbeat prints every 500 ms.
heartbeat 1 millis=...
```

## HW-409 Flashing Wiring

Use the ESP32-CAM bare module, not the ESP32-CAM-MB motherboard.

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

After flashing, unplug USB, remove the GPIO0-to-GND jumper, then reconnect USB or press reset to run the sketch.

Set the HW-409 to 5V output if it has a jumper or switch. Do not power the ESP32-CAM from the adapter's weak 3.3V pin.

## PlatformIO Commands

From this folder:

```powershell
python -m platformio run
python -m platformio run --target upload
python -m platformio device monitor
```

The current `platformio.ini` uses `COM4`. If Windows assigns a different port, update `upload_port` and `monitor_port`.
