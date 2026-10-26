# R2-2024-Down-Down-1

## Sources and structured answer

The Down clue sheet is
`sources/past/r2/2024/Crossnumber_Down_2024_R2_UK_University_Integration_Bee.pdf`,
p.2. The numbered completed grid was read visually from
`sources/past/r2/2024/Mark_Scheme_R2_2024_UK_University_Integration_Bee.pdf`,
p.3. The Down map is

`{1:128, 3:495, 5:25, 6:18381, 9:91423, 10:1728, 12:5303, 13:7921, 14:990, 15:517, 16:642, 17:389}`.

Two layout details matter. Down 5 prints `20*pi - (25*log(2))/2`,
not `(20*pi-25*log(2))/2`. In Down 13, the root index on `e` is
`sqrt(a+b)`, so its factor is `exp(1/sqrt(a+b))`. Both readings were
confirmed from enlarged original-page renders.

## Down derivations

1. The digits are 1,2,8. In the permitted order take `a=8,b=2,c=1`:
   `a^3=512`, `abs(a-b)^3=216`, and both 2 and 1 occur in each cube.
   The checker searches all six orders of the supplied three digits.

3. Put `u=integral_0^1 f`, `v=integral_1^2 f`, `w=integral_2^3 f`.
   The stated equations are `45u+25v=2025` and
   `20u+45v+20w=2520`. Subtracting gives
   `20(v+w)-25u=495`. Its absolute value is 495.

5. A primitive of `(a*x+5)/(x^2-6*x+10)` is
   `(a/2)log((x-3)^2+1)+(3a+5)atan(x-3)`.
   Its difference between 2 and 3 is
   `-a*log(2)/2+(3a+5)*pi/4`. At `a=25` this is precisely the printed
   `20*pi-25*log(2)/2`. The code differentiates the primitive and checks
   its exact endpoint difference.

6. 18381 is a palindrome and `18381=11*1671`.

9. The two largest entries are 390625 and 91423. Their quotient has
   floor 4, the middle digit of 91423. The checker sorts both supplied
   directional maps to obtain the two entries.

10. Across entries give the exponent `84/12-5=2`. For `0<x<pi`,
    Dirichlet convergence and the Abel logarithmic sum yield
    `sum_{n>=1} sin(nx)/n=(pi-x)/2`.
    To fix the argument branch, use
    `1-exp(ix)=-2i exp(ix/2) sin(x/2)` with `sin(x/2)>0`.
    Its principal argument is `x/2-pi/2`. The factorization is checked
    symbolically. The endpoint values do not change the integral.
    Hence the integral of the square is `pi^3/12`, checked directly.
    The displayed set is then
    `{1728*pi^(3k-9): k in Z}`.
    Every nonzero integer power of the transcendental number pi is
    transcendental: otherwise pi would be algebraic over the algebraic
    numbers and hence algebraic. Thus only `k=3` gives an integer,
    namely 1728. The certificate uses `pi.is_transcendental` and the
    exact polynomial integral; no numerical integer recognition occurs.

12. The upper limit is `89+84=173`. On `n<=x<n+1` with integer `n>=1`,
    `n^2<=n*x<n^2+n<(n+1)^2`, so `floor(sqrt(x floor x))=n`.
    Meanwhile `floor(n*x)-n^2` takes the values `0,...,n-1` on `n`
    equal subintervals. Its integral over that unit interval is
    `(n-1)/2`. The initial interval `[0,1)` contributes zero. Therefore
    the requested value is
    `sum_{n=1}^{172}(n-1)/2-2050=7353-2050=5303`.
    The checker performs the finite rational sum and the square bounds.

13. Complete the square: `-x^2+x=-(x-1/2)^2+1/4`.
    The full Gaussian integral is `exp(n/4)*sqrt(pi/n)`. SymPy checks
    the Gaussian factor, and
    `log(sqrt(pi/n))/n -> 0`, so the required nth-root limit is
    `exp(1/4)`. For the printed digits `a=7,b=9,c=2,d=1`, the right
    side is
    `((9-7)/2)*exp(1/sqrt(7+9))=exp(1/4)`.
    Their second-smallest digit is 2, exactly twice the nonzero final
    digit 1.

14. `990=2*495`, so 3 Down divides this entry.

15. `517=11*47` is not prime.

16. The last digit of 642 is 2, which is `5-3`, where 5 is the first
    digit of 15 Down.

17. 389 is odd, `3<8<9`, and `3+8+9=20`.

The entries 517,642,389 contain each digit 1 through 9 exactly once.
The proof helper checks that joint condition, each individual condition,
and all crossings against the shared completed-grid lattice.
