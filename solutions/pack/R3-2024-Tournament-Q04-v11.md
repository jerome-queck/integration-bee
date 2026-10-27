# R3-2024-Tournament-Q04-v11

## Status: resolved (derived)

- verify: sympy
- conflict: This answer-slide alias inherits v10's conflict between the integral value \(\pi/2^m\) and the printed exponent \(m-2n\).
- derived / problem reading: \(\pi/2^m\) for the integral on slide 169; this row is its answer-slide alias.
- printed mark: \(\pi/2^{m-2n}\) on slide 171 and solutions p.15.
- erratum: none documented in the cited repository sources as of 2026-10-27.
- registry: docs/decisions/0016-pack-source-holds.md

- Problem: [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf#page=169) (Battle 4, Fight 2, problem 4, slide 169; answer-label alias on slide 170)
- Printed answer: [`Tournament slides, slide 171`](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf#page=171) (slide 171)
- Worked source: [`sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf#page=15) (page 15, section 4.2, problem 1)
- Verification: **sympy**, using the shared `doubled_sine_product_value` certificate in `verify/pack_handoff_q.py`.

The catalog grades the derived value \(\pi/2^{m}\) with `verify: sympy`. The
printed value \(\pi/2^{m-2n}\) remains documented as a source conflict. The
correction follows from the printed integral and the Jacobian below; no
publisher-issued erratum is claimed.

## Problem

The original extract for this row was the word `Answer` on slide 170. This is an answer-slide alias of the preceding problem, not a second integral. The catalog now transcribes the integral from slide 169 for display and automatic grading and retains the original extract as provenance. Slide 171 prints the source's final value for the same Battle 4, Fight 2, problem 4:

For integers \(m>n\),

\[
\int_{0}^{\pi/2^{n}}\frac{\sin\bigl((2^{m}+2025\cdot 2^{n})x\bigr)}{\sin(2^{m}x)}\prod_{k=1}^{m-n}\cos(2^{m-k}x)\,dx.
\]

The integral itself is on slide 169, catalogued as `R3-2024-Tournament-Q04-v10`.

The encoded inputs preserve the product, both bounds, and the condition that \(m,n\) are integers with \(m>n\). This alias shares the certificate and the derived answer \(\pi/2^{m}\) with `R3-2024-Tournament-Q04-v10`.

Slide 171 prints \(\pi/2^{m-2n}\), and the solutions PDF prints the same exponent. That exponent is what the calculation produces if \(dx=dy/2^{n}\) is replaced by \(dx=2^{n}\,dy\). The value of the integral is \(\pi/2^{m}\).

## Solution

Write \(d=m-n\), so \(d\) is a positive integer. Either \(m\) or \(n\) may
be negative; \(2^n>0\) for every integer \(n\), so the substitution below
preserves the orientation of the interval.

The double-angle formula for sine, applied \(m-n\) times, is

\[
\sin(2^{m}x)=2^{m-n}\sin(2^{n}x)\prod_{k=1}^{m-n}\cos(2^{m-k}x).
\]

The product in the integrand therefore cancels, and the integral equals

\[
\frac{1}{2^{m-n}}\int_{0}^{\pi/2^{n}}\frac{\sin\bigl((2^{m}+2025\cdot 2^{n})x\bigr)}{\sin(2^{n}x)}\,dx.
\]

Set \(y=2^{n}x\), so \(dx=dy/2^{n}\) and the limits become \(0\) and \(\pi\). The prefactor is

\[
\frac{1}{2^{m-n}}\cdot\frac{1}{2^{n}}=\frac{1}{2^{m}},
\]

and the integral is

\[
\frac{1}{2^{m}}\int_{0}^{\pi}\frac{\sin\bigl((2^{m-n}+2025)y\bigr)}{\sin y}\,dy.
\]

Here \(2^{m-n}\) is even and \(2025\) is odd, so the coefficient \(N=2^{m-n}+2025\) is an odd positive integer. For every such \(N\),

\[
\int_{0}^{\pi}\frac{\sin(Ny)}{\sin y}\,dy=\pi,
\]

because

\[
\frac{\sin(Ny)}{\sin y}
=1+2\sum_{j=1}^{(N-1)/2}\cos(2jy).
\]

This finite identity follows by telescoping
\(2\sin y\cos(2jy)=\sin((2j+1)y)-\sin((2j-1)y)\). Every nonconstant
cosine term integrates to zero on \([0,\pi]\), so the integral equals
\(\pi/2^{m}\).

The cancellations are first made where the original denominator is nonzero.
The finite cosine sum extends the reduced integrand continuously across all
of the original denominator's zeros, including the endpoints. All these
singularities are removable, and integrating the extension gives the same
value as the corresponding improper integral.

The solutions PDF and the answer slide both print \(\pi/2^{m-2n}\).
On page 15, the solutions PDF changes the prefactor from \(2^{-(m-n)}\)
to \(2^{-(m-2n)}\) at the substitution \(y=2^n x\). This is the factor
produced by using \(dx=2^n\,dy\); the correct Jacobian is
\(dx=dy/2^n\). For \(n=0\) the two final expressions agree, which would
hide the error in that special case. For \((m,n)=(2,1)\), the derived
value is \(\pi/4\), while the printed formula gives \(\pi\). For
\((m,n)=(0,-1)\), the derived value is \(\pi\), while the printed
formula gives \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{2^{m}}.
\]

The solutions PDF and slide 171 print \(\pi/2^{m-2n}\). The value of the integral is \(\pi/2^{m}\).

## SymPy self-check

The SymPy fields use an arbitrary integer \(m\) and a positive integer
\(d=m-n\). Substituting \(n=m-d\) into the literal integrand and bounds
gives product upper index \(d\) and integration upper bound
\(\pi/2^{m-d}\). This bijective parameterization enforces exactly
\(m,n\in\mathbb Z\), \(m>n\),
including negative values of \(m\) or \(n\). The displayed problem keeps
its original \(m,n\) notation, and the final remains \(\pi/2^m\).

`verify/pack_handoff_q.py` supplies the shared `doubled_sine_product_value`
certificate. It checks the double-angle induction, the transformed bounds
and Jacobian, and the finite odd Dirichlet-kernel identity with vanishing
cosine integrals. `verify/pack_handoff_q_check.py` exercises all three catalog
aliases, several valid integer parameter pairs, and wrong-answer controls
that reject the printed \(\pi/2^{m-2n}\).

`solutions/self_check.py` loads `check_r3_2024_tournament_q04_v11` from
`solutions/pack_checks_tournament_rem.py`. It delegates to
`check_r3_2024_tournament_q04_v10` with the original problem.
