# R3-2024-Tournament-Q03-v12

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 1, problem 3, answer slide 165)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 165)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.1, problem 3)
- The catalog uses the equivalent bounded limit family checked below.

## Problem

The catalog text of this row is the line printed on slide 165, not the integral. Slide 165 is the answer reveal for Battle 4, Fight 1, problem 3:

\[
\lim_{n\to\infty}n\int_{0}^{\pi/4}\tan^{n}x\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q03-v10`.

## Solution

Write \(I_{n}=\int_{0}^{\pi/4}\tan^{n}x\,dx\). Then

\[
I_{n}+I_{n+2}=\int_{0}^{\pi/4}\tan^{n}x\,(1+\tan^{2}x)\,dx=\left[\frac{\tan^{n+1}x}{n+1}\right]_{0}^{\pi/4}=\frac{1}{n+1},
\]

because the integrand is the derivative of \(\tan^{n+1}x/(n+1)\). On \((0,\pi/4]\) one has \(0<\tan x\le 1\), so \(I_{n}\) decreases in \(n\). Therefore

\[
\frac{1}{n+1}=I_{n}+I_{n+2}\le 2I_{n}\le I_{n}+I_{n-2}=\frac{1}{n-1}.
\]

Multiplying through by \(n/2\) squeezes \(n I_{n}\) to \(1/2\). The answer slide prints \(1/2\).

## Gate reduction

For each positive integer \(n\), set \(u=\tan^{n+1}t\). This gives the exact identity

\[
n\int_0^{\pi/4}\tan^n t\,dt
=\int_0^1\frac{n}{(n+1)(1+u^{2/(n+1)})}\,du.
\]

The new integrands lie between \(0\) and \(1\) on \((0,1)\) and converge
pointwise there to \(1/2\). The constant dominating function \(1\) is integrable,
so dominated convergence gives the limit \(1/2\). The value at the single
endpoint \(u=0\) does not affect the integral. The gate stores this transformed
limit family and checks the finite-\(n\) substitution and domination before
interchanging the limit and integral. It does not interchange the limit with
the original, undominated family \(n\tan^n t\).

## Final answer

\[
\dfrac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q03_v12`. That check runs `check_r3_2024_tournament_q03_v10` for `R3-2024-Tournament-Q03-v10`. SymPy differentiates \(\tan^{n+1}x/(n+1)\) and checks that the endpoint difference is \(1/(n+1)\).

`verify/pack_handoff_e_tournament.py` also checks the finite-parameter Jacobian, endpoints, monotonicity, integrable bound, and pointwise limit used by the catalog gate.
