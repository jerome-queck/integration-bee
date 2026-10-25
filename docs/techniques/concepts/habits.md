# Habits on top of a parent move

Coach card for the eleven nodes that package more than one identity. Original fences on this page were checked with SymPy. They are not catalog rows. Stored drills stay in the unit file named below. A contest row is not a source for a new number.

Open the parent card in `README.md` first. Open this page when the integrand is one of the shapes below. Teach the stored drill in the unit, then the fence. Stop. Do not tick `floor` or `dutis`. Do not invent a value for `vector-calc`, `beta`, `zeta`, `euler-mascheroni`, or `catalan`. Unit 35 already prints two Basel values. This page does not add another. Unit 36 leaves Catalan's constant as \(G\).

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `modified-textbook` | 3 | `algebra-manipulation` | `units/12-modified-sneaky-algebra/teaching.tex` |
| `sneaky-algebra` | 3 | `algebra-manipulation` | the same file |
| `sneaky-u-sub` | 3 | `power-substitution` | `units/19-power-sneaky-usub/teaching.tex` |
| `sneaky-symmetry` | 3 | `symmetry` | `units/18-sneaky-symmetry-product/teaching.tex` |
| `sneaky-product-rule` | 3 | `reverse-product-rule` | the same file |
| `speed-bashing` | 3 | `basic-integration-by-parts` | `units/23-periodicity-speed/teaching.tex` |
| `complexifying` | 4 | `basic-integration-by-parts` | `units/32-taylor-complex/teaching.tex` |
| `ninja-substitution` | 4 | `basic-trig-substitution` | `units/33-ninja-inversion/teaching.tex` |
| `inversion` | 4 | `kings-queens-rule` | the same file |
| `modified-famous` | 4 | `advanced-gaussian` or `dirichlet` | `units/35-modified-famous/teaching.tex` |
| `unique-tricks` | 4 | `feynman` | `units/36-unique-tricks/teaching.tex` |

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| A fresh technique for an integrand that is already \(e^u\,du\) | `U12-D01` |
| Partial fractions on a polynomial that already cancels | `U12-D05` |
| A root substitution on an integrand that is already an arctangent | `U19-D08`, stored \(\pi/2\) |
| A report of \(0\) for an even integrand | `U18-D04`, stored \(\pi^3/96\) |
| Parts begun before the product is guessed | `U18-D05` |
| A new identity for a sum of textbook terms | `U23-D08` |
| Two parts reductions for one complex exponential | `U32-D05`, stored \(1/2\) |
| The half-angle substitution when the numerator is already the derivative | `U33-D01`, stored \((\ln 2)/2\) |
| Inversion when the numerator is already the derivative of the denominator | `U33-D08`, stored \(1/2\) |
| A new zeta value, or an elementary antiderivative of \(e^{-x^2}\) | `U35-D01` for the scale. The stored series stay `U35-D04` and `U35-D05`. Do not tick `zeta`. |
| A Gaussian quote on the linear exponent \(e^{-3x}\) | `U35-D03`, stored \(1/3\). |
| A series on \((e^{-x}-e^{-2x})/x\) | `U35-D07`, stored \(\ln 2\). That integral is `U34-D01`. |
| \(G\) replaced by a logarithm or a rational | `U36-D03` stays \(G\). The parameter drill is `U36-D01`, stored \(\ln 2\). |
| \(\ln 2\) written for \((x^2-1)/\ln x\) | `U36-D07`, stored \(\ln 3\). |
| \(\ln|\ln x|\) written for \(\int(\ln x)/x\,dx\) | `U36-D08`, stored \(\frac12(\ln x)^2\). |
| The cosine antiderivative was written for \(\int e^x\sin x\,dx\) | `U32-D08`, stored \(\frac12 e^x(\sin x-\cos x)\). The cosine antiderivative is `U32-D07`. |
| The sign of \(\ln x\) was dropped under \(x\mapsto 1/x\) | `U33-D07`, stored \(0\). |

## Modified textbook

Use this when one textbook antiderivative is hiding behind an extra derivative factor. The stored drill is `U12-D01`: \(u=e^x\) turns \(\int e^x e^{e^x}\,dx\) into \(e^{e^x}+C\). The same substitution on \([0,1]\) is the fence.

```ib-example
integrand: exp(x)*exp(exp(x))
limits: 0, 1
answer: exp(E)-E
```

`U12-D02` splits \(1/(1+e^x)^2\) into the logistic integral and one derivative. `U12-D03` is the half-angle reading of \(\sqrt{(1-x)/(1+x)}\) on \([0,1]\), value \(\pi/2-1\). `U12-D04` splits into an arcsine and a square root.

The miss is a fresh technique for an integrand that is already \(e^u\,du\), or already \(\arcsin x\) plus a square-root derivative.

