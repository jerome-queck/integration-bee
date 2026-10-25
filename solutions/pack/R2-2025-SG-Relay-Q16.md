# R2-2025-SG-Relay-Q16

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 16). The same integral is relay 20 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 20)
- Worked source: derived in this note; the UK mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\left\lfloor\int_{2}^{2025}\frac{1}{\lfloor 2\log_{x}5+4\log_{x}3\rfloor}\,dx\right\rfloor.
\]

## Solution

The change-of-base formula gives

\[
2\log_{x}5+4\log_{x}3=\log_{x}2025.
\]

For \(x>1\), \(\lfloor\log_{x}2025\rfloor=k\) on \((2025^{1/(k+1)},2025^{1/k}]\). A \(40\)-digit evaluation puts \(\log_{2}2025\) strictly between \(10\) and \(11\), and puts \(2025^{1/11}<2<2025^{1/10}\). The integers \(k\) that meet \([2,2025]\) therefore run from \(1\) through \(10\), with the left endpoint truncated at \(2\). The integrand equals \(1/k\) on each piece, so the integral is

\[
\frac{2025^{1/10}-2}{10}+\sum_{k=2}^{9}\frac{2025^{1/k}-2025^{1/(k+1)}}{k}+(2025-45),
\]

because \(2025^{1/2}=45\). At \(40\) decimal places this value lies strictly between \(1999\) and \(2000\), so its floor is \(1999\). The UK mark scheme prints \(1999\).

## Final answer

\[
1999.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q16`. SymPy checks \(2\ln 5+4\ln 3=\ln 2025\). A \(40\)-digit evaluation checks the endpoint inequalities and places the split integral strictly between \(1999\) and \(2000\).
