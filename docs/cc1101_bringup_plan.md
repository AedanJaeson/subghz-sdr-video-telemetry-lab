# CC1101 Bring-Up Plan

Updated: 2026-05-26

This phase starts with SPI/register verification before any RF transmission.

## Wiring

Use the ESP32-CAM bare module with the HW-409 USB-to-serial adapter. Do not use the ESP32-CAM-MB board while wiring the CC1101, because it covers the side header pins.

### HW-409 To ESP32-CAM

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

After flashing, unplug USB, remove GPIO0 from GND, then reconnect or reset to run the sketch.

### ESP32-CAM To CC1101

| CC1101 | ESP32-CAM |
| --- | --- |
| GND | GND |
| VCC | 3V3 |
| SCK | GPIO14 |
| MISO | GPIO12 |
| MOSI | GPIO13 |
| CSN | GPIO15 |
| GDO0 | GPIO2 |
| GDO2 | GPIO16 |

CC1101 VCC is 3.3 V only. Do not connect it to 5 V.

## Stage 1 - SPI/Register Check

Default firmware setting:

```ini
CC1101_TRANSMIT_ENABLED=0
```

This mode:

- boots the ESP32-CAM,
- blinks GPIO4,
- reads CC1101 `PARTNUM` and `VERSION`,
- initializes RadioLib at the configured frequency,
- prints `CC1101 SPI OK` if the bus and radio init work,
- does not transmit.

Expected serial output:

```text
ESP32-CAM CC1101 staged bring-up
CC1101 bring-up
Transmit enabled: NO
CC1101 PARTNUM read OK
CC1101 VERSION read OK
RadioLib CC1101 init ... success
CC1101 SPI OK
```

If this fails, check:

- CC1101 VCC is on ESP32-CAM 3V3, not 5 V.
- All grounds are common.
- CSN/SCK/MISO/MOSI are not swapped.
- The module is not rotated or connected to the wrong pin row.
- GPIO0 is removed from GND after flashing.
- GDO2 is connected to GPIO16 before running blocking transmit tests.

## Stage 2 - Short Low-Power Test Packet

Only enable this after:

- local ACMA/LIPD rules have been checked,
- the CC1101 frequency variant is verified,
- a suitable antenna or dummy load is connected,
- the Nooelec SDR is not directly cabled to the transmitter without proper attenuation,
- the test is low-power, short-range, and controlled.

Change `platformio.ini`:

```ini
-D CC1101_TRANSMIT_ENABLED=1
-D CC1101_FREQ_MHZ=433.92
-D CC1101_OUTPUT_POWER_DBM=-10
```

Then flash and monitor:

```powershell
python -m platformio run --target upload
python -m platformio device monitor
```

Expected TX serial output:

```text
TX packet: SUBGHZ_LAB_TEST_0 ... started; wait 250 ms for SDR burst; finish ... success
```

If the older blocking `radio.transmit(...)` path fails with RadioLib code `-5`, that is `RADIOLIB_ERR_TX_TIMEOUT`. If SDR# shows a burst anyway, the CC1101 probably transmitted and the ESP32 did not observe the expected GDO2 edge. For first RF bring-up, the firmware uses `startTransmit(...)`, waits for the short packet to leave the radio, then calls `finishTransmit(...)`. This makes the SDR waterfall the primary proof point.

Still check that:

```text
CC1101 GDO2 -> ESP32-CAM GPIO16
```

Use SDR++/SDR# or the Nooelec SDR receive chain to look for short bursts at the configured frequency.
