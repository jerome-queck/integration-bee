# Unit 27 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit27.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U27-D01 | reverse-quotient | yang:4.6 | indefinite | `(x*cos(x)-sin(x))/x**2` |  | `sin(x)/x` | $\frac{\sin{\left(x \right)}}{x}+C$ |
| U27-D02 | reverse-quotient | yang:4.6 | indefinite | `exp(x)*(x-1)/x**2` |  | `exp(x)/x` | $\frac{e^{x}}{x}+C$ |
| U27-D03 | reverse-quotient | yang:4.6 | indefinite | `(1-log(x))/x**2` |  | `log(x)/x` | $\frac{\log{\left(x \right)}}{x}+C$ |
| U27-D04 | reverse-quotient | yang:4.6 | indefinite | `(sin(x)-x*cos(x))/sin(x)**2` |  | `x/sin(x)` | $\frac{x}{\sin{\left(x \right)}}+C$ |
| U27-D05 | reverse-quotient | yang:4.6 | indefinite | `(log(x)-1)/x**2` |  | `-log(x)/x` | $- \frac{\log{\left(x \right)}}{x}+C$ |
| U27-D06 | reverse-quotient | yang:4.6 | indefinite | `((x+1)*exp(x)-exp(x))/(x+1)**2` |  | `exp(x)/(x+1)` | $\frac{e^{x}}{x + 1}+C$ |
| U27-D07 | reverse-quotient | yang:4.6 | indefinite | `(x*sec(x)**2-tan(x))/x**2` |  | `tan(x)/x` | $\frac{\tan{\left(x \right)}}{x}+C$ |
| U27-D08 | reverse-quotient | yang:4.6 | indefinite | `(x**2*cos(x)-2*x*sin(x))/x**4` |  | `sin(x)/x**2` | $\frac{\sin{\left(x \right)}}{x^{2}}+C$ |
