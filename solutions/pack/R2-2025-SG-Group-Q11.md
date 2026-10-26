# R2-2025-SG-Group-Q11

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (PDF page 2, group 11)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- Verification: `sympy`. The original PDF prints an outer floor, with bottom horizontal bracket strokes visible on page 2. The earlier derived catalog final omitted this floor; its corrected final is 20. No Singapore mark scheme is in this tree; the UK mark scheme is not an answer source for this distinct problem.

## Problem

\[
\left\lfloor\int_{0}^{1}\Biggl(\pi(e^{\pi x}-1)+(1+x)\sum_{k=0}^{998}(-x)^{k}\Biggr)\,dx\right\rfloor.
\]

## Solution

The finite geometric sum is
\[
(1+x)\sum_{k=0}^{998}(-x)^{k}=1-(-x)^{999}=1+x^{999}
\]
for \(x\neq -1\), hence on \([0,1]\). The integral before taking the floor splits into
\[
\int_{0}^{1}\pi(e^{\pi x}-1)\,dx+\int_{0}^{1}(1+x^{999})\,dx=(e^{\pi}-1-\pi)+\Bigl(1+\frac{1}{1000}\Bigr)=e^{\pi}-\pi+\frac{1}{1000}.
\]
The integral itself is therefore \(I=e^{\pi}-\pi+1/1000\). The requested answer is \(\lfloor I\rfloor\).

Here is a rational enclosure, rather than a floating-point decision near the integer \(20\). Put
\[
S_m(z)=\sum_{k=0}^{m-1}\frac{(-1)^kz^{2k+1}}{2k+1},\qquad
p=\frac{31415926535}{10^{10}},\quad q=\frac{31415926536}{10^{10}}.
\]
The alternating arctangent series and Machin's identity
\(\pi=16\arctan(1/5)-4\arctan(1/239)\) give
\[
p<16S_{12}(1/5)-4S_5(1/239)<\pi
<16S_{13}(1/5)-4S_4(1/239)<q.
\]
For \(T_{30}(z)=\sum_{k=0}^{30}z^k/k!\), positivity of the exponential series and a geometric bound on its tail imply
\[
T_{30}(p)-q+\frac1{1000}<I<
T_{30}(q)+\frac{q^{31}}{31!\,(1-q/32)}-p+\frac1{1000}.
\]
Exact rational arithmetic places this entire interval strictly between \(20\) and \(200001/10000=20.0001\). Thus \(\lfloor I\rfloor=20\).

## Final answer

\[
20.
\]

## SymPy self-check

SymPy evaluates the reduced integral as \(e^{\pi}-\pi+1/1000\); exact rational arithmetic verifies both displayed enclosures. The gate retains the outer floor as `Subs(floor(v), v, Integral(...))`, including the finite geometric sum and original bounds. This unevaluated form survives serialization without triggering a numerical floor evaluation. The exact rational enclosure above certifies the requested floor; the unrounded integral is not used as the final answer.
