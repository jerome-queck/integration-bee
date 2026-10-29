# Worked solutions

These notes record printed finals and worked readings. They do not change `problems/records.jsonl` or any verify flag. At tip `770c6e4` every resource-pack catalog row is `verify: sympy` (674 SymPy / 0 manual / 0 unchecked). The index below lists 81 of those notes. `YANG-1.3-Ex01`, `YANG-1.3-Ex02`, and `YANG-1.3-Ex03` are `verify: sympy`. Lane L1 also proves `YANG-1.1-P01`–`P06` and `YANG-1.2-P01`–`P20`. Lane L2 proves `YANG-1.4-P01`–`P18` and `YANG-1.5-P01`–`P20`. Lane L3 proves `YANG-1.6-P01`–`P20` and `YANG-1.7-P01`–`P10`. Lane L6 proves `YANG-2.3-P01`–`P18` and `YANG-2.4-P01`–`P12`. Lane L7 proves `YANG-2.5-P01`–`P18` and `YANG-2.6-P01`–`P16`. Lane L4 proves `YANG-1.8-P01`–`P17` and `YANG-1.11-P01`–`P20`. Lane L8 proves the checked rows in sections 2.7, 3.4, 3.8, 4.4, 4.6, 6.1, and 6.7. Lane L5 proves 36 rows in §§1.12, 1.15, 1.17, 1.18, and 1.20. 6 other Yang rows stay `unchecked`.

Each pack final is the value printed in the cited answers PDF or solutions PDF. Where a worked PDF and an answers PDF print equivalent antiderivatives, the note records both and the constant relating them. Yang notes for `YANG-1.3-Ex01` and `YANG-1.3-Ex03` copy finals the guide prints. Lane L4 adds derived notes for the proved §1.8 and §1.11 practice rows. Those list items print no final. The catalog grade is the pack-gate value. Other Yang rows are left without a final.

Re-run the machine notes with:

```bash
python3 solutions/self_check.py
```

## Pack

