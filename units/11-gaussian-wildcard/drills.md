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
