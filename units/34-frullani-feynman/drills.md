# Unit 34 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit34.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U34-D01 | frullani | yang:6.6 | definite | `(exp(-x)-exp(-2*x))/x` | [0, oo] | `log(2)` | $\log{\left(2 \right)}$ |
| U34-D02 | frullani | yang:6.6 | definite | `(exp(-x)-exp(-3*x))/x` | [0, oo] | `log(3)` | $\log{\left(3 \right)}$ |
| U34-D03 | frullani | yang:6.6 | definite | `(cos(x)-cos(2*x))/x` | [0, oo] | `log(2)` | $\log{\left(2 \right)}$ |
| U34-D04 | feynman | yang:6.7 | definite | `(x**2-1)/log(x)` | [0, 1] | `log(3)` | $\log{\left(3 \right)}$ |
| U34-D05 | feynman | yang:6.7 | definite | `x**2*log(x)` | [0, 1] | `-Rational(1,9)` | $- \frac{1}{9}$ |
| U34-D06 | feynman | yang:6.7 | definite | `exp(-x)*sin(x)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
| U34-D07 | feynman | yang:6.7 | definite | `log(1+x)/(1+x)` | [0, 1] | `log(2)**2/2` | $\frac{\log{\left(2 \right)}^{2}}{2}$ |
| U34-D08 | feynman | yang:6.7 | definite | `x*exp(-x)` | [0, oo] | `1` | $1$ |
