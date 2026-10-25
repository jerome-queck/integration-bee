# R2-2025-SG-Relay-Q08

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 8). The same integral is relay 7 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 7)
- Worked source: derived in this note; the UK mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{\pi/4}^{\pi/2}\sin(x)^{\tan x-2}\bigl(\tan^{2}x\,\ln(\sin x)+\sin^{2}x\bigr)\,dx.
\]

## Solution

Let \(u(x)=\sin(x)^{\tan x}=\exp(\tan x\,\ln\sin x)\) on \((\pi/4,\pi/2)\). Logarithmic differentiation gives

\[
\frac{u'}{u}=\sec^{2}x\,\ln(\sin x)+1.
\]

The printed integrand divided by \(u\) is \(\tan^{2}x\,\ln(\sin x)/\sin^{2}x+1\). The identity \(\tan^{2}x/\sin^{2}x=\sec^{2}x\) makes this equal to \(u'/u\), so the integrand is \(u'\). At the lower limit, \(\sin(\pi/4)^{\tan(\pi/4)}=1/\sqrt{2}\). As \(x\to(\pi/2)^{-}\), \(\tan x\,\ln(\sin x)\to 0\), so \(u(x)\to 1\). The improper integral is \(1-1/\sqrt{2}\). The UK mark scheme prints \(1-1/\sqrt{2}\).

## Final answer

\[
1-\frac{1}{\sqrt{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q08`. SymPy checks the logarithmic derivative, the secant identity, the value at \(\pi/4\), and the limit at \(\pi/2\).
