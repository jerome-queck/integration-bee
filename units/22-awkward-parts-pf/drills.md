# Unit 22 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit22.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U22-D01 | awkward-parts | yang:3.5 | indefinite | `log(x)**2` |  | `x*log(x)**2-2*x*log(x)+2*x` | $x \log{\left(x \right)}^{2} - 2 x \log{\left(x \right)} + 2 x+C$ |
| U22-D02 | awkward-parts | yang:3.5 | indefinite | `atan(x)` |  | `x*atan(x)-log(1+x**2)/2` | $x \operatorname{atan}{\left(x \right)} - \frac{\log{\left(x^{2} + 1 \right)}}{2}+C$ |
| U22-D03 | awkward-parts | yang:3.5 | indefinite | `x**2*exp(x)` |  | `exp(x)*(x**2-2*x+2)` | $\left(x^{2} - 2 x + 2\right) e^{x}+C$ |
| U22-D04 | awkward-parts | yang:3.5 | indefinite | `asin(x)` |  | `x*asin(x)+sqrt(1-x**2)` | $x \operatorname{asin}{\left(x \right)} + \sqrt{1 - x^{2}}+C$ |
| U22-D05 | awkward-parts | yang:3.5 | indefinite | `exp(x)*sin(x)` |  | `exp(x)*(sin(x)-cos(x))/2` | $\frac{\left(\sin{\left(x \right)} - \cos{\left(x \right)}\right) e^{x}}{2}+C$ |
| U22-D06 | intermediate-partial-fractions | yang:3.6 | indefinite | `x/((x+1)*(x+2)*(x+3))` |  | `-log(x+1)/2+2*log(x+2)-3*log(x+3)/2` | $- \frac{\log{\left(x + 1 \right)}}{2} + 2 \log{\left(x + 2 \right)} - \frac{3 \log{\left(x + 3 \right)}}{2}+C$ |
| U22-D07 | intermediate-partial-fractions | yang:3.6 | indefinite | `1/(x**2*(x+1))` |  | `-1/x-log(x)+log(x+1)` | $- \log{\left(x \right)} + \log{\left(x + 1 \right)} - \frac{1}{x}+C$ |
| U22-D08 | intermediate-partial-fractions | yang:3.6 | definite | `1/(x**2*(x+1))` | [1, 2] | `Rational(1,2)+log(Rational(3,4))` | $\log{\left(\frac{3}{4} \right)} + \frac{1}{2}$ |
