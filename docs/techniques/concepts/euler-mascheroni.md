# Euler–Mascheroni: the harmonic sum's offset

## Status

- Catalog node: `euler-mascheroni`; status: ready; depth: card; unit: `14-gamma`.
- Optional syllabus lesson, with no Round 1 gate. Ready means the lesson is available, not that the learner has mastered it.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); [NIST DLMF 5.2.3](https://dlmf.nist.gov/5.2.E3) defines Euler's constant.
- Use: recognize the constant in a harmonic-sum limit or a logarithmic Gamma integral. Keep an exact answer as \(\gamma\) when that is what the derivation gives.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `euler-mascheroni` | 4 | `gamma`, `basic-series` | [unit 14, optional Euler–Mascheroni recognition](../../../units/14-gamma/teaching.tex) |

The recognition drill below follows the worked, faded, and bare pattern in `pedagogy/README.md`. It is an oral check of the definitions and sign, with no machine drill id or `practice check` submission. It does not supply automatic tick evidence. The parameter argument is supplied below; [the DUTIS note](../introduce-constant.md) teaches the general move.

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

## Worked recognition drill

Ask what distinguishes \(\gamma\), \(\Gamma(1)\), and \(\Gamma'(1)\). The coach models the answer: \(\gamma\) is the limiting offset of the harmonic sum, \(\Gamma(1)=\int_0^\infty e^{-x}\,dx=1\), and \(\Gamma'(1)=-\gamma\) has a logarithm in the integrand. The finite expression \(H_2-\log2=3/2-\log2\) lies above \(\gamma\); it is not equal to it.

## Faded step

Hide the identities above and ask the learner to fill

\[
\frac{\partial}{\partial s}x^{s-1}
=x^{s-1}\square,\qquad
\int_0^\infty e^{-x}\log x\,dx=\square\gamma.
\]

The blanks are \(\log x\) and \(-1\). The two integrable bounds above justify bringing the derivative inside. The sign comes from the cited identity for \(\Gamma'(1)\); differentiating under the integral alone does not determine it.

## Bare recognition and refusal

With the worked line closed, ask for the definition of \(\gamma\), the two distinct values \(\Gamma(1)\) and \(\Gamma'(1)\), and why a finite harmonic sum is insufficient. A successful answer states the limit, gives \(1\) and \(-\gamma\), and uses the strictly decreasing sequence \(H_n-\log n\) to reject \(\gamma=3/2-\log2\). No new special-function evaluation is requested.

SymPy checks the logarithmic integral and \(\Gamma'(1)\) as \(-\gamma\). The comparison argument supplies the refusal of a finite approximation; it is not a decimal tolerance check.

## Coach prompts and failures

Ask the learner to distinguish \(\gamma\), the constant, from \(\Gamma(s)\), the function. The integral above is \(-\gamma\), so dropping the sign matters. Subtract the finite expressions before taking their limit; do not separately subtract two infinities. A decimal approximation or a finite harmonic sum is not an exact replacement for \(\gamma\).

On a sign or notation miss, return to the faded step. On a limit miss, repeat the rectangle comparison. The host unit's Gamma drills support the prerequisite; they do not by themselves establish recognition of Euler's constant. Stop at the justified named constant.
