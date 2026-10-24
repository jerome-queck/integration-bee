# units/

Concept units before past papers. Each unit directory:

```
meta.yaml          # id, tags, yang:*, past_paper flag
teaching.tex       # canonical teaching (→ PDF; templates/ later)
drills.tex
solutions.tex
drills.md          # thin CLI table: ids, tags, sympy answers
```

## Units

| dir | title | yang (primary) | status |
|---|---|---|---|
| `01-foundations-substitution/` | Foundations & Substitution | 1.1, 1.2 (+light 1.10) | ready |
| `02-symmetry-basic-trig/` | Symmetry & Basic Trig | 1.3, 1.5 | ready |
| `03-exponential-parts/` | Exp & Integration by Parts | 1.4, 1.6 | ready |
| `04-trig-sub-circle/` | Trig-Sub & Partial Circle | 1.7, 1.9 | ready |
| `05-partial-fractions/` | Basic Partial Fractions | 1.8 | ready |
| `06-intermediate-u-sub/` | Intermediate U-Sub | 1.11 | ready |
| `07-abs-reverse-product/` | Abs Values & Reverse Product | 1.12, 1.13 | ready |
| `08-basic-series/` | Basic Series | 1.14 | ready |
| `09-intermediate-trig/` | Intermediate Trig / Trig-Sub | 1.15, 1.16 | ready |
| `10-inverse-kings/` | Inverse & King's Rule | 1.17, 1.18 | ready |
| `11-gaussian-wildcard/` | Gaussian & Wildcard | 1.19, 1.20 | ready |
| `12-modified-sneaky-algebra/` | Modified Textbook & Sneaky Algebra | 2.1, 2.2 | ready |
| `13-forced-u-sub/` | Basic Forced U-Substitutions | 2.3 | ready |
| `14-gamma/` | Gamma Function Integral | 2.4 | ready |
| `15-parts-regular/` | Integration by Parts (Regular) | 2.5 | ready |
| `16-trig-id-trig-sub/` | Trig Identities & Intermediate Trig-Sub | 2.6, 2.7 | ready |
| `17-infinite-functions/` | Infinite Functions | 2.8 | ready |
| `18-sneaky-symmetry-product/` | Sneaky Symmetry & Sneaky Product Rule | 2.9, 2.10 | ready |
| `19-power-sneaky-usub/` | Power Substitution and Sneaky U-Sub Tricks | 3.1, 3.2 | ready |
| `20-wallis/` | Wallis' Trick | 3.3 | ready |
| `21-advanced-trig-sub/` | Advanced Trig-Substitution | 3.4 | ready |
| `22-awkward-parts-pf/` | Awkward Parts and Intermediate Partial Fractions | 3.5, 3.6 | ready |
| `23-periodicity-speed/` | Basic Periodicity and Speed Bashing | 3.7, 3.8 | ready |
| `24-undertow-square/` | Undertow and Square-Square | 4.1, 4.2 | ready |
| `25-advanced-kings/` | Advanced King's/Queen's Rule | 4.4 | ready |
| `26-weierstrass/` | Weierstrass Substitution | 4.5 | ready |
| `27-reverse-quotient/` | Reverse Quotient Rule | 4.6 | ready |
| `28-semi-parts/` | Semi-Integration by Parts | 5.1 | ready |
| `29-advanced-trig/` | Advanced Trig Integrals | 5.2 | ready |
| `30-gaussian-dirichlet/` | Advanced Gaussian and Dirichlet | 5.3, 5.4 | ready |
| `31-inverse-jailbreak/` | Inverse Jailbreaking | 6.1 | ready |
| `32-taylor-complex/` | Taylor Series and Complexifying | 6.2, 6.3 | ready |
| `33-ninja-inversion/` | Ninja Substitution and Inversion | 6.4, 6.5 | ready |
| `34-frullani-feynman/` | Frullani Integrals and Feynman Technique | 6.6, 6.7 | ready |
| `35-modified-famous/` | Modified Famous Integrals | 6.8 | ready |
| `36-unique-tricks/` | Unique Tricks | 6.9 | ready |

Yang Ch.1–6 concept units through 6.9 are complete (inventory 4.3 skipped). Every unit note inputs `templates/`. Past pedagogy lives under `../past/` (not as `units/*` past_paper dirs). Gate: `../verify/unit_order_check.py` + `past_presence_check.py`.
