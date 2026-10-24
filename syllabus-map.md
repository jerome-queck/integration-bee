# Syllabus → technique → sample / drill map

Official contest source of truth: https://integration.soc.srcf.net/
Yang companion: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf` (Yuepeng Alex Yang, 2nd Ed)
Citations use local mirrors. Page/section numbers from `pdftotext` of the real PDFs.

## Contest facts (homepage)

From `sources/index.html`:
- Round 1: **30 problems**, team of up to **3**, **2 hours**; typically **early November**.
- **NTU** joined 2024 (Singapore track with NUS).
- Most Round 1 integrals are definite; indefinite also appear.

## Local sources

| Path | What |
|---|---|
| `sources/index.html` | Homepage HTML mirror |
| `sources/pastcomp.html` | Past-comp narrative |
| `sources/UK_University_Integration_Bee_Syllabus.pdf` | Official syllabus §1–§2 |
| `sources/UK_University_Integration_Bee_Techniques_Guide.pdf` | Basic Techniques Guide |
| `sources/Integration_Competition_Sample_problems.pdf` | Sample Q1–Q20 |
| `sources/Virtual_integration_competition_sample_hints.pdf` | Hints |
| `sources/Integration_bee_sample_problems_answers.pdf` | Answers |
| `sources/UK_University_integration_bee_sample_problems_solutions.pdf` | Solutions |
| `sources/Resource_pack.zip` | Full pack (fetch.sh) |
| `sources/Formula_sheet.pdf` | From Resource pack |
| `sources/past/r1/2020` through `r1/2025/` | Round 1 papers (from Resource pack) |
| `sources/past/r2/` | Round 2 papers, with `uk` and `sg` under 2025 |
| `sources/past/r3/` | Round 3 papers |
| `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf` | **Yang Topics Guide 2nd Ed (committed)** |
| `sources/user/yang-topics-inventory.md` | Yang topic id inventory |

Fetch official binaries: `sources/fetch.sh` + `sources/sha256sums`.

---

## Yang Chapter 1 (Round 1 priority) — full 1.1–1.20

Source: Yang Contents pp.7–37 (`Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`).
Inventory: `sources/user/yang-topics-inventory.md`.

| yang id | Topic | Official overlap (syllabus / Techniques Guide) | Sample / drill ids | Unit status |
|---|---|---|---|---|
| `yang:1.1` | Basic Integration | Syllabus §1 A-Level/STEP; Guide Intro p.2 | `U01-D07`, `U01-D08` | **Unit 01** |
| `yang:1.2` | Basic U-Substitution | Syllabus §1 substitution; Guide Intro p.2 | `U01-D01`…`U01-D06` | **Unit 01** |
| `yang:1.3` | Symmetry | Guide §1.1 Odd and Even (Contents p.3); Syllabus §1 odd/even | `U02-D01`…`U02-D04`; sample Q10; bridge `U01-D07` | **Unit 02** |
| `yang:1.4` | Basic Exponential Functions | Syllabus §1 A-Level; sample Q13, Q17, Q20 | `U03-D01`,`U03-D02`,`U03-D07`; sample Q13, Q17, Q20 | **Unit 03** |
| `yang:1.5` | Basic Trig Integrals | Guide §1.8 Trigonometric Identities (p.18); sample Q11, Q12, Q18 | `U02-D05`…`U02-D10`; sample Q11, Q12, Q18 | **Unit 02** |
| `yang:1.6` | Basic Integration by Parts | Syllabus §1 parts; Guide Intro p.2; sample Q7 | `U03-D03`…`U03-D06`,`U03-D08`; sample Q7 | **Unit 03** |
| `yang:1.7` | Basic Trig-Substitution | Syllabus §1 / A-Level trig sub; sample Q5, Q19 | `U04-D01`,`U04-D03`,`U04-D05`…`U04-D07`; sample Q5, Q19 | **Unit 04** |
| `yang:1.8` | Basic Partial Fractions | Syllabus §1 A-Level; sample Q15 | `U05-D01`…`U05-D06`; sample Q15 | **Unit 05** |
| `yang:1.9` | Area of a Partial Circle | Geometric definite integrals (A-Level area) | `U04-D02`,`U04-D04`,`U04-D08` | **Unit 04** |
| `yang:1.10` | Algebra Manipulation | Used inside Guide/Syllabus tricks; supports Unit 01 drills | `U01-D06` (light) | **Unit 01** (light) |
| `yang:1.11` | Intermediate U-Substitution | Syllabus §1 substitution (deeper); sample Q4, Q14 | `U06-D01`…`U06-D08`; sample Q4, Q14 | **Unit 06** |
| `yang:1.12` | Absolute Values | Piecewise definite integrals | `U07-D01`…`U07-D03`,`U07-D07` | **Unit 07** |
| `yang:1.13` | Reverse Product Rule | Related to parts / recognising derivatives; sample Q12 | `U07-D04`…`U07-D06`,`U07-D08`; sample Q12 | **Unit 07** |
| `yang:1.14` | Basic Series | Syllabus §1 infinite series; sample Q6, Q8 | `U08-D01`…`U08-D06`; sample Q6, Q8 | **Unit 08** |
| `yang:1.15` | Intermediate Trig Integrals | Guide §1.8; sample Q11, Q18 | `U09-D01`…`U09-D04`,`U09-D07`; sample Q11, Q18 | **Unit 09** |
| `yang:1.16` | Intermediate Trig-Substitution | Syllabus §1; sample Q16 (Weierstrass adjacent) | `U09-D05`,`U09-D06`,`U09-D08`; sample Q16 | **Unit 09** |
| `yang:1.17` | Inverse Functions | Guide §1.5 Integral of Inverse (Contents p.14) | `U10-D01`…`U10-D03`,`U10-D08` | **Unit 10** |
| `yang:1.18` | King’s/Queen’s Rule | Syllabus §1 reflection property; Guide §1.2 (p.7); sample Q3 | `U10-D04`…`U10-D07`; sample Q3, Q5 | **Unit 10** |
| `yang:1.19` | Gaussian Integrals | Related to Gamma (Syllabus §2) / special forms | `U11-D01`…`U11-D04`,`U11-D08` | **Unit 11** |
| `yang:1.20` | Special Wildcard | Catch-all / mixed easy contest openers | `U11-D05`…`U11-D07` | **Unit 11** |

**Done:** Units 01–11 cover every `yang:1.1`…`yang:1.20` (1.10 light in Unit 01). Sample bridge + past pack: `past/` (SAMPLE-Q01…20 tagged; mocks ready).

---

## Official §1 Integration Techniques → samples

Syllabus: `UK_University_Integration_Bee_Syllabus.pdf` §1 (p.1).

| Technique slug | Syllabus / Guide cite | Sample ids |
|---|---|---|
| `u-sub` / `linear-sub` / `du/u` | Syllabus §1 topic 1; Guide Intro p.2 | Q4, Q5, Q12–Q14, Q17, Q19, Q20; drills `U01-D01`–`D06` |
| `parts` | Syllabus §1 topic 1 | Q7, Q10 |
| `dutis` | Syllabus §1 DUTIS | Q1, Q2 |
| `weierstrass` | Syllabus §1 Weierstrass | Q16 |
| `series` | Syllabus §1 infinite series | Q6, Q8 |
| `reflection` / `kings-rule` | Syllabus §1 reflection; Guide §1.2 | Q3 |
| `odd-even` | Syllabus §1; Guide §1.1 | Q10; `U01-D07` |
| `vector-calc` | Syllabus §1 end — not required | — |

## Official §2 Functions → samples

Syllabus §2 (p.2): Gamma Q7; Beta —; zeta Q6/Q8/Q9; floor Q9; Wallis Guide §1.4; γ —; Catalan's listed.

## Techniques Guide foundation order

Guide Contents: §1.1 Odd/Even p.3 → §1.2 Reflection p.7 → §1.3 Recurrence p.11 → §1.4 Wallis* p.13 → §1.5 Inverse p.14 → §1.6 T-sub p.15 → §1.7 Floor p.17 → §1.8 Trig p.18 → §1.9 Constants p.21 → §1.10 Exercises p.22.

## Yang Chapter 2 (started)

| yang id | Topic | Unit status |
|---|---|---|
| `yang:2.1` | Modified Textbook Problems | **Unit 12** (`U12-D01`…`D04`) |
| `yang:2.2` | Sneaky Algebra Manipulation | **Unit 12** (`U12-D05`…`D08`) |

Remaining `yang:2.3`…`yang:2.10` still deferred.

## Deferred — Yang Ch.2+ (after Ch.1 solid)

Do **not** build units yet. Listed for tracker only (inventory):

- Ch.2 Regular: `yang:2.3`…`yang:2.10` remaining (`2.1`/`2.2` in Unit 12; incl. Gamma `2.4`, sneaky symmetry `2.9`)
- Ch.3 Intermediate: `yang:3.1`…`yang:3.8` (Wallis trick `3.3`, periodicity `3.7`)
- Ch.4 Advanced-lite: `yang:4.1`…`yang:4.6` (Weierstrass `4.5`, advanced King’s `4.4`)
- Ch.5 Advanced: `yang:5.1`…`yang:5.4` (Dirichlet `5.4`)
- Ch.6 Very advanced: `yang:6.1`…`yang:6.9` (Feynman `6.7`, Frullani `6.6`, Taylor `6.2`)

## Pedagogy order (Round 1)

1. Units 01–11 → full Yang Ch.1 (`yang:1.1`…`yang:1.20`)
2. Official sample Q1–Q20 in teaching order
3. Past Round 1 papers only after concept units exist (`verify/unit_order_check.py`)
