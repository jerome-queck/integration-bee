# Unit 32 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit32.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U32-D01 | taylor-series | yang:6.2 | definite | `1/(1+x)` | [0, 1] | `log(2)` | $\log{\left(2 \right)}$ |
| U32-D02 | taylor-series | yang:6.2 | definite | `1-x**2+x**4/2-x**6/6` | [0, 1] | `1-Rational(1,3)+Rational(1,10)-Rational(1,42)` | $\frac{26}{35}$ |
| U32-D03 | taylor-series | yang:6.2 | indefinite | `x*exp(x**2)` |  | `exp(x**2)/2` | $\frac{e^{x^{2}}}{2}+C$ |
| U32-D04 | taylor-series | yang:6.2 | definite | `x**3` | [0, 1] | `Rational(1,4)` | $\frac{1}{4}$ |
| U32-D05 | complexifying | yang:6.3 | definite | `exp(-x)*cos(x)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
| U32-D06 | complexifying | yang:6.3 | definite | `exp(-x)*sin(x)` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
| U32-D07 | complexifying | yang:6.3 | indefinite | `exp(x)*cos(x)` |  | `exp(x)*(cos(x)+sin(x))/2` | $\frac{\left(\sin{\left(x \right)} + \cos{\left(x \right)}\right) e^{x}}{2}+C$ |
| U32-D08 | complexifying | yang:6.3 | indefinite | `exp(x)*sin(x)` |  | `exp(x)*(sin(x)-cos(x))/2` | $\frac{\left(\sin{\left(x \right)} - \cos{\left(x \right)}\right) e^{x}}{2}+C$ |
