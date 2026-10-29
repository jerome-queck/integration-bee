# YANG-1.12-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 05, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-2\pi}^{2\pi} |\sin x|\,dx.
\]

## Solution

The minimum of \(\sin\) on \([0,\pi]\) is \(0\), so \(|\sin t|=\sin t\) there. On each interval \([k\pi,(k+1)\pi]\) for \(k=-2,-1,0,1\),

\[
\sin(k\pi+t)=(-1)^{k}\sin t,
\]

and \(|\sin(k\pi+t)|=\sin t\). The signed antiderivative of \((-1)^{k}\sin x\) therefore increases by \(2\) on every piece. Four pieces give \(8\).

The direct integrator returns \(4\). Its antiderivative is \(\cos x\) for \(x\le 0\), then \(2-\cos x\) for \(x\le\pi\), then \(\cos x+4\). Differentiating that formula gives \(-\sin x\) for every \(x\le 0\). On \([-2\pi,-\pi]\), \(\sin x\) is nonnegative, so \(|\sin x|=\sin x\) and the formula has the wrong sign. At \(x=-3\pi/2\) the formula's derivative minus \(|\sin x|\) equals \(-2\). Integrating the formula on \([-2\pi,-\pi]\) returns \(-2\), and that missing \(4\) is why the full interval comes out as \(4\) instead of \(8\).

The guide does not print a final for practice item 5. The printed \(4\) on the same page is the warning example \(\int_{0}^{2\pi}\sqrt{1-\sin^{2}x}\,dx=\int_{0}^{2\pi}|\cos x|\,dx\), which is a different integral.

## Final answer

\[
8.
\]

## SymPy self-check

`verify/pack_gate.py` proves `Abs(sin(x))` against `8` (definite). The check is an exact closed evaluation. A reduction, when one is used, is `verify/yang_certificates.py`.
