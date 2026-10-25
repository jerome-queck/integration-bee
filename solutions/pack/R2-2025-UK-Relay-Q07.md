# R2-2025-UK-Relay-Q07

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 7)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 7)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{\pi/4}^{\pi/2}\sin(x)^{\tan x-2}\bigl(\tan^{2}x\,\ln(\sin x)+\sin^{2}x\bigr)\,dx.
\]

## Solution

The integrand is the derivative of \(\sin(x)^{\tan x}\). At the lower limit,
\[
\sin(\pi/4)^{\tan(\pi/4)}=\Bigl(\frac{\sqrt{2}}{2}\Bigr)^{1}=\frac{1}{\sqrt{2}}.
\]
At the upper limit, set \(\varepsilon=\pi/2-x\). Then \(\tan x\ln(\sin x)=\cot\varepsilon\,\ln(\cos\varepsilon)\to 0\) as \(\varepsilon\downarrow 0\), so the power tends to \(e^{0}=1\). The definite integral is \(1-1/\sqrt{2}\). The mark scheme prints \(1-1/\sqrt{2}\).

## Final answer

\[
1-\frac{1}{\sqrt{2}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q07`. SymPy differentiates \(\sin(x)^{\tan x}\), checks the value at \(\pi/4\), and checks the cotangent-logarithm limit.
