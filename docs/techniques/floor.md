# Floor integrals

Guide section 1.7. The floor drills are stored. `U11-D09` through `U11-D12` sit on unit 11, the special-wildcard node, because the catalog id `floor` has no unit of its own. The coach assigns those drills with that node. This note is the teaching for the gap. The Yang Topics Guide has no floor chapter. The syllabus lists the floor in section 2, and the Techniques Guide teaches the split. Those two, plus the checks below and the four drills, are the sources.

The floor of x is the greatest integer less than or equal to x. Write it \(\lfloor x\rfloor\). On each half-open interval \([k, k+1)\) the floor is the constant \(k\). You split at integers, pull that constant out, and sum the pieces. A single endpoint does not change a definite integral. A piece that stops between integers contributes its actual length, not a full unit.

## A step on two units

On \([0, 2]\) the floor is 0 on \([0, 1)\) and 1 on \([1, 2)\). The single point at 2 does not change the value. The integral of that step is the length of the second piece.

```ib-example
integrand: Piecewise((0, x < 1), (1, x < 2), (0, True))
limits: 0, 2
answer: 1
```

SymPy leaves `integrate(floor(x), (x, 0, 2))` unevaluated, so the checked fence is the piecewise split, not a call to `floor`. A contest row tagged floor in the sample list is still `verify: manual` until its own integrand is checked. Do not copy that answer into this note.

## Three units

On \([0, 3]\) the pieces contribute \(0\cdot 1 + 1\cdot 1 + 2\cdot 1 = 3\).

```ib-example
integrand: Piecewise((0, x < 1), (1, x < 2), (2, x < 3), (0, True))
limits: 0, 3
answer: 3
```

The same count works on \([0, n]\) for a positive integer \(n\): the integral of \(\lfloor x\rfloor\) is \(0+1+\cdots+(n-1) = n(n-1)/2\).

## Stop between integers

The formula \(n(n-1)/2\) needs an integer right endpoint. On \([0, 5/2]\) the pieces are \([0,1)\), \([1,2)\), and \([2, 5/2)\). The last piece has length \(1/2\) and floor \(2\), so it contributes \(1\), and the total is \(1+1=2\).

```ib-example
integrand: Piecewise((0, x < 1), (1, x < 2), (2, x < 5/2), (0, True))
limits: 0, 5/2
answer: 2
```

Find the points where the inside of the floor is an integer, split there, and use the length you actually have.

## A negative argument

\(\lfloor -0.2\rfloor = -1\), not \(0\). On \([-1, 0)\) the floor is the constant \(-1\), and on \([0, 1)\) it is \(0\). The integral on \([-1, 1]\) is \(-1\).

```ib-example
integrand: Piecewise((-1, x < 0), (0, x < 1), (0, True))
limits: -1, 1
answer: -1
```

The same split works for a negative integer endpoint. Do not replace \(\lfloor x\rfloor\) by \(|x|\) or by truncation toward zero.

## The floor is constant; the other factor is not

On \([0, 2]\), \(x\lfloor x\rfloor\) is \(0\) on \([0, 1)\) and \(x\) on \([1, 2)\). Pull out the constant \(1\), then integrate \(x\) on that piece: \(\int_1^2 x\,dx = 3/2\).

```ib-example
integrand: Piecewise((0, x < 1), (x, x < 2), (0, True))
limits: 0, 2
answer: 3/2
```

If the other factor is not constant on the piece, it stays inside the integral.

## The fractional part

The fractional part is \(\{x\} = x - \lfloor x\rfloor\). It lies in \([0, 1)\). On each interval \([k, k+1)\) it is the sawtooth \(x-k\), and the integral of one tooth is \(1/2\). Over two teeth the value is 1.

```ib-example
integrand: Piecewise((x, x < 1), (x-1, x < 2), (0, True))
limits: 0, 2
answer: 1
```

So an integral of \(\{x\}\) on \([0, n]\) is \(n/2\). An integral of \(x\) on that interval is \(n^2/2\), and subtracting the floor integral \(n(n-1)/2\) leaves the same \(n/2\).

## A fractional part over a power

On a finite range the same split can carry a rational weight. On \([1, 3]\),

\[
\frac{\{x\}}{x^2} =
\begin{cases}
(x-1)/x^2 & 1 \le x < 2, \\
(x-2)/x^2 & 2 \le x < 3.
\end{cases}
\]

Each piece is \(1/x\) minus a constant over \(x^2\). The value is \(\ln 3 - 5/6\).

```ib-example
integrand: Piecewise(((x-1)/x**2, x < 2), ((x-2)/x**2, x < 3), (0, True))
limits: 1, 3
answer: -5/6 + log(3)
```

An infinite upper limit turns that split into a series. This note does not check a zeta value. Do not quote one from a contest row.

## A linear argument

\(\lfloor ax+b\rfloor\) is constant between the points where \(ax+b\) is an integer. Solve \(ax+b = k\) for those points, split the interval there, and pull out \(k\). Do the same when the floor sits on a simple function you can invert, such as \(\lfloor e^x\rfloor\) or \(\lfloor 1/x\rfloor\), and stop at the last piece that meets the limits. If a piece is improper, check that the integral still exists before you quote a value.

## A sum of shifts

For a positive integer \(n\),

\[
\sum_{k=0}^{n-1}\lfloor x + k/n\rfloor = \lfloor nx\rfloor.
\]

Check \(n=2\), \(x=1/2\): \(\lfloor 1/2\rfloor + \lfloor 1\rfloor = 1\) and \(\lfloor 1\rfloor = 1\). A sum of shifted floors can collapse with this identity before you integrate term by term. This is Hermite's identity. It is not a license to import a contest value.

On \([0, 1]\) the identity says \(\lfloor x\rfloor + \lfloor x+1/2\rfloor = \lfloor 2x\rfloor\). Both sides integrate to \(1/2\): the left is \(0\) on \([0, 1/2)\) and \(1\) on \([1/2, 1)\).

## Stored drills

The feed stores the piecewise split, because SymPy leaves `floor` unevaluated. The learner still sees the floor.

- `U11-D09` is \(\lfloor x\rfloor\) on \([0, 4]\). Four full steps give \(0+1+2+3=6\).
- `U11-D10` is the fractional part on \([0, 3]\). Three teeth give \(3/2\).
- `U11-D11` stops at \(5/2\). The value is 2, the same fence as the section above.
- `U11-D12` is \(\lfloor x\rfloor\) on \([-2, 0]\). The pieces are \(-2\) then \(-1\), and the value is \(-3\).

## On a miss

Teach this file. Split the graph at the integers in the limits, write the piecewise, and add the areas. Watch a negative argument and a piece that ends between integers. Then set `U11-D09`, `U11-D10`, `U11-D11`, or `U11-D12`. Do not tick `floor`. Do not invent a pack answer.
