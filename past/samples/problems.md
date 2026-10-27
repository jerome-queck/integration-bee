# Official sample problems Q1–Q20

Problems PDF: `sources/Integration_Competition_Sample_problems.pdf`  
Answers PDF: `sources/Integration_bee_sample_problems_answers.pdf` (Vishal Gupta)  
Solutions PDF: `sources/UK_University_integration_bee_sample_problems_solutions.pdf`  
Hints: `sources/Virtual_integration_competition_sample_hints.pdf`

Technique tags map to `syllabus-map.md` (Yang + official syllabus).  
**Answers below are cited from the answers PDF** (page reading, 2026-10-25), except SAMPLE-Q15. That printed final has the wrong arctan sign. The catalog grades the corrected antiderivative. Do not invent the others.

| Id | Sketch (from problems PDF) | Technique tags | Yang | Answers PDF (cite) | verify |
|---|---|---|---|---|---|
| SAMPLE-Q01 | ∫₀¹ (x⁵−1)/ln x dx | dutis, frullani-adjacent | yang:1.20 | ln 6 | sympy |
| SAMPLE-Q02 | ∫₀^∞ (sin x)/x dx | dirichlet, special | yang:1.20 | π/2 | sympy |
| SAMPLE-Q03 | ∫₀^{π/2} √(sin)/(√sin+√cos) dx | kings-rule, reflection | yang:1.18 | π/4 | sympy |
| SAMPLE-Q04 | ∫₀^∞ ln x /(x²+1) dx | u-sub, odd-even (ln) | yang:1.11 | 0 | sympy |
| SAMPLE-Q05 | ∫₁² ln x /(x²−2x+2) dx | trig-sub / complete square | yang:1.7 | (π ln 2)/8 | sympy |
| SAMPLE-Q06 | ∫₀¹ ln(1−x)/x dx | series | yang:1.14 | −π²/6 | sympy |
| SAMPLE-Q07 | ∫₀^∞ x^{n−1} e^{−x} dx (n∈Z⁺) | gamma, parts | yang:1.6 | Γ(n)=(n−1)! | sympy |
| SAMPLE-Q08 | ∫₀^∞ x^{s−1}/(e^x−1) dx | series, gamma-zeta | yang:1.14 | Γ(s)ζ(s) | sympy |
| SAMPLE-Q09 | ∫₁^∞ (x−⌊x⌋)/x⁴ dx | floor | yang:1.20 | 1/2 − ζ(3)/3 | sympy |
| SAMPLE-Q10 | ∫₋₂² (x³ cos(x/2) + ½) √(4−x²) dx | odd-even, partial-circle | yang:1.3, yang:1.9 | π | sympy |
| SAMPLE-Q11 | ∫ dx/(1+tan x) | trig-identities | yang:1.5 | ½(x+ln(sin x+cos x))+C | sympy |
| SAMPLE-Q12 | ∫ √(tan x) / sin(2x) dx | reverse-product / trig | yang:1.13, yang:1.5 | √(tan x) (+C) | sympy |
| SAMPLE-Q13 | ∫ dx/(1+e^x) | basic-exp | yang:1.4 | −ln(1+e^{−x}) (+C) | sympy |
| SAMPLE-Q14 | ∫ dx /(x(1+sin²(ln x))) | intermediate-u-sub | yang:1.11 | (1/√2) arctan(√2 tan(ln x))+C | sympy |
| SAMPLE-Q15 | ∫ dx/(x³+1) | partial-fractions | yang:1.8 | corrected antiderivative (printed final has the wrong arctan sign) | sympy |
| SAMPLE-Q16 | ∫ dx/(2+sin x) | weierstrass | yang:1.16 | (2/√3) arctan((2tan(x/2)+1)/√3)+C | sympy |
| SAMPLE-Q17 | ∫ x^(1/ln x) dx | rewrite-exponent | — | answers sheet `ex+c` means e·x + C | sympy |
| SAMPLE-Q18 | ∫ dx/(1−sin x) | trig-identities | yang:1.5, yang:1.15 | sec x + tan x + C | sympy |
| SAMPLE-Q19 | ∫ x √((1−x²)/(1+x²)) dx | trig-sub | yang:1.7 | ½(sin(arccos(x²))−arccos(x²))+C (PDF) | sympy |
| SAMPLE-Q20 | ∫ (e^{2x}+e^{3x})/(e^x+e^{−x}) dx | basic-exp, algebra | yang:1.4 | e^x − arctan(e^x) + (1/2) sec^2(arctan(e^x)) + ln\|cos(arctan(e^x))\| + C | sympy |

Machine feed: `answers_feed.json`. SymPy gate: `verify/check_samples.py` (rows with `"verify": "sympy"`). Catalog rows and worked notes: `problems/records.jsonl` and `solutions/sample/`. `solutions/sample_self_check.py` checks both.

SAMPLE-Q17 is \(x^{1/\ln x}\). The solutions PDF reduces it to the constant \(e\), so the integral is \(ex+C\). The earlier reading \(\int dx/(x\ln x)=\ln|\ln x|+C\) came from a text extract and is withdrawn.

SAMPLE-Q15's printed final puts a minus sign on the arctan term. That expression is not an antiderivative. The catalog grades the antiderivative from the previous line of the solutions PDF.

All twenty SAMPLE rows are `verify: sympy`. SAMPLE-Q05, SAMPLE-Q08, SAMPLE-Q09, and SAMPLE-Q19 are included. None is deferred.
