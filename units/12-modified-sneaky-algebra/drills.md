# Unit 12 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit12.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U12-D01 | modified-textbook | yang:2.1 | indefinite | `exp(x)*exp(exp(x))` |  | `exp(exp(x))` | $e^{e^{x}}+C$ |
| U12-D02 | modified-textbook | yang:2.1 | indefinite | `1/(1+exp(x))**2` |  | `x - log(exp(x) + 1) + 1/(exp(x) + 1)` | $x-\ln(1+e^{x})+\dfrac{1}{1+e^{x}}+C$ |
| U12-D03 | modified-textbook | yang:2.1 | definite | `sqrt((1-x)/(1+x))` | [0,1] | `-1 + pi/2` | $\pi/2 - 1$ |
| U12-D04 | modified-textbook | yang:2.1 | indefinite | `(1-x)/sqrt(1-x**2)` |  | `asin(x) + sqrt(1-x**2)` | $\arcsin x+\sqrt{1-x^{2}}+C$ |
| U12-D05 | sneaky-algebra | yang:2.2 | definite | `(x-4)/(sqrt(x)-2)` | [0,1] | `8/3` | $8/3$ |
| U12-D06 | sneaky-algebra | yang:2.2 | definite | `x**2 - 1` | [-1,1] | `-4/3` | $- \frac{4}{3}$ |
| U12-D07 | sneaky-algebra | yang:2.2 | definite | `(x-1)*(x-2)*(x-3)*(x-4)` | [3,4] | `-19/30` | $-19/30$ |
| U12-D08 | sneaky-algebra | yang:2.2 | indefinite | `x**2 * (x**3 + 1)**2` |  | `(x**3+1)**3 / 9` | $\dfrac{(x^{3}+1)^{3}}{9}+C$ |
