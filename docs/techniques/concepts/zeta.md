# Zeta: a name for a convergent sum

## Status

- Catalog node: `zeta`; status: ready; depth: card; unit: `35-modified-famous`.
- Round 1: optional, with no readiness gate. Content readiness does not award a learner mastery tick.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [NIST DLMF 25.2.1](https://dlmf.nist.gov/25.2.E1) defines the convergent zeta series.
- Coach policy: [the series card](series.md) and [unit 35](../../../units/35-modified-famous/teaching.tex) keep their cited values. Do not invent a new evaluation of \(\zeta(s)\).

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `zeta` | 4, optional recognition | `basic-series`, `gamma` | [unit 35](../../../units/35-modified-famous/teaching.tex), optional zeta recognition |

Use the oral recognition drill below, then the stored series pair `U35-D04` and `U35-D05` if practice is wanted. Those ids retain their practice credit on `modified-famous`. The optional `zeta` node has no automatic drill queue, and host-unit answers do not automatically credit it.

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

## Recognition drill

**Worked.** Use the nonnegative expansion above to identify the shifted index and the factor 2. Stop at \(2\zeta(3)\); no further evaluation of \(\zeta(3)\) is supplied.

**Faded.** Hide the result of \(\int_0^1 x^n(\log x)^2\,dx\). Ask for the substitution \(x=e^{-t}\), then scale \(u=(n+1)t\) to recover \(2/(n+1)^3\) for integers \(n\geq0\).

**Bare.** Ask whether \(\sum_{n=1}^{\infty}n^{-1}\) and \(\sum_{n=1}^{\infty}n^{-3}\) both define ordinary convergent zeta sums, and ask which sum the worked integral produced. The first diverges; the second is \(\zeta(3)\), and the worked integral is twice it. Require the range \(s>1\) and the index shift, not a guessed decimal or logarithm. This is a recognition prompt, not a machine drill id.

Preserve the exact named value when it is the answer's form. Use only the existing cited unit values when a stored drill requires further evaluation. The lesson is ready for an optional session; it grants no permission to fill a pack answer or award mastery without evidence.
