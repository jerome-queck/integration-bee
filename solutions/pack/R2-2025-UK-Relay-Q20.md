# R2-2025-UK-Relay-Q20

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (page 6, relay 20)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (page 4, relay 20)
- Worked source: derived in this note; the mark scheme prints the final value.
- Verification: **manual**. The value is proved below, but the current catalog's definite-integral kind cannot preserve the outer floor.

## Problem

\[
\left\lfloor\int_{2}^{2025}\frac{1}{\lfloor 2\log_{x}5+4\log_{x}3\rfloor}\,dx\right\rfloor.
\]

## Solution

The change-of-base formula gives
\[
2\log_{x}5+4\log_{x}3=\log_{x}(5^{2}\cdot 3^{4})=\log_{x}2025.
\]
The source PDF prints a reciprocal and an outer floor; both are essential. For \(x>1\), \(\lfloor\log_{x}2025\rfloor=k\) on the interval \((2025^{1/(k+1)},2025^{1/k}]\). Since \(2^{10}<2025<2^{11}\), the integers \(k\) that meet \([2,2025]\) run from \(1\) through \(10\), with the left endpoint truncated at \(2\). The integral before taking the floor is
\[
\frac{2025^{1/10}-2}{10}+\sum_{k=2}^{9}\frac{2025^{1/k}-2025^{1/(k+1)}}{k}+(2025-45),
\]
because \(2025^{1/2}=45\) and \(2025^{1/1}=2025\). Collecting coefficients gives the exact value
\[
I=2025-\frac15-\sum_{k=2}^{10}\frac{2025^{1/k}}{k(k-1)}.
\]
An exact rational enclosure, described below, is
\[
1999<\frac{2518880572069}{1260000000}
<I<\frac{2518880573203}{1260000000}<2000.
\]
Consequently \(\lfloor I\rfloor=1999\), agreeing with the mark scheme. The integral itself is not \(1999\).

## Final answer

\[
1999.
\]

## SymPy self-check

For \(k=2,\ldots,10\), take the integers
\[
(a_2,\ldots,a_{10})=(45000000,12651489,6708203,4584426,3556893,
2967197,2590020,2330132,2141127).
\]
Integer arithmetic checks
\(a_k^k\le 2025\cdot10^{6k}<(a_k+1)^k\). Hence
\(a_k/10^6\le2025^{1/k}<(a_k+1)/10^6\).
Substituting these bounds in the exact sum gives the displayed rational enclosure. This proves the floor without a floating-point comparison.

No ordinary-integral transcript with answer \(1999\) is added: it would omit the outer floor and certify the wrong operation. Promotion requires a catalog/consumer representation for a floor of a definite integral.
