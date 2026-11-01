# Known limits

## Sample-based antiderivative checks miss a spike that vanishes at every probe

`verify/pack_gate.py` accepts some indefinite answers when the derivative
matches for x>0 and the integrand and derivative agree at the probe points
on both signs of 0 (`_positive_domain_derivative`, compared by
`_compare_sample`). A term that is zero at every probe point but nonzero
between them, such as a narrow spike built to vanish on the probe set, is not
seen by sampling. Catching it needs a symbolic proof, and that proof does not
finish within `PROOF_TIMEOUT` (20s), so the timeout ends the attempt.

This is accepted as a known limit of sample-based checking (receipt
ibe-structural-close-2026-11-01). Do not raise `PROOF_TIMEOUT` or skip proofs
to work around it. Non-real samples, small values of opposite sign, and
assumptions on declared symbols are not part of this limit: those are checked
and covered by `verify/e_false_pass_check.py`.

## Samples that are non-real on both sides are not judged

Where both the integrand and the derivative of the answer are non-real, the
sample is outside the real domain of the integral and `_compare_sample`
treats it as quiet: it does not reject and does not count as agreement.
Branch choices there make correct answers disagree (R1-2021-Q09,
R3-2024-Chainlink-G1-Q03, YANG-2.5-P14). A real side against a non-real side
is still a reject, apart from a whole 2*pi*I logarithm branch.
