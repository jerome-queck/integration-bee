# Zeta: a name for a convergent sum

## Status

- Catalog node: `zeta`; depth: deferred-noted.
- Round 1: leave unticked. This recognition note adds no unit, drill, or gate.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [NIST DLMF 25.2.1](https://dlmf.nist.gov/25.2.E1) defines the convergent zeta series.
- Coach policy: [the series card](series.md) and [unit 35](../../../units/35-modified-famous/teaching.tex) keep their cited values. Do not invent a new evaluation of \(\zeta(s)\).

## Definition and scope

For real \(s>1\),

\[
\zeta(s)=\sum_{n=1}^{\infty}\frac1{n^s}.
\]

The exponent \(s\) is a parameter; \(n\) indexes the positive integers. The integral test proves convergence in this range. Naming a sum \(\zeta(3)\) is an exact description; it does not evaluate \(\zeta(3)\) as a rational number, logarithm, or power of \(\pi\). Definitions by analytic continuation elsewhere do not make a divergent series into an ordinary convergent sum.

## Sourced identity and a recognition example

[DLMF 25.5.1](https://dlmf.nist.gov/25.5.E1) gives, for real \(s>1\),

\[
\int_0^\infty\frac{t^{s-1}}{e^t-1}\,dt=\Gamma(s)\zeta(s).
\]

Here is an expository specialization, not a contest answer or drill. Substituting \(x=e^{-t}\) at \(s=3\) gives

\[
\int_0^1\frac{(-\log x)^2}{1-x}\,dx=2\zeta(3).
\]

The mechanism can be checked without evaluating \(\zeta(3)\). Expand \(1/(1-x)=\sum_{n=0}^\infty x^n\) on \(0<x<1\). All terms after multiplication by \((\log x)^2\) are nonnegative, so monotone convergence permits termwise integration. The same substitution gives

\[
\int_0^1x^n(\log x)^2\,dx
=\int_0^\infty t^2e^{-(n+1)t}\,dt
=\frac{2}{(n+1)^3}.
\]

The last equality follows by scaling and two integrations by parts. Summing yields \(2\zeta(3)\), and we stop there. The endpoint near \(x=1\) behaves like \(1-x\); near zero, \((\log x)^2\) is integrable. Thus the displayed integral converges.

## Coach prompts and failures

Ask where the series starts, why the power is 3, and what justifies exchanging sum and integral. Forgetting the index shift or the factor 2 changes the result. Applying the defining series at \(s=1\) ignores divergence. Positive-term interchange here does not justify an arbitrary signed series interchange.

Preserve the exact named value when it is the answer's form. Use only the existing cited unit values when a stored drill requires further evaluation. This note grants no permission to fill a pack answer or tick `zeta`.
