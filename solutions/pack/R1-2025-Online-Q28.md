# R1-2025-Online-Q28

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 28)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 28)
- The catalog row is not changed.

## Problem

\[
\int_{-90}^{90}\operatorname{mrt}\bigl(x^{3}-(3+a)x^{2}+(4+2a)x-(2+a)\bigr)\,da.
\]

## Solution

The solutions PDF defines \(\operatorname{mrt}(f)\) to be \(0\) when \(f\) has fewer than two distinct real roots, and otherwise the smallest distance between distinct real roots. The cubic factors as
\[
(x-1)\bigl(x^{2}-(2+a)x+(2+a)\bigr).
\]
The other roots are
\[
\frac{2+a\pm\sqrt{a^{2}-4}}{2}=1+\frac{a\pm\sqrt{a^{2}-4}}{2},
\]
so \(\operatorname{mrt}=0\) for \(|a|<2\). For \(a>2\) the smaller positive distance is \((a-\sqrt{a^{2}-4})/2\) when \(a>3/\sqrt{2}\), and \(\sqrt{a^{2}-4}\) between \(2\) and \(3/\sqrt{2}\). The signs reverse for \(a<-2\). The integral reduces to
\[
\Biggl(2\int_2^{3/\sqrt{2}}-\int_{3/\sqrt{2}}^{90}\Biggr)\sqrt{a^{2}-4}\,da+\int_{3/\sqrt{2}}^{90}a\,da.
\]
With \(F(a)=a\sqrt{a^{2}-4}/2-2\ln(a+\sqrt{a^{2}-4})\), the solutions PDF evaluates
\[
-F(90)+3F\Bigl(\frac{3}{\sqrt{2}}\Bigr)-2F(2)+\frac{16191}{4}.
\]
The constant \(16191/4=(90^{2}-(3/\sqrt{2})^{2})/2\), and \(\sqrt{2024}=2\sqrt{506}\). The leftover logarithms cancel because \((45-2\sqrt{506})(45+2\sqrt{506})=1\). The mark scheme prints
\[
90\bigl(45-\sqrt{2024}\bigr)-2\ln\bigl(45-\sqrt{2024}\bigr)-3\ln 2.
\]

## Final answer

\[
90\bigl(45-\sqrt{2024}\bigr)-2\ln\bigl(45-\sqrt{2024}\bigr)-3\ln 2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q28`. SymPy factors the cubic, checks the distance comparison at \(3/\sqrt{2}\), and reduces the antiderivative combination to the printed value.
