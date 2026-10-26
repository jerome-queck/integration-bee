# R2-2024-Across-Across-1

## Sources and structured answer

The Across clue sheet is
`sources/past/r2/2024/Crossnumber_Across_2024_R2_UK_University_Integration_Bee.pdf`,
p.2. The numbered completed grid was read visually from
`sources/past/r2/2024/Mark_Scheme_R2_2024_UK_University_Integration_Bee.pdf`,
p.3. Both directional sheets use that single 10-by-11 lattice. The Across
map is

`{1:12, 2:84, 4:5832, 6:15, 7:89, 8:114, 11:390625, 12:58720, 15:563, 18:148, 19:729}`.

`verify/pack_grid_2024.py` contains exact checks for each clue, the full
source transcription, both maps, and printed clue-start coordinates.
The contract verifies those checks and the full crossing lattice; it
does not replace the puzzle with one scalar integral.

## Across derivations

1. Let `I=integral_-1^1 f`. Integration of
   `f(x)+I=24x^2-25x+52` yields `3I=120`, so `I=40` and `f(0)=12`.

2. Put `c=a^(1/b)`. For `a>1`, the even integral is
   `2[-1/log(x+c)]_0^infinity=2/log(c)=2b/log(a)`.
   The case `a=1` diverges at zero and cannot satisfy the clue.
   Since `log(3)+2log(2)=log(12)`, the displayed equation is equivalent to
   `a^7=12^b`. Exact enumeration of coprime integers `2<=a<20,1<=b<20`
   gives only `(a,b)=(12,7)`, so `ab=84`.
   The checker differentiates the primitive, checks its infinite endpoint,
   and performs the finite integer search.

4. `5832=18^3`.

6. Here the integral is a Borwein-type sinc integral. Let `U_k` be
   independent uniforms on `[-1/(2k-1),1/(2k-1)]`, and write
   `Y=U_2+...+U_n`, `S=U_1+Y`. Their characteristic function is precisely
   the printed product of sinc factors. For `n>=2`, Fourier inversion
   gives the printed integral as `pi*p_S(1)`. The density of `U_1` is
   `1/2` on `[-1,1]`, so
   `p_S(1)=(1/2)*P(0<=Y<=2)`.

   The density of `Y` is symmetric, supported on `[-B_n,B_n]`, and
   strictly positive in the interior of that interval, where
   `B_n=sum_{k=2}^n 1/(2k-1)`. Consequently `P(0<=Y<=2)=1/2` exactly
   when `B_n<=2`; if `B_n>2`, a strictly positive tail lies above 2 and
   the integral is strictly smaller than `pi/4`. For `n=1`, the direct
   Dirichlet integral `integral_0^infinity sin(2x)/(2x) dx=pi/4` applies.
   Thus the first unequal value is determined by an exact rational sum,
   with no delicate numerical oscillatory integration.

   The checker finds `B_56<2<B_57`; monotonicity of the positive partial
   sums establishes that 57 is the smallest index. Since
   `gcd(15,57)=3>1`, the printed entry 15 satisfies the clue.

7. `sqrt(7921)=89` from Down 13.

8. Write `h(t)=t^t`. The product substitution and Fubini give
   `integral_0^1 integral_0^1 h(xy) dx dy`
   `=integral_0^1 -log(t)h(t) dt`.
   Since `h'(t)=(1+log(t))h(t)` and `h(0+)=h(1)=1`, integration by
   parts gives this double integral equal to `integral_0^1 h(t)dt`.
   Both integrals are positive, so the reduced ratio is `a/b=1/1`.
   The requested answer is `89^1+25^1=114`. The derivative and endpoint
   limit are checked by SymPy.

11. Across 2 gives the first coefficient `floor(84/10)/20=2/5`.
    Let `r=a/b`. Applying the inequality to the two constant convex
    functions `f=1` and `f=-1` forces equal total masses:
    `r=2/5+(2/3)(3/5)=4/5`. Thus it remains to prove that this forced
    value works, not to search over possible endpoints. The first
    moments also agree:
    `(2/5)/2+(2/3)(3/5)^2/2=(4/5)^2/2=8/25`.

    A continuous convex function is a uniform limit of convex piecewise
    linear functions; each such function is affine plus a nonnegative
    linear combination of hinges `(x-t)_+`. Mass and moment equality
    cancel the affine part. For a hinge, the left-minus-right integral
    is zero outside `0<t<1`, and within that interval it is

    - `t^2/30` for `0<=t<=3/5`;
    - `(1-t)^2/5-(4/5-t)^2/2` for `3/5<=t<=4/5`;
    - `(1-t)^2/5` for `4/5<=t<=1`.

    The first and third expressions are nonnegative. The middle
    quadratic is concave and its endpoint values are `3/250` and
    `1/125`, so it too is nonnegative throughout. These identities and
    endpoint inequalities are exact SymPy checks. Therefore every
    continuous convex function satisfies the inequality for `4/5`.
    The answer is `(5^4)^2=390625`.

12. In 58720 the final two-digit number is 20 and `5+8+7=20`.

15. 563 is prime and differs by 6 from the prime 557 (also from 569).

18. 148 is even.

19. `729=27^2>20*25`.

The three entries 563,148,729 contain precisely one of every digit
1 through 9. All these integer and digit conditions are checked jointly
with the relevant clue predicates.

## Certificate scope

The analytic parts above justify the finite symbolic identities checked
by the code: Fourier inversion for a convolution of bounded uniforms,
the product substitution, and the convex hinge characterization. No
floating-point agreement or literal answer assertion substitutes for
those arguments. Each clue check runs separately under the existing
proof timeout.
