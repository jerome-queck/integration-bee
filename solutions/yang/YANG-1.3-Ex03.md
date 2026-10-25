# YANG-1.3-Ex03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.3 Symmetry, Example 3
- The catalog row stays `verify: manual`. Its stored `answer_plain` is an extraction fragment. The guide prints \(2\tan^{-1}(3)\).

## Problem

\[
\int_0^6\frac{(x-2)(x-3)(x-4)+1}{x^2-6x+10}\,dx.
\]

## Solution

The guide sets \(u=x-3\). The limits become \(-3\) and \(3\), and the integral is

\[
\int_{-3}^{3}\frac{u(u^2-1)+1}{u^2+1}\,du.
\]

Polynomial division gives

\[
\frac{u^3-u+1}{u^2+1}=u-\frac{2u}{u^2+1}+\frac{1}{u^2+1}.
\]

The first two summands are odd, so their integrals on \([-3,3]\) vanish. The guide's displayed step keeps the remaining term:

\[
\int_{-3}^{3}\frac{du}{u^2+1}=2\tan^{-1}(3).
\]

## Final answer

\[
2\tan^{-1}(3).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_yang_1_3_ex03`. SymPy checks the division identity, checks that the discarded piece is odd, and integrates \(1/(u^2+1)\) from \(-3\) to \(3\) to \(2\arctan 3\).
