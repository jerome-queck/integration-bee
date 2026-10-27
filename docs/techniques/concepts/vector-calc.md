# Vector calculus: optional Gaussian background

## Status

- Catalog node: `vector-calc`; depth: deferred-noted.
- Round 1: leave unticked. There is no unit or drill assigned to this node.
- Source: [syllabus §1](../../../sources/UK_University_Integration_Bee_Syllabus.pdf), which excludes vector calculus from the Round 1 requirement; [unit 30](../../../units/30-gaussian-dirichlet/teaching.tex) supplies the optional Gaussian sketch.
- Use: explain where the Gaussian constant comes from when the learner asks. This note adds no multivariable contest problem or final.

## When to mention it

Vector calculus studies vector fields and their derivatives and integrals, including integrals over curves and surfaces. Unit 30 needs only one piece of multivariable integration: changing a double integral from Cartesian coordinates \((x,y)\) to polar coordinates \((r,\theta)\). A learner can use the stored Gaussian values and one-variable scaling without this background. Teach [the Gaussian card](gaussian-dirichlet.md) first.

## The optional sketch, with its assumptions

Let \(I=\int_{-\infty}^{\infty}e^{-x^2}\,dx\). It is positive and finite: for \(x\geq1\), \(e^{-x^2}\leq e^{-x}\), and the integrand is even. Multiplying two copies and integrating the nonnegative product gives

\[
I^2=\iint_{\mathbb R^2}e^{-(x^2+y^2)}\,dx\,dy.
\]

Use \(x=r\cos\theta\), \(y=r\sin\theta\). Here \(r\geq0\) is distance from the origin and \(0\leq\theta<2\pi\) is the angle. The area factor is \(dx\,dy=r\,dr\,d\theta\): the absolute Jacobian determinant is \(r\). On the disk of radius \(R\),

\[
\int_0^{2\pi}\int_0^R e^{-r^2}r\,dr\,d\theta
=\pi(1-e^{-R^2}).
\]

Increasing the disks to the whole plane and using nonnegativity gives \(I^2=\pi\). Since \(I>0\), \(I=\sqrt\pi\). Evenness gives the half-line value \(\sqrt\pi/2\), stored as `U30-D01`; the full line is `U30-D03`. This is the derivation of those existing values, not a new drill.

## Coach prompts and failures

Ask why the area factor is \(r\), why the angular interval has length \(2\pi\), and why the positive square root is selected. A missing \(r\), a half-plane used for the full plane, or a full-line value copied onto a half-line changes the answer. Nonnegative integrands justify the product and increasing-domain limits here; an arbitrary improper double integral needs its own justification.

Stop after the requested background. Return to unit 30 for scaling or to unit 11 for elementary Gaussian cousins. Do not turn this explanation into a prerequisite for Round 1 or a tick of `vector-calc`.
