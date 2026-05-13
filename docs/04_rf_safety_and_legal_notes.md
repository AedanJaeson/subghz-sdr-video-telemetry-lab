# RF Safety And Legal Notes

This project is for lawful communications engineering learning. It is not legal advice. Always verify current local rules before transmitting.

## Default Rule

Receive-only work comes first. Do not transmit until the checklist below is complete.

## Pre-Transmit Compliance Checklist

- [ ] I have checked the current ACMA/LIPD rules for my location and intended band.
- [ ] The frequency is in a legal shared-device band for this hardware and use case.
- [ ] The CC1101 module frequency variant has been verified, not guessed.
- [ ] Transmit power is set low and is appropriate for a short-range lab test.
- [ ] The test is short-duration and controlled.
- [ ] A suitable antenna or dummy load is connected before transmit.
- [ ] I am not transmitting near aviation, emergency, cellular, GPS, broadcast, Defence, or protected bands.
- [ ] I am not transmitting into the SDR input directly without suitable attenuation.
- [ ] Bench testing, shielding, attenuation, or very short-range operation has been considered first.
- [ ] The test objective is benign: no jamming, spoofing, surveillance, interception, or disruption.

## Receive-Only Experiments

Receive-only SDR tasks are the safe first phase. They should focus on tool setup, waterfall interpretation, public signals, and local RF literacy without decoding private content.

## Transmit Experiments

Transmit phases are optional and must be labelled:

- low-power
- short-range
- legal-band
- controlled
- documented

When uncertain, do not transmit. Use simulation, dummy loads, attenuators, or a second CC1101 on the bench instead.

## SDR Input Protection

An RTL-SDR input can be damaged or overloaded by nearby transmitters. Do not cable a transmitter directly into the SDR without a designed attenuation path and power calculation.

