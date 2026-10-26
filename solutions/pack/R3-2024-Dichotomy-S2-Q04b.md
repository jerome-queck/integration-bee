# R3-2024-Dichotomy-S2-Q04b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 4b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 4b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 4b)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\int_{0}^{\infty}\frac{1}{\bigl(x+\sqrt{x^{2}+1}\bigr)(1+x)}\,dx.\]

## Solution

The same rationalizing factor produces \((\sqrt{x^{2}+1}-x)/(x+1)\). The solutions PDF substitutes \(x=\tan u\) and then a Weierstrass substitution, and partial fractions give \[-1-\ln 2-(\sqrt{2}+1)\ln(\sqrt{2}-1)+(\sqrt{2}-1)\ln(\sqrt{2}+1).\]

The answers sheet also prints \(-1-\ln 2+2\sqrt{2}\ln(1+\sqrt{2})\), \(-1-\ln 2+2\sqrt{2}\operatorname{arsinh} 1\), and \(-1-\ln 2+2\sqrt{2}\operatorname{artanh}(1/\sqrt{2})\).

## Final answer

\[-1-\ln 2-(\sqrt{2}+1)\ln(\sqrt{2}-1)+(\sqrt{2}-1)\ln(\sqrt{2}+1).\]

## SymPy self-check

The gate checks the inverse substitution \(x=(1-t^2)/(2t)\), its orientation, and the positive square root. It differentiates a real logarithmic primitive of the resulting rational function and evaluates both endpoints. The value equals the printed multilog form.
