# Unit 11 — drill feed (CLI)

Machine JSON: `../../verify/drills_unit11.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U11-D01 | gaussian | yang:1.19 | definite | x*exp(-x**2) | [0, 1] | (1-exp(-1))/2 | (1-e^{-1})/2 |
| U11-D02 | gaussian | yang:1.19 | definite | x*exp(-x**2) | [-1, 1] | 0 | 0 |
| U11-D03 | gaussian | yang:1.19 | definite | exp(-x**2) | ['-oo', 'oo'] | sqrt(pi) | \sqrt{\pi} |
| U11-D04 | gaussian | yang:1.19 | definite | exp(-x) | [0, 'oo'] | 1 | 1 |
| U11-D05 | wildcard | yang:1.20 | definite | 1/(1+x**2) | [-1, 1] | pi/2 | \pi/2 |
| U11-D06 | wildcard | yang:1.20 | definite | Abs(x)*exp(-Abs(x)) | [-1, 1] | 2-4*exp(-1) | 2-4e^{-1} |
| U11-D07 | wildcard | yang:1.20 | definite | sin(x)/(sin(x)+cos(x)) | [0, 'pi/2'] | pi/4 | \pi/4 |
| U11-D08 | gaussian | yang:1.19 | definite | x*exp(-x) | [0, 'oo'] | 1 | 1 |
| U11-D09 | floor | yang:1.20 | definite | `Piecewise((0, x < 1), (1, x < 2), (2, x < 3), (3, x < 4), (0, True))` | [0, 4] | 6 | 6 |
| U11-D10 | floor | yang:1.20 | definite | `Piecewise((x, x < 1), (x-1, x < 2), (x-2, x < 3), (0, True))` | [0, 3] | 3/2 | 3/2 |
| U11-D11 | floor | yang:1.20 | definite | `Piecewise((0, x < 1), (1, x < 2), (2, x < 5/2), (0, True))` | [0, 5/2] | 2 | 2 |
| U11-D12 | floor | yang:1.20 | definite | `Piecewise((-2, x < -1), (-1, x < 0), (0, True))` | [-2, 0] | -3 | -3 |
| U11-D13 | dutis | yang:1.20 | definite | `x**4*log(x)` | [0, 1] | `-Rational(1,25)` | -1/25 |
| U11-D14 | dutis | yang:1.20 | definite | `x*exp(-2*x)` | [0, oo] | `Rational(1,4)` | 1/4 |
| U11-D15 | dutis | yang:1.20 | definite | `(x**3-1)/log(x)` | [0, 1] | `log(4)` | \ln 4 |
