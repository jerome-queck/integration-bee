# YANG-1.12-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.12 Absolute Values, practice item 10, printed p. 21 (PDF p. 22).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int_{-2}^{2} \frac{1}{\sqrt{|1-x^{2}|}+1}\,dx.
\]

## Solution

The integrand is even, and \(x=-t\) reverses \([-2,0]\) onto \([0,2]\), so the integral is twice the integral on \([0,2]\). That half splits where \(|1-x^{2}|\) changes formula.

On \([0,1]\) both \(1-x\) and \(1+x\) are nonnegative, and their product is \(1-x^{2}\), so \(|1-x^{2}|=1-x^{2}\). The substitution \(x=\sin\theta\) runs from \(0\) to \(\pi/2\). There \(\cos\theta=\sin(\pi/2-\theta)\) stays nonnegative, and \(\sqrt{1-\sin^{2}\theta}=\cos\theta\). The integrand becomes

\[
\frac{\cos\theta}{1+\cos\theta}=1-\frac12\sec^{2}\frac\theta2.
\]

The antiderivative \(\theta-\tan(\theta/2)\) evaluates to \(\pi/2-1\).

On \([1,2]\) both \(x-1\) and \(x+1\) are nonnegative, so \(|1-x^{2}|=x^{2}-1\). The substitution \(x=\cosh u\) runs from \(0\) to \(\operatorname{acosh} 2\). For \(u\ge 0\), \(\sqrt{\cosh^{2}u-1}=\sinh u\), and the integrand becomes \(\sinh u/(1+\sinh u)\). With \(t=\tanh(u/2)\),

\[
u-\frac{\sqrt2}{2}\log(t+\sqrt2-1)+\frac{\sqrt2}{2}\log(\sqrt2+1-t)
\]

differentiates back to that reduced integrand. \(\cosh\log(2+\sqrt3)=2\) and the logarithm is positive, so the upper limit is \(\log(2+\sqrt3)\). The half-angle identities give \(\tanh\) of half that limit as \(1/\sqrt3\), and both logarithms stay defined. The definite value on \([1,2]\) is

\[
\log(2+\sqrt3)-\frac1{\sqrt2}\log(\sqrt2+\sqrt3).
\]

Doubling the sum of the two pieces gives the final value below.

## Final answer

\[
-2 - \sqrt{2} \log{\left(\sqrt{2} + \sqrt{3} \right)} + 2 \log{\left(\sqrt{3} + 2 \right)} + \pi.
\]

## SymPy self-check

`verify/pack_gate.py` proves `1/(sqrt(Abs(x**2 - 1)) + 1)` against `-2 - sqrt(2)*log(sqrt(2) + sqrt(3)) + 2*log(sqrt(3) + 2) + pi` (definite). The check is an exact closed evaluation. The reduction is `verify/yang_certificates.py`.
