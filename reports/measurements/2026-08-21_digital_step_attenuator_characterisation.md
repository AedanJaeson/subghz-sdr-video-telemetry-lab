# Digital Step Attenuator Characterisation — 2026-08-21

## Purpose

Record the first two-port LiteVNA measurement of the unbranded 0–63.5 dB digital RF step attenuator. The results are provisional until the post-measurement THRU check described under **Validation status** is completed.

## Equipment and configuration

| Item | Configuration |
| --- | --- |
| VNA | Zeenko LiteVNA-64 |
| Port extension | 5 cm RG316 male-to-female saver on each VNA port |
| Test cables | Two blue SS405 SMA cables; one assigned to each port |
| DUT | Unbranded digital step attenuator; SMA female-to-female; displayed range 0–63.5 dB |
| Sweep | 100 MHz to 3.000 GHz; 201 points |
| Measured parameter | S21 log magnitude, dB |
| Marker frequencies | 100 MHz, 433.5 MHz, 1086 MHz and 2405.5 MHz |

The calibration reference planes were intended to be the exposed male ends of the blue cables, with the RG316 savers and blue cables installed before calibration. OPEN, SHORT and LOAD were applied at Port 1's reference plane and the supplied female-to-female barrel was used for THRU.

## Raw S21 results

All values are measured S21 in dB. More-negative values mean greater total through-path loss.

| Commanded setting | 100 MHz | 433.5 MHz | 1086 MHz | 2405.5 MHz |
| ---: | ---: | ---: | ---: | ---: |
| 0 dB | -2.41 | -2.41 | -3.37 | -7.55 |
| 0.5 dB | -2.88 | -2.93 | -3.83 | -7.90 |
| 1 dB | -3.43 | -3.41 | -4.35 | -8.35 |
| 3 dB | -5.28 | -5.25 | -6.21 | -10.02 |
| 6 dB | -8.44 | -8.37 | -9.50 | -12.98 |
| 10 dB | -12.24 | -12.16 | -13.25 | -16.63 |
| 20 dB | -22.23 | -22.15 | -23.20 | -26.60 |
| 30 dB | -32.19 | -32.11 | -33.19 | -36.47 |
| 40 dB | -42.12 | -42.07 | -43.01 | -46.73 |
| 50 dB | -52.05 | -52.02 | -52.93 | -56.50 |
| 63.5 dB | -65.50 | -66.50 | -67.10 | -70.50 |

## Calculation method

For each frequency, the measured 0 dB setting was treated as the minimum-loss baseline:

```text
added attenuation = S21(0 dB setting) - S21(commanded setting)
attenuation error = added attenuation - commanded attenuation
```

A negative error means the DUT produced less additional attenuation than commanded. This comparison removes the DUT's measured minimum insertion loss from step-accuracy calculations; it does not remove that loss from the physical RF path.

## Derived added attenuation and error

Each entry is `added attenuation (error)` in dB.

| Command | 100 MHz | 433.5 MHz | 1086 MHz | 2405.5 MHz |
| ---: | ---: | ---: | ---: | ---: |
| 0.5 dB | 0.47 (-0.03) | 0.52 (+0.02) | 0.46 (-0.04) | 0.35 (-0.15) |
| 1 dB | 1.02 (+0.02) | 1.00 (+0.00) | 0.98 (-0.02) | 0.80 (-0.20) |
| 3 dB | 2.87 (-0.13) | 2.84 (-0.16) | 2.84 (-0.16) | 2.47 (-0.53) |
| 6 dB | 6.03 (+0.03) | 5.96 (-0.04) | 6.13 (+0.13) | 5.43 (-0.57) |
| 10 dB | 9.83 (-0.17) | 9.75 (-0.25) | 9.88 (-0.12) | 9.08 (-0.92) |
| 20 dB | 19.82 (-0.18) | 19.74 (-0.26) | 19.83 (-0.17) | 19.05 (-0.95) |
| 30 dB | 29.78 (-0.22) | 29.70 (-0.30) | 29.82 (-0.18) | 28.92 (-1.08) |
| 40 dB | 39.71 (-0.29) | 39.66 (-0.34) | 39.64 (-0.36) | 39.18 (-0.82) |
| 50 dB | 49.64 (-0.36) | 49.61 (-0.39) | 49.56 (-0.44) | 48.95 (-1.05) |
| 63.5 dB | 63.09 (-0.41) | 64.09 (+0.59) | 63.73 (+0.23) | 62.95 (-0.55) |

## Findings

1. **The commanded attenuation steps operate across all four measured frequencies.** The 0.5 dB increments and full 63.5 dB displayed range were functionally demonstrated at the sampled points.
2. **Step accuracy is strong through 1086 MHz.** Up to the 50 dB setting, measured error remained within -0.44 dB to +0.13 dB. At 63.5 dB, the largest absolute error below 1.1 GHz was +0.59 dB at 433.5 MHz.
3. **Step accuracy degrades at 2405.5 MHz.** From 10 dB through 50 dB, the DUT under-attenuated by approximately 0.82–1.08 dB. The 63.5 dB result was -0.55 dB, but readings around -70 dB may be influenced by the VNA transmission floor, leakage and connection repeatability.
4. **The measured minimum through loss rises with frequency.** At the DUT's displayed 0 dB setting, S21 was -2.41 dB at 100/433.5 MHz, -3.37 dB at 1086 MHz and -7.55 dB at 2405.5 MHz. If the calibration and THRU validation are sound, this makes the attenuator materially lossy at 2.4 GHz even before commanded attenuation is added.
5. **“0 dB” is a control setting, not a lossless bypass.** Total path attenuation must use measured S21 or include the frequency-dependent minimum insertion loss; the displayed attenuation alone is insufficient.

## Validation status

These findings remain **provisional** because the supplied THRU barrel has not yet been re-measured after the DUT run. Before treating the 0 dB insertion-loss values as DUT characteristics:

1. Replace the attenuator with the same female-to-female THRU used during calibration.
2. Without changing sweep settings or cable placement, record S21 at all four markers.
3. Confirm the THRU is close to 0 dB and reasonably flat.
4. Repeat the THRU connection three times to estimate connector repeatability.
5. Record whether the LiteVNA calibration indicator shows a directly applicable calibration or interpolation.

If the THRU exhibits several decibels of loss or strong high-frequency tilt, repeat the calibration and DUT measurements before accepting the insertion-loss conclusion.

## Current usable characterisation

Subject to the validation above, the attenuator is operationally verified from 100 MHz to 2405.5 MHz over its displayed 0–63.5 dB range. Below approximately 1.1 GHz, its added attenuation is within about 0.6 dB of command across the sampled settings. At 2.4 GHz, apply a measured frequency-and-setting correction rather than trusting the display alone.

The listing claim of 9 kHz–6 GHz has **not** been verified by this experiment. Maximum RF input power, damage limits, absolute calibration traceability, return loss, phase response, directionality, powered/unpowered behaviour and performance above 2.405 GHz remain `TBD`.
