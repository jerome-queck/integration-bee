# R2-2022-Crossnumber-Down-1

## Source and map

The complete Down clues were read visually from `sources/past/r2/2022/Crossnumber_R2_2022_UK_University_Integration_Bee.pdf`, PDF p.3, together with the Across clues on p.2. The entries were transcribed from the completed grid in `sources/past/r2/2022/Mark_Scheme_R2_2022_UK_University_Integration_Bee_(2).pdf`, PDF p.3.

| Down clue | Printed entry |
|---|---:|
| 1 | 13579 |
| 2 | 191 |
| 4 | 6561 |
| 8 | 38 |
| 9 | 64 |
| 11 | 343 |
| 12 | 625 |
| 13 | 954 |

The answer contract is a complete clue-to-integer map. `verify/pack_grid_2022.py` stores the shared completed lattice, explicit printed starts, source statements, and one exact certificate per clue. Clue 2 starts above clue 1; inferred row-major numbering would be wrong. The sibling Across map and every shared cell are checked by the common grid contract. The Across derivations are in `solutions/pack/R2-2022-Crossnumber-Across-1.md`.

## Derivations

### D1, D4, D11, D12, D13: exact digit and integer constraints

The digits of (13579) form an arithmetic progression with common difference 2. The entry (6561=9^4) is a power of 9. The palindrome cube is (343=7^3), while (625=25^2) is a square. Finally

\[
954=9\cdot106=9A_7,\qquad9>5>4,
\]

so D13 is a multiple of A7 with strictly decreasing digits. The certificates check these properties using integers and exact integer roots. Their conjunction with the printed lattice, rather than a fabricated scalar integral, determines the accepted map.

### D2: a function defined by its integral

Write (C=\int_3^5f(t)\,dt). The source states

\[
f(x)-C=x+\frac{D_8}2=x+19.
\]

Therefore (f(x)=x+19+C). Integrating from 3 to 5 gives

\[
C=\int_3^5(x+19+C)\,dx=46+2C,
\]

so (C=-46), (f(x)=x-27), and (f(218)=191). SymPy computes the integral and solves the constant equation exactly.

### D8: the third iterate is the identity

Here (f(x)=1-1/x), (f_n) denotes the (n)-fold composition, and the answer is

\[
4\int_y^{y+1}f_{D_{13}}(x)\,dx,
\]

where (y) is the second digit of A9. The shared entries give (y=9), (D_{13}=954). Direct rational simplification gives

\[
f_2(x)=\frac1{1-x},\qquad f_3(x)=x.
\]

For (x\in[9,10]), the orbit alternates between (x>1), (0<f(x)<1), and (f_2(x)<0); no intermediate denominator vanishes. Since (954\equiv0\pmod3),

\[
4\int_9^{10}f_{954}(x)\,dx
=4\int_9^{10}x\,dx=38.
\]

The certificate verifies the rational composition identity and performs the remaining elementary integral. It checks the domain condition (y>1), so cancellation cannot hide a pole on the integration interval.

### D9: a removable-endpoint logarithm

The source asks for (n^3), where

\[
\int_0^{\pi/4}\left(\frac1x-
\frac{\sin2x}{1-\cos2x}\right)dx
=\log\left(\frac{\pi\sqrt2}{n}\right).
\]

On this interval the second term is \(\cot x\). A primitive is

\[
F(x)=\log x-\log(\sin x).
\]

Since \(\sin x/x\to1\) from the right, \(F(x)\to0\) as \(x\downarrow0\). At the upper endpoint,

\[
F(\pi/4)=\log\left(\frac{\pi\sqrt2}{4}\right).
\]

Thus (n=4) and D9 is (4^3=64). The code checks the primitive derivative against the original double-angle expression, computes the one-sided endpoint limit, and compares the exact logarithms.

## Verification

All eight Down certificates return exact Python `True`. Together with the ten Across certificates, this checks all 18 printed clues. Each integral certificate is individually bounded by the unchanged proof timeout. The common contract must reject a digit mutation, missing or surplus keys, an empty map, or a bare scalar, and must reject disagreement with the sibling map at any crossing.
