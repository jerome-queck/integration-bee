# Aptitude session

Aptitude state lives in `session.json`. The phase, the skip offer, and the coverage flag are one `aptitude` value. The dosage the coach reads is `policy`, keyed by node id. There is no second tracker file.

`{"kind":"aptitude"}` opens one unit drill first. A correct mark opens one contest probe and does not write `skipped`. The contest mark stores an attempt and does not tick a node. The existing `R1-2022-MIT-TB-Q01` probe remains selected after its SymPy certification: its printed integral grades `1` automatically, without a verdict. A manual fallback still requires an explicit verdict. When a node has SymPy evidence and has not been declined, the phase becomes `proposing`. `{"kind":"confirm","nodes":[...]}` is the only new writer of `skipped`, and only for ids in that offer. An empty list declines the offer and writes no skip. A declined id is not offered again. `progress tick` can still set `skipped` by hand.

The learner does not place every Round 1 node before teaching. After confirm, `{"kind":"teach"}` is the next turn. Another aptitude turn places the next drill.

A confirmed skip leaves the default coach queue. The mock gate stays solid-only. A skipped Round 1 node still blocks a non-cold mock. `{"kind":"cover","full":true}` is the only turn that sets full coverage. The default is false. A later miss on a skipped node's drill writes `learning`.

A derived board in a second file can replay the offer from the attempt log. This page keeps the offer on `session.json` so one replace holds the phase, the offer, and the policy. The schedule above is the part taken from that board. A correct drill can be confirmed before the rest of Round 1 is probed.
