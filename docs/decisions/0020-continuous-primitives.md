# Continuous primitives for jumping antiderivatives

Audit receipt ibe-audit-remediation-2026-10-31, lane L1b, item A7. Six indefinite answers were antiderivatives on each open piece and jumped at the joins. The catalog now stores a continuous primitive. The ordinary derivative check is unchanged: it still accepts the smooth local formula, and it still rejects a floor term because SymPy leaves `Derivative(floor)` in the difference.

`verify/piecewise_primitive.py` is the check for these formulas. On each piece the floor index is an integer constant and the ordinary derivative equals the integrand. The left and right limits agree at every join. A jumping answer, and a floor sign with the step omitted, fail that check.

### Stored primitives

| Id | Continuous value |
|---|---|
| `YANG-1.15-P08`, `YANG-2.6-P01` | `2*(-1)**floor(x/(2*pi)+1/2)*sqrt(2)*sin(x/2) + 4*sqrt(2)*floor(x/(2*pi)+1/2)` |
| `YANG-1.6-P19` | `(2*x+2)*exp(x/2)` for `x>=-3`, and `(-2*x-2)*exp(x/2)-8*exp(-3/2)` for `x<-3` |
| `YANG-2.6-P09` | `atan(tan(x)/3)/3 + pi*floor(x/pi+1/2)/3` |
| `SAMPLE-Q14` | `sqrt(2)*atan(sqrt(2)*tan(log(x)))/2 + sqrt(2)*pi*floor(log(x)/pi+1/2)/2` |
| `SAMPLE-Q16` | `2*sqrt(3)*atan(2*sqrt(3)*tan(x/2)/3+sqrt(3)/3)/3 + 2*sqrt(3)*pi*floor(x/(2*pi)+1/2)/3` |

The answers PDF still prints the jumping local formulas for `SAMPLE-Q14` and `SAMPLE-Q16`. The Yang practice lists print no final. Those marks stay in the notes.

Numeric checks use mpmath at 80 decimals. The largest absolute error of a central difference of step `1e-20`, or of the two sides of a join approached by `1e-40`, is below `1e-30`:

| Id | Absolute error |
|---|---|
| `YANG-1.15-P08` | `5.8e-42` |
| `YANG-2.6-P01` | `5.8e-42` |
| `YANG-1.6-P19` | `1.0e-40` |
| `YANG-2.6-P09` | `1.0e-40` |
| `SAMPLE-Q14` | `3.2e-39` |
| `SAMPLE-Q16` | `5.0e-41` |

Do not mark a row impossible.
