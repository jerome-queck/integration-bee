# Real branches for the L1 audit rows

Audit receipt ibe-audit-remediation-2026-10-31, lane L1. The printed mark is kept in the solution note when it is only a local piece. The catalog stores a gate-proved reading that stays real on every component where the integrand is real.

Numeric checks use mpmath. Unless a row says otherwise, `mp.mp.dps` is 50 and the recorded figure is the absolute error.

### Escalation / unlock: R1-2020-Q31 and R1-2022-MIT-TB-Q15

- What changed: the catalog antiderivative is the continuous primitive `4*sqrt(2)*(2*floor(u/pi)-(-1)**floor(u/pi)*cos(u))` with `u=x/4+pi/4`. `verify/pack_handoff_b.py` proves it from the half-angle square, the constant-floor derivative, and matching left and right limits at `u=m*pi`.
- PDF problem / mark: the answers sheets print `4*(sin(x/4)-cos(x/4))`, which matches only where `sin(x/4)+cos(x/4)` is nonnegative.
- Proposed follow-up encode prompt:
  1. Preserve the printed problem, conflicting mark, and any quoted correction; identify every affected alias.
  2. Solve the chosen source reading independently and cite its answer authority.
  3. Encode the stated domains, endpoints, and branch assumptions.
  4. Add an exact gate-accepted certificate tied to that reading and wrong-answer controls.
  5. Verify the derived catalog answer, then update grading fixtures and counts.
  6. Run doctor, make check, and review; open a separate PR.
- Do not mark impossible.

Finite-difference error of that primitive against `sqrt(1+sin(x/2))`, step `1e-18`, dps 40: at `x=-7.3`, `2.2e-23`; at `x=-1`, `2.7e-23`; at `x=0.3`, `5.3e-24`; at `x=2`, `2.2e-24`; at `x=10`, `1.7e-23`.

### Escalation / unlock: R3-2024-TB3-Q01

- What changed: `answer_sympy` is `asec(Abs(x + 2))`.
- PDF problem / mark: the tiebreaker sheet prints `asec(x+2)`, valid for `x>-2`.
- Proposed follow-up encode prompt: the same six steps as above.
- Do not mark impossible.

Central-difference error at dps 50, step `1e-16`: `x=-8` gives `1.3e-35`; `x=-4` gives `1.0e-33`; `x=-3.2` gives `5.4e-32`; `x=0` gives `1.0e-33`; `x=3` gives `2.1e-35`.

### Other corrected values

| Id | Stored value | Numeric error |
|---|---|---|
| R1-2021-Q37 | nested towers, integral `0` | quad on `[0, pi/2]` at dps 40: `2.1e-43` |
| R1-2021-Q12 | `pi/(2*sin(pi*n/2)*gamma(n))` | `n=1` quadosc error `0` against `pi/2`. The gamma ratio `gammasimp` simplifies to `1`, and the limit at `n=1` is `pi/2`. |
| R1-2021-Q27 | `pi*exp(-Abs(a*b))/(2*Abs(b))` | dps 50 quadosc: `(1,2)`, `(-1,2)`, `(1,-2)`, `(0.5,1)` error `0`; `(-3,-4)` error `9.0e-55` |
| R1-2021-Q32 | `pi*(Abs(b)-Abs(a))/2` | `∫_0^∞ (1-cos u)/u^2 du` equals `pi/2` with error `1.3e-34` at dps 60 (smooth head plus sine-integral tail). The gate checks the substitution `u=|k|x` for nonzero real `k`, and a zero coefficient separately, before it returns `π(|b|-|a|)/2`. |
| R2-2022-Relay-Q04 | `pi/(2*Abs(a)*sqrt(a**2-1))` | dps 40: `a=2` and `a=-3` error `0`; `a=1.2` error `2.3e-41` |
| R1-2021-Q21 | printed formula kept | convention only: real for `|a|<pi/2`, `a!=0` |

Cube-root integrands `YANG-1.2-P11`, `YANG-2.3-P06`, and `YANG-2.3-P13` now use `sign` and `Abs`. Their previous absolute-value antiderivatives are unchanged and still differentiate to the real integrand.

Real logarithms replace `log` by `log(Abs(...))` on the rows whose imaginary part was a fixed rational multiple of `pi` while the integrand was real: `R1-2023-Q16`, `R2-2024-Relay-Q20`, `SAMPLE-Q11`, `SAMPLE-Q15`, and the Yang rows `1.15-P15`, `1.15-P18`, `1.15-P19`, `1.20-P06`, `1.4-P05`, `1.4-P14`, `1.5-P01`, `1.5-P08`, `1.5-P09`, `1.5-P19`, `1.6-P05`. The same wrap is in drills `U01-D06`, `U05-D04`, `U22-D06`, `U22-D07`, `U23-D08`, `U24-D01`, `U24-D03`, and `U24-D04`.

Nest conventions, without replacing a closed form the gate already proves: `R1-2020-Q24` converges for `x>3/4`; `R1-2024-Q17` uses the unique branch in `[0,1]`; `R1-2025-Online-Q19` uses the algebraic closed forms, and the minus iteration converges only for `x>3/4`.
