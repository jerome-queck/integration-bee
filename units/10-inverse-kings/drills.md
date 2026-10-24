# Unit 10 — drill feed (CLI)

Machine JSON: `../../verify/drills_unit10.json`.

| id | technique | yang | kind | sympy_expr | limits | answer_sympy | answer_display |
|---|---|---|---|---|---|---|---|
| U10-D01 | inverse-functions | yang:1.17 | definite | asin(x) | [0, 1] | pi/2 - 1 | \pi/2-1 |
| U10-D02 | inverse-functions | yang:1.17 | definite | atan(x) | [0, 1] | pi/4 - log(2)/2 | \pi/4-(\ln 2)/2 |
| U10-D03 | inverse-functions | yang:1.17 | definite | acos(x) | [0, 1] | 1 | 1 |
| U10-D04 | kings-rule | yang:1.18 | definite | sin(x)/(sin(x)+cos(x)) | [0, 'pi/2'] | pi/4 | \pi/4 |
| U10-D05 | kings-rule | yang:1.18 | definite | cos(x)/(sin(x)+cos(x)) | [0, 'pi/2'] | pi/4 | \pi/4 |
| U10-D06 | kings-rule | yang:1.18 | definite | x/(1+x) | [0, 1] | 1-log(2) | 1-\ln 2 |
| U10-D07 | kings-rule | yang:1.18 | definite | sin(x)**2 | [0, 'pi/2'] | pi/4 | \pi/4 |
| U10-D08 | inverse-functions | yang:1.17 | definite | asin(x) | [0, '1/2'] | pi/12 + sqrt(3)/2 - 1 | \pi/12+\sqrt{3}/2-1 |
