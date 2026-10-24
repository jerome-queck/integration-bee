# Unit 28 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit28.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U28-D01 | semi-parts | yang:5.1 | indefinite | `x*exp(x)` |  | `exp(x)*(x-1)` | $\left(x - 1\right) e^{x}+C$ |
| U28-D02 | semi-parts | yang:5.1 | indefinite | `x*sin(x)` |  | `-x*cos(x)+sin(x)` | $- x \cos{\left(x \right)} + \sin{\left(x \right)}+C$ |
| U28-D03 | semi-parts | yang:5.1 | indefinite | `x*cos(x)` |  | `x*sin(x)+cos(x)` | $x \sin{\left(x \right)} + \cos{\left(x \right)}+C$ |
| U28-D04 | semi-parts | yang:5.1 | indefinite | `x*log(x)` |  | `x**2*log(x)/2-x**2/4` | $\frac{x^{2} \log{\left(x \right)}}{2} - \frac{x^{2}}{4}+C$ |
| U28-D05 | semi-parts | yang:5.1 | definite | `exp(x)*sin(x)` | [0, pi] | `(1+exp(pi))/2` | $\frac{1}{2} + \frac{e^{\pi}}{2}$ |
| U28-D06 | semi-parts | yang:5.1 | indefinite | `log(x)` |  | `x*log(x)-x` | $x \log{\left(x \right)} - x+C$ |
| U28-D07 | semi-parts | yang:5.1 | definite | `x*exp(x)` | [0, 1] | `1` | $1$ |
| U28-D08 | semi-parts | yang:5.1 | indefinite | `x**2*sin(x)` |  | `-x**2*cos(x)+2*x*sin(x)+2*cos(x)` | $- x^{2} \cos{\left(x \right)} + 2 x \sin{\left(x \right)} + 2 \cos{\left(x \right)}+C$ |
