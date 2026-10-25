# Introducing a constant

Guide section 1.9 is an algebraic move. You add and subtract a constant so the numerator matches the derivative of the denominator, or so a fraction becomes 1 plus a remainder. You can also multiply and divide by a constant that does not depend on \(x\), when that constant is the numerator an addition formula wants. This move is not dutis.

The syllabus names DUTIS as its own technique, in two forms: a fixed interval, and an interval whose endpoints move with the parameter. The catalog id `dutis` has no unit of its own, and nothing in this note ticks it. The fixed-interval drills are `U11-D13`, `U11-D14`, and `U11-D15` on the special-wildcard node. Differentiating under the integral sign when an endpoint moves is `units/34-frullani-feynman/teaching.tex`.

## Rewrite the fraction

The integral below is not a stored drill. On \([0, 1]\),

\[
\frac{x+1}{x+2} = 1 - \frac{1}{x+2}.
\]

The numerator is 1 less than the derivative of the denominator, so you add and subtract that 1. The antiderivative is \(x - \ln|x+2|\). The definite value is \(1 + \ln(2/3)\).

```ib-example
integrand: (x+1)/(x+2)
limits: 0, 1
answer: 1 + log(2/3)
```

## A square that is almost a derivative

On the same interval the denominator \((x+1)^2 = x^2+2x+1\) has derivative \(2x+2\). The numerator \(x^2+2x\) is that denominator minus 1, so

\[
\frac{x^2+2x}{x^2+2x+1} = 1 - \frac{1}{(x+1)^2}.
\]

\[
\int_0^1\left(1 - \frac{1}{(x+1)^2}\right)dx = \Bigl[x + \frac{1}{x+1}\Bigr]_0^1 = \Bigl(1+\frac12\Bigr) - 1 = \frac12.
\]

```ib-example
integrand: (x**2+2*x)/(x**2+2*x+1)
limits: 0, 1
answer: 1/2
```

Use this when the numerator is a polynomial of the same degree as the denominator, or one degree lower and close to the derivative. Divide first. The remainder is the integral you actually compute. A partial-fraction decomposition is the same idea after the division, and it lives in units 05 and 22.

## A multiple of the denominator

The constant you introduce can be a coefficient, not only \(1\). On \([0, 1]\),

\[
\frac{3x+5}{x+1} = 3 + \frac{2}{x+1},
\]

because \(3x+5 = 3(x+1)+2\). The integral is \(3 + 2\ln 2\).

```ib-example
integrand: (3*x+5)/(x+1)
limits: 0, 1
answer: 3 + 2*log(2)
```

Do this before a substitution. A lone constant or a single factor in the numerator is a shorter integral than the mixed numerator you started with.

## Multiply and divide by a constant

Some products want a numerator that an addition formula can split. The constant \(\sin(\pi/3) = \sqrt{3}/2\) does not depend on \(x\). On \([0, \pi/3]\),

\[
\sin\frac\pi3 = \sin x\cos\Bigl(\frac\pi3-x\Bigr) + \cos x\sin\Bigl(\frac\pi3-x\Bigr),
\]

so

\[
\frac{\sin(\pi/3)}{\cos x\cos(\pi/3-x)} = \tan x + \tan\Bigl(\frac\pi3-x\Bigr).
\]

Each tangent integrates to \(\ln 2\) on this interval: \(\int_0^{\pi/3}\tan x\,dx = -\ln\cos(\pi/3) = \ln 2\), and the reflected tangent is the same. The sum is \(2\ln 2\). Divide by \(\sin(\pi/3)\):

\[
\int_0^{\pi/3}\frac{dx}{\cos x\cos(\pi/3-x)} = \frac{2\ln 2}{\sqrt{3}/2} = \frac{4\ln 2}{\sqrt{3}}.
\]

```ib-example
integrand: 1/(cos(x)*cos(pi/3 - x))
limits: 0, pi/3
answer: 4*log(2)/sqrt(3)
```

This integral is not a stored drill. The constant had to be independent of \(x\). If the factor you want depends on \(x\), you are substituting, not introducing a constant.

## A smaller parameter

The smaller parameter here is the same idea on a different power. You introduce a constant in the exponent, integrate a family you already know, and differentiate.

For \(a > -1\), the integral of \(x^a\) from 0 to 1 is \(1/(a+1)\). The integrand \(x^a \ln x\) is the derivative of that family in \(a\). On a compact interval \([\varepsilon, 1]\) with \(\varepsilon>0\), \(x^a\ln x\) is continuous for \(a>-1\), so the Leibniz rule applies there: the derivative in \(a\) passes under the integral sign. Then let \(\varepsilon\to 0\). The integral of \(x^a\ln x\) from 0 to 1 is \(-1/(a+1)^2\). At \(a=3\) the value is \(-1/16\).

```ib-example
integrand: x**3*log(x)
limits: 0, 1
answer: -1/16
```

That is a smaller parameter than the unit 34 chapter. The stored drill `U34-D05` is the same family at \(a=2\), where the value is \(-1/9\). Do not tick `dutis` from this note.

Differentiate again. The second derivative of \(1/(a+1)\) is \(2/(a+1)^3\), and that is \(\int_0^1 x^a(\ln x)^2\,dx\). At \(a=1\) the value is \(1/4\).

```ib-example
integrand: x*log(x)**2
limits: 0, 1
answer: 1/4
```

The Leibniz rule you are using, on a rectangle where \(f\) and \(\partial f/\partial a\) are continuous, is

\[
\frac{d}{da}\int_c^d f(x,a)\,dx = \int_c^d \partial_a f(x,a)\,dx.
\]

An infinite limit or an endpoint blow-up needs the limit argument above, or a sign that lets you switch the integrals. Unit 34 writes that out for the Frullani shape \((e^{-x}-e^{-2x})/x\), and it writes the syllabus form whose endpoints move with the parameter. A moving endpoint is not the algebra on this page.

## Stored DUTIS drills

These three are the fixed-interval form. The moving-limit form stays in unit 34.

`U11-D13` is the smaller parameter at a new power. Differentiate \(1/(a+1)\) and set \(a=4\):

\[
\int_0^1 x^4\ln x\,dx=-\frac{1}{25}.
\]

`U11-D14` differentiates \(\int_0^\infty e^{-ax}\,dx=1/a\) at \(a=2\). The integral of \(x e^{-2x}\) from 0 to \(\infty\) is \(1/4\). Take the limit of a compact interval \([0, R]\) before you quote the value.

`U11-D15` integrates the parameter instead of differentiating it. For \(a>-1\), \(\int_0^1 x^a\,dx=1/(a+1)\). Integrate in \(a\) from 0 to 3:

\[
\int_0^1\frac{x^3-1}{\ln x}\,dx=\ln 4.
\]

That is the stored answer of `U11-D15`. It is an original power, not a contest row.

## On a miss

Teach this file when the miss is the algebra, and teach `units/34-frullani-feynman/teaching.tex` when the miss is a moving limit. For a fixed-interval parameter, set `U11-D13`, `U11-D14`, or `U11-D15`. Do not invent an unchecked answer. Do not tick `dutis`. A correct final answer that used the wrong method still needs the method named in the mark.
