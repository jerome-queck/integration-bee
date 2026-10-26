# R3-2024-Dichotomy-S2-Q07a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf`, PDF p. 4 (problem 7a).
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF p. 5 (Segment 2, problem 7a).
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF p. 12 (Set 1/Segment 2, problem 7a).
- Catalog contract: positive infinity, with the complete limit and its inner bounds retained. The exact lower-bound certificate is in `verify/pack_handoff_b.py` and is reused by `verify/pack_handoff_f_integrals.py`.

## Problem

\[\lim_{n\to\infty}\int_{1}^{n}\ln\left(1+\frac{e}{n}+\frac{1}{\sqrt[e]{nx}}\right)dx.\]

## Solution

The solutions PDF treats \(\int_{1}^{n}\ln\bigl(a_{n,p}+1/\sqrt[p]{nx}\bigr)\,dx\) by the substitution \(x=1/(n y^{p})\). For \(p=e\) and \(a_{n,e}=1+e/n\), the boundary term \(n\ln\bigl(1+e/n+n^{-2/e}\bigr)\) tends to \(+\infty\), and the remaining integral is positive. The limit is \(+\infty\). The answers sheet also accepts \(\infty\).

## Final answer

\[+\infty.\]

## SymPy self-check

The gate retains the complete `Limit(Integral(...),n,oo)`. For \(1\le x\le n\), the decreasing power term is at least \(n^{-2/e}\). The derivative-checked inequality \(\log(1+t)\ge t/(1+t)\) bounds the integral below by \((n-1)/(1+n^{2/e})\). The symbolic limit is \(+\infty\), since \(1-2/e>0\). Only the answer `oo` matches this derived divergent value. The signed-infinity comparator uses exact equality before subtraction, so it accepts `oo` against `oo` without producing `nan`; negative infinity and every finite answer fail. Finite scalar comparison retains its existing algebraic checks.
