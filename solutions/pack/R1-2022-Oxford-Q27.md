# R1-2022-Oxford-Q27

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 27)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi/2}\frac{\cos x}{2-\sin 2x}\,dx.
\]

## Solution

The denominator identity \(2-\sin 2x=1+(\sin x-\cos x)^{2}\) suggests \(u=\sin x-\cos x\). Then \(du=(\cos x+\sin x)\,dx\) and \(u\) runs from \(-1\) to \(1\). King's substitution \(x\mapsto\pi/2-x\) shows that
\[
\frac{\cos x}{2-\sin 2x}+\frac{\sin x}{2-\sin 2x}=\frac{\cos x+\sin x}{1+u^{2}},
\]
so twice the integral is
\[
\int_{-1}^{1}\frac{du}{1+u^{2}}=\frac{\pi}{2}.
\]
Hence the integral is \(\pi/4\). The mark scheme prints \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q27`. SymPy checks \(1+(\sin x-\cos x)^{2}=2-\sin 2x\) and evaluates \(\int_{-1}^{1}du/(1+u^{2})=\pi/2\).
