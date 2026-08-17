# Hardware Inventory

Use this file to record verified hardware. Unknowns remain marked `TBD` until checked from silkscreen, receipts, datasheets, the instrument version screen, or direct testing. Items purchased but not yet physically verified are marked `Ordered`; items not yet purchased are marked `To Buy`.

Last reconciled: **2026-08-17**

## Core RF and Embedded Hardware

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| Zeenko LiteVNA-64 | 1 | Owned; HW revision verification pending | Purchased from the Zeenko Store as **HW 0.3.3**. Listing specification: 50 kHz to 6.3 GHz, 4-inch display, 2000 mAh battery. Unit powers on and produces S11/S21 traces. Capture the CONFIG/VERSION screen before treating the hardware revision and firmware as verified. |
| Open-source Pluto+ SDR | 1 | Owned / operational | AD9363A-based receive/transmit SDR, approximately 70 MHz to 6 GHz in the current configuration. Exact board revision, oscillator option, firmware and calibration status remain `TBD`. |
| Nooelec NESDR SMArt v5 | 1 | Owned / operational | RTL2832U + R820T2/R860-style receive-only RTL-SDR, approximately 100 kHz to 1.75 GHz, 0.5 ppm TCXO. Standard SMArt v5 does not have an always-on bias tee. FM and ADS-B reception have been demonstrated. |
| ESP32-CAM with OV2640 | 1 | Owned; exact variant TBD | Board is available and has been used with the CC1101 project. Record exact board variant and flash/programming method. |
| CC1101 module | 1 | SPI verified; verify RF band before TX | SPI/register access verified on 2026-05-26. Firmware is configured for 433.920 MHz, but the module marking, RF matching network and actual frequency variant must still be verified before RF transmission. |
| Digital RF step attenuator | 1 | Owned; specification TBD | Small display/rotary-control attenuator visible in the RF kit. Record model, connector gender, frequency range, step size, attenuation range, maximum input power and insertion loss from its listing or direct VNA testing. |
| DIY 1090 MHz quarter-wave ground-plane antenna | 1 | Built / under test | Designed for ADS-B around 1090 MHz. Initial VNA work showed the intended resonance plus a suspicious lower-frequency resonance around 399 MHz. Re-measure using a fresh calibration and controlled feedline geometry. |
| Decommissioned PC Wi-Fi antennas | Approx. 4 | Owned; characteristics TBD | Likely 2.4/5 GHz antennas. Connector type, internal matching and usable frequency range must be checked before relying on them. |

## LiteVNA Kit and Calibration Hardware

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| Zeenko SS405 SMA test cables | 2 | Owned | Blue precision-style VNA cables supplied with the LiteVNA. Nominal length appears to be approximately 30 cm; verify length and connector gender. Dedicate one cable to Port 1 and one to Port 2 where practical. |
| LiteVNA open calibration standard | 1 | Owned | Use at the final measurement reference plane after all permanent adapters/port savers and the test cable are installed. |
| LiteVNA short calibration standard | 1 | Owned | Supplied calibration standard. Keep capped and clean. |
| LiteVNA 50 ohm load calibration standard | 1 | Owned | Suitable as an OSL calibration standard. Do **not** assume it is a transmitter-rated dummy load. |
| SMA female-to-female through barrel | 1 | Owned | Supplied with the LiteVNA for through calibration and cable/component measurements. Exact rated frequency remains `TBD`. |
| LiteVNA USB data/charging cable | 1 | Owned | Confirm stable PC data operation as well as charging. |
| LiteVNA carrying/storage case | 1 | Owned | Stores the analyzer, standards and leads. |
| SMA port savers / straight adapters | TBD | Owned in adapter assortment; identify exact pieces | Select two mechanically sound straight adapters, label them P1/P2 and keep them installed during a calibration session. Their loss and repeatability can be characterised with the VNA. |

