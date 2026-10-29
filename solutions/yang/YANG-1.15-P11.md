# YANG-1.15-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 11, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sqrt{2\tan^{2}x+2\sec x\tan x+1}\,dx.
\]

## Solution

The radicand expands to \((\sec x+\tan x)^{2}\). The square root is the nonnegative root, so the integrand is \(|\sec x+\tan x|\) wherever secant and tangent are defined, that is wherever \(\cos x\neq 0\).

\(\sec x+\tan x=(1+\sin x)/\cos x\), and \(1+\sin x=(\sin(x/2)+\cos(x/2))^{2}\) is nonnegative. The quotient therefore has the sign of \(\cos x\). Where \(\cos x>0\) the integrand is \(\sec x+\tan x\), and

\[
\log(\sec x)+\log(\sec x+\tan x)
\]

differentiates to \((1+\sin x)/\cos x\). Where \(\cos x<0\) the integrand is \(-(\sec x+\tan x)\), and

\[
-\log(-\sec x)-\log(-(\sec x+\tan x))
\]

differentiates to \(-(1+\sin x)/\cos x\). The two formulas are used on opposite sides of the singularities at \(\cos x=0\); they are not required to meet there.

## Final answer

\[
\begin{cases} \log{\left(\tan{\left(x \right)} + \sec{\left(x \right)} \right)} + \log{\left(\sec{\left(x \right)} \right)} & \text{for}\: \cos{\left(x \right)} > 0 \\- \log{\left(- \tan{\left(x \right)} - \sec{\left(x \right)} \right)} - \log{\left(- \sec{\left(x \right)} \right)} & \text{otherwise} \end{cases}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(2*tan(x)**2 + 2*tan(x)*sec(x) + 1)` against `Piecewise((log(tan(x) + sec(x)) + log(sec(x)), cos(x) > 0), (-log(-tan(x) - sec(x)) - log(-sec(x)), True))` (indefinite). The check differentiates each piece on the sign of \(\cos x\). The reduction is `verify/yang_certificates.py`.
