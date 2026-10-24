# Unit 30 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit30.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U30-D01 | advanced-gaussian | yang:5.3 | definite | `exp(-x**2)` | [0, oo] | `sqrt(pi)/2` | $\frac{\sqrt{\pi}}{2}$ |
| U30-D02 | advanced-gaussian | yang:5.3 | definite | `x*exp(-x**2)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
| U30-D03 | advanced-gaussian | yang:5.3 | definite | `exp(-x**2)` | [-oo, oo] | `sqrt(pi)` | $\sqrt{\pi}$ |
| U30-D04 | advanced-gaussian | yang:5.3 | definite | `exp(-x**2)*x**2` | [0, oo] | `sqrt(pi)/4` | $\frac{\sqrt{\pi}}{4}$ |
| U30-D05 | dirichlet | yang:5.4 | definite | `sin(x)/x` | [0, oo] | `pi/2` | $\frac{\pi}{2}$ |
| U30-D06 | dirichlet | yang:5.4 | definite | `sin(x)**2/x**2` | [0, oo] | `pi/2` | $\frac{\pi}{2}$ |
| U30-D07 | dirichlet | yang:5.4 | definite | `exp(-x)*sin(x)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
| U30-D08 | dirichlet | yang:5.4 | definite | `exp(-x)*cos(x)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
