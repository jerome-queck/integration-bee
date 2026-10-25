# Floor integrals

Guide section 1.7. This node stays deferred. The catalog node `floor` has no unit, so the coach does not assign a floor drill. This note is the teaching for that gap.

The floor of x is the greatest integer less than or equal to x. On each half-open interval [k, k+1) the floor is the constant k. You split at integers, pull that constant out, and sum the pieces.

On [0, 2] the floor is 0 on [0, 1) and 1 on [1, 2). The single point at 2 does not change the value. The integral of that step is the length of the second piece.

```ib-example
integrand: Piecewise((0, x < 1), (1, x < 2), (0, True))
limits: 0, 2
answer: 1
```

SymPy leaves `integrate(floor(x), (x, 0, 2))` unevaluated, so the checked fence is the piecewise split, not a call to `floor`. A contest row tagged floor in the sample list is still `verify: manual` until its own integrand is checked. Do not copy that answer into this note.
