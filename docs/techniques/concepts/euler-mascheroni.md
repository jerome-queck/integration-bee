# Euler–Mascheroni: the harmonic sum's offset

## Status

- Catalog node: `euler-mascheroni`; depth: deferred-noted.
- Round 1: leave unticked. There is no unit or stored drill for this node.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [NIST DLMF 5.2.3](https://dlmf.nist.gov/5.2.E3) defines Euler's constant.
- Use: recognize the constant in a harmonic-sum limit or a logarithmic Gamma integral. Keep an exact answer as \(\gamma\) when that is what the derivation gives.

## Definition and intuition

For a positive integer \(n\), write \(H_n=\sum_{k=1}^n1/k\). Then

\[
\gamma=\lim_{n\to\infty}(H_n-\log n).
\]

The logarithm is the area \(\int_1^n dx/x\); the harmonic sum is a sum of rectangles for the same decreasing curve. Their difference has a finite limiting offset.

To check that a limit exists, let \(a_n=H_n-\log n\). Rectangle comparison gives \(a_n>0\), while

\[
a_n-a_{n+1}
=\int_n^{n+1}\frac{dx}{x}-\frac1{n+1}>0.
\]

Thus \(a_n\) decreases and is bounded below. A finite value such as \(a_2=3/2-\log2\) is an approximation from above, not the definition's limiting value. This comparison is explanatory work, not a new drill.

## Where it appears in integration

The Gamma integral from [unit 14](../../../units/14-gamma/teaching.tex) gives

\[
\Gamma'(1)=\int_0^\infty e^{-x}\log x\,dx=-\gamma.
\]

The final equality follows from [DLMF 5.4.11](https://dlmf.nist.gov/5.4.E11), the [logarithmic derivative definition](https://dlmf.nist.gov/5.2.E2), and \(\Gamma(1)=1\). For the integral step, differentiate \(\Gamma(s)=\int_0^\infty e^{-x}x^{s-1}\,dx\) at \(s=1\). On \(1/2\leq s\leq3/2\), the derivative integrand is bounded by \(x^{-1/2}|\log x|\) on \((0,1)\) and \(e^{-x}x^{1/2}\log x\) on \([1,\infty)\); both bounds are integrable. They justify the differentiation. This is a named special-function identity, not a contest final supplied by the card.

## Coach prompts and failures

Ask the learner to distinguish \(\gamma\), the constant, from \(\Gamma(s)\), the function. The integral above is \(-\gamma\), so dropping the sign matters. Subtract the finite expressions before taking their limit; do not separately subtract two infinities. A decimal approximation or a finite harmonic sum is not an exact replacement for \(\gamma\).

There is no need to force a rational or logarithmic answer. Stop at the justified named constant and leave `euler-mascheroni` unticked.
