# Packet Protocol

Initial protocol target, subject to test-vector validation:

| Field | Purpose |
| --- | --- |
| Preamble | Help receiver settle and clock recovery acquire. |
| Sync word | Mark packet boundary. |
| Protocol version | Allow future format changes. |
| Frame ID | Identify image/frame. |
| Packet ID | Identify packet within frame. |
| Total packets | Know when a frame is complete. |
| Payload length | Validate final partial packet and parsing. |
| Payload | Image or test bytes. |
| CRC | Reject corrupted packets. |

Open decisions:

- Exact sync word.
- Header byte order.
- Payload size limit.
- CRC width and polynomial.
- Whether whitening/FEC/interleaving are deferred until after MVP.

