# Unit 06 — drill feed (CLI)

Canonical: `teaching.tex`, `drills.tex`, `solutions.tex`.
Machine JSON: `../../verify/drills_unit6.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U06-D01 | intermediate-u-sub | yang:1.11 | definite | x**3 * exp(x**4) | [0, 1] | (exp(1)-1)/4 | (e-1)/4 |
| U06-D02 | intermediate-u-sub | yang:1.11 | definite | sin(x)*cos(x)*exp(sin(x)**2) | [0, 'pi/2'] | (exp(1)-1)/2 | (e-1)/2 |
| U06-D03 | intermediate-u-sub | yang:1.11 | definite | 1/(x*log(x)) | ['E', 'E**2'] | log(2) | \ln 2 |
| U06-D04 | intermediate-u-sub | yang:1.11 | definite | cos(x)/(sin(x)+2) | [0, 'pi/2'] | log(3)-log(2) | \ln(3/2) |
| U06-D05 | intermediate-u-sub | yang:1.11 | definite | 2*x/(x**2+1)**2 | [0, 1] | 1/2 | 1/2 |
| U06-D06 | intermediate-u-sub | yang:1.11 | definite | log(x)/x | [1, 'E'] | 1/2 | 1/2 |
| U06-D07 | intermediate-u-sub | yang:1.11 | definite | tan(x)*sec(x)**2 | [0, 'pi/4'] | 1/2 | 1/2 |
| U06-D08 | intermediate-u-sub | yang:1.11 | definite | x*sqrt(1+x**2) | [0, 1] | (2*sqrt(2)-1)/3 | (2\sqrt{2}-1)/3 |
