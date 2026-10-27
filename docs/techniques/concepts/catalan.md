# Catalan: keep the named constant

## Status

- Catalog node: `catalan`; depth: deferred-noted.
- Round 1: leave unticked. This card adds no unit or drill for the deferred node.
- Sources: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [unit 36](../../../units/36-unique-tricks/teaching.tex), worked `U36-D03`; [Wolfram's defining sum](https://reference.wolfram.com/language/ref/Catalan.html).
- Coach route: open unit 36 for its worked, faded, and bare doses. This note clarifies the exact constant and the endpoint argument.

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

Ask for the general integrated term and why the value at zero is harmless. Forgetting the alternating sign, using all positive integers in the denominator, or losing the square produces a different sum. Faded and bare practice use the existing `U36-D03`; they do not create a `catalan` drill or readiness tick.

Stop at \(G\). Do not replace it with a guessed logarithm, rational number, or decimal equality. This stopping rule makes no claim that such replacements have been proved impossible. A correct cited identity is what would justify any alternate exact form. The [series card's policy](series.md) applies here too: a named constant left in the unit stays named. Keep `catalan` unticked.
