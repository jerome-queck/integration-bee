# Introducing a constant

Guide section 1.9 is an algebraic move. You add and subtract a constant so the numerator matches the derivative of the denominator, or so a fraction becomes 1 plus a remainder. This move is not dutis.

The syllabus names DUTIS as its own technique. The catalog id `dutis` stays deferred, and nothing in this note ticks it. Differentiating under the integral sign is a later, separate move. The chapter for that move is `units/34-frullani-feynman/teaching.tex`.

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

## A smaller parameter

The smaller parameter here is the same idea on a different power. You introduce a constant in the exponent, integrate a family you already know, and differentiate.

For \(a > -1\), the integral of \(x^a\) from 0 to 1 is \(1/(a+1)\). The integrand \(x^a \ln x\) is the derivative of that family in \(a\). On a compact interval \([\varepsilon, 1]\) with \(\varepsilon>0\), \(x^a\ln x\) is continuous for \(a>-1\), so the Leibniz rule applies there: the derivative in \(a\) passes under the integral sign. Then let \(\varepsilon\to 0\). The integral of \(x^a\ln x\) from 0 to 1 is \(-1/(a+1)^2\). At \(a=3\) the value is \(-1/16\).

```ib-example
integrand: x**3*log(x)
limits: 0, 1
answer: -1/16
```

That is a smaller parameter than the unit 34 chapter. The stored drill `U34-D05` is the same family at \(a=2\), where the value is \(-1/9\). Do not tick `dutis` from this note.

The Leibniz rule you are using, on a rectangle where \(f\) and \(\partial f/\partial a\) are continuous, is

\[
\frac{d}{da}\int_c^d f(x,a)\,dx = \int_c^d \partial_a f(x,a)\,dx.
\]

An infinite limit or an endpoint blow-up needs the limit argument above, or a sign that lets you switch the integrals. Unit 34 writes that out for the Frullani shape \((e^{-x}-e^{-2x})/x\).

## On a miss

Teach this file when the miss is the algebra, and teach `units/34-frullani-feynman/teaching.tex` when the miss is the parameter. Do not invent an unchecked answer. A correct final answer that used the wrong method still needs the method named in the mark.
