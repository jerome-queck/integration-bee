# Gaussian and Dirichlet pointers

Coach card. The two named values are the ones units 11 and 30 already store. The elementary scalings on this page were checked with SymPy. The Dirichlet line is the substitution \(u=bx\) applied to the value unit 30 stores. It was not recomputed as a fresh improper integral. A contest row is not a source for a new number. This page does not invent an antiderivative of \(e^{-x^2}\).

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `gaussian-integrals` | 2 | `basic-u-substitution`, `symmetry` | `units/11-gaussian-wildcard/teaching.tex` |
| `advanced-gaussian` | 4 | `gaussian-integrals` | `units/30-gaussian-dirichlet/teaching.tex` |
| `dirichlet` | 4 | `advanced-gaussian`, `basic-integration-by-parts` | the same file |
| `modified-famous` | 4 | `advanced-gaussian` or `dirichlet` | `units/35-modified-famous/teaching.tex` |

`special-wildcard` routes through `README.md` in this directory. Floor drills on that node are `piecewise.md`. Parameter drills are `algebra.md`.

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

## Elementary cousins

These are substitutions, not the named Gaussian.

Unit 11 stores \(\int_0^1 x e^{-x^2}\,dx=(1-e^{-1})/2\) as `U11-D01`, with \(u=x^2\). The same integrand on \([-1,1]\) is odd, so `U11-D02` is 0. \(\int_0^{\infty} e^{-x}\,dx=1\) is `U11-D04`. \(\int_0^{\infty} x e^{-x}\,dx=1\) is `U11-D08`, which is \(J_1\) from unit 14.

On \([0,\infty)\),

\[
\int_0^{\infty} e^{-2x}\,dx=\frac12, \qquad \int_0^{\infty} x e^{-x^2}\,dx=\frac12.
\]

The second is unit 30's `U30-D02`. The first is the exponential integral at \(a=2\).

## The named Gaussian

Units 11 and 30 treat

\[
\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt{\pi}
\]

as known. Unit 11 stores it as `U11-D03`. Evenness gives the half-line

\[
\int_0^{\infty} e^{-x^2}\,dx=\frac{\sqrt{\pi}}{2},
\]

which unit 30 stores as `U30-D01`.

The polar sketch, optional background in unit 30, is

\[
\Bigl(\int_{-\infty}^{\infty} e^{-x^2}\,dx\Bigr)^2
=\int_0^{2\pi}\int_0^{\infty} e^{-r^2} r\,dr\,d\theta=\pi.
\]

Vector calculus is not required for Round 1. The sketch is the reason the constant is \(\sqrt{\pi}\). Quoting the stored value is enough for a drill.

## Scaling

For \(a>0\), \(u=x\sqrt{a}\) turns \(\int_0^{\infty} e^{-a x^2}\,dx\) into \(\frac12\sqrt{\pi/a}\).

On \([0,\infty)\),

\[
\int_0^{\infty} e^{-4x^2}\,dx=\frac{\sqrt{\pi}}{4}.
\]

Here \(u=2x\), so \(dx=du/2\) and the integral is half of `U30-D01`. Unit 35 stores the case \(a=2\) as `U35-D01`. Differentiating the scaled Gaussian in the parameter is unit 30's `U30-D04`, value \(\sqrt{\pi}/4\) for \(\int_0^{\infty} x^2 e^{-x^2}\,dx\). That differentiation is the Leibniz rule, taken as a limit of compact intervals. The compact statement is unit 34.

## The Dirichlet integral

Unit 30 stores

\[
\int_0^{\infty}\frac{\sin x}{x}\,dx=\frac{\pi}{2}
\]

as `U30-D05`. The unit's argument introduces \(I(a)=\int_0^{\infty} e^{-ax}(\sin x)/x\,dx\), differentiates in \(a\), and reads \(I(a)=\pi/2-\arctan a\). The limit \(a\to 0^+\) is the stored value. Teach that derivation from the unit. This card uses the stored value and scales it.

For \(b>0\), the substitution \(u=bx\) gives

\[
\int_0^{\infty}\frac{\sin(bx)}{x}\,dx=\frac{\pi}{2}.
\]

The \(b\) in the sine and the \(b\) in \(dx\) cancel against the chain rule, and the integral is again `U30-D05`. In particular \(b=3\) is the same \(\pi/2\). Unit 35 stores a scaled Dirichlet drill as `U35-D02`. Open that file for the stored limits. Past the scaling, unit 35 also has series and a logarithm of sine. Those stay in the unit. The Gaussian scale \(e^{-9x^2}\) and the Dirichlet scale at \(b=3\) are checked on `habits.md`. This card does not quote a zeta number.

## Faded step

\(\int_{-\infty}^{\infty} x e^{-x^2}\,dx\). The integrand is odd and the integral exists, so the value is 0. The half-line version is the \(1/2\) above, not 0. Say which interval you were given before you quote either number.

## Where this goes wrong

An elementary antiderivative of \(e^{-x^2}\) was invented. The elementary cases are the ones with an extra factor of \(x\), or a plain \(e^{-ax}\).

The full-line value \(\sqrt{\pi}\) was used on \([0,\infty)\). The half-line is half of that, because the integrand is even.

A parameter derivative was taken under an infinite integral with no limit from a compact interval. Unit 34 states the compact case. Unit 30 takes the limit after that.

\((\sin x)/x\) was integrated by finding an antiderivative in elementary functions. Quote `U30-D05`, then substitute.

## On a miss

Teach this file. A cousin with an extra \(x\) opens unit 11. The named values open unit 30. Set `U11-D01` while `gaussian-integrals` is learning. Set `U30-D01` or `U30-D05` only after the elementary cousins are solid. Leave the catalog ids as they stand. A correct quote of \(\sqrt{\pi}\) on the wrong interval still needs the interval named.
