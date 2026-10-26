# R3-2024-Dichotomy-S2-Q07a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 7a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 7a)
- Catalog verification: `manual`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\lim_{n\to\infty}\int_{1}^{n}\ln\left(1+\frac{e}{n}+\frac{1}{\sqrt[e]{nx}}\right)dx.\]

## Solution

The solutions PDF treats \(\int_{1}^{n}\ln\bigl(a_{n,p}+1/\sqrt[p]{nx}\bigr)\,dx\) by the substitution \(x=1/(n y^{p})\). For \(p=e\) and \(a_{n,e}=1+e/n\), the boundary term \(n\ln\bigl(1+e/n+n^{-2/e}\bigr)\) tends to \(+\infty\), and the remaining integral is positive. The limit is \(+\infty\). The answers sheet also accepts \(\infty\).

## Final answer

\[+\infty.\]

## SymPy self-check

The gate retains the complete `Limit(Integral(...),n,oo)`. For \(1\le x\le n\), the decreasing power term is at least \(n^{-2/e}\). The derivative-checked inequality \(\log(1+t)\ge t/(1+t)\) bounds the integral below by \((n-1)/(1+n^{2/e})\). The symbolic limit is \(+\infty\), since \(1-2/e>0\). Only the answer `oo` matches this derived divergent value. The row remains manual because `turn_contract.grade_problem` currently rejects a correct `oo` submission against the stored answer `oo`. Its comparator subtracts the two infinities and obtains `nan`. The transcript is held from recovery until that separate grading defect is fixed; the printed answer is unchanged.
