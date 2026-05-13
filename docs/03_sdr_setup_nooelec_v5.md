# SDR Setup - Nooelec NESDR SMArt v5

This page records the receive-only bring-up workflow.

## Device Facts

- RTL2832U-based RTL-SDR with R820T2/R860 style tuner.
- Approximate tuning range: 100 kHz to 1.75 GHz.
- Practical sample rates are commonly up to about 2.4 MSPS reliably, with higher rates such as 3.2 MSPS depending on host and driver stability.
- 0.5 ppm TCXO.
- Standard SMArt v5 does not have an always-on bias tee.

## Bring-Up Checklist

- Install SDR++ or SDR#.
- On Windows, install the RTL-SDR WinUSB driver with Zadig if required.
- Confirm the device appears in the software.
- Start with a local FM broadcast station as a known-good signal.
- Record OS, driver, app version, antenna, center frequency, sample rate, and gain.

## Log Template

| Date | OS | App | Driver | Frequency | Sample rate | Gain | Antenna | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

