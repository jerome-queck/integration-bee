# YANG-1.17-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.17 Inverse Functions, practice item 01, printed p. 30 (PDF p. 31).
- Printed answer: the guide prints the final below. Worked source: derived in this note.

## Problem

\[
\int_{0}^{1}\bigl(\ln(2)^{2}\,2^{\sqrt{x}}+\ln(1+x)^{2}\bigr)\,dx.
\]

## Solution

The guide sets \(u=x\ln(2)^{2}\) on the first term, which becomes \(\int_{0}^{\ln(2)^{2}} e^{\sqrt{u}}\,du\). Split the integrand as \((e^{\sqrt{u}}-1)+1\). The inverse of \(\ln(1+x)^{2}\) is \(e^{\sqrt{x}}-1\), and those two functions run between \(0\) and \(\ln(2)^{2}\). Their integrals add to \(\ln(2)^{2}\). The extra \(+1\) adds another \(\ln(2)^{2}\). The total is \(2\ln(2)^{2}\), which is the final printed in the guide.

## Final answer

\[
2 \log{\left(2 \right)}^{2}.
\]

## SymPy self-check

`verify/yang_worked_check.py` rechecks the worked solution stored on this row. Each stated derivative is differentiated, and the inverse-function sum is an exact endpoint evaluation. `verify/pack_gate.py` proves `2**(sqrt(x))*log(2)**2 + log(x + 1)**2` against `2*log(2)**2`.
