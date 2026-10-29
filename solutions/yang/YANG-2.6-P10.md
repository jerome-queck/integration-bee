# YANG-2.6-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §2.6 Trig-Identities Manipulation, practice list item 10, printed p. 45 (PDF p. 46).
- [Printed problem](https://github.com/jerome-queck/integration-bee/blob/0d87725e7c5c2b4752bb486ced9b43acfc951e24/sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf#page=46).

## Status: derived final

The practice list prints the integral and does not print a final. This note derives one. `verify/yang_certificates.py` accepts it. Worked source: derived in this note.

## Problem

\[
\int \sqrt{\sqrt{\sqrt{\sin{\left(x \right)} \tan{\left(x \right)}} \tan{\left(x \right)}} \tan{\left(x \right)}} \sec^{2}{\left(x \right)}\,dx.
\]

## Solution

The printed nest and \(\tan(x)^{7}\sin(x)\) have the same eighth power. Substituting positive factors for \(\tan(x)\) and \(\sin(x)\) denests that nest to \(\tan(x)^{7/8}\sin(x)^{1/8}\). Where sine and cosine are positive, the derivative of \(\frac{8}{15}\sec(x)^{15/8}\) and the denested integrand both reduce to \(\sin(x)/\cos(x)^{23/8}\).

## Final answer

\[
\frac{8 \sec^{\frac{15}{8}}{\left(x \right)}}{15}.
\]

The catalog omits a constant of integration.

## SymPy self-check

`sympy_expr` is `sqrt(sqrt(sqrt(sin(x)*tan(x))*tan(x))*tan(x))*sec(x)**2`. `answer_sympy` is `8*sec(x)**(15/8)/15`. `verify/yang_certificates.py` checks the eighth-power identity, the positive-factor denesting, and the sine-cosine reduction of the derivative. `make check` re-proves the stored row.
