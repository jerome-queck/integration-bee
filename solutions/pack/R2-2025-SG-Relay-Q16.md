# R2-2025-SG-Relay-Q16

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (page 4, relay 16). The same floor of an integral is relay 20 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (page 6).
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (page 4, UK relay 20)
- Worked source: derived in this note; the UK mark scheme prints the final value.
- Verification: **manual**. The value is proved below, but the current catalog's definite-integral kind cannot preserve the outer floor.

## Problem

\[
\left\lfloor\int_{2}^{2025}\frac{1}{\lfloor 2\log_{x}5+4\log_{x}3\rfloor}\,dx\right\rfloor.
\]

## Solution

The change-of-base formula gives

\[
2\log_{x}5+4\log_{x}3=\log_{x}2025.
\]

For \(x>1\), \(\lfloor\log_{x}2025\rfloor=k\) on \((2025^{1/(k+1)},2025^{1/k}]\). The exact integer inequalities \(2^{10}<2025<2^{11}\) imply \(2025^{1/11}<2<2025^{1/10}\). The integers \(k\) that meet \([2,2025]\) therefore run from \(1\) through \(10\), with the left endpoint truncated at \(2\). The integrand equals \(1/k\) on each piece, so the integral before taking the floor is

\[
\frac{2025^{1/10}-2}{10}+\sum_{k=2}^{9}\frac{2025^{1/k}-2025^{1/(k+1)}}{k}+(2025-45),
\]

because \(2025^{1/2}=45\). Collecting coefficients gives
\[
I=2025-\frac15-\sum_{k=2}^{10}\frac{2025^{1/k}}{k(k-1)}.
\]
The exact integer-power bounds in the [UK relay 20 note](R2-2025-UK-Relay-Q20.md) prove
\[
1999<\frac{2518880572069}{1260000000}
<I<\frac{2518880573203}{1260000000}<2000.
\]
Thus \(\lfloor I\rfloor=1999\), agreeing with the UK mark. The integral itself is not \(1999\).

## Final answer

\[
1999.
\]

## SymPy self-check

SymPy checks \(2\ln 5+4\ln 3=\ln 2025\). The enclosure uses only integer powers and rational arithmetic, so it does not depend on numerical agreement at a chosen precision.

No ordinary-integral transcript with answer \(1999\) is added: it would omit the outer floor and certify the wrong operation. Promotion requires a catalog/consumer representation for a floor of a definite integral.
