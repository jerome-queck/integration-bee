# R2-2025-UK-Relay-Q02

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 2)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 2)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}(1-x\tan x)\tan x\,dx.
\]

## Solution

Rewrite \(\tan^{2}x=\sec^{2}x-1\):
\[
(1-x\tan x)\tan x=\tan x-x\sec^{2}x+x.
\]
An antiderivative is
\[
-2\ln(\cos x)-x\tan x+\frac{x^{2}}{2}.
\]
The limit at \(0\) is \(0\). At \(\pi/4\),
\[
-2\ln\Bigl(\frac{\sqrt{2}}{2}\Bigr)-\frac{\pi}{4}+\frac{\pi^{2}}{32}=\ln 2-\frac{\pi}{4}+\frac{\pi^{2}}{32}.
\]

## Final answer

\[
\ln 2-\dfrac{\pi}{4}+\dfrac{\pi^{2}}{32}.
\]

## SymPy self-check

SymPy differentiates \(-2\ln(\cos x)-x\tan x+x^{2}/2\) back to \((1-x\tan x)\tan x\). The value at \(\pi/4\), minus the limit at \(0\), simplifies to \(\ln 2-\pi/4+\pi^{2}/32\).
