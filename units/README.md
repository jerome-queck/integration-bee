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

Yang Ch.1 (01–11) and Ch.2 (12–18) concept units complete. Past pedagogy lives under `../past/` (not as `units/*` past_paper dirs). Gate: `../verify/unit_order_check.py` + `past_presence_check.py`.
