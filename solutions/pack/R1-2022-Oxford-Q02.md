# R1-2022-Oxford-Q02

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 2)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int\sqrt{x\sqrt[3]{x\sqrt[4]{x\sqrt[5]{x\cdots}}}}\,dx.
\]

## Solution

The radical starts at the square root, so the exponent of \(x\) is \(\sum_{k\ge 2}1/k!=e-2\). The integrand is \(x^{e-2}\), and
\[
\frac{d}{dx}\frac{x^{e-1}}{e-1}=x^{e-2}.
\]
The mark scheme prints \(x^{e-1}/(e-1)\).

## Final answer

\[
\dfrac{x^{e-1}}{e-1}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q02`. SymPy sums \(\sum_{n\ge 2}1/n!\) to \(e-2\) and differentiates \(x^{e-1}/(e-1)\) back to \(x^{e-2}\).
