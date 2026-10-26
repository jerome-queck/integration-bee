# R2-2025-SG-Relay-Q24

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (p. 7, relay 24). The same integral is relay 14 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p. 3, UK relay 14)
- Worked source: derived in this note; the UK mark scheme prints the final value.
- Catalog proof: the source integral and final are checked by `verify/pack_gate.py`.

## Problem

\[
\int_{0}^{\infty}\frac{x^{e/2-1}(1+\ln x)}{x^{e}+1}\,dx.
\]

## Solution

Set \(t=\ln x\), so \(x=e^{t}\) and \(dx=e^{t}\,dt\). The integral becomes

\[
\int_{-\infty}^{\infty}\frac{1+t}{2\cosh(et/2)}\,dt.
\]

The summand \(t\operatorname{sech}(et/2)\) is odd and absolutely integrable, so its integral is \(0\). The remaining integral is

\[
\frac12\int_{-\infty}^{\infty}\operatorname{sech}\frac{et}{2}\,dt.
\]

The substitution \(u=et/2\) multiplies by \(2/e\). Since the antiderivative of \(\operatorname{sech}u\) is \(\arctan(\sinh u)\),

\[
\frac{1}{e}\bigl[\arctan(\sinh u)\bigr]_{-\infty}^{\infty}=\frac{\pi}{e}.
\]

The UK mark scheme prints \(\pi/e\).

## Final answer

\[
\frac{\pi}{e}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q24`. SymPy checks the substitution algebra, the oddness of \(t\operatorname{sech}(et/2)\), the derivative of \(\arctan(\sinh u)\), and the factor \(1/e\).
