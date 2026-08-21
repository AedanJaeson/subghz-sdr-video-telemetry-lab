# Component Inventory Addendum — 2026-08-21

This additive record supplements `docs/02_hardware_inventory.md` without changing that existing inventory. Items were identified from photographs on 2026-08-21. Where a value, part number, connector gender or quantity cannot be read reliably, it remains `TBD`.

## Positively identified

| Item | Qty | Status | Evidence / notes |
| --- | ---: | --- | --- |
| Multi-colour heat-shrink sleeve assortment | 328 pieces | Owned / visually verified | Labelled black, yellow, red and green. Size breakdown is recorded below. Useful for insulation, strain relief, lead identification and cable-harness work. Shrink ratio and material are not stated on the visible label and remain `TBD`. |
| Dupont-style rainbow jumper-wire ribbon sets | 3 sets; approximately 40 conductors per set | Owned / visually verified; details TBD | Three separable rainbow ribbons are visible. They appear to provide mixed plug/socket gender combinations, but each end should be physically checked before assigning male-to-male, male-to-female or female-to-female. Exact length is not established from the photographs. |
| Assorted through-hole electronics component lot | 1 mixed lot | Owned / unsorted / untested | Photographs show through-hole LEDs, axial resistors, capacitors, a trimmer potentiometer, DIP-package ICs and at least one single-digit seven-segment display. Exact quantities, values, polarity, IC part numbers and working condition remain `TBD`. |
| Small loose-component bag | 1 bag | Owned / unsorted / untested | Red LEDs and axial resistors are visible. The bag carries an old `WG6028 / LEAD JUMPER PLG-SKT / 40 PC KIT 150MM` label, but the visible contents do not match that description; the label is retained only as packaging traceability and is not treated as an inventory specification. |

## Heat-shrink label breakdown

| Nominal internal diameter | Cut length | Qty |
| ---: | ---: | ---: |
| 1.0 mm | 40 mm | 120 |
| 2.0 mm | 40 mm | 60 |
| 3.0 mm | 40 mm | 32 |
| 4.0 mm | 40 mm | 32 |
| 6.0 mm | 40 mm | 32 |
| 8.0 mm | 80 mm | 20 |
| 10.0 mm | 80 mm | 16 |
| 14.0 mm | 80 mm | 16 |
| **Total** |  | **328** |

## What this adds to the apprenticeship bench

- Breadboard and low-voltage digital prototyping interconnects.
- LED current-limiting, pull-up/pull-down and basic RC experiments after component values are measured.
- Seven-segment display and simple counter/decoder experiments once the display pinout and DIP IC markings are identified.
- Soldering, lead dressing, insulation, strain-relief and cable-labelling practice using the heat-shrink assortment.
- Component-identification practice using package markings, resistor colour codes, capacitance markings, diode/LED polarity checks and multimeter measurements.

## Sorting and verification gate

Before using the mixed lot in a circuit:

1. Separate components by type and package.
2. Photograph and transcribe every DIP IC marking; do not infer logic family or pinout from package shape.
3. Decode resistor colour bands and confirm resistance with the multimeter.
4. Record capacitor markings, type and polarity; discard visibly damaged or leaking electrolytics.
5. Identify LED polarity and determine a safe test current using a series resistor.
6. Map the seven-segment display pins with a current-limited supply and determine common-anode versus common-cathode.
7. Verify every jumper end and check continuity before relying on it in a circuit.

Do not assume any item in the scavenged component lot is RF-rated, precision-grade or suitable for mains/high-voltage work based only on appearance.
