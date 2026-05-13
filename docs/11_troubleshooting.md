# Troubleshooting

## SDR Bring-Up

| Symptom | Likely causes | Checks |
| --- | --- | --- |
| Device not detected | Driver issue, bad USB cable, wrong USB port | Try another data cable, check Device Manager, run Zadig on Windows if needed. |
| Waterfall is blank | Wrong source, antenna issue, gain too low | Confirm RTL-SDR source, tune FM broadcast, adjust gain. |
| Strong signals are smeared | Gain too high, overload | Reduce gain, move antenna, check nearby transmitters. |
| Audio demod sounds wrong | Wrong mode, wrong center frequency, sample-rate issue | Confirm WFM mode and station frequency. |
| Capture cannot replay | Unknown file format/sample rate | Record metadata next to every capture. |

## Receiver Demodulation

To be expanded during Phase 7:

- frequency offset
- wrong deviation
- wrong symbol rate
- gain clipping
- clock recovery issues
- bit inversion
- sync not found

