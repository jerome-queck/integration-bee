# R1-2022-Oxford-Q29

- Problem: `sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf` (problem 29)
- Printed answer: `sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_0^{\pi}\sec x\ln\Bigl(1+\frac{\cos x}{3}\Bigr)\,dx.
\]

## Solution

The factor \(\sec x\) is singular at \(\pi/2\), but \(\ln(1+a\cos x)\sim a\cos x\) there, so the integrand extends continuously for \(|a|<1\). Set
\[
I(a)=\int_0^{\pi}\sec x\ln(1+a\cos x)\,dx.
\]
Differentiating under the integral gives
\[
I'(a)=\int_0^{\pi}\frac{dx}{1+a\cos x}.
\]
The Weierstrass substitution \(t=\tan(x/2)\) has derivative
\[
\frac{d}{dt}\left(\frac{2}{\sqrt{1-a^{2}}}\arctan\Bigl(t\sqrt{\frac{1-a}{1+a}}\Bigr)\right)=\frac{2}{(1+a)+(1-a)t^{2}},
\]
and \(\arctan t\to\pi/2\) as \(t\to\infty\), so \(I'(a)=\pi/\sqrt{1-a^{2}}\). Also \(I(0)=0\), hence \(I(a)=\pi\arcsin a\). The printed value is the case \(a=1/3\). The mark scheme prints \(\pi\sin^{-1}(1/3)\).

## Final answer

\[
\pi\arcsin\dfrac13.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2022_oxford_q29`. SymPy differentiates the Weierstrass antiderivative, checks \(\lim_{t\to\infty}\arctan t=\pi/2\), and differentiates \(\pi\arcsin a\).
