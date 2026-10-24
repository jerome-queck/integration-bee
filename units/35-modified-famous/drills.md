# Unit 35 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit35.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U35-D01 | modified-famous | yang:6.8 | definite | `exp(-2*x**2)` | [0, oo] | `sqrt(2)*sqrt(pi)/4` | $\frac{\sqrt{2} \sqrt{\pi}}{4}$ |
| U35-D02 | modified-famous | yang:6.8 | definite | `sin(2*x)/x` | [0, oo] | `pi/2` | $\frac{\pi}{2}$ |
| U35-D03 | modified-famous | yang:6.8 | definite | `exp(-3*x)` | [0, oo] | `Rational(1,3)` | $\frac{1}{3}$ |
| U35-D04 | modified-famous | yang:6.8 | definite | `log(x)/(1-x)` | [0, 1] | `-pi**2/6` | $- \frac{\pi^{2}}{6}$ |
| U35-D05 | modified-famous | yang:6.8 | definite | `log(x)/(1+x)` | [0, 1] | `-pi**2/12` | $- \frac{\pi^{2}}{12}$ |
| U35-D06 | modified-famous | yang:6.8 | definite | `log(sin(x))` | [0, pi/2] | `-pi*log(2)/2` | $- \frac{\pi \log{\left(2 \right)}}{2}$ |
| U35-D07 | modified-famous | yang:6.8 | definite | `(exp(-x)-exp(-2*x))/x` | [0, oo] | `log(2)` | $\log{\left(2 \right)}$ |
| U35-D08 | modified-famous | yang:6.8 | definite | `-log(x)` | [0, 1] | `1` | $1$ |
