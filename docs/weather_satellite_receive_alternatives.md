# Weather Satellite Receive Alternatives

The original backlog included an optional NOAA APT receive-planning task. As of 2026, that should not be treated as an expected receive experiment.

## Current NOAA POES/APT Status

NOAA's legacy POES satellites that carried the easy-to-receive analog APT downlinks have been decommissioned:

- NOAA-18: decommissioned on 2025-06-06.
- NOAA-19: decommissioned on 2025-08-13.
- NOAA-15: decommissioned on 2025-08-19.

This means the old beginner path of "receive NOAA APT on 137 MHz" is no longer a reliable project task.

Sources checked on 2026-05-14:

- NOAA OSPO POES status: https://www.ospo.noaa.gov/operations/poes/status.html
- NOAA NESDIS POES decommissioning story: https://www.nesdis.noaa.gov/news/legacy-orbit-noaa-decommissions-the-poes-satellite-constellation

## How To Use This In The Project

Keep the task receive-only and treat it as a research/planning note:

1. Verify current satellite status before buying antennas or planning a pass.
2. Decide whether to skip weather satellites for this lab.
3. If continuing, pick a realistic alternative and document the hardware jump.

## Candidate Alternatives

| Alternative | Notes | Fit for this project |
| --- | --- | --- |
| Meteor-M LRPT | Digital low-rate weather image downlink when active and locally receivable. Requires current status checks and compatible decode tooling. | Possible stretch, but not core. |
| GOES HRIT/LRIT | Geostationary weather imagery path. Usually needs more antenna and LNA planning than a simple RTL-SDR starter task. | Advanced separate project. |
| JPSS/NOAA online data | Use public data products without RF receive hardware. | Good comparison/reference path, not SDR practice. |
| Skip weather satellites | Focus Phase 2 on ADS-B and local receive-only ISM observation. | Recommended for MVP momentum. |

## Recommended Decision

For this lab, keep weather satellites optional and low-priority. The strongest first proof point remains:

```text
Nooelec detected -> FM receive -> IQ capture -> ADS-B or local receive-only RF observations
```
