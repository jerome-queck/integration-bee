# Beta: recognizing two endpoint powers

## Status

- Catalog node: `beta`; status: ready; depth: card; unit: `14-gamma`.
- Optional syllabus lesson, with no Round 1 gate. Ready means the lesson is available, not that the learner has mastered it.
- Source: [syllabus §2](../../../sources/UK_University_Integration_Bee_Syllabus.pdf); definitions and identity in [NIST DLMF 5.12.1](https://dlmf.nist.gov/5.12.E1).
- Prerequisite: substitution and the Gamma integral in [unit 14](../../../units/14-gamma/teaching.tex).

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `beta` | 3 | `basic-u-substitution`, `gamma` | [unit 14, optional Beta recognition](../../../units/14-gamma/teaching.tex) |

The recognition drill below follows the worked, faded, and bare pattern in `pedagogy/README.md`. It is an oral check of this card's exposition; it has no machine drill id and is not submitted to `practice check`. It does not supply automatic tick evidence.

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

## Worked recognition drill

This is exposition, not a contest answer or a drill id:

\[
\int_0^1 t(1-t)^2\,dt
=B(2,3)
=\frac{1!\,2!}{4!}=\frac1{12}.
\]

An elementary check is \(\int_0^1(t-2t^2+t^3)\,dt=1/2-2/3+1/4=1/12\). For integer arguments, \(\Gamma(n)=(n-1)!\); [DLMF 5.4.1](https://dlmf.nist.gov/5.4.E1) gives that convention. On this small polynomial, direct integration is already enough. Beta is useful as a name for the pattern when the endpoint powers are less convenient.

## Faded step

Hide the worked line. Give only

\[
a-1=1,\qquad b-1=2,\qquad
B(a,b)=\frac{\Gamma(\square)\Gamma(\square)}{\Gamma(\square)}.
\]

Ask for the three arguments, the factorial indices, and the integral's value. The coach key is \(2,3,5\), then \(1!,2!,4!\), then \(1/12\). Both endpoint exponents exceed \(-1\).

## Bare recognition and refusal

With the worked line closed, ask the learner to name the Beta integral for \(t(1-t)^2\) on \([0,1]\), state the endpoint conditions, and give a direct polynomial check. Then ask whether the same definition would give a finite value for \(\int_0^1 t^{-1}(1-t)^2\,dt\). The answer is no: the first argument would be \(0\), and near zero the integrand behaves like \(1/t\). A successful answer identifies \(B(2,3)\), reproduces \(1/12\), and refuses the divergent variant.

The polynomial value and Gamma ratio were checked with SymPy. This remains an original recognition exercise, not a new contest answer or stored drill.

## Coach prompts and failures

Ask the learner to identify \(a-1\) and \(b-1\) before naming \(B(a,b)\). The common errors are using \(B(1,2)\) for the example, replacing \(\Gamma(n)\) by \(n!\), or applying this improper-integral formula when either endpoint exponent is at most \(-1\). An integral over other limits needs a substitution and its scale factor first.

On an index error, repeat the faded step. On a convergence error, compare the two endpoint powers with \(t^p\) for \(p>-1\). The host unit's existing Gamma drills support the prerequisite; a correct Gamma drill alone does not establish Beta recognition. A named identity does not authorize an uncited contest final.