## RF Protection, Attenuation and Bias Hardware

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| 10 dB SMA fixed attenuator | 1 | Owned | Listing claims 2 W and DC to 6 GHz. Verify actual S21 flatness, return loss and body marking before relying on its power rating. |
| 30 dB SMA fixed attenuator | 1 | Owned | Listing claims 2 W and DC to 6 GHz. Verify actual S21 flatness, return loss and body marking before relying on its power rating. |
| SMA inner-conductor DC blocks | 2 | Ordered / received; verify exact units | AliExpress pair sold as DC to 6 GHz. Record connector genders, low-frequency cutoff and voltage/power limits from markings or testing. |
| N male-to-N female DC block | 1 | Ordered; receipt/markings TBD | Listing claims 50 ohm, DC to 6 GHz and 50 V. Confirm arrival and do not infer whether the outer conductor is isolated without checking the topology. |
| Enclosed RF bias tee | 1 | Ordered / likely still in transit | Listing title claims approximately 10 MHz to 6 GHz. Record RF/DC port labels, allowable DC voltage/current, insertion loss and isolation when received. Do not confuse a bias tee with a DC block. |
| Dedicated transmitter dummy load | 0 | To Buy | The LiteVNA calibration load is not a substitute for a power-rated dummy load. Purchase only when controlled CC1101/Pluto conducted-transmit work requires it; specify connector, frequency range and wattage. |
| RF shielding/test enclosure | 0 | To Buy / optional | Useful for controlled legal-band conducted tests and leakage reduction, but not required for receive-only work or passive VNA measurements. |

## RF Cables, Pigtails and Adapters

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| Short RG316 coax jumpers/pigtails | 2 | Ordered / received | Approximately 5 cm each. Exact connector genders and measured insertion loss remain `TBD`. |
| Mixed SMA/RP-SMA straight adapters | 7 | Ordered / received; mapping TBD | Order record: listing **Type 1 x2, Type 12 x2 and Type 7 x3**. Decode each seller type into actual SMA/RP-SMA male/female interfaces and label physically before use. |
| SMA/N/BNC/RP-SMA adapter assortment | Assorted | Owned / received; full count TBD | Several gold RF adapters are present. Inventory each by **body gender and centre-contact gender**; RP-SMA is frequently misidentified. Characterise unknown adapters when using them above approximately 1 GHz. |
| Nooelec magnetic antenna base and RG-58 cable | 1 | Owned | Approximately 2 m cable supplied with the Nooelec antenna kit. Exact connector chain and cable loss remain `TBD`. |
| General USB data cables | Assorted | Owned / verify individually | Mark known data-capable cables so charge-only cables do not waste debugging time. |
| USB hub | 1 | Owned; power arrangement TBD | A hub is available. Confirm whether it is externally powered and whether it remains stable with the Pluto+, RTL-SDR and LiteVNA connected. |

## Items Deliberately Not Purchased

| Item | Status | Reason |
| --- | --- | --- |
| tinySA Ultra+ / ZS407 | Deferred | Considerable overlap with Pluto+/B210-class SDR access for present experiments. Reconsider when standalone harmonic sweeps or portable interference hunting become recurring needs. |
| LiteVNA-67 | Not required | Adds workflow/headroom improvements but little new measurement theory for the current antenna, cable and filter projects. |
| tinyGTC | Deferred | Only justified when precision clock/frequency metrology becomes a defined project requirement. |
| Raspberry Pi | Deferred | Existing PCs provide more capability for current SDR, VNA and simulation work. Buy later only for a deliberate always-on ground-station or remote receiver role. |
| RF signal generator and calibrated power sensor | Future upgrade | These would add genuinely new receiver sensitivity, gain, compression and calibrated-power capability, but were not part of the current purchase. |

## Current Hardware Blockers and Safety Gates

As of 2026-08-17, CC1101 SPI/register verification has passed and the RF lab now includes receive hardware, a transmit-capable Pluto+, a LiteVNA and basic passive RF protection components.

CC1101 over-the-air transmission remains gated until:

- The CC1101 module frequency variant and matching network are verified.
- The intended operating frequency and duty cycle are checked against current ACMA/LIPD requirements.
- A suitable antenna or genuinely power-rated dummy load is attached.
- Output level, attenuation and receiver protection are understood.
- The RF safety checklist is complete.

Additional bench rules:

