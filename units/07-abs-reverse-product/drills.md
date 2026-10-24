# Unit 07 — drill feed (CLI)

Machine JSON: `../../verify/drills_unit7.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U07-D01 | absolute-value | yang:1.12 | definite | Abs(x) | [-1, 1] | 1 | 1 |
| U07-D02 | absolute-value | yang:1.12 | definite | Abs(x-1) | [0, 2] | 1 | 1 |
| U07-D03 | absolute-value | yang:1.12 | definite | Abs(sin(x)) | [0, 'pi'] | 2 | 2 |
| U07-D04 | reverse-product | yang:1.13 | definite | sin(x)+x*cos(x) | [0, 'pi/2'] | pi/2 | \pi/2 |
| U07-D05 | reverse-product | yang:1.13 | definite | exp(x)*(sin(x)+cos(x)) | [0, 'pi/2'] | exp(pi/2) | e^{\pi/2} |
| U07-D06 | reverse-product | yang:1.13 | definite | cos(x)-x*sin(x) | [0, 'pi/2'] | 0 | 0 |
| U07-D07 | absolute-value | yang:1.12 | definite | Abs(x) | [-2, 1] | 5/2 | 5/2 |
| U07-D08 | reverse-product | yang:1.13 | definite | 2*x*cos(x**2) | [0, 1] | sin(1) | \sin 1 |
