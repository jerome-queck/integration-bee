# R2-2025-UK-Relay-Q20

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 20)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 20)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\left\lfloor\int_{2}^{2025}\lfloor 2\log_{x}5+4\log_{x}3\rfloor\,dx\right\rfloor.
\]

## Solution

The change-of-base formula gives
\[
2\log_{x}5+4\log_{x}3=\log_{x}(5^{2}\cdot 3^{4})=\log_{x}2025.
\]
For \(x>1\), \(\lfloor\log_{x}2025\rfloor=k\) on the interval \((2025^{1/(k+1)},2025^{1/k}]\). Since \(\log_{2}2025\) lies strictly between \(10\) and \(11\), and \(2025^{1/11}<2\), the integers \(k\) that meet \([2,2025]\) run from \(1\) through \(10\), with the left endpoint truncated at \(2\). The integral is
\[
\frac{2025^{1/10}-2}{10}+\sum_{k=2}^{9}\frac{2025^{1/k}-2025^{1/(k+1)}}{k}+(2025-45),
\]
because \(2025^{1/2}=45\) and \(2025^{1/1}=2025\). At \(40\) decimal places this value is about \(1999.1115657464932246\), so its floor is \(1999\). The mark scheme prints \(1999\).

## Final answer

\[
1999.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q20`. SymPy checks \(2\ln 5+4\ln 3=\ln 2025\). A \(40\)-digit evaluation of the split integral lies strictly between \(1999\) and \(2000\).
