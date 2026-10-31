# R2-2025-SG-Relay-Q30

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 30). The same integral is relay 11 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 11)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{\sin x\ln x}{x}\,dx.
\]

## Solution

For \(0<a<2\),
\[
\int_{0}^{\infty}x^{a-1}\sin x\,dx=\Gamma(a)\sin\frac{\pi a}{2}=\frac{\Gamma(a+1)}{a}\sin\frac{\pi a}{2}.
\]
The strip \(0<a<2\) is open at \(0\). Differentiate \(I(a)=\Gamma(a)\sin(\pi a/2)\) on \((0,2)\). On each compact subinterval the derivative \(x^{a-1}\sin x\log x\) is dominated by an integrable function, so differentiation under the integral is valid there. The boundary value is the limit \(\lim_{a\downarrow 0} I'(a)\), not a derivative taken at \(a=0\). That limit is
\[
-\frac{\pi\gamma}{2},
\]
where \(\gamma\) is the Euler-Mascheroni constant. The mark scheme prints \(-\pi\gamma/2\).

## Final answer

\[
-\frac{\pi\gamma}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q30`. SymPy checks the same gamma expansion as the UK relay 11 note.
