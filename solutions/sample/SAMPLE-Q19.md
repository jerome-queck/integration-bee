# SAMPLE-Q19

- Problem: `sources/Integration_Competition_Sample_problems.pdf`, p. 2, question 19
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`, p. 1, answer 19
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf`, p. 20, question 19

## Status: resolved symbolic certificate

Catalog row `SAMPLE-Q19` is `verify: sympy`. The gate proves the derivative identity on \(-1<x<1\), with real square roots and the principal real arccosine. The derived antiderivative agrees with the printed answer and worked source. Numerical probes alone are not used as a proof.

## Problem

\[
\int x\sqrt{\frac{1-x^2}{1+x^2}}\,dx.
\]

## Solution

The solutions PDF sets \(u=x^2\), then \(u=\cos 2v\). Using \(1-u=2\sin^2 v\) and \(1+u=2\cos^2 v\), the integral reduces to

\[
\frac12\bigl(\sin 2v-2v\bigr)+C=\frac12\bigl(\sin(\arccos(x^2))-\arccos(x^2)\bigr)+C.
\]

The PDF notes that another method can produce an equivalent expression that looks different.

To check the branches explicitly, \(\sin(\arccos(x^2))=\sqrt{1-x^4}\) for \(|x|\le1\). Write

\[
F(x)=\frac12\left(\sqrt{1-x^4}-\arccos(x^2)\right).
\]

For \(-1<x<1\), both \(1-x^2\) and \(1+x^2\) are positive, so differentiation and the positive square-root product identity give

\[
\begin{aligned}
F'(x)
&=\frac{-x^3+x}{\sqrt{1-x^4}}\\
&=\frac{x(1-x^2)}{\sqrt{(1-x^2)(1+x^2)}}\\
&=x\sqrt{\frac{1-x^2}{1+x^2}}.
\end{aligned}
\]

The factor \(x\) keeps its sign, so the argument covers negative \(x\) and \(x=0\) as well as positive \(x\). The real integrand and antiderivative extend continuously to the endpoints \(x=\pm1\); the derivative certificate concerns the open interval, where all intermediate denominators are nonzero.

## Final answer

\[
\frac12\bigl(\sin(\arccos(x^2))-\arccos(x^2)\bigr)+C.
\]

## SymPy self-check

`verify/sample_certificates.py` supplies the exact real-domain derivative certificate through `pack_gate.proven`. It checks the original radical integrand and establishes the symbolic identity with the permitted square-root branches.

The candidate must also be continuous throughout \((-1,1)\). This rejects
piecewise constant jumps that symbolic differentiation alone can erase.
Learner grading uses this same certificate, so a positive-side-only answer
cannot bypass its branch checks through the generic absolute-value matcher.

`solutions/sample_self_check.py` reproves the stored row and requires `check_q19` to accept both the algebraic form and the printed trigonometric form with an additive constant. Sanity probes cover both signs of \(x\) and zero. Wrong-answer controls reject zero, the wrong sign on the arccosine term, and twice the antiderivative.
