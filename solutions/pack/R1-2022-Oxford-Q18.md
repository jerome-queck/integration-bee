# R1-2022-Oxford-Q18

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 18)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}\frac{\arctan(b\sin x)}{\sin x}\,dx.
\]

## Solution

Let
\[
I(b)=\int_0^{\pi/2}\frac{\arctan(b\sin x)}{\sin x}\,dx.
\]
Both sides of the closed form are odd in \(b\), so it is enough to differentiate for \(b>0\). Then
\[
I'(b)=\int_0^{\pi/2}\frac{1}{1+b^{2}\sin^{2}x}\,dx.
\]
The substitution \(u=\tan x\) rewrites the integrand as \(1/((b^{2}+1)u^{2}+1)\) and gives
\[
I'(b)=\frac{\pi}{2\sqrt{b^{2}+1}}.
\]
Since \(I(0)=0\),
\[
I(b)=\frac{\pi}{2}\operatorname{arsinh} b=\frac{\pi}{2}\ln\bigl(b+\sqrt{b^{2}+1}\bigr).
\]
The mark scheme prints \((\pi/2)\sinh^{-1}(b)\).

## Final answer

\[
\dfrac{\pi}{2}\operatorname{arsinh} b.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q18`. SymPy evaluates the substituted integral as \(\pi/(2\sqrt{b^{2}+1})\), checks the tangent rewrite of the kernel, and differentiates \((\pi/2)\operatorname{arsinh} b\).
