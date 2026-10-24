# Unit 13 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit13.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U13-D01 | forced-u-sub | yang:2.3 | indefinite | `exp(sqrt(x))` |  | `2*exp(sqrt(x))*(sqrt(x)-1)` | $2e^{\sqrt{x}}(\sqrt{x}-1)+C$ |
| U13-D02 | forced-u-sub | yang:2.3 | indefinite | `sin(log(x))` |  | `x*(sin(log(x))-cos(log(x)))/2` | $\dfrac{x}{2}(\sin\ln x-\cos\ln x)+C$ |
| U13-D03 | forced-u-sub | yang:2.3 | definite | `1/(1+sqrt(x))**2` | [0, 1] | `-1 + 2*log(2)` | $2\ln 2-1$ |
| U13-D04 | forced-u-sub | yang:2.3 | indefinite | `cos(sqrt(x))` |  | `2*(sqrt(x)*sin(sqrt(x))+cos(sqrt(x)))` | $2(\sqrt{x}\sin\sqrt{x}+\cos\sqrt{x})+C$ |
| U13-D05 | forced-u-sub | yang:2.3 | indefinite | `sin(sqrt(x))` |  | `2*(sin(sqrt(x))-sqrt(x)*cos(sqrt(x)))` | $2(\sin\sqrt{x}-\sqrt{x}\cos\sqrt{x})+C$ |
| U13-D06 | forced-u-sub | yang:2.3 | definite | `exp(sqrt(x))` | [0, 4] | `2+2*exp(2)` | $2+2e^{2}$ |
| U13-D07 | forced-u-sub | yang:2.3 | indefinite | `cos(log(x))` |  | `x*(sin(log(x))+cos(log(x)))/2` | $\dfrac{x}{2}(\sin\ln x+\cos\ln x)+C$ |
| U13-D08 | forced-u-sub | yang:2.3 | definite | `1/(1+sqrt(x))` | [0, 1] | `2-2*log(2)` | $2-2\ln 2$ |
