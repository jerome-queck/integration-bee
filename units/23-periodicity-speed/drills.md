# Unit 23 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit23.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U23-D01 | periodicity | yang:3.7 | definite | `sin(3*x)*sin(5*x)` | [0, 2*pi] | `0` | $0$ |
| U23-D02 | periodicity | yang:3.7 | definite | `(sin(x)+sin(2*x)+sin(3*x))**2` | [0, 2*pi] | `3*pi` | $3 \pi$ |
| U23-D03 | periodicity | yang:3.7 | definite | `sin(23*x)*sin(19*x)` | [0, pi] | `0` | $0$ |
| U23-D04 | periodicity | yang:3.7 | definite | `20*sin(x)**2` | [0, 2*pi] | `20*pi` | $20 \pi$ |
| U23-D05 | periodicity | yang:3.7 | definite | `cos(3*x)*cos(5*x)` | [0, 2*pi] | `0` | $0$ |
| U23-D06 | speed-bashing | yang:3.8 | indefinite | `x**3*exp(x)` |  | `exp(x)*(x**3-3*x**2+6*x-6)` | $\left(x^{3} - 3 x^{2} + 6 x - 6\right) e^{x}+C$ |
| U23-D07 | speed-bashing | yang:3.8 | indefinite | `sin(x)**3+cos(x)**3` |  | `-cos(x)+cos(x)**3/3+sin(x)-sin(x)**3/3` | $- \frac{\sin^{3}{\left(x \right)}}{3} + \sin{\left(x \right)} + \frac{\cos^{3}{\left(x \right)}}{3} - \cos{\left(x \right)}+C$ |
| U23-D08 | speed-bashing | yang:3.8 | indefinite | `1/x**2+1/x+1-1/(x**2+1)` |  | `-1/x+log(Abs(x))+x-atan(x)` | $x + \log{\left(x \right)} - \operatorname{atan}{\left(x \right)} - \frac{1}{x}+C$ |
