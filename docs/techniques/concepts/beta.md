# Beta: recognizing two endpoint powers

## Status

- Catalog node: `beta`; depth: deferred-noted.
- Round 1: leave unticked. No unit, stored drill, or readiness credit is added.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); definitions and identity in [NIST DLMF 5.12.1](https://dlmf.nist.gov/5.12.E1).
- Prerequisite: substitution and the Gamma integral in [unit 14](../../../units/14-gamma/teaching.tex).

## Definition and the link to Gamma

For real \(a,b>0\), define

\[
B(a,b)=\int_0^1 t^{a-1}(1-t)^{b-1}\,dt,
\qquad
\Gamma(a)=\int_0^\infty e^{-u}u^{a-1}\,du.
\]

The restrictions make both endpoint powers integrable. The Gamma definition is [DLMF 5.2.1](https://dlmf.nist.gov/5.2.E1). The beta identity is

\[
B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}.
\]

To see the connection, multiply the two Gamma integrals. In the positive quadrant set \(u=rt\), \(v=r(1-t)\), with \(r>0\) and \(0<t<1\). The absolute Jacobian is \(r\), so the nonnegative double integral separates into

\[
\int_0^\infty e^{-r}r^{a+b-1}\,dr
\int_0^1t^{a-1}(1-t)^{b-1}\,dt
=\Gamma(a+b)B(a,b).
\]

This explains why the denominator has argument \(a+b\).

## Original micro-example

This is exposition, not a contest answer or a drill id:

\[
\int_0^1 t(1-t)^2\,dt
=B(2,3)
=\frac{1!\,2!}{4!}=\frac1{12}.
\]

An elementary check is \(\int_0^1(t-2t^2+t^3)\,dt=1/2-2/3+1/4=1/12\). For integer arguments, \(\Gamma(n)=(n-1)!\); [DLMF 5.4.1](https://dlmf.nist.gov/5.4.E1) gives that convention. On this small polynomial, direct integration is already enough. Beta is useful as a name for the pattern when the endpoint powers are less convenient.

## Coach prompts and failures

Ask the learner to identify \(a-1\) and \(b-1\) before naming \(B(a,b)\). The common errors are using \(B(1,2)\) for the example, replacing \(\Gamma(n)\) by \(n!\), or applying this improper-integral formula when either endpoint exponent is at most \(-1\). An integral over other limits needs a substitution and its scale factor first.

Teach recognition and the two computations above, then return to the stored unit drills. Keep `beta` unticked. A named identity does not authorize an uncited contest final.
