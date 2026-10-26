# R3-2024-Dichotomy-S1-Q04b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 4b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 4b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 4b)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\int_{0}^{1/2}\left(\frac{x}{\sqrt{x+\dfrac{x}{\sqrt{x+\cdots}}}}+\sqrt{x^{3}+x^{2}\sqrt{x^{3}+x^{2}\sqrt{\cdots}}}\right)dx.\]

## Solution

Write \(f(x)\) for the first continued radical and \(g(x)\) for the second. Then \(f^{3}+f^{2}x-x^{2}=0\) and \(g^{2}-x^{2}g-x^{3}=0\). Swapping the variables turns one polynomial equation into the other, so \(f\) and \(g\) are inverse functions. The solutions PDF records \(g(0)=0\) and \(g(1/2)=1/2\), and the integral of a function plus its inverse on that interval is \((1/2)\cdot(1/2)=1/4\).

## Final answer

\[\dfrac{1}{4}.\]

## SymPy self-check

For a literal expression evaluable by SymPy, put \(A=x^2/2-x^3/27+\sqrt{x^4/4-x^5/27}\). The continued fractions/radicals are transcribed as \(f=A^{1/3}+x^2/(9A^{1/3})-x/3\) and \(g=(x^2+\sqrt{x^4+4x^3})/2\), with their continuous values at zero. The certificate checks Cardano's polynomial identity and positivity of the selected root on \((0,1/2]\), and the positive quadratic identity for g. The original iteration maps \(z\mapsto x/\sqrt{x+z}\) and \(z\mapsto\sqrt{x^3+x^2z}\) are contractions in logarithmic coordinates, since their log derivatives have absolute value \(z/[2(x+z)]<1/2\). Thus these formulas are the limits of the printed nests. The checked root equations become negatives of each other after swapping variables. Positivity and uniqueness show f and g are inverses. Finally the gate checks g is increasing and has endpoints 0 and 1/2, so the inverse-area identity gives \(\int(f+g)=1/4\).
