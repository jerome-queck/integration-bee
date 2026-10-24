# Unit 05 — drill feed (CLI)

Canonical: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit5.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U05-D01 | partial-fractions | yang:1.8 | definite | 1/((x+1)*(x+2)) | [0, 1] | log(4/3) | \ln(4/3) |
| U05-D02 | partial-fractions | yang:1.8 | definite | 1/(x*(x+1)) | [1, 2] | log(4/3) | \ln(4/3) |
| U05-D03 | partial-fractions | yang:1.8 | definite | 1/((x-1)*(x-2)) | [3, 4] | log(4/3) | \ln(4/3) |
| U05-D04 | partial-fractions | yang:1.8 | indefinite | 1/(x**2-1) |  | log(x-1)/2 - log(x+1)/2 | \frac12\ln\left|\frac{x-1}{x+1}\right|+C |
| U05-D05 | partial-fractions | yang:1.8 | definite | (3*x+4)/((x+1)*(x+2)) | [0, 1] | log(9/2) | \ln(9/2) |
| U05-D06 | partial-fractions | yang:1.8 | definite | (x+5)/((x+1)*(x+2)) | [0, 1] | log(128/27) | \ln(128/27) |
