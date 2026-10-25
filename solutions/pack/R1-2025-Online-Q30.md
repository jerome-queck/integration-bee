# R1-2025-Online-Q30

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 30)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 30)
- The catalog row is not changed.

## Problem

\[
\int_1^2\frac{\arctan(1+x)}{x}\,dx.
\]

## Solution

The substitution \(x\mapsto 2/x\) preserves \(dx/x\) and replaces \(\arctan(1+x)\) by \(\arctan(1+2/x)\). Adding the two copies, and using \((1+x)(1+2/x)>1\), the arctangent sum is
\[
\arctan(1+x)+\arctan\Bigl(1+\frac2x\Bigr)=\pi+\arctan(-1)=\frac{3\pi}{4}.
\]
Therefore
\[
I=\frac12\int_1^2\frac{3\pi}{4x}\,dx=\frac{3\pi\ln 2}{8}.
\]
The mark scheme prints \(3\pi\ln 2/8\).

## Final answer

\[
\frac{3\pi\ln 2}{8}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q30`. SymPy checks \(((1+x)+(1+2/x))/(1-(1+x)(1+2/x))=-1\), evaluates \(\pi+\arctan(-1)=3\pi/4\), and integrates \((3\pi/8)/x\) from \(1\) to \(2\). The substitution \(x=2/u\) preserves \(dx/x\) up to sign.
