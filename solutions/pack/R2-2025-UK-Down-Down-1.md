# R2-2025-UK-Down-Down-1

## Source and answer contract

- Clues, visually read: `sources/past/r2/2025/uk/2025_Crossnumber_Down_Round_2.pdf`, pp.2-3.
- Completed grid, visually read: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, p.2.
- Crossing clues: `sources/past/r2/2025/uk/2025_Crossnumber_Across_Round_2.pdf`, p.2.
- Certificates and transcribed lattice: `verify/pack_grid_2025.py`.

The structured answer is

```text
{1:422, 2:945, 3:2551, 4:6338, 6:13, 8:11, 10:78,
 13:191, 14:8106, 16:67, 17:267, 18:405, 19:891, 20:495}
```

Every entry is visually checked against the completed grid. The contract
compares this map, checks all printed widths and Across crossings, and runs
one independent exact certificate per selected clue. A printed digit clue
need not determine a number without its crossings. The checks below validate
its full printed condition, rather than claiming an isolated scalar answer.

## Clue-by-clue derivation

### D1: 422

The clue asks for **a divisor of five times the integral**. It does not claim
that the integral is 422. For \(x\ge15\), all roots below have their positive
real values, and
\[
\sqrt{2x-2\sqrt{x^2-1}}=\sqrt{x+1}-\sqrt{x-1}.
\]
After adding the next \(\sqrt{x-1}\), the outer square root is
\((x+1)^{1/4}\). Therefore
\[
5\int_{15}^{80}(x+1)^{1/4}\,dx
=4\,[\,(x+1)^{5/4}\,]_{15}^{80}
=4(243-32)=844.
\]
Since \(844=2\cdot422\), the printed entry satisfies the clue. Its
three-digit divisors are 211, 422, and 844; the crossing last digit 2 from
A3 selects 422. The certificate checks the radical identity, derivative,
endpoint powers, and exact divisibility.

### D2: 945

An integral equals its average for every integrable function on a nonempty
interval exactly when that interval has length 1. Necessity follows by
testing a function equal to 1 on that interval and 0 outside it, which is
integrable even if the clue requires integrability on all of the real line;
sufficiency follows from the definition
of average. The interval in the clue therefore requires
\[
x^2-2ax+2026=1,
\qquad (x-a)^2+2025-a^2=0.
\]
It has exactly one real solution if and only if \(a^2=2025\), hence
\(a=\pm45\). The possible positive three-digit values \(ka\) are the
three-digit multiples of 45. The largest is 990; the second largest is
945. The certificate checks the discriminant and enumerates that finite set.

### D3: 2551

Split the digits as \(25,5,1\). These are consecutive terms of a geometric
sequence with ratio \(1/5\). The certificate enumerates possible digit
splittings and checks the exact relation \(b^2=ac\), with the necessary
nonnegative/zero restrictions.

### D4: 6338

The entry supplies \(a/b=6/3=2\), \(c/d=3/8\), and one may take \(k=2\).
To evaluate the integral, substitute
\[
x=\frac{2q}{1+q^2},\qquad 0<q<1.
\]
Then \(\sqrt{1-x^2}=(1-q^2)/(1+q^2)\), so the positive real inverse
hyperbolic tangent is \(-\log q\). Also
\[
1-x=\frac{(1-q)^2}{1+q^2},\qquad
\frac{dx}{1-x}=-d\log\frac{(1-q)^2}{1+q^2}.
\]
Integration by parts gives
\[
I=-\int_0^1\frac{2\log(1-q)-\log(1+q^2)}q\,dq
=2\zeta(2)+\frac12\eta(2)=\frac{3\pi^2}{8}.
\]
Here \(\eta(2)=\zeta(2)/2\). The log series can be integrated termwise:
the sum of the absolute term integrals is finite. The integration-by-parts
boundary product \(\log q\log((1-q)^2/(1+q^2))\) vanishes at both ends,
using \(q\log q\to0\) and \((1-q)\log(1-q)\to0\).
The certificate checks the rational substitution, branch-defining ratio,
parts identity, and zeta evaluation.

### D6: 13

13 is prime and divides D10=78. Reversing its digits gives the prime 31.

### D8: 11

11 is prime. Its digit-square iteration is
\(11,2,4,16,37,58,89,145,42,20,4\), so it is unhappy.

### D10: 78

