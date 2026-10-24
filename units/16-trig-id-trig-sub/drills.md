# Unit 16 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit16.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U16-D01 | trig-identities | yang:2.6 | definite | `sin(x)**2 * cos(x)**2` | [0, 'pi/2'] | `pi/16` | $\pi/16$ |
| U16-D02 | trig-identities | yang:2.6 | indefinite | `sin(x)**3` |  | `cos(x)**3/3 - cos(x)` | $-\cos x+\dfrac{\cos^{3}x}{3}+C$ |
| U16-D03 | trig-identities | yang:2.6 | definite | `sin(x)**2` | [0, 'pi'] | `pi/2` | $\pi/2$ |
| U16-D04 | trig-identities | yang:2.6 | definite | `1/(1+cos(x))` | [0, 'pi/2'] | `1` | $1$ |
| U16-D05 | intermediate-trig-sub | yang:2.7 | definite | `sqrt(4-x**2)` | [0, 2] | `pi` | $\pi$ |
| U16-D06 | intermediate-trig-sub | yang:2.7 | definite | `x**2 / sqrt(1-x**2)` | [0, 1] | `pi/4` | $\pi/4$ |
| U16-D07 | intermediate-trig-sub | yang:2.7 | indefinite | `1/(x**2+4)` |  | `atan(x/2)/2` | $\dfrac{1}{2}\arctan(x/2)+C$ |
| U16-D08 | intermediate-trig-sub | yang:2.7 | definite | `1/sqrt(x**2+1)` | [0, 1] | `log(1+sqrt(2))` | $\ln(1+\sqrt{2})$ |
