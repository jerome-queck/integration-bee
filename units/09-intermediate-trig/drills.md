# Unit 09 — drill feed (CLI)

Machine JSON: `../../verify/drills_unit9.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U09-D01 | intermediate-trig | yang:1.15 | definite | sin(x)**2 | [0, 'pi'] | pi/2 | \pi/2 |
| U09-D02 | intermediate-trig | yang:1.15 | definite | cos(x)**2 | [0, 'pi/2'] | pi/4 | \pi/4 |
| U09-D03 | intermediate-trig | yang:1.15 | definite | sin(x)*cos(x)**3 | [0, 'pi/2'] | 1/4 | 1/4 |
| U09-D04 | intermediate-trig | yang:1.15 | definite | tan(x)**2 | [0, 'pi/4'] | 1-pi/4 | 1-\pi/4 |
| U09-D05 | intermediate-trig-sub | yang:1.16 | definite | 1/sqrt(x**2+1) | [0, 1] | log(1+sqrt(2)) | \ln(1+\sqrt{2}) |
| U09-D06 | intermediate-trig-sub | yang:1.16 | definite | sqrt(x**2+1) | [0, 1] | log(1+sqrt(2))/2 + sqrt(2)/2 | \frac12\ln(1+\sqrt{2})+\frac{\sqrt{2}}{2} |
| U09-D07 | intermediate-trig | yang:1.15 | definite | sin(x)**3 | [0, 'pi/2'] | 2/3 | 2/3 |
| U09-D08 | intermediate-trig-sub | yang:1.16 | definite | 1/(x**2+1) | [0, 'sqrt(3)'] | pi/3 | \pi/3 |
