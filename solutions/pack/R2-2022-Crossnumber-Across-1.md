# R2-2022-Crossnumber-Across-1

## Source and answer contract

The source is `sources/past/r2/2022/Crossnumber_R2_2022_UK_University_Integration_Bee.pdf`, Across clues on PDF p.2 and Down clues on p.3. The completed grid was read visually from `sources/past/r2/2022/Mark_Scheme_R2_2022_UK_University_Integration_Bee_(2).pdf`, PDF p.3. This is the paper labelled **2022/23**, held in February 2023; the repository's `2022` id is retained.

The answer is the complete clue-to-integer map, not one concatenated integer:

| Across clue | Printed entry |
|---|---:|
| 1 | 1729 |
| 3 | 17062 |
| 5 | 13 |
| 6 | 25 |
| 7 | 106 |
| 9 | 6996 |
| 10 | 13824 |
| 12 | 639600 |
| 14 | 505 |
| 15 | 449 |

`verify/pack_grid_2022.py` retains the full 11-by-14 completed lattice and explicit printed clue starts. The numbers are **not** in row-major order: Down 2 starts above Across/Down 1. Crossings are checked using these explicit starts, against the sibling Down map. Every Across clue has its own exact certificate; the helper does not promote a grid merely because it equals the mark grid.

Write (A_j,D_j) for Across and Down entries. The sibling entries are

\[
D_1=13579,\quad D_2=191,\quad D_4=6561,\quad D_8=38,
\quad D_9=64,\quad D_{11}=343,\quad D_{12}=625,\quad D_{13}=954.
\]

## Clue-by-clue derivation

### A1: equal sums of cubes

The clue requires (x^3+y^3=z^3+w^3), with integer (x<z<w<y), (x) the final digit of (D_4), and (w) the product of the last two digits of (D_{12}). Thus (x=1), (w=2\cdot5=10). The printed entry satisfies

\[
1729=1^3+12^3=9^3+10^3,\qquad1<9<10<12.
\]

The certificate computes the exact integer cube roots of (A_1-x^3) and (A_1-w^3), then checks the strict ordering. It does not assume that the decimal entry alone certifies the equation.

### A3 and A5: crossing arithmetic

(A_3=A_{15}D_8=449\cdot38=17062). Excluding A5 itself, the other two smallest grid entries are 25 and 38. Their difference is 13, giving A5. The check actually sorts the full Across/Down entry collection with A5 removed.

### A6: an iterated quadratic

The source defines (f(x)=2x(1-x)), (f_n=f\circ\cdots\circ f), and asks for the numerator plus denominator of

\[
\int_0^1 f_{\sqrt[3]{D_9}}(x)\,dx=\frac ab
\]

The source does not explicitly impose lowest terms. We use the canonical
reduced fraction as a witness for its equation, and check the resulting
entry against the completed grid. Here (n=\sqrt[3]{64}=4). The identity

\[
1-2f(x)=(1-2x)^2
\]

iterates to (f_n(x)=[1-(1-2x)^{2^n}]/2). Therefore

\[
\int_0^1f_4(x)\,dx
=\frac12\left(1-\frac1{17}\right)=\frac8{17},
\qquad a+b=25.
\]

The machine path independently composes and expands the degree-16 polynomial, integrates it exactly with SymPy, and extracts the reduced numerator and denominator.

### A7: two equations between integrals

Let (U=\int_0^1f) and (T=\int_0^2f), so (\int_1^2f=T-U). The printed equations are

\[
5U-2T=23,\qquad 3T-4(T-U)=82.
\]

Solving gives (U=47,T=106). Thus A7 is 106. The certificate solves these exact equations rather than introducing a particular function (f).

### A9: palindrome

The entry 6996 reads the same in both directions. This is the full printed clue; its remaining digits are constrained by the shared lattice.

### A10: trigonometric integral, then factorial, then cube

The source has both a factorial and an outer cube:

\[
\left[\left(\frac1\pi\int_0^{2\pi}
\frac{\sin^2(5x)\sin^2(4x)}{\sin^2x}\,dx\right)!\right]^3.
\]

The removable singularities at multiples of (\pi) do not change the integral. For (z=e^{ix}),

\[
\frac{\sin4x}{\sin x}=z^3+z+z^{-1}+z^{-3},\qquad
\sin5x=\frac{z^5-z^{-5}}{2i}.
\]

The integrand is a finite Laurent polynomial in (z). Its constant coefficient is 2; all its other Fourier modes integrate to zero over a full period. Thus the integral is (4\pi), and the answer is

\[
(4!)^3=24^3=13824.
\]

SymPy verifies the finite quotient identity and expands the Laurent polynomial to extract its constant coefficient. No infinite Fourier exchange or numerical quadrature is used.

### A12: the floor-ceiling integral

The upper limit is (10\sqrt[3]{D_9}=40). On each open unit interval (k<t<k+1), the integrand is (k(k+1)t). Endpoint values have measure zero. Hence

\[
\int_0^{40}\lceil t\rceil t\lfloor t\rfloor\,dt
=\sum_{k=0}^{39}\frac{k(k+1)(2k+1)}2
=639600.
\]

The code evaluates this finite sum exactly with SymPy.

### A14 and A15

For A15 put (C=\int_1^2 f(x)\,dx). The equation is (f(x)+C=\lfloor x\rfloor^2+17). Integrating over ([1,2]), where the floor equals 1 almost everywhere, gives (2C=18), hence (C=9). Thus

\[
f(21)=21^2+17-9=449.
\]

Finally (A_{14}=D_{13}-A_{15}=954-449=505).

## Verification

Every selected Across thunk returns Python `True`, with exact SymPy arithmetic for the integral clues. The completed lattice, explicit label starts, and sibling digits are checked separately by the grid contract. Mutating a clue value, removing a key, returning an empty map, or replacing the map by a concatenated scalar must fail the answer contract even when the mutated number still happens to satisfy an underdetermined clue such as "palindrome". The proof timeout remains unchanged.
