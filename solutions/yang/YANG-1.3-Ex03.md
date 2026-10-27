# YANG-1.3-Ex03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.3 Symmetry, Example 3, printed p. 9 (PDF p. 10).
- [Printed problem and worked answer](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=10).

## Status: resolved extraction error

The guide prints a definite integral from \(0\) to \(6\), evaluated as
\(2\tan^{-1}(3)\). The earlier catalog mistakenly classified it as indefinite
and stored the extraction fragment `Z x` as the answer. The catalog now records
the printed limits, integrand, and answer, with `kind: definite` and
`verify: sympy`. The guide's answer is unchanged.

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

The denominator \(u^2+1\) is strictly positive for real \(u\), so each term is
continuous on \([-3,3]\). There is no singularity or principal-value convention
hidden in the symmetry argument.

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

`verify/yang_certificates.py` repeats the exact substitution and parity proof
inside the gate. It first matches the printed integrand and limits \([0,6]\),
checks the shifted denominator and decomposition, and verifies
\((\arctan u)'=1/(1+u^2)\) before evaluating the endpoints. The catalog stores
`answer_sympy=2*atan(3)`. Wrong answers such as `0` and `atan(3)` fail the gate's
exact value comparison; numerical quadrature is not used to certify the row.
