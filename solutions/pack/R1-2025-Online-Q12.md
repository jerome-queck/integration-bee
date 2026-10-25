# R1-2025-Online-Q12

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 12)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 12)
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}\int_0^1\bigl|x-\bigl|x^{2}-\bigl|\cdots\bigl|x^{n}\bigr|\cdots\bigr|\bigr|\,dx.
\]

## Solution

On \([0,1]\) the powers decrease, so each absolute value unfolds:
\[
\bigl|x-|x^{2}-|\cdots||\bigr|=x-x^{2}+x^{3}-\cdots+(-1)^{n+1}x^{n}.
\]
The solutions PDF integrates that polynomial and passes to the limit. The partial integrals are the partial sums of the alternating harmonic series, with limit \(1-\ln 2\). The mark scheme prints \(1-\ln 2\). It also records half credit for the series without the closed value; the final value is the closed form.

## Final answer

\[
1-\ln 2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q12`. SymPy checks one absolute-value unfolding and sums \(\sum_{k\ge 1}(-1)^{k+1}/(k+1)\) to \(1-\ln 2\).
