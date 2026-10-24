# Unit 21 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit21.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U21-D01 | advanced-trig-substitution | yang:3.4 | definite | `asin(2*x/(1+x**2))/(1+x**2)` | [0, 1] | `pi**2/16` | $\frac{\pi^{2}}{16}$ |
| U21-D02 | advanced-trig-substitution | yang:3.4 | definite | `asin(sqrt(x/(x+1)))` | [0, 1] | `-1+pi/2` | $-1 + \frac{\pi}{2}$ |
| U21-D03 | advanced-trig-substitution | yang:3.4 | definite | `sqrt(x**2-1)/x` | [1, sqrt(2)] | `1-pi/4` | $1 - \frac{\pi}{4}$ |
| U21-D04 | advanced-trig-substitution | yang:3.4 | definite | `atan(sqrt((1-x)/(1+x)))` | [0, 1] | `Rational(1,2)` | $\frac{1}{2}$ |
| U21-D05 | advanced-trig-substitution | yang:3.4 | indefinite | `1/sqrt(x**2+1)` |  | `log(x+sqrt(x**2+1))` | $\log{\left(x + \sqrt{x^{2} + 1} \right)}+C$ |
| U21-D06 | advanced-trig-substitution | yang:3.4 | definite | `sqrt(x**2-1)/x**2` | [1, sqrt(2)] | `-sqrt(2)/2+log(1+sqrt(2))` | $- \frac{\sqrt{2}}{2} + \log{\left(1 + \sqrt{2} \right)}$ |
| U21-D07 | advanced-trig-substitution | yang:3.4 | definite | `sqrt(x**2-1)` | [1, sqrt(2)] | `-log(1+sqrt(2))/2+sqrt(2)/2` | $- \frac{\log{\left(1 + \sqrt{2} \right)}}{2} + \frac{\sqrt{2}}{2}$ |
| U21-D08 | advanced-trig-substitution | yang:3.4 | definite | `x**2/sqrt(1-x**2)` | [0, 1] | `pi/4` | $\frac{\pi}{4}$ |
