# R2-2025-SG-Relay-Q22

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 22). The same integral is relay 16 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 16)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{\sqrt{2}-1}^{\sqrt{2}+1}\frac{dx}{x\bigl(e+(x^{2}+1)^{1/\ln x}\bigr)}.
\]

## Solution

Set \(x=e^{t}\). The limits are \(\pm\ln(1+\sqrt{2})\), because \((\sqrt{2}-1)(\sqrt{2}+1)=1\). Write
\[
A(t)=\exp\bigl(\ln(e^{2t}+1)/t\bigr).
\]
Then \(A(-t)=e^{2}/A(t)\), and
\[
\frac{1}{e+A(t)}+\frac{1}{e+e^{2}/A(t)}=\frac{1}{e}.
\]
The integrand in \(t\) is the first term. Folding the symmetric interval multiplies the constant \(1/e\) by the half-length, and the integral is \((\ln(1+\sqrt{2}))/e\). The mark scheme prints \((1/e)\ln(\sqrt{2}+1)\).

## Final answer

\[
\dfrac{1}{e}\ln(1+\sqrt{2}).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q22`. SymPy checks the same endpoint reflection as the UK relay 16 note.
