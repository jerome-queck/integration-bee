# Unit 18 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit18.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U18-D01 | sneaky-symmetry | yang:2.9 | definite | `(x-1)*(x-2)*(x-3)*(x-4)*(x-5)` | [2, 4] | `0` | $0$ |
| U18-D02 | sneaky-symmetry | yang:2.9 | definite | `x*(x**2-1)*(x**2-4)` | [-1, 1] | `0` | $0$ |
| U18-D03 | sneaky-symmetry | yang:2.9 | definite | `x**3 * cos(x)` | ['-pi/2', 'pi/2'] | `0` | $0$ |
| U18-D04 | sneaky-symmetry | yang:2.9 | definite | `atan(x)**2 / (1+x**2)` | [-1, 1] | `pi**3/96` | $\pi^{3}/96$ |
| U18-D05 | sneaky-product-rule | yang:2.10 | indefinite | `sec(x)**3 + sec(x)*tan(x)**2` |  | `sec(x)*tan(x)` | $\sec x\tan x+C$ |
| U18-D06 | sneaky-product-rule | yang:2.10 | indefinite | `exp(x)*(2*sqrt(x)+1/sqrt(x))` |  | `2*sqrt(x)*exp(x)` | $2\sqrt{x}\,e^{x}+C$ |
| U18-D07 | sneaky-product-rule | yang:2.10 | indefinite | `exp(x)*(sin(x)-cos(x))` |  | `-exp(x)*cos(x)` | $-e^{x}\cos x+C$ |
| U18-D08 | sneaky-product-rule | yang:2.10 | indefinite | `sin(log(x))+cos(log(x))` |  | `x*sin(log(x))` | $x\sin(\ln x)+C$ |