## Sneaky algebra

Cancel a factor, or shift and expand. The stored drill is `U12-D05`: \(x-4=(\sqrt{x}-2)(\sqrt{x}+2)\) on \([0,1]\), value \(8/3\). The fence replaces \(2\) by \(3\).

```ib-example
integrand: (x-9)/(sqrt(x)-3)
limits: 0, 1
answer: 11/3
```

`U12-D06` is the even polynomial \(x^2-1\) on \([-1,1]\), value \(-4/3\). `U12-D07` shifts by \(u=x-3\) and integrates, value \(-19/30\). `U12-D08` is \(u=x^3+1\), antiderivative \((x^3+1)^3/9\).

The miss is a partial-fraction decomposition of a polynomial that is already elementary.

## Sneaky substitution

The power move is `u-substitution.md`. These drills start after that move. `U19-D05` sets \(u=\sqrt{x^2+x}\) and reaches \(\arctan(2u)\). The fence is the same \(u\) with \(2x+1\) left in the numerator.

```ib-example
integrand: (2*x+1)/sqrt(x**2+x)
limits: 0, 3
answer: 4*sqrt(3)
```

`U19-D06` is the fractional linear substitution, value \(-5/6+\ln 2\). `U19-D07` shifts and uses \(t=\sin^2\theta\), value \(\pi/2\). `U19-D08` is \(\int_0^\infty dx/(1+x^2)=\pi/2\). A power \(x=u^n\) stops there.

The miss is a root substitution on an integrand that is already an arctangent.

## Sneaky symmetry

Shift until the midpoint sits at the origin, then read the odd part. The stored drill is `U18-D01`. The center is \(3\), and \(u=x-3\) is odd on \([-1,1]\), so the integral on \([2,4]\) is \(0\). The fence is the three-factor product with the same idea.

```ib-example
integrand: (x-1)*(x-2)*(x-3)
limits: 1, 3
answer: 0
```

`U18-D02` and `U18-D03` are already odd. Their stored values are \(0\). `U18-D04` is even. The substitution \(u=\arctan x\) produces \(\pi^3/96\).

The miss is a report of \(0\) for an even integrand, or a shift on an interval that is already symmetric.

## Sneaky product rule

