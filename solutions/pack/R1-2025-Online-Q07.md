# R1-2025-Online-Q07

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 7)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: derived in this note; the mark scheme prints the final value. The solutions PDF works a different integral.
- The catalog row is not changed.

## Problem

\[
\int_0^1\left(\sum_{k=0}^{2025}x^{k}-\sum_{m=1}^{2025}\{x^{\circ m}\}\right)\,dx,
\]
where \(x^{\circ 1}=x\) and \(x^{\circ(m+1)}=x\cdot x^{\circ m}\), and \(\{\,\cdot\,\}\) is the fractional part. The second sum is the one the problem sheet braces as \(2025\) nested copies.

## Solution

On \([0,1)\), \(\{x\}=x\). If a value \(y\) lies in \([0,1)\), then \(\{xy\}=xy\). Starting from \(\{x\}=x\) and repeating that step shows
\[
\{x^{\circ m}\}=x^{m}\qquad\text{for }1\le m\le 2025.
\]
The integrand is therefore
\[
\sum_{k=0}^{2025}x^{k}-\sum_{m=1}^{2025}x^{m}=1
\]
on \([0,1)\). The value at the single point \(x=1\) does not change the integral, so
\[
\int_0^1 1\,dx=1.
\]
The mark scheme prints \(1\).

`sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 7) instead integrates \(\{x\}+\{x\{x\}\}+\cdots-1/x\) and says that integral diverges, with Cauchy principal value \(-1\). That is not the integral printed on the problem sheet, so it is not used here.

## Final answer

\[
1.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q07`. SymPy simplifies \(\sum_{k=0}^{2025}x^{k}-\sum_{k=1}^{2025}x^{k}\) to \(1\), evaluates \(\int_0^1 1\,dx=1\), and checks \(\{2^{-n}\}=2^{-n}\) for \(1\le n\le 5\).
