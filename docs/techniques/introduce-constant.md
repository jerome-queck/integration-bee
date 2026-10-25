# Introducing a constant

Guide section 1.9 is an algebraic move. You add and subtract a constant so the numerator matches the derivative of the denominator, or so a fraction becomes 1 plus a remainder. This move is not dutis.

The integral below is not a stored drill. On [0, 1],

(x+1)/(x+2) = 1 - 1/(x+2).

The antiderivative is x - ln|x+2|. The definite value is 1 + ln(2/3).

```ib-example
integrand: (x+1)/(x+2)
limits: 0, 1
answer: 1 + log(2/3)
```

## A smaller parameter

Differentiating under the integral sign is a later move. The catalog id `dutis` stays deferred. The chapter note is `units/34-frullani-feynman/teaching.tex`, and it walks the stored drill `U34-D05`. The smaller parameter here is the same idea on a different power.

For a > -1, the integral of x^a from 0 to 1 is 1/(a+1). Differentiate in a. The integral of x^a ln x from 0 to 1 is -1/(a+1)^2. At a = 3 the value is -1/16.

```ib-example
integrand: x**3*log(x)
limits: 0, 1
answer: -1/16
```

That is a smaller parameter than the unit 34 chapter. Do not tick `dutis` from this note.
