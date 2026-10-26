# R2-2023-Crossnumber-Across-1

## Sources and answer shape

Clues and numbered black-cell lattice were read visually from
`sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf`,
p.2. Digits were read from the completed grid in
`sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf`,
p.3. The answer is a map of clue numbers to integers, not one scalar:

`{1:10, 2:16, 3:532416, 5:36, 6:4320, 8:53, 9:2201, 10:610, 11:271, 12:343, 13:738, 16:295, 17:146}`.

`verify/pack_grid_2023.py` records every printed clue, both directional maps,
the 12-by-8 lattice, the printed start coordinates, and one exact check per
clue. The shared contract also compares the answer to the printed map and
checks all its crossings with the sibling grid. Its Across proof does not
promote the Down row: Down 7 has a missing regularity hypothesis, documented
in `R2-2023-Crossnumber-Down-1.md`.

## Across derivations

1. Put `u=integral_0^1 f`, `v=integral_1^2 f`. The two displayed equations
   become `3u+5v=5` and `2u+3v=4`. Hence `u=5`, `v=-2` and `abs(uv)=10`.
   The checker solves these equations exactly with SymPy.

2. Down 11 is 27, so the exponent is 7. With `z=sqrt(log x)`, the odd
   powers cancel even though the principal square root is imaginary for
   `0<x<1`. The sum is
   `2+42 log x+70(log x)^2+14(log x)^3`. Substitution `x=exp(-t)` gives
   `integral_0^1 (log x)^k dx=(-1)^k k!`; the result is
   `2-42+140-84=16`. The finite polynomial and all coefficients are checked.
   The exponent comes from the independently verified 26-fold integration
   in Down 11, not from an assumed value of Down 7.

3. The six digits `5,3,2,4,1,6` are precisely 1 through 6, and
   `5>3>2`, `4>1`, `5*3*2+4*1-6=28`. This is an exact digit predicate.

5. The floor brackets are **inside** the printed limit. For `0<=x<1`,
   `atan(x^n)` tends to zero; for `1<x<=24`, it tends to `pi/2`.
   Its absolute value is bounded by `pi/2` throughout the finite interval.
   Dominated convergence therefore gives `23*pi/2`, strictly between 36
   and 37. The integrals eventually lie in that same open interval, so
   their floors tend to 36. The checker confirms the two positive-parameter
   exponential limits, and computes the exact floor.

6. In the full printed grid the largest two entries are 532416 and 69134;
   the smallest two are 10 and 16. The required floor is
   `floor(69134/16)=4320`. The checker sorts the supplied maps rather than
   storing this ratio as an unrelated answer.

8. The three smallest entries are 10, 16 and 27; their sum is 53.

9. Factor `20 exp(1337x)` from numerator and denominator. Write
   `h(t)=log(1+(6/5)exp(-t))`. The integrand is
   `[h(917x)-h(1268x)]/x`. Its near-zero difference is `O(x)` and its
   tail decreases exponentially, so the improper integral converges.
   For positive `alpha,beta`, integration of the derivative with respect
   to a scale parameter, or the fundamental theorem and Fubini, gives
   
   `integral_0^infinity [h(alpha*x)-h(beta*x)]/x dx`
   `=(h(0)-h(infinity))*log(beta/alpha)`.
   
   Here `h'(t)=-6/(5 exp(t)+6)` is integrable,
   `h(0)=log(11/5)` and `h(infinity)=0`. Thus the answer is
   `log(1268/917)*log(11/5)`. Both fractions are reduced and
   `1268+917+11+5=2201`. The checker verifies the derivative, endpoint
   limits, exponent differences and coprimality exactly.

10. `610=F_15` for `F_0=0,F_1=1`. The integer Fibonacci check passes.

11. Evenness followed by `t=x^2` gives
    `integral_0^1 t^(-1/2) log(t) log(1-t) dt`.
    This is the mixed derivative of `B(p,q)` at `(1/2,1)`.
    Differentiation under the integral is justified on a compact
    neighborhood with `p,q>0` by the integrable logarithmic endpoint
    bounds. The gamma quotient and its mixed derivative give
    `16-pi^2-8 log(2)=16-pi^2-log(256)`.
    The trigamma recurrence used by the checker is
    `psi_1(3/2)=psi_1(1/2)-4=pi^2/2-4`.
    Therefore `a+b-1=16+256-1=271`.

12. `343=7^3`.

13. `738+1=739` is prime.

16. `295=5*59`, a product of two primes.

17. `1*4*6=24` and `1+4+6=11`.

The entries in Across 13,16,17 concatenate to `738295146`; their digits
are exactly 1 through 9 with no repetition, as required jointly.

## Verification boundary

Every Across clue has its own mathematical or exact integer check. The
clue maps and crossings are additional checks, not substitutes for these
derivations. No whole-paper symbolic integral is attempted. The sibling
Down map is the visually read mark grid; its defective Down 7 clue remains
manual and is not represented as a proved point-value theorem.
