# Unit 08 — drill feed (CLI)

Machine JSON: `../../verify/drills_unit8.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U08-D01 | basic-series | yang:1.14 | definite | 1+x+x**2+x**3 | [0, 1] | 25/12 | 25/12 |
| U08-D02 | basic-series | yang:1.14 | definite | 1/(1-x) | [0, '1/2'] | log(2) | \ln 2 |
| U08-D03 | basic-series | yang:1.14 | definite | x**5 | [0, 1] | 1/6 | 1/6 |
| U08-D04 | basic-series | yang:1.14 | definite | 1-x+x**2 | [0, 1] | 5/6 | 5/6 |
| U08-D05 | basic-series | yang:1.14 | definite | 1/(1+x) | [0, '1/3'] | log(4/3) | \ln(4/3) |
| U08-D06 | basic-series | yang:1.14 | definite | x**2*(1+x) | [0, 1] | 7/12 | 7/12 |
