# R2-2025-SG-Relay-Q02

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 2). The same integral is relay 2 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 2)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}(1-x\tan x)\tan x\,dx.
\]

## Solution

The antiderivative \(-2\ln(\cos x)-x\tan x+x^{2}/2\) vanishes at \(0\) and equals \(\ln 2-\pi/4+\pi^{2}/32\) at \(\pi/4\). The UK mark scheme prints that value for this integral.

## Final answer

\[
\ln 2-\dfrac{\pi}{4}+\dfrac{\pi^{2}}{32}.
\]

## SymPy self-check

SymPy differentiates \(-2\ln(\cos x)-x\tan x+x^{2}/2\) back to \((1-x\tan x)\tan x\), and the definite evaluation simplifies to \(\ln 2-\pi/4+\pi^{2}/32\).
