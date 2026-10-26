# R2-2025-UK-Across-Across-3

## Source and answer contract

- Clues, visually read: `sources/past/r2/2025/uk/2025_Crossnumber_Across_Round_2.pdf`, p.2.
- Completed grid, visually read: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf`, p.2.
- Crossing clues: `sources/past/r2/2025/uk/2025_Crossnumber_Down_Round_2.pdf`, pp.2-3.
- Certificates and the transcribed 11-by-12 lattice: `verify/pack_grid_2025.py`.

The answer is a map, not the value of one integral:

```text
{3:2026, 5:4915, 7:351, 9:357, 11:189, 12:18181,
 15:1681, 17:248, 21:609, 22:639, 23:751, 24:55}
```

All entries agree with the printed grid. The shared grid contract requires
the exact clue keys, positive integer values of the printed widths, the
printed lattice, and consistency with every crossing Down entry. Each
selected clue has its own lazy certificate and its own unchanged proof
timeout. The mathematical conditions below are checked in addition to the
mark-grid comparison. Several digit clues intentionally admit multiple
numbers in isolation; their remaining digits are supplied by the crossings.

The SG clue sheet is identical. The SG catalog selects A3 alone; that does
not turn the entire clue sheet into a single scalar integral.

## Clue-by-clue derivation

### A3: 2026

The two brackets in the original are **ceilings**. Put
\(A=\int_2^5 f\), \(B=\int_2^6 f\), and \(p=B-A=\int_5^6 f\).
Nonnegativity gives \(0\le A<B\), while \(p\) is a positive perfect number
and \(A^2+B^2=1076\). Thus \(p^2\le1076\), so \(p\le32\).
Enumerating proper divisors in this finite range gives precisely \(p=6,28\).

Solving the quadratic gives
\[
A=\frac{\sqrt{2152-p^2}-p}{2},\qquad B=A+p.
\]
For \(p=6\), \((A,B)=(20,26)\). For \(p=28\),
\((A,B)=(\sqrt{342}-14,\sqrt{342}+14)\), whose ceilings are \((5,33)\).
The latter cannot provide the two-digit prefix of a four-digit entry.
The unique entry is therefore 2026. Existence is immediate from the
nonnegative piecewise constant function \(f=20/3\) on \([2,5]\) and
\(f=6\) on \((5,6]\). The certificate checks the finite perfect-number
enumeration and both quadratic/ceiling cases exactly.

### A5: 4915

For \(q=e^a>0\), the rational factor splits as
\[
\frac{1+2qx+q^2}{x+q+q^2x+qx^2}
=\frac1{x+q}+\frac q{1+qx}.
\]
The antiderivative
\(\log x\log(1+x/q)+\operatorname{Li}_2(-x/q)\)
proves the first term's integral formula by differentiation; the second is
the same formula with \(q\) replaced by \(1/q\). Hence the clue integral is
\[
J(a)=\operatorname{Li}_2(-e^{-a})+\operatorname{Li}_2(-e^a)
=-\frac{a^2}{2}-\frac{\pi^2}{6}.
\]
For completeness, \(J'(a)=-a\) follows from
\((1+e^a)/(1+e^{-a})=e^a\), and
\(J(0)=2\operatorname{Li}_2(-1)=-\pi^2/6\). All logarithms here are real.
At \(a=4,b=9\), the printed right side is
\((-48-\pi^2)/6=-8-\pi^2/6\), exactly the integral. The suffix is 15,
which divides D2=945 (and D18=405). The certificate checks the rational
identity, the reflection identity, the base value, and the digit equation.

### A7: 351

For an integer \(k\ge1\),
\[
\int_k^{k+1}\frac{\sin(\pi x)}{\lfloor x\rfloor^2}\,dx
=\frac{2(-1)^k}{\pi k^2}.
\]
The sum converges absolutely, so splitting into unit intervals is valid.
Separating even and odd terms gives
\[
\int_1^\infty\frac{\sin(\pi x)}{\lfloor x\rfloor^2}\,dx
=\frac2\pi\left(\frac2{2^2}-1\right)\zeta(2)
=-\frac\pi6.
\]
Now \(351\equiv1\pmod{10}\),
\(\lceil351/10\rceil=36\), and \(\lfloor\sqrt{11}\rfloor=3\).
Both sides of the clue are \(6\pi\). The ceiling in the first factor must
not be replaced with a floor.

### A9: 357

D4=6338 has mean digit \((6+3+3+8)/4=5\), the middle digit of 357.
The outer digits are supplied by the crossings.

### A11: 189

Let the first integral be \(I\). The base \(2+5x^2\) is positive and even,
and \((2+5(-x)^2)^{-x}\) is the reciprocal of \((2+5x^2)^x\).
Pairing \(x\) and \(-x\), using
\(1/(1+w)+1/(1+w^{-1})=1\), gives
\(I=\int_0^\pi\sin x\,dx=2\).

For the second integral, expand the real logarithm to obtain
\[
J=\frac12\int_0^\pi
\bigl[\cos x\log(1-\cos x)-\sin x\log(1-\sin x)\bigr]\,dx.
\]
Integration by parts gives
\[
\int_0^\pi\cos x\log(1-\cos x)\,dx
=-\int_0^\pi(1+\cos x)\,dx=-\pi,
\]
\[
\int_0^\pi\sin x\log(1-\sin x)\,dx
=-\int_0^\pi(1+\sin x)\,dx=-\pi-2.
\]
The second integration is split at \(\pi/2\). Its inner boundary terms,
and the endpoint terms in the first integration, vanish by
\(t\log t\to0\). The logarithmic singularities are integrable.
Thus \(J=1\) and the clue is \(67\cdot2+55\cdot1=189\).
The certificate checks the rational reflection, both trigonometric
identities used in parts, the elementary integrals, and the boundary limit.

### A12: 18181

The digit string reads the same forwards and backwards. Crossings fix the
five digits.

### A15: 1681

\(1681=41^2\), and the first and last digits are both 1.

### A17, A21, A23: 248, 609, 751

The combined digit string `248609751` contains nine distinct digits,
omitting only 3, which is the first digit of A9.

- A17: \(2,4,8\) are powers of 2.
- A21: \(6,0,9\) are all divisible by 3; \(0+9\) is divisible by 9;
  the last digit is positive.
- A23: the happy digits are 7 and 1. For 7 the iteration of digit-square
  sums is \(7,49,97,130,10,1\). The middle digit 5 is unhappy: its orbit
  reaches the cycle \(89,145,42,20,4,16,37,58,89\). It is prime and does not
  divide 609. Finally \(\gcd(891,\lfloor18181/10\rfloor)
  =\gcd(891,1818)=9>3\). The last digit of A23 is the crossing last digit
  of D19. The certificate computes these finite digit orbits and gcd exactly.

### A22: 639

\((351+639)/2=495\), the value of D20.

### A24: 55

The exponents in the original are \(t^x\) and \(y^x\), and the prefactor
is \(yt^{x-2}\). For fixed \(x\ge e\), put \(Y=y^x\) and
\(v=y^x-t^x\). Then
\[
\int_0^y yt^{x-2}e^{t^x-y^x}\,dt
=\frac1x\int_0^Y(1-v/Y)^{-1/x}e^{-v}\,dv.
\]
This converges to \(1/x\), with an elementary domination argument that
also justifies the outer integral. On \(0\le v\le Y/2\), the factor
\((1-v/Y)^{-1/x}\le\sqrt2\), because \(x\ge e>2\), and it tends to 1.
On the remaining interval its integral is bounded by
\[
e^{-Y/2}\int_0^Y(1-v/Y)^{-1/x}\,dv
=\frac{Y e^{-Y/2}}{1-1/x}\le2Y e^{-Y/2}\longrightarrow0.
\]
For \(x\in[e,z]\) and \(y\) sufficiently large, this bound is uniform:
\(Y\ge y^e\), and \(Y e^{-Y/2}\) is decreasing for \(Y>2\).
The main part is dominated by \(\sqrt2 e^{-v}\); dominated convergence
on the finite outer interval therefore yields
\[
f(z)=\int_e^z\frac{dx}{x}=\log z-1.
\]
At \(z=e^{56}\), the result is 55. The certificate checks the substitution
factor, a primitive for the tail weight, its vanishing bound, and the
unit exponential mass. It never evaluates the original double integral
as one unbounded symbolic request.

## Verification

All 12 selected Across thunks pass, with each substantially below 20 seconds
on the authoring run. All 26 printed spans were independently checked against
the lattice. The shared contract supplies malformed-map, changed-digit,
empty-map, scalar-answer, and crossing controls. No proof timeout is raised.
