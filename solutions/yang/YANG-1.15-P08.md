# YANG-1.15-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 08, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sqrt{1+\cos x}\,dx.
\]

## Solution

The half-angle identity gives \(\sqrt{1+\cos x}=\sqrt{2}\,|\cos(x/2)|\). On each interval where \(\lfloor x/(2\pi)+1/2\rfloor\) is a constant integer \(k\), \(\cos(x/2)\) has sign \((-1)^k\), and the ordinary derivative of \(2\sqrt{2}(-1)^k\sin(x/2)\) is the integrand. The formula \(2\sin x/\sqrt{1+\cos x}\) equals that piece between the odd multiples of \(\pi\) and jumps by \(-4\sqrt{2}\) at each of those points. Adding \(4\sqrt{2}\lfloor x/(2\pi)+1/2\rfloor\) removes the jump. The left and right limits agree at every odd multiple of \(\pi\).

## Final answer

\[
2(-1)^{\lfloor x/(2\pi)+1/2\rfloor}\sqrt{2}\sin(x/2)+4\sqrt{2}\lfloor x/(2\pi)+1/2\rfloor.
\]

## SymPy self-check

`verify/piecewise_primitive.py` differentiates the formula on each piece, with the floor held constant, and checks that the one-sided values agree at every join. The ordinary derivative check still applies to the smooth piece \(2\sqrt{2}\sin(x/2)\) and still rejects a raw floor term.
