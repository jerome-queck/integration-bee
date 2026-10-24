# Unit 25 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit25.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U25-D01 | advanced-kings-queens | yang:4.4 | definite | `sin(x)/(sin(x)+cos(x))` | [0, pi/2] | `pi/4` | $\frac{\pi}{4}$ |
| U25-D02 | advanced-kings-queens | yang:4.4 | definite | `cos(x)/(sin(x)+cos(x))` | [0, pi/2] | `pi/4` | $\frac{\pi}{4}$ |
| U25-D03 | advanced-kings-queens | yang:4.4 | definite | `exp(x)/(exp(x)+exp(1-x))` | [0, 1] | `Rational(1,2)` | $\frac{1}{2}$ |
| U25-D04 | advanced-kings-queens | yang:4.4 | definite | `1/(1+tan(x))` | [0, pi/4] | `pi/8+log(2)/4` | $\frac{\log{\left(2 \right)}}{4} + \frac{\pi}{8}$ |
| U25-D05 | advanced-kings-queens | yang:4.4 | definite | `sin(x)**3/(sin(x)**3+cos(x)**3)` | [0, pi/2] | `pi/4` | $\frac{\pi}{4}$ |
| U25-D06 | advanced-kings-queens | yang:4.4 | definite | `x/(1+sin(x))` | [0, pi] | `pi` | $\pi$ |
| U25-D07 | advanced-kings-queens | yang:4.4 | definite | `x/(1+x)` | [0, 1] | `1-log(2)` | $1 - \log{\left(2 \right)}$ |
| U25-D08 | advanced-kings-queens | yang:4.4 | definite | `sin(x)*cos(x)` | [0, pi/2] | `Rational(1,2)` | $\frac{1}{2}$ |