| Id | Printed final | Note |
|---|---|---|
| R1-2020-Q06 | \(\pi^2/24\) | [pack/R1-2020-Q06.md](pack/R1-2020-Q06.md) |
| R1-2020-Q10 | \(1\) | [pack/R1-2020-Q10.md](pack/R1-2020-Q10.md) |
| R1-2020-Q11 | \(\frac25(x^6+x^4+x^{-4})^{5/4}+C\) | [pack/R1-2020-Q11.md](pack/R1-2020-Q11.md) |
| R1-2020-Q13 | \(\ln\bigl\|(\sqrt{1+e^x}-1)/(\sqrt{1+e^x}+1)\bigr\|+2\sqrt{1+e^x}+C\) | [pack/R1-2020-Q13.md](pack/R1-2020-Q13.md) |
| R1-2020-Q15 | \(-\operatorname{arsinh}(e^{-x})+C\) | [pack/R1-2020-Q15.md](pack/R1-2020-Q15.md) |
| R1-2020-Q18 | \(\ln\bigl\|(\tan(x/2)+1)/(\tan(x/2)+3)\bigr\|+C\) | [pack/R1-2020-Q18.md](pack/R1-2020-Q18.md) |
| R1-2020-Q19 | \(\sum_{k\ge 1} k^{-k}\) | [pack/R1-2020-Q19.md](pack/R1-2020-Q19.md) |
| R1-2020-Q20 | \(\pi^3/8\) | [pack/R1-2020-Q20.md](pack/R1-2020-Q20.md) |
| R1-2020-Q21 | \(2\pi\ln\pi\) | [pack/R1-2020-Q21.md](pack/R1-2020-Q21.md) |
| R1-2020-Q23 | \(\pi^2/12-1/2\) | [pack/R1-2020-Q23.md](pack/R1-2020-Q23.md) |
| R1-2020-Q24 | \((4x-3)^{3/2}/12-x/2+C\) | [pack/R1-2020-Q24.md](pack/R1-2020-Q24.md) |
| R1-2020-Q25 | \(\pi\ln\bigl((a+\sqrt{a^2-b^2})/2\bigr)\) for \(a>b>0\) | [pack/R1-2020-Q25.md](pack/R1-2020-Q25.md) |
| R1-2020-Q27 | \(\pi^2/4\) | [pack/R1-2020-Q27.md](pack/R1-2020-Q27.md) |
| R1-2020-Q28 | \(2-\pi^2/6\) | [pack/R1-2020-Q28.md](pack/R1-2020-Q28.md) |
| R1-2020-Q31 | \(4(\sin(x/4)-\cos(x/4))+C\) on the positive branch | [pack/R1-2020-Q31.md](pack/R1-2020-Q31.md) |
| R1-2020-Q32 | \((\ln 2)^2-2\ln 2+2-\pi^2/6\) | [pack/R1-2020-Q32.md](pack/R1-2020-Q32.md) |
| R1-2020-Q34 | \(e^{e^x}+C\) | [pack/R1-2020-Q34.md](pack/R1-2020-Q34.md) |
| R1-2020-Q39 | \(\pi^2/6\) | [pack/R1-2020-Q39.md](pack/R1-2020-Q39.md) |
| R1-2020-Q40 | \((\pi/8)\ln 2\) | [pack/R1-2020-Q40.md](pack/R1-2020-Q40.md) |
| R1-2021-Q01 | \(x^{e-1}/(e-1)+C\) | [pack/R1-2021-Q01.md](pack/R1-2021-Q01.md) |
| R1-2021-Q02 | \(\pi\,2^{-419}\binom{420}{210}\) | [pack/R1-2021-Q02.md](pack/R1-2021-Q02.md) |
| R1-2021-Q03 | \(1/6\) | [pack/R1-2021-Q03.md](pack/R1-2021-Q03.md) |
| R1-2021-Q09 | \(2\arctan\sqrt{(x^2+x+1)/x}+C\) | [pack/R1-2021-Q09.md](pack/R1-2021-Q09.md) |
| R1-2021-Q11 | \(2011!/2010^{2012}\) | [pack/R1-2021-Q11.md](pack/R1-2021-Q11.md) |
| R1-2021-Q12 | \(\sin((1-n)\pi/2)\,\Gamma(1-n)\) | [pack/R1-2021-Q12.md](pack/R1-2021-Q12.md) |
| R1-2021-Q13 | \(1/3\) | [pack/R1-2021-Q13.md](pack/R1-2021-Q13.md) |
| R1-2021-Q15 | \(x+\sec x-\tan x+C\) | [pack/R1-2021-Q15.md](pack/R1-2021-Q15.md) |
| R1-2021-Q16 | \(\frac12\bigl(\pi-\ln(\sinh\pi/\pi)\bigr)\) | [pack/R1-2021-Q16.md](pack/R1-2021-Q16.md) |
| R1-2021-Q18 | \(\arcsin\sqrt{x}+\sqrt{x(1-x)}+C\) | [pack/R1-2021-Q18.md](pack/R1-2021-Q18.md) |
| R1-2021-Q20 | \(\frac{x}{2}\sqrt{x^2-1}-\frac12\operatorname{acosh} x+C\) | [pack/R1-2021-Q20.md](pack/R1-2021-Q20.md) |
| R1-2021-Q26 | \(\operatorname{arccot}(1+e)\) | [pack/R1-2021-Q26.md](pack/R1-2021-Q26.md) |
| R1-2021-Q30 | \(\frac1{16}\ln^2(3-2\sqrt{2})\) | [pack/R1-2021-Q30.md](pack/R1-2021-Q30.md) |
| R1-2021-Q31 | \(2-\pi^2/6\) | [pack/R1-2021-Q31.md](pack/R1-2021-Q31.md) |
| R1-2021-Q32 | \(\pi(b-a)/2\) for \(a>0\), \(b>0\) | [pack/R1-2021-Q32.md](pack/R1-2021-Q32.md) |
| R1-2021-Q36 | \(\pi G/2-7\zeta(3)/8\) | [pack/R1-2021-Q36.md](pack/R1-2021-Q36.md) |
| R1-2021-Q37 | \(0\) | [pack/R1-2021-Q37.md](pack/R1-2021-Q37.md) |
| R1-2021-Q39 | \(\arctan(\tan(2x)/\sqrt{2})/\sqrt{2}+C\) | [pack/R1-2021-Q39.md](pack/R1-2021-Q39.md) |
| R1-2021-Q40 | \(\pi/\sinh\pi\) | [pack/R1-2021-Q40.md](pack/R1-2021-Q40.md) |
| R1-2022-Q02 | \(333300\) | [pack/R1-2022-Q02.md](pack/R1-2022-Q02.md) |
| R1-2022-Q04 | \(\frac{5}{12}(1+\sqrt{5})\) | [pack/R1-2022-Q04.md](pack/R1-2022-Q04.md) |
| R1-2022-Q05 | \(1-\gamma\) | [pack/R1-2022-Q05.md](pack/R1-2022-Q05.md) |
| R1-2022-Q07 | \(1\) | [pack/R1-2022-Q07.md](pack/R1-2022-Q07.md) |
| R1-2022-Q11 | \(1/2\) | [pack/R1-2022-Q11.md](pack/R1-2022-Q11.md) |
| R1-2022-Q15 | \((\pi-2)/4\) | [pack/R1-2022-Q15.md](pack/R1-2022-Q15.md) |
| R1-2022-Q16 | \(1-\gamma\) | [pack/R1-2022-Q16.md](pack/R1-2022-Q16.md) |
| R1-2022-Q17 | \(\pi\operatorname{sech}(\pi/2)\) | [pack/R1-2022-Q17.md](pack/R1-2022-Q17.md) |
| R1-2022-Q20 | \(\pi^2/9\) | [pack/R1-2022-Q20.md](pack/R1-2022-Q20.md) |
| R1-2022-Q21 | \(e\sqrt{\pi}/2\) | [pack/R1-2022-Q21.md](pack/R1-2022-Q21.md) |
| R1-2022-Q22 | \(\pi^2/4\) | [pack/R1-2022-Q22.md](pack/R1-2022-Q22.md) |
| R1-2022-Q23 | \(\pi/(2\sqrt{2})\) | [pack/R1-2022-Q23.md](pack/R1-2022-Q23.md) |
| R1-2022-Q24 | \(2\pi/n!\) for \(n=0,1,2,\ldots\) | [pack/R1-2022-Q24.md](pack/R1-2022-Q24.md) |
| R1-2022-Q25 | \(-\gamma\pi/2\) | [pack/R1-2022-Q25.md](pack/R1-2022-Q25.md) |
| R1-2022-Q28 | \(4G\) | [pack/R1-2022-Q28.md](pack/R1-2022-Q28.md) |
| R1-2022-Q30 | \(\pi\ln^2(1+a)/(2a^2)\) for \(a>0\) | [pack/R1-2022-Q30.md](pack/R1-2022-Q30.md) |
| R1-2023-Q04 | \(2xX+C\) | [pack/R1-2023-Q04.md](pack/R1-2023-Q04.md) |
| R1-2023-Q05 | \(0\) | [pack/R1-2023-Q05.md](pack/R1-2023-Q05.md) |
| R1-2023-Q08 | \(3/(2\ln 2)\) | [pack/R1-2023-Q08.md](pack/R1-2023-Q08.md) |
| R1-2023-Q09 | \(\ln 2\) | [pack/R1-2023-Q09.md](pack/R1-2023-Q09.md) |
| R1-2023-Q14 | \(-1\) | [pack/R1-2023-Q14.md](pack/R1-2023-Q14.md) |
| R1-2023-Q17 | \(e^{\pi/2}+1\) | [pack/R1-2023-Q17.md](pack/R1-2023-Q17.md) |
| R1-2023-Q20 | \(1/4\) | [pack/R1-2023-Q20.md](pack/R1-2023-Q20.md) |
| R1-2023-Q21 | \(x-\ln\bigl(1+(2024/2023)^x\bigr)/\ln(2024/2023)+C\) | [pack/R1-2023-Q21.md](pack/R1-2023-Q21.md) |
| R1-2023-Q25 | \(e+1/2\) | [pack/R1-2023-Q25.md](pack/R1-2023-Q25.md) |
| R1-2023-Q28 | \(9\) | [pack/R1-2023-Q28.md](pack/R1-2023-Q28.md) |
| R1-2023-Q30 | \(\pi\) | [pack/R1-2023-Q30.md](pack/R1-2023-Q30.md) |
| R1-2024-Q01 | \(\sin 1\) | [pack/R1-2024-Q01.md](pack/R1-2024-Q01.md) |
| R1-2024-Q04 | \(s^2\mathrm{in}^2/2+\mathrm{cos}^3/3+C\) | [pack/R1-2024-Q04.md](pack/R1-2024-Q04.md) |
| R1-2024-Q07 | \(\pi^4/120\) | [pack/R1-2024-Q07.md](pack/R1-2024-Q07.md) |
| R1-2024-Q09 | \(4\) | [pack/R1-2024-Q09.md](pack/R1-2024-Q09.md) |
| R1-2024-Q10 | \(\sqrt{\pi}\,e^{-x^2}/2\) | [pack/R1-2024-Q10.md](pack/R1-2024-Q10.md) |
| R1-2024-Q11 | \(\pi^2/8\) | [pack/R1-2024-Q11.md](pack/R1-2024-Q11.md) |
| R1-2024-Q13 | \(\pi/2\) | [pack/R1-2024-Q13.md](pack/R1-2024-Q13.md) |
| R1-2024-Q15 | \(1\) | [pack/R1-2024-Q15.md](pack/R1-2024-Q15.md) |
| R1-2024-Q17 | \((1+\ln 2)/2\) | [pack/R1-2024-Q17.md](pack/R1-2024-Q17.md) |
| R1-2024-Q20 | \(4950\) | [pack/R1-2024-Q20.md](pack/R1-2024-Q20.md) |
| R1-2024-Q21 | \(0\) | [pack/R1-2024-Q21.md](pack/R1-2024-Q21.md) |
| R1-2024-Q22 | \((\pi/2)\ln(b/a)\) for \(a>0\), \(b>0\) | [pack/R1-2024-Q22.md](pack/R1-2024-Q22.md) |
| R1-2024-Q24 | \(\pi^2/4\) | [pack/R1-2024-Q24.md](pack/R1-2024-Q24.md) |
| R1-2024-Q26 | \(\pi/4\) | [pack/R1-2024-Q26.md](pack/R1-2024-Q26.md) |
| R1-2024-Q28 | \(\pi^2/4\) | [pack/R1-2024-Q28.md](pack/R1-2024-Q28.md) |
| R1-2024-Q30 | \((\pi/2)\ln 2\) | [pack/R1-2024-Q30.md](pack/R1-2024-Q30.md) |

