# Unit 15 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit15.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U15-D01 | parts | yang:2.5 | definite | `x*log(x+1)` | [0, 1] | `1/4` | $1/4$ |
| U15-D02 | parts | yang:2.5 | indefinite | `exp(x)*sin(x)` |  | `exp(x)*(sin(x)-cos(x))/2` | $\dfrac{e^{x}}{2}(\sin x-\cos x)+C$ |
| U15-D03 | parts | yang:2.5 | definite | `exp(x)*sin(x)` | [0, 'pi'] | `(1+exp(pi))/2` | $\dfrac{1+e^{\pi}}{2}$ |
| U15-D04 | parts | yang:2.5 | definite | `x*cos(x)` | [0, 'pi/2'] | `-1+pi/2` | $\pi/2-1$ |
| U15-D05 | parts | yang:2.5 | definite | `log(x)/x**2` | [1, 'E'] | `1-2*exp(-1)` | $1-\dfrac{2}{e}$ |
| U15-D06 | parts | yang:2.5 | indefinite | `log(x)**2 / x**3` |  | `-log(x)**2/(2*x**2) - log(x)/(2*x**2) - 1/(4*x**2)` | $-\dfrac{(\ln x)^{2}}{2x^{2}}-\dfrac{\ln x}{2x^{2}}-\dfrac{1}{4x^{2}}+C$ |
| U15-D07 | parts | yang:2.5 | definite | `atan(x)/x**2` | [1, 'oo'] | `log(2)/2 + pi/4` | $\dfrac{\ln 2}{2}+\dfrac{\pi}{4}$ |
| U15-D08 | parts | yang:2.5 | indefinite | `x*asin(x)/sqrt(1-x**2)` |  | `x - sqrt(1-x**2)*asin(x)` | $x-\sqrt{1-x^{2}}\arcsin x+C$ |
| U15-D09 | parts | yang:2.5 | definite | `x**5*log(x)` | [0, 1] | `-Rational(1,36)` | $-1/36$ |
| U15-D10 | parts | yang:2.5 | definite | `x**6*log(x)` | [0, 1] | `-Rational(1,49)` | $-1/49$ |
| U15-D11 | parts | yang:2.5 | definite | `x**3/(1+x)` | [0, 1] | `Rational(5,6)-log(2)` | $5/6-\ln 2$ |
