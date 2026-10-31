# Unit 01 — drill feed (CLI)

Canonical prose/PDF: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit1.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U01-D01 | u-sub | yang:1.2 | definite | 2*x/(x**2+1) | [0,1] | log(2) | \ln 2 |
| U01-D02 | u-sub | yang:1.2 | definite | sin(x)*cos(x) | [0,pi/2] | 1/2 | 1/2 |
| U01-D03 | u-sub | yang:1.2 | definite | x*exp(x**2) | [0,1] | (exp(1)-1)/2 | (e-1)/2 |
| U01-D04 | linear-sub | yang:1.2 | definite | 1/(2*x+1) | [0,1] | log(3)/2 | (\ln 3)/2 |
| U01-D05 | u-sub | yang:1.2 | definite | sin(x)**2*cos(x) | [0,pi/2] | 1/3 | 1/3 |
| U01-D06 | du/u | yang:1.2;yang:1.10 | indefinite | (2*x+3)/(x**2+3*x+2) | | log(Abs(x**2+3*x+2)) | \ln\|x^2+3x+2\|+C |
| U01-D07 | odd-even | yang:1.1 | definite | x**3 | [-1,1] | 0 | 0 |
| U01-D08 | standard-arctan | yang:1.1 | definite | 1/(1+x**2) | [0,1] | pi/4 | \pi/4 |
