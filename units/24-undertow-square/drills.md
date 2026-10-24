# Unit 24 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit24.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U24-D01 | undertow | yang:4.1 | indefinite | `(2*x**3-1)/(x**4+x)` |  | `log(x**2+1/x)` | $\log{\left(x^{2} + \frac{1}{x} \right)}+C$ |
| U24-D02 | undertow | yang:4.1 | indefinite | `(4*x**5-1)/(x**5+x+1)**2` |  | `-x/(x**5+x+1)` | $- \frac{x}{x^{5} + x + 1}+C$ |
| U24-D03 | undertow | yang:4.1 | indefinite | `(exp(x)-sin(x))/(exp(x)+cos(x))` |  | `log(exp(x)+cos(x))` | $\log{\left(e^{x} + \cos{\left(x \right)} \right)}+C$ |
| U24-D04 | undertow | yang:4.1 | indefinite | `(x**2-1)/(x**3+x)` |  | `log(x+1/x)` | $\log{\left(x + \frac{1}{x} \right)}+C$ |
| U24-D05 | square-square | yang:4.2 | indefinite | `sqrt(x)+1/sqrt(x)` |  | `(2/3)*x**(Rational(3,2))+2*sqrt(x)` | $\frac{2 x^{\frac{3}{2}}}{3} + 2 \sqrt{x}+C$ |
| U24-D06 | square-square | yang:4.2 | definite | `sqrt(x)+1/sqrt(x)` | [1, 4] | `Rational(20,3)` | $\frac{20}{3}$ |
| U24-D07 | square-square | yang:4.2 | definite | `sqrt(x+2+1/x)` | [1, 4] | `Rational(20,3)` | $\frac{20}{3}$ |
| U24-D08 | square-square | yang:4.2 | definite | `sqrt(x)-1/sqrt(x)` | [1, 4] | `Rational(8,3)` | $\frac{8}{3}$ |
