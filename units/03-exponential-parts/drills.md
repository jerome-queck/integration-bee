# Unit 03 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit3.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U03-D01 | basic-exp | yang:1.4 | definite | exp(x) | [0, 1] | E-1 | e-1 |
| U03-D02 | basic-exp | yang:1.4 | definite | exp(2*x) | [0, 1] | (exp(2)-1)/2 | (e^2-1)/2 |
| U03-D03 | parts | yang:1.6 | definite | x*exp(x) | [0, 1] | 1 | 1 |
| U03-D04 | parts | yang:1.6 | indefinite | x*exp(x) |  | exp(x)*(x-1) | e^x(x-1)+C |
| U03-D05 | parts | yang:1.6 | definite | log(x) | [1, 'E'] | 1 | 1 |
| U03-D06 | parts | yang:1.6 | definite | exp(x)*sin(x) | [0, 'pi/2'] | (exp(pi/2)+1)/2 | (e^{\pi/2}+1)/2 |
| U03-D07 | basic-exp | yang:1.4 | definite | 2**x | [0, 1] | 1/log(2) | 1/\ln 2 |
| U03-D08 | parts | yang:1.6 | definite | x*log(x) | [1, 'E'] | (exp(2)+1)/4 | (e^2+1)/4 |
