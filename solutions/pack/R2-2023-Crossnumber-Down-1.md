# R2-2023-Crossnumber-Down-1

## Status: resolved by grading clarification

- verify: sympy; kind: grid
- conflict: Down 7's integral limit does not determine \(f(0)\) without an additional hypothesis such as continuity at zero.
- derived / problem reading: Under the published grading clarification that \(f\) is absolutely integrable on \([-1,1]\) and continuous at zero, the integral limit is \((\pi/5)f(0)\), uniquely giving \(250\). Without that clarification the point value is undetermined.
- printed mark: Down 7: \(250\); the complete marked Down map is retained below.
- erratum: none claimed; Jerome's t636u override and Handoff N explicitly authorize this published regularity clarification.
- registry: docs/decisions/0016-pack-source-holds.md

## Sources and certified map

The numbered lattice and Down clues were read visually from
[the Crossnumber problem, p.3](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf).
The completed grid is in
[the Mark Scheme, p.3](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf).
Its unchanged Down map is

`{1:115, 2:14183, 4:376, 6:4320, 7:250, 10:69134, 11:27, 13:721, 14:394, 15:856}`.

## Grading clarification

Handoff N explicitly authorizes a regularity clarification for grading
Down 7. The certificate adopts:

> For grading Down 7, f is absolutely integrable on [-1,1] and continuous at 0.

Continuity is needed only at the requested point, not everywhere on the
interval. Absolute integrability is sufficient for the tail estimate below;
ordinary Riemann integrability on the compact interval also suffices.
These are stated hypotheses of the certified reading, not an organizer
erratum or a claim that the original PDF already contains them. The literal
clue transcript is retained separately from the explicit clarification in
the grid manifest and learner-facing prompt.

Under this reading, Down 7 has the unique value 250. All ten Down checks
and the unchanged lattice are certified by the grid gate, so this row is
`kind: grid`, `verify: sympy`. Its answer is the entire map above.

## Down 7: what the printed hypothesis alone establishes

The literal statement on problem p.3 asks for `f(0)` when

\[
\lim_{n\to0^+}\int_{-1}^{1}\frac{n f(x)}{25n^2+x^2}\,dx=50\pi.
\]

It gives no continuity assumption at zero. The problem's cover and two
clue pages supply no general regularity assumption. Thus the marked answer
is not uniquely implied by the unclarified problem.

For any real number `c`, set `f(x)=250` for `x!=0` and `f(0)=c`.
This is Riemann-integrable on `[-1,1]`. Changing one point does not alter
any integral, and for `n>0`,

`integral_-1^1 n*f(x)/(25*n^2+x^2) dx`
`=100*atan(1/(5*n)) -> 50*pi`.

Thus every `c` satisfies the printed integral limit. In particular,
the source hypotheses hold with `f(0)=0` as well as with the completed
grid's 250. This counterexample remains valid for the printed statement;
it is excluded by the explicitly adopted continuity hypothesis unless
`c=250`. No mark-grid digit has been inferred from a point-value theorem
without its required hypothesis.

## Down 7: proof under the clarification

Write `c=f(0)` and `K_n(x)=n/(25*n^2+x^2)` for `n>0`. The primitive
`atan(x/(5*n))/5` is checked by symbolic differentiation. Consequently,

\[
\int_{-1}^{1} K_n(x)\,dx
=\frac25\arctan\!\left(\frac1{5n}\right)\longrightarrow\frac\pi5,
\qquad
\int_{-\infty}^{\infty}K_n(x)\,dx=\frac\pi5.
\]

It remains to justify replacing `f(x)` by `c` in the limit. For any
`epsilon>0`, continuity at zero supplies `0<delta<=1` with
`|f(x)-c|<epsilon` when `|x|<delta`. The positive kernel therefore gives

\[
\int_{|x|<\delta} K_n(x)|f(x)-c|\,dx
\leq\epsilon\frac\pi5.
\]

On the remaining part of `[-1,1]`, `K_n(x)<=n/delta^2`. This follows
from the exact nonnegative difference, with `x^2=delta^2+u`, `u>=0`:

\[
\frac n{\delta^2}-\frac n{25n^2+\delta^2+u}
=\frac{n(25n^2+u)}{\delta^2(25n^2+\delta^2+u)}\geq0.
\]

Absolute integrability gives a finite bound
`M >= integral_-1^1 |f(x)-c| dx`. Hence