81 pack notes. Their catalog rows are `verify: sympy`. Pack manuals are 0.

## Yang

| Id | Printed final | Note |
|---|---|---|
| YANG-1.3-Ex01 | \(8/3\) | [yang/YANG-1.3-Ex01.md](yang/YANG-1.3-Ex01.md) |
| YANG-1.3-Ex02 | \(2\) | [yang/YANG-1.3-Ex02.md](yang/YANG-1.3-Ex02.md) |
| YANG-1.3-Ex03 | \(2\tan^{-1}(3)\) | [yang/YANG-1.3-Ex03.md](yang/YANG-1.3-Ex03.md) |

Lane L4 derived notes are `solutions/yang/YANG-1.8-P01.md` through `YANG-1.8-P17.md` and `solutions/yang/YANG-1.11-P01.md` through `YANG-1.11-P20.md`. Each header says the printed answer is absent.

## Sample

The UK site sample sheet is `solutions/sample/SAMPLE-Q01.md` through `SAMPLE-Q20.md`. Those ids are catalog rows, and all 20 are `verify: sympy`. `python3 solutions/sample_self_check.py` re-proves them, including Q05, Q08, Q09, and Q19. Q15 grades the antiderivative obtained by finishing the solutions PDF's correct split. The printed last line has the wrong sign on the arctan term. Q17 is \(x^{1/\ln x}\), graded as \(ex+C\).
