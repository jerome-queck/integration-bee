# YANG-1.17-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.17 Inverse Functions, practice item 01, printed p. 30 (PDF p. 31).
- Printed answer: the guide prints the final below. Worked source: derived in this note.

## Problem

\[
\int_{0}^{1}\bigl(\ln(2)^{2}\,2^{\sqrt{x}}+\ln(1+x)^{2}\bigr)\,dx.
\]

## Solution

The substitution \(u=x\ln(2)^{2}\) turns the first term into \(\int_{0}^{\ln(2)^{2}} e^{\sqrt{u}}\,du=-2+4\ln 2\). SymPy evaluates \(\int_{0}^{1}\ln(1+x)^{2}\,dx=2+2\ln(2)^{2}-4\ln 2\). The sum is \(2\ln(2)^{2}\), which is the final printed in the guide.

## Final answer

\[
2 \log{\left(2 \right)}^{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `2**(sqrt(x))*log(2)**2 + log(x + 1)**2` against `2*log(2)**2` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
