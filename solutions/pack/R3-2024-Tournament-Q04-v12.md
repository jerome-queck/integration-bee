# R3-2024-Tournament-Q04-v12

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 2, problem 4, slide 169; answer-value alias on slide 171)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 171)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (page 15, section 4.2, problem 1)
- Status: **manual**; answer-slide alias of `R3-2024-Tournament-Q04-v10`; source conflict; fields encoded for display. The original integral and the printed answer disagree.

## Problem

The original extract for this row was the answer value printed on slide 171. This is an answer-slide alias of the preceding problem, not a second integral. The catalog now transcribes the integral from slide 169 for display and retains the original extract as provenance. Slide 171 is the answer reveal for the same Battle 4, Fight 2, problem 4:

For integers \(m>n\),

\[
\int_{0}^{\pi/2^{n}}\frac{\sin\bigl((2^{m}+2025\cdot 2^{n})x\bigr)}{\sin(2^{m}x)}\prod_{k=1}^{m-n}\cos(2^{m-k}x)\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q04-v10`.

The encoded inputs preserve the product, both bounds, and the condition that \(m,n\) are integers with \(m>n\). They do not promote this row to `sympy` or encode the printed mark as a proved answer. The printed answer remains \(\pi/2^{m-2n}\) pending an authoritative correction.

Slide 171 prints \(\pi/2^{m-2n}\), and the solutions PDF prints the same exponent. That exponent is what the calculation produces if \(dx=dy/2^{n}\) is replaced by \(dx=2^{n}\,dy\). The value of the integral is \(\pi/2^{m}\).

## Solution

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

because \(\sin(Ny)/\sin y=1+2\sum_{j=1}^{(N-1)/2}\cos(2jy)\). The integral equals \(\pi/2^{m}\).

The solutions PDF and the answer slide both print \(\pi/2^{m-2n}\). That exponent is what the same calculation produces if \(dx=dy/2^{n}\) is replaced by \(dx=2^{n}\,dy\). For \(n=0\) the two expressions agree. For \((m,n)=(2,1)\) the corrected value is \(\pi/4\), while the printed formula gives \(\pi\).

## Final answer

\[
\dfrac{\pi}{2^{m}}.
\]

The solutions PDF and slide 171 print \(\pi/2^{m-2n}\). The value of the integral is \(\pi/2^{m}\).

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q04_v12`. That check runs `check_r3_2024_tournament_q04_v10` for `R3-2024-Tournament-Q04-v10`. SymPy checks the product identity for \((m,n)=(3,1)\), \((4,2)\), and \((5,2)\), the factor \(1/2^{m-n}\cdot 1/2^{n}=1/2^{m}\), that this exponent differs from the printed exponent \(m-2n\), and the Dirichlet evaluation \(\int_{0}^{\pi}\sin(Ny)/\sin y\,dy=\pi\) for the odd values \(N=1,5,9\).
