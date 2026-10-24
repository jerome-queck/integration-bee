# Unit 31 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit31.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U31-D01 | inverse-jailbreaking | yang:6.1 | definite | `asin(x)` | [0, 1] | `-1+pi/2` | $-1 + \frac{\pi}{2}$ |
| U31-D02 | inverse-jailbreaking | yang:6.1 | definite | `atan(x)` | [0, 1] | `pi/4-log(2)/2` | $- \frac{\log{\left(2 \right)}}{2} + \frac{\pi}{4}$ |
| U31-D03 | inverse-jailbreaking | yang:6.1 | definite | `acos(x)` | [0, 1] | `1` | $1$ |
| U31-D04 | inverse-jailbreaking | yang:6.1 | indefinite | `atan(x)` |  | `x*atan(x)-log(1+x**2)/2` | $x \operatorname{atan}{\left(x \right)} - \frac{\log{\left(x^{2} + 1 \right)}}{2}+C$ |
| U31-D05 | inverse-jailbreaking | yang:6.1 | definite | `asin(x)` | [0, Rational(1,2)] | `-1+pi/12+sqrt(3)/2` | $-1 + \frac{\pi}{12} + \frac{\sqrt{3}}{2}$ |
| U31-D06 | inverse-jailbreaking | yang:6.1 | indefinite | `x*atan(x)` |  | `(x**2+1)*atan(x)/2-x/2` | $- \frac{x}{2} + \frac{\left(x^{2} + 1\right) \operatorname{atan}{\left(x \right)}}{2}+C$ |
| U31-D07 | inverse-jailbreaking | yang:6.1 | definite | `x*asin(x)` | [0, 1] | `pi/8` | $\frac{\pi}{8}$ |
| U31-D08 | inverse-jailbreaking | yang:6.1 | indefinite | `asin(x)` |  | `x*asin(x)+sqrt(1-x**2)` | $x \operatorname{asin}{\left(x \right)} + \sqrt{1 - x^{2}}+C$ |
