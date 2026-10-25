# R2-2025-SG-Relay-Q11

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 11)
- Printed answer: none in the pack. The value below is derived in this note.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{0}\Biggl(\frac{3x^{2}+2x}{x^{3}+x^{2}-1}+\frac{6x^{2}+2x}{2x^{3}+x^{2}-2}\Biggr)\sqrt{(x^{3}+x^{2}-1)(2x^{3}+x^{2}-2)}\,dx.
\]

## Solution

Let \(a=x^{3}+x^{2}-1\) and \(b=2x^{3}+x^{2}-2\). Then \(a'=3x^{2}+2x\) and \(b'=6x^{2}+2x\), so the integrand is
\[
\Bigl(\frac{a'}{a}+\frac{b'}{b}\Bigr)\sqrt{ab}=2\frac{d}{dx}\sqrt{ab}.
\]
On \([-1,0]\) both cubics stay negative: the critical value \(a(-2/3)=-23/27\) is the highest value of \(a\), and \(b\) is likewise negative, so \(ab>0\). The endpoints are \(\sqrt{ab(-1)}=\sqrt{3}\) and \(\sqrt{ab(0)}=\sqrt{2}\). The definite integral is \(2(\sqrt{2}-\sqrt{3})\).

## Final answer

\[
2(\sqrt{2}-\sqrt{3}).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q11`. SymPy checks the derivative identity and the endpoint products.
