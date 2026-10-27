# Catalan: keep the named constant

## Status

- Catalog node: `catalan`; status: ready; depth: card; unit: `36-unique-tricks`.
- Round 1: optional, with no readiness gate. Content readiness does not award a learner mastery tick.
- Sources: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [unit 36](../../../units/36-unique-tricks/teaching.tex), worked `U36-D03`; [Wolfram's defining sum](https://reference.wolfram.com/language/ref/Catalan.html).
- Coach route: open unit 36 for its worked, faded, and bare doses. This note clarifies the exact constant and the endpoint argument.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `catalan` | 4, optional recognition | `basic-series`, `basic-trig-integrals` | [unit 36](../../../units/36-unique-tricks/teaching.tex), worked/faded/bare `U36-D03` |

`U36-D03` remains one stored drill with its practice credit on `unique-tricks`. The optional `catalan` node has no automatic drill queue. Three doses use the same drill id and do not automatically award `catalan` mastery.

## Definition

Catalan's constant is the real number

\[
G=\sum_{k=0}^{\infty}\frac{(-1)^k}{(2k+1)^2}.
\]

The index \(k\) starts at zero; the denominators are odd squares. The series converges absolutely because its absolute terms are bounded by a convergent square-reciprocal series. The stored symbolic spelling in `verify/drills_unit36.json` is `Catalan`. It denotes the same \(G\).

## Why the stored integral equals \(G\)

`U36-D03` stores

\[
\int_0^1\frac{\arctan x}{x}\,dx=G.
\]

At \(x=0\), the integrand has a removable singularity with limiting value 1. For \(0\leq x\leq1\), integrating a finite geometric expansion of \(1/(1+x^2)\) gives

\[
\arctan x=\sum_{k=0}^N\frac{(-1)^k x^{2k+1}}{2k+1}+R_N(x),
\qquad
|R_N(x)|\leq\frac{x^{2N+3}}{2N+3}.
\]

After division by \(x\) and integration, the error is at most \(1/(2N+3)^2\), which tends to zero. Each polynomial term integrates to \((-1)^k/(2k+1)^2\). Hence the integral is precisely the defining sum for \(G\), with no unsupported interchange at the endpoint.

## Coach prompts and failures

Ask for the general integrated term and why the value at zero is harmless. Forgetting the alternating sign, using all positive integers in the denominator, or losing the square produces a different sum.

## Recognition drill

**Worked.** Read the finite-series argument above alongside `U36-D03`, including the remainder bound. Identify the result as the defining sum for \(G\).

**Faded.** Hide the integrated term and error bound. Ask the learner to recover \((-1)^k/(2k+1)^2\) and \(1/(2N+3)^2\), then explain why the error tends to zero.

**Bare.** Set the existing `U36-D03` without the series. Accept \(G\) (the stored symbolic name is `Catalan`) with the derivation above. Refuse a guessed logarithm or a rational and reopen the faded term. The recognition explanation supplements this same stored drill; it creates no new id and does not automatically award a mastery tick.

Stop at \(G\). Do not replace it with a guessed logarithm, rational number, or decimal equality. This stopping rule makes no claim that such replacements have been proved impossible. A correct cited identity is what would justify any alternate exact form. The [series card's policy](series.md) applies here too: a named constant left in the unit stays named.
