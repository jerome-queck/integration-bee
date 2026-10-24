# Unit 33 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit33.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U33-D01 | ninja-substitution | yang:6.4 | definite | `x/(1+x**2)` | [0, 1] | `log(2)/2` | $\frac{\log{\left(2 \right)}}{2}$ |
| U33-D02 | ninja-substitution | yang:6.4 | definite | `1/(1+sin(x)**2)` | [0, pi/2] | `pi/(2*sqrt(2))` | $\frac{\sqrt{2} \pi}{4}$ |
| U33-D03 | ninja-substitution | yang:6.4 | indefinite | `1/(x*sqrt(x**2-1))` |  | `atan(sqrt(x**2-1))` | $\operatorname{atan}{\left(\sqrt{x^{2} - 1} \right)}+C$ |
| U33-D04 | ninja-substitution | yang:6.4 | definite | `log(1+x)/(1+x**2)` | [0, 1] | `pi*log(2)/8` | $\frac{\pi \log{\left(2 \right)}}{8}$ |
| U33-D05 | inversion | yang:6.5 | definite | `1/(1+x**2)` | [0, oo] | `pi/2` | $\frac{\pi}{2}$ |
| U33-D06 | inversion | yang:6.5 | definite | `1/((1+x**2)*(1+x))` | [0, oo] | `pi/4` | $\frac{\pi}{4}$ |
| U33-D07 | inversion | yang:6.5 | definite | `log(x)/(1+x**2)` | [0, oo] | `0` | $0$ |
| U33-D08 | inversion | yang:6.5 | definite | `x/(1+x**2)**2` | [0, oo] | `Rational(1,2)` | $\frac{1}{2}$ |
