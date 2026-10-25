# Unit 20 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit20.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U20-D01 | wallis | yang:3.3 | definite | `cos(x)**4` | [0, pi/2] | `3*pi/16` | $\frac{3 \pi}{16}$ |
| U20-D02 | wallis | yang:3.3 | definite | `sin(x)**2*cos(x)**2` | [0, pi/2] | `pi/16` | $\frac{\pi}{16}$ |
| U20-D03 | wallis | yang:3.3 | definite | `(1+sin(x))**3` | [0, pi/2] | `Rational(11,3)+5*pi/4` | $\frac{11}{3} + \frac{5 \pi}{4}$ |
| U20-D04 | wallis | yang:3.3 | definite | `sin(x)**5` | [0, pi/2] | `Rational(8,15)` | $\frac{8}{15}$ |
| U20-D05 | wallis | yang:3.3 | definite | `cos(x)**6` | [0, pi/2] | `5*pi/32` | $\frac{5 \pi}{32}$ |
| U20-D06 | wallis | yang:3.3 | definite | `sin(x)**3*cos(x)**2` | [0, pi/2] | `Rational(2,15)` | $\frac{2}{15}$ |
| U20-D07 | wallis | yang:3.3 | definite | `sin(x)**4` | [0, pi/2] | `3*pi/16` | $\frac{3 \pi}{16}$ |
| U20-D08 | wallis | yang:3.3 | definite | `cos(x)**3` | [0, pi/2] | `Rational(2,3)` | $\frac{2}{3}$ |

## Speed unrolls

`teaching.tex` has three timed unrolls. They are not new ids.

| Unroll | Clock | Check |
|---|---|---|
| even line \(I_0,I_2,I_4,I_6\) | 90s | `U20-D01`, `U20-D07`, `U20-D05` |
| odd line \(I_1,I_3,I_5\) | 60s | `U20-D08`, `U20-D04` |
| alternating \(I_2\), \(I_3\) | 90s | `U15-D11` for \(I_3\) |

`U20-D06` stays a substitution. Its stored value is in the table above.