The integrand is \((fg)'\). Guess the product and differentiate it. The stored drill is `U18-D05`: the derivative of \(\sec x\tan x\) is \(\sec^3 x+\sec x\tan^2 x\). The fence halves the coefficient in `U18-D06`, so the product is \(\sqrt{x}\,e^x\).

```ib-example
integrand: exp(x)*(sqrt(x)+1/(2*sqrt(x)))
limits: 1, 4
answer: 2*exp(4)-E
```

`U18-D06` stores \(2\sqrt{x}\,e^x\). `U18-D07` stores \(-e^x\cos x\). `U18-D08` stores \(x\sin(\ln x)\).

The miss is an integration by parts that begins before the product has been guessed.

## Speed bashing

Split a sum, or unroll a short parts reduction, and stop. The stored drill is `U23-D08`, the four-term antiderivative \(x+\ln|x|-\arctan x-1/x\). The fence is a two-term split.

```ib-example
integrand: x+1/(1+x)
limits: 0, 1
answer: 1/2+log(2)
```

`U23-D06` unrolls \(\int x^3 e^x\,dx\) in three parts steps. The stored antiderivative is \(e^x(x^3-3x^2+6x-6)\). `U23-D07` splits \(\sin^3 x+\cos^3 x\) into two odd powers. A reduction \(I_n\) waits for unit 20.

The miss is a new identity for a sum of textbook terms.

## Complexifying

Replace \(e^{ax}\cos bx\) by the real part of \(e^{(a+ib)x}\), and \(e^{ax}\sin bx\) by the imaginary part. The stored drill is `U32-D05`: \(\int_0^\infty e^{-(1-i)x}\,dx=(1+i)/2\), so both the cosine and the sine integrals equal \(1/2\). The fence raises the decay from \(1\) to \(2\).

```ib-example
integrand: exp(-2*x)*cos(x)
limits: 0, oo
answer: 2/5
```

`U32-D06` is the sine partner of `U32-D05`. `U32-D07` stores \(\frac12 e^x(\cos x+\sin x)\). `U32-D08` stores \(\frac12 e^x(\sin x-\cos x)\).

The miss is two separate parts reductions for a pair that is one complex exponential.

## Ninja substitution

Try \(x=\tan\theta\) when \(1+x^2\) is in the denominator and the numerator is a logarithm or an arctangent. The stored drill is `U33-D04`: \(x=\tan\theta\) and the reflection \(\theta\mapsto\pi/4-\theta\) give \(\pi\ln 2/8\). The fence drops the logarithm and integrates the arctangent against its own derivative.

```ib-example
integrand: atan(x)/(1+x**2)
limits: 0, 1
answer: pi**2/32
```

`U33-D01` is \(\int_0^1 x/(1+x^2)\,dx=(\ln 2)/2\). The numerator is already \(du\). `U33-D02` uses the cosine formula from unit 26 and stores \(\sqrt{2}\,\pi/4\). `U33-D03` sets \(u=\sqrt{x^2-1}\) and stores \(\arctan u\).

The miss is the half-angle substitution on an integrand whose differential is already \(dx/(1+x^2)\).

## Inversion

On \((0,\infty)\), write the copy at \(1/x\) and add. The stored drill is `U33-D06`. The two numerators cancel \(1+x\), and \(2I=\pi/2\), so \(I=\pi/4\). The fence is the finite-interval form of `U33-D08`, where inversion is the long path and \(u=1+x^2\) finishes the integral.

```ib-example
integrand: x/(1+x**2)**2
limits: 0, 1
answer: 1/4
```

`U33-D05` is \(\pi/2\). Inversion reproduces it. `U33-D07` changes the sign of \(\ln x\) and stores \(0\). `U33-D08` on \((0,\infty)\) stores \(1/2\).

The miss is an inversion of an integrand whose numerator is already the derivative of the denominator.

## Modified famous integrals

Scale a stored Gaussian or a stored Dirichlet integral, then stop. `U35-D01` sets \(u=x\sqrt{2}\) in `U30-D01` and stores \(\sqrt{2\pi}/4\). The Gaussian fence is the same half-line with \(u=3x\).

```ib-example
integrand: exp(-9*x**2)
limits: 0, oo
answer: sqrt(pi)/6
```

`U35-D02` sets \(u=2x\) in `U30-D05` and stores \(\pi/2\). The Dirichlet fence is the factor \(3\). The \(b\) in the sine cancels the chain rule, and the value is again `U30-D05`.

```ib-example
integrand: sin(3*x)/x
limits: 0, oo
answer: pi/2
```

`U35-D03` is the elementary integral \(1/3\), and it is the bare drill. `U35-D04` and `U35-D05` are the series the unit already prints, \(-\pi^2/6\) and \(-\pi^2/12\). `U35-D06` is \(-\frac\pi2\ln 2\). `U35-D07` is `U34-D01`, value \(\ln 2\). `U35-D08` is \(1\), and it is the bare series drill.

The miss is a new zeta value, or an elementary antiderivative of \(e^{-x^2}\).

## Unique tricks

Three devices, and then stop. A quotient \((x^b-x^a)/\ln x\) is the parameter integral from unit 34. The stored drill is `U36-D01`, value \(\ln 2\). `U36-D07` stores \(\ln 3\). The fence runs the parameter from \(0\) to \(4\).

```ib-example
integrand: (x**4-1)/log(x)
limits: 0, 1
answer: log(5)
```

`U36-D04` is \(\ln|\ln x|\). `U36-D05` stores \(\ln 2\) on \([2,4]\). `U36-D06` stores \(1\) on \([e,e^e]\). `U36-D08` stores \(\frac12(\ln x)^2\). `U36-D02` is `U35-D06`.

`U36-D03` stores \(G\). The series at the endpoint is the definition of Catalan's constant. Leave \(G\) as \(G\). The fence \(\ln 5\) is a parameter value.

The miss is a replacement of \(G\) by a logarithm or a rational number, or a series expansion of \(\ln x\) in the denominator.

## Where this goes wrong

The parent move already finished the integral, and a second technique was started anyway. `U19-D08`, `U23-D08`, and `U33-D08` are those stops.

A symmetric interval produced an automatic \(0\). Check odd against even. `U18-D04` is even and equals \(\pi^3/96\).

A named constant was unwrapped. \(G\) stays \(G\). The Basel values in unit 35 stay the two stored series.

## On a miss

Teach this file, then the unit in the table. Use the miss table, then the stored drill named in the section. Complexifying works `U32-D05`, fades `U32-D07`, and sets bare `U32-D08`. Ninja substitution works `U33-D04`, fades `U33-D03`, and sets bare `U33-D02`. Inversion works `U33-D06`, fades `U33-D07`, and sets bare `U33-D05`. Modified famous works `U35-D01`, fades `U35-D02`, and sets bare `U35-D03`. Its series works `U35-D04`, fades `U35-D05`, and sets bare `U35-D08`. Unique tricks works `U36-D01`, fades `U36-D07`, and sets bare `U36-D06`. `U36-D03` stays \(G\). The fences above are scales of those drills. They are not drill ids. Leave `floor` and `batis` unticked. A correct value reached by a second technique still needs the first move named.
