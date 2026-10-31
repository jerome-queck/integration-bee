# YANG-2.6-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice item 12, printed p. 45 (PDF p. 46).
- Printed answer: absent.
- Worked source: derived in this note.
- Transcription: corrected from the page image after audit A1 (31 Oct 2026).

## Problem

∫ dx/(√3 sin(x) + cos(x))

\[
\frac{1}{\sqrt{3} \sin{\left(x \right)} + \cos{\left(x \right)}}
\]

## Solution

Write √3 sin x + cos x = 2 sin(x + π/6). With t = x + π/6 the integral is ½∫ csc t dt = ½ log|tan(t/2)| = ½ log|tan(x/2 + π/12)|.

## Final answer

\[
\frac{\log{\left(\left|{\tan{\left(\frac{x}{2} + \frac{\pi}{12} \right)}}\right| \right)}}{2}
\]

Stored `answer_sympy`: `log(Abs(tan(x/2 + pi/12)))/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by differentiating the stored antiderivative back to the stored integrand. The value was also re-checked with mpmath at 40 digits.
