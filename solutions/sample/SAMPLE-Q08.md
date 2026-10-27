# SAMPLE-Q08

- Problem: `sources/Integration_Competition_Sample_problems.pdf`, p. 1, question 8
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`, p. 1, answer 8
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf`, p. 9, question 8

## Status: resolved symbolic certificate

Catalog row `SAMPLE-Q08` is `verify: sympy`. The printed answer and worked derivation agree with the value below. The PDFs do not state the convergence restriction; this certificate makes it explicit: \(\Re s>1\).

The stored symbolic expression parametrizes the entire half-plane as \(s=1+\sigma+i\tau\), where \(\sigma>0\) and \(\tau\in\mathbb R\). Both symbol assumptions survive canonicalization. The displayed printed answer remains \(\Gamma(s)\zeta(s)\); the symbolic fields use the equivalent expression in \(\sigma,\tau\).

## Problem

\[
\int_0^\infty \frac{x^{s-1}}{e^x-1}\,dx.
\]

Here \(x^{s-1}=\exp((s-1)\ln x)\) uses the real logarithm for \(x>0\), and \(\Re s>1\).

## Solution

The solutions PDF divides numerator and denominator by \(e^x\) and expands the geometric series:

\[
\frac{x^{s-1}}{e^x-1}=\sum_{k\ge 1} x^{s-1}e^{-kx}.
\]

For \(x>0\), the geometric ratio satisfies \(0<e^{-x}<1\). Put \(\rho=\Re s\). Near zero, the absolute value of the integrand behaves like \(x^{\rho-2}\), which is integrable precisely when \(\rho>1\). At infinity it is bounded by a constant times \(x^{\rho-1}e^{-x}\). Moreover,

\[
\sum_{k\ge1}|x^{s-1}e^{-kx}|=\frac{x^{\rho-1}}{e^x-1}.
\]

This integrable majorant justifies interchanging the series and integral by absolute convergence.

The substitution \(u=kx\) on each term produces

\[
\int_0^\infty x^{s-1}e^{-kx}\,dx=\frac{1}{k^s}\int_0^\infty u^{s-1}e^{-u}\,du=\frac{\Gamma(s)}{k^s}.
\]

Summing over \(k\) gives \(\Gamma(s)\zeta(s)\).

This proves the ordinary improper integral on its convergent half-plane. Analytic continuation of the final special functions does not define the improper integral at parameters outside that domain.

## Final answer

\[
\Gamma(s)\zeta(s),\qquad \Re s>1.
\]

## SymPy self-check

`verify/sample_certificates.py` supplies the series certificate through `pack_gate.proven`. It checks the integrand, the endpoints \(0,\infty\), and the positive real part of \(s-1\); verifies the geometric series, the Gamma moment, and the zeta sum; and returns their exact product. It does not admit an unconstrained parameter merely because the special-function expression exists.

`solutions/sample_self_check.py` reproves the stored parametric row and runs `check_q08`, including the Gamma-moment identity. Wrong-answer controls reject zero, twice the product, and the product plus one.