NASA gives Kepler's birth as 27 December 1571 and death as 15 November 1630,
and explicitly gives his age at death as 58:
[NASA, Orbits and Kepler's Laws](https://science.nasa.gov/solar-system/orbits-and-keplers-laws/).
The exact comparison is \(78>58\). The history is a sourced input to this
digit condition, not something inferred by symbolic integration.

### D13: 191

Put \(B=\int_2^5 f\), \(C=\int_5^6 f\). The printed system is
\[
2B+8C=26,\qquad 5B+2C=25,
\]
so \(B=37/9\), \(C=20/9\), and one period has integral
\(B+C=19/3\). The interval \([-6,6]\) is three periods of length 4,
giving integral 19. This equals \(\lfloor191/10\rfloor\).
The final digit is fixed by its crossing; the floor is part of the clue.

### D14: 8106

Let \(r_n\) be the nested radical with exactly \(n\) square roots, and set
\(\theta=\arccos(\cos x)\in[0,\pi]\). Induction with the positive half-angle
formula gives
\[
r_n(x)=2\cos\left(\frac\theta{2^n}\right).
\]
This is \(2\pi\)-periodic. A period integral is
\(4\cdot2^n\sin(\pi/2^n)\); there are \(2^{n-1}\) periods in the printed
interval \([0,2^n\pi]\). Consequently
\[
\frac1\pi\int_0^{2^n\pi}r_n(x)\,dx
=\frac{2^{2n+1}}\pi\sin\left(\frac\pi{2^n}\right).
\]
For \(n\ge2\), use \(t-t^3/6<\sin t<t\) for \(0<t\le\pi/4\).
The upper inequality follows by integrating \(1-\cos t>0\) once.
For the lower one, the third derivative of
\(\sin t-t+t^3/6\) is \(1-\cos t>0\), and its first three initial
values vanish, so three integrations give strict positivity. They imply
\[
0<2^{n+1}-\frac{2^{2n+1}}\pi\sin\left(\frac\pi{2^n}\right)
<\frac{\pi^2}{3\cdot2^n}\le\frac{\pi^2}{12}<1.
\]
Thus the **ceiling** in the clue is exactly \(2^{n+1}\).
Its hexadecimal digit count is \(\lfloor(n+1)/4\rfloor+1\).
A3+1=2027 digits requires \(8104\le n+1<8108\); the largest possible
\(n\) is 8106. The exceptional \(n=1\) cannot affect this maximum.
The certificate checks the half-angle identity, period primitive, remainder
bound, and integer digit-count comparison, without expanding a giant integer.

### D16: 67

The smallest prime divisor of A3=2026 is \(k=2\). Under \(x=1/t\),
the printed integral becomes
\[
-\int_0^1\frac{(1+2t)\log t}{1+t+t^2}\,dt
=\int_0^1\frac{\log(1+t+t^2)}t\,dt.
\]
The equality is integration by parts; its boundary term vanishes at both
ends. Factoring \(1+t+t^2=(1-t^3)/(1-t)\) gives
\[
I=-\frac{\zeta(2)}3+\zeta(2)=\frac{\pi^2}{9}.
\]
For the entry 67 the other side is
\(\sqrt[3]{\pi^6}/(7+2)=\pi^2/9\), on the positive real branch.
The certificate checks the reciprocal Jacobian, logarithmic derivative,
factorization, and exact value.

### D17, D18, D19: 267, 405, 891

The combined string `267405891` has nine distinct digits from 0 through 9.

- D17: \(2\cdot6>7\), \(2\cdot7>6\), and \(6\cdot7>2\).
- D18: \(405=20^2+5\).
- D19: \(8\cdot9=72\), and \(7-2=5\), the last digit of D18.

### D20: 495

The polynomial is the fifteenth cyclotomic polynomial, with the directly
checked factorization
\[
x^8-x^7+x^5-x^4+x^3-x+1
=\frac{(1-x)(1-x^{15})}{(1-x^3)(1-x^5)}.
\]
Every displayed factor is positive on \((0,1)\), so the real logarithms
split without a branch ambiguity. The identity
\[
\int_0^1\frac{\log(1-x^m)}x\,dx=-\frac{\zeta(2)}m
\]
follows by \(u=x^m\) and the absolutely summable logarithm-series term
integrals. Therefore the original integral is
\[
\left(-1-\frac1{15}+\frac13+\frac15\right)\zeta(2)
=-\frac{4\pi^2}{45}.
\]
The printed absolute value is \(4\pi^2/45\), equal to
\(a\pi^2/(bc)\) for \(a=4,b=9,c=5\). The denominator is the product
of the digits, not their concatenation.

## Verification

All 14 selected Down certificates pass, with each substantially below the
unchanged 20-second timeout on the authoring run. The full shared lattice
matches every Across and Down span. The grid contract adds wrong-map and
crossing rejection to these clue-condition proofs.
