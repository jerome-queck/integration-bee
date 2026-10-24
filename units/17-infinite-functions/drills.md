# Unit 17 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit17.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U17-D01 | infinite-functions | yang:2.8 | definite | `1/(1-x)` | [0, '1/2'] | `log(2)` | $\ln 2$ |
| U17-D02 | infinite-functions | yang:2.8 | definite | `exp(-x)/(1+exp(-x))` | [0, 'oo'] | `log(2)` | $\ln 2$ |
| U17-D03 | infinite-functions | yang:2.8 | definite | `1/(1-x**2)` | [0, '1/2'] | `log(3)/2` | $\dfrac{\ln 3}{2}$ |
| U17-D04 | infinite-functions | yang:2.8 | definite | `exp(x)` | [0, 1] | `-1+E` | $e-1$ |
| U17-D05 | infinite-functions | yang:2.8 | definite | `x + x/sqrt(1-x**2)` | [0, 1] | `3/2` | $3/2$ |
| U17-D06 | infinite-functions | yang:2.8 | definite | `exp(x)-1` | [0, 1] | `E-2` | $e-2$ |
