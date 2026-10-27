# Vector calculus: optional Gaussian background

## Status

- Catalog node: `vector-calc`; status: ready; depth: card; unit: `30-gaussian-dirichlet`.
- Round 1: optional, with no readiness gate. Content readiness does not award a learner mastery tick.
- Source: [syllabus §1](../../../sources/UK_University_Integration_Bee_Syllabus.pdf), which excludes vector calculus from the Round 1 requirement; [unit 30](../../../units/30-gaussian-dirichlet/teaching.tex) supplies the optional Gaussian sketch.
- Use: explain where the Gaussian constant comes from when the learner asks. This note adds no multivariable contest problem or final.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `vector-calc` | 4, optional recognition | `basic-u-substitution`, `gaussian-integrals` | [unit 30](../../../units/30-gaussian-dirichlet/teaching.tex), optional polar recognition |

The recognition drill below is an oral worked/faded/bare pattern. The optional node has no automatic drill queue. `U30-D01` and `U30-D03` remain stored one-variable follow-ups, with practice credit on their existing `advanced-gaussian` node. Their correct answers alone do not demonstrate understanding of a change of area coordinates or automatically credit `vector-calc`.

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

## Recognition drill

**Worked.** Read the finite-disk computation above and identify the radial variable, angular interval, area factor, and increasing-domain limit. The conclusion is the existing full-line value `U30-D03`.

**Faded.** Hide the factor multiplying \(dr\,d\theta\). Ask the learner to differentiate \(x=r\cos\theta\), \(y=r\sin\theta\) and recover the absolute determinant \(r\), then explain why the positive square root is used.

**Bare.** Give only \(I=\int_{-\infty}^{\infty}e^{-x^2}\,dx\) and ask for the polar setup for \(I^2\), its radial bounds, and the reason the half-line result is half as large. Accept the derivation above; reject a setup without \(r\) or an angular range of length \(\pi\) for the whole plane. This is a recognition explanation, not a new contest answer or a `practice check` id.

Stop after the requested background. Return to unit 30 for scaling or to unit 11 for elementary Gaussian cousins. This card is ready to teach but is not a prerequisite for Round 1; using a quoted Gaussian value does not automatically establish `vector-calc` mastery.