\[
\left|\int_{-1}^{1}K_n(x)(f(x)-c)\,dx\right|
\leq\epsilon\frac\pi5+\frac{nM}{\delta^2}.
\]

First let `n->0+` with the chosen `delta` fixed, then let `epsilon->0+`.
The remainder tends to zero, establishing the approximate-identity limit

\[
\lim_{n\to0^+}\int_{-1}^{1}K_n(x)f(x)\,dx
=\frac\pi5 f(0)=50\pi,
\qquad f(0)=250.
\]

`verify/pack_grid_2023.py::_cauchy_point_value` checks the primitive,
kernel positivity, exact full mass and compact-interval mass limit,
nonnegative tail-bound difference, iterated remainder-bound limit, and
the final scalar equation. It is not an equality check against an
unexplained stored 250. Wrong point values fail this certificate even
before the independent lattice check.

## Other Down derivations

1. Put `u=integral_0^1 f`, `v=integral_1^2 f`. The equations are
   `-4u+3v=23`, `3u-2v=0`, so `u=46,v=69` and the requested sum is 115.

2. Across 1 gives `c=10`. Substitute `x=exp(-t)`:
   `integral_0^1 x(log x)^10 dx=10!/2^11=14175/8`.
   The numerator and denominator are coprime, giving `14175+8=14183`.

4. Let `I=integral_-1^1 f`. Integration of
   `f(x)+I=3x^2+x+8` gives `3I=18`, hence `I=6` and
   `f(11)=3*121+11+8-6=376`.

6. The three smallest marked entries are 10,16,27. Their product is 4320.

10. The identity
    `d/dx[f'(x)sin(x)-f(x)cos(x)]=(f''(x)+f(x))sin(x)`
    gives `f(pi)+f(0)=70000`. Since `f(pi)=866`, `f(0)=69134`.
    The symbolic derivative is checked directly, with the endpoint sine
    factors zero and the endpoint cosine factors `-1,1`.

11. The nested integral uses every letter from `a` through `z`, hence
    26 integrations of the initial function `z`. Repeated integration of
    `t^m/m!` from 0 to the next upper variable gives
    `t^(m+1)/(m+1)!`. The outer upper endpoint is 1, so the result is
    `1/27!` and `A=27`. The checker executes this finite recurrence.

13. `721=6!+1`.

14. The digits of 394 have product 108 and sum 16.

15. The digits of 856 alternate even, odd, even.

The entries in Down 13,14,15 concatenate to `721394856`, which contains
every digit 1 through 9 exactly once. The shared grid contract checks all
crossings; each Down clue also has its own independent certificate.

## Handoff J source recheck (2026-10-27)

The complete problem PDF (pp.1-3) and complete mark PDF (pp.1-4) were
rendered and reread visually. Down 7 on problem p.3 explicitly has
`n -> 0+`; it still gives no continuity condition. The cover and Across
page add none. Mark p.3 gives the completed lattice and digit-by-digit
marking instructions, without supplementing the function hypothesis.

The [current official resource pack](https://integration.soc.srcf.net/Resource%20pack.zip)
was downloaded for this recheck. Its 2023 Crossnumber and Mark Scheme
PDFs are byte-for-byte identical to the committed copies. Its Round 2/2023
directory contains only the problem, blank grid, group round, mark scheme,
and relay PDFs; it supplies no separate 2023 participant or marker guide.
The [official 2023/24 syllabus](https://integration.soc.srcf.net/UK_University_Integration_Bee_Syllabus.pdf),
pp.1-2, also supplies no general continuity assumption. Its statement
setting aside convergence questions concerns interchanging infinite
series and integrals, not recovering a function's value at an isolated
point. The [official contest page](https://integration.soc.srcf.net/)
and [past-competitions page](https://integration.soc.srcf.net/pastcomp.html),
and targeted searches for a crossnumber correction, provided no applicable
erratum. This records the scope of the search, not a claim that no
unpublished clarification exists.

The counterexample above was rechecked symbolically: for positive `n`,
the integral is exactly `100*atan(1/(5*n))`, and its right-hand limit at
zero is `50*pi`. Any finite change to `f(0)` preserves each integral.
Thus neither ordinary Riemann integrability alone nor the syllabus's
convergence convention supplies the missing point-value information.
Handoff J retained manual status on that basis. Handoff N resolves the
hold through the explicit grading clarification and conditional proof
above; the historical source search is not treated as an organizer erratum.
