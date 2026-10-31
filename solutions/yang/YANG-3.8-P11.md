# YANG-3.8-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, Yang §3.8 Speed Bashing, practice item 11, printed p. 68 (PDF p. 69).
- Printed answer: absent.
- Worked source: derived in this note.
- Transcription: corrected from the page image after audit A1 (31 Oct 2026).

## Problem

∫_0^{∞} dx/(e^x + 1/(e^x+1))

\[
\frac{1}{e^{x} + \frac{1}{e^{x} + 1}}
\]

## Solution

Substitute u = e^x. The integral becomes ∫_1^∞ (u+1)/(u(u²+u+1)) du = ∫_1^∞ (1/u − u/(u²+u+1)) du. An antiderivative is log u − ½log(u²+u+1) + (1/√3)arctan((2u+1)/√3). It tends to π/(2√3) at infinity and equals −½log 3 + π/(3√3) at u = 1, so the value is ½log 3 + π/(6√3).

## Final answer

\[
\frac{\sqrt{3} \pi}{18} + \frac{\log{\left(3 \right)}}{2}
\]

Stored `answer_sympy`: `log(3)/2 + sqrt(3)*pi/18`.

## SymPy self-check

`verify/yang_worked_check.py` checks the substitution, the partial fractions, the antiderivative and both endpoint values exactly. The value was also re-checked with mpmath at 40 digits.