- Never connect a powered CC1101, Pluto+, USRP or other transmitter output directly to either LiteVNA port.
- Use a DC block whenever a DUT or RF path might carry DC, after checking that the required signal frequency is above the block's cutoff.
- Do not trust an attenuator's maximum power from appearance alone; verify the listing/marking and derate cheap units.
- Calibrate at the final reference plane for the exact frequency span, cables, adapters and sweep configuration.
- Keep SMA interfaces clean, avoid rotating the connector body against the centre pin, and cap unused standards/ports.
- Treat the calibration load as a metrology standard, not a transmit dummy load.

Work that can continue now:

- RTL-SDR and Pluto+ receive-only IQ capture workflows.
- Passive antenna, cable, adapter, attenuator and filter measurements with the LiteVNA.
- MATLAB/CST antenna modelling and measured-versus-simulated S-parameter comparison.
- Python packet framing, CRC, JPEG chunking and file reconstruction tests.
- ESP32-CAM still-image capture and frame-size budgeting.
- Serial or file-loopback tests that prove image serialisation before any RF transmission.

## Nooelec Kit Antennas

| Antenna | Type | Frequency Range | Gain | Best Use / Notes | Identification |
| --- | --- | --- | --- | --- | --- |
| Telescopic whip | Adjustable-length whip | Approximately 100-800 MHz, strongly dependent on length and ground/counterpoise | Not specified | General VHF/UHF scanning and experimental resonance measurements | Mast with adjustable telescopic sections and spring/coil base |
| 433 MHz antenna | Fixed-length black whip | Nominal 433 MHz ISM/SRD band | Seller claim approximately 3 dBi; unverified | Use only if the CC1101 is confirmed as a 433 MHz variant and transmission is legal for the location/configuration | Longer straight black antenna |
| UHF antenna | Fixed-length short black whip | Seller claim approximately 800-2200 MHz | Seller claim approximately 5 dBi; unverified | General higher-UHF use and initial ADS-B reception experiments | Remaining shorter black antenna |

The Nooelec bundle includes a magnetic antenna base with an approximately 2 m RG-58 cable and three modular masts. Seller frequency/gain claims are provisional until measured or confirmed from the exact kit documentation.

## Provisional ESP32-CAM to CC1101 Wiring Plan

The CC1101 has arrived and SPI/register communication has been verified, but this wiring plan remains provisional until the exact module pinout, RF frequency variant and reset/boot behaviour are fully recorded.

| CC1101 Pin | ESP32-CAM Pin | Notes |
| --- | --- | --- |
| VCC | 3V3 | 3.3 V only - never 5 V |
| GND | GND | Use a short, reliable common ground connection |
| SCK | IO14 | HSPI clock |
| MOSI | IO13 | SPI data into CC1101 |
| MISO | IO12 | SPI data out; IO12 is a boot-strapping pin, so verify its level during reset |
| CSn | IO15 | Chip select; IO15 is also a boot-strapping pin |
| GDO0 | IO2 | Main interrupt / packet-ready signal; IO2 boot behaviour must be considered |
| GDO2 | IO16 | Used by the current RadioLib blocking transmit-completion workflow |

### Important Board Notes

- **MicroSD slot:** IO12-15 are shared with the microSD interface, so the current SPI assignment prevents simultaneous normal use of the onboard card slot.
- **Flash LED:** The white flash LED is connected to IO4 and is not used by the current CC1101 wiring.
- **Power:** Power the ESP32-CAM from a stable 5 V supply capable of at least 1 A. Power the CC1101 from the ESP32-CAM's regulated 3.3 V rail only if that rail is verified stable under transmit load.
- **Boot pins:** IO2, IO12 and IO15 affect ESP32 boot behaviour. If startup becomes unreliable, measure these pins during reset and revise the wiring rather than assuming the radio library is at fault.

### Physical Connection

1. Fit straight 2.54 mm headers to the ESP32-CAM if they are not already installed.
2. Use short Dupont jumpers for initial SPI verification, then replace them with a mechanically secure interconnect for repeatable RF tests.
3. Verify every CC1101 module label and antenna connector before attaching an antenna.
4. Never command RF transmission without a suitable antenna or power-rated dummy load connected.
