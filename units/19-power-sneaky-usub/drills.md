# Unit 19 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit19.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U19-D01 | power-substitution | yang:3.1 | definite | `1/(1+sqrt(x))` | [0, 1] | `2-2*log(2)` | $2 - 2 \log{\left(2 \right)}$ |
| U19-D02 | power-substitution | yang:3.1 | definite | `1/(1+x**(Rational(1,3)))` | [0, 1] | `-Rational(3,2)+log(8)` | $- \frac{3}{2} + \log{\left(8 \right)}$ |
| U19-D03 | power-substitution | yang:3.1 | definite | `sqrt(x)/(1+sqrt(x))` | [0, 1] | `-1+log(4)` | $-1 + \log{\left(4 \right)}$ |
| U19-D04 | power-substitution | yang:3.1 | definite | `1/(sqrt(x)+x**(Rational(1,3)))` | [1, 64] | `11+log(64/729)` | $\log{\left(\frac{64}{729} \right)} + 11$ |
| U19-D05 | sneaky-u-sub | yang:3.2 | indefinite | `1/((2*x+1)*sqrt(x**2+x))` |  | `atan(2*sqrt(x**2+x))` | $\operatorname{atan}{\left(2 \sqrt{x^{2} + x} \right)}+C$ |
| U19-D06 | sneaky-u-sub | yang:3.2 | definite | `((x-1)/(x+1))**3/(x+1)` | [0, 1] | `-Rational(5,6)+log(2)` | $- \frac{5}{6} + \log{\left(2 \right)}$ |
| U19-D07 | sneaky-u-sub | yang:3.2 | definite | `sqrt((2-x)/(x-1))` | [1, 2] | `pi/2` | $\frac{\pi}{2}$ |
| U19-D08 | sneaky-u-sub | yang:3.2 | definite | `1/(1+x**2)` | [0, oo] | `pi/2` | $\frac{\pi}{2}$ |
