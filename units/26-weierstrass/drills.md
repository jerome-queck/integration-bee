# Unit 26 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit26.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U26-D01 | weierstrass | yang:4.5 | definite | `1/(1+sin(x))` | [0, pi/2] | `1` | $1$ |
| U26-D02 | weierstrass | yang:4.5 | definite | `1/(2+cos(x))` | [0, pi] | `pi/sqrt(3)` | $\frac{\sqrt{3} \pi}{3}$ |
| U26-D03 | weierstrass | yang:4.5 | definite | `1/(3+2*cos(x))` | [0, pi] | `pi/sqrt(5)` | $\frac{\sqrt{5} \pi}{5}$ |
| U26-D04 | weierstrass | yang:4.5 | indefinite | `1/(1+sin(x))` |  | `tan(x)-sec(x)` | $\tan{\left(x \right)} - \sec{\left(x \right)}+C$ |
| U26-D05 | weierstrass | yang:4.5 | definite | `1/(5+4*cos(x))` | [0, pi] | `pi/3` | $\frac{\pi}{3}$ |
| U26-D06 | weierstrass | yang:4.5 | definite | `1/(1+cos(x)+sin(x))` | [0, pi/2] | `log(2)` | $\log{\left(2 \right)}$ |
| U26-D07 | weierstrass | yang:4.5 | definite | `1/(2+cos(x))` | [0, pi/3] | `2*sqrt(3)*atan(Rational(1,3))/3` | $\frac{2 \sqrt{3} \operatorname{atan}{\left(\frac{1}{3} \right)}}{3}$ |
| U26-D08 | weierstrass | yang:4.5 | definite | `1/(2+sin(x))` | [0, pi/2] | `sqrt(3)*pi/9` | $\frac{\sqrt{3} \pi}{9}$ |
