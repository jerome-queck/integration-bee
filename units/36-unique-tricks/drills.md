# Unit 36 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit36.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U36-D01 | unique-tricks | yang:6.9 | definite | `(x-1)/log(x)` | [0, 1] | `log(2)` | $\log{\left(2 \right)}$ |
| U36-D02 | unique-tricks | yang:6.9 | definite | `log(sin(x))` | [0, pi/2] | `-pi*log(2)/2` | $- \frac{\pi \log{\left(2 \right)}}{2}$ |
| U36-D03 | unique-tricks | yang:6.9 | definite | `atan(x)/x` | [0, 1] | `Catalan` | $G$ |
| U36-D04 | unique-tricks | yang:6.9 | indefinite | `1/(x*log(x))` |  | `log(log(x))` | $\log{\left(\log{\left(x \right)} \right)}+C$ |
| U36-D05 | unique-tricks | yang:6.9 | definite | `1/(x*log(x))` | [2, 4] | `log(2)` | $\log{\left(2 \right)}$ |
| U36-D06 | unique-tricks | yang:6.9 | definite | `1/(x*log(x))` | [E, exp(E)] | `1` | $1$ |
| U36-D07 | unique-tricks | yang:6.9 | definite | `(x**2-1)/log(x)` | [0, 1] | `log(3)` | $\log{\left(3 \right)}$ |
| U36-D08 | unique-tricks | yang:6.9 | indefinite | `log(x)/x` |  | `log(x)**2/2` | $\frac{\log{\left(x \right)}^{2}}{2}+C$ |
