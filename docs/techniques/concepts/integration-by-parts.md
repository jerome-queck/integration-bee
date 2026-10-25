# Integration by parts

Coach card. Original examples on this page were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

The formula is

\[
\int u\,dv = uv - \int v\,du.
\]

On a definite interval, write the boundary term \([uv]\) before the remaining integral. A boundary term that looks infinite is a limit. Write the limit.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `basic-integration-by-parts` | 2 | `basic-exponential`, `basic-integration` | `units/03-exponential-parts/teaching.tex` |
| `reverse-product-rule` | 2 | `basic-integration-by-parts` | `units/07-abs-reverse-product/teaching.tex` |
| `parts-regular` | 3 | `basic-integration-by-parts` | `units/15-parts-regular/teaching.tex` |
| `gamma` | 3 | `parts-regular` | `units/14-gamma/teaching.tex` |
| `awkward-parts` | 3 | `parts-regular` | `units/22-awkward-parts-pf/teaching.tex` |
| `semi-parts` | 3 | `basic-integration-by-parts` | `units/28-semi-parts/teaching.tex` |
| `reverse-quotient` | 3 | `reverse-product-rule` | `units/27-reverse-quotient/teaching.tex` |

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

## When to use it

Differentiate the factor that gets simpler. That is a polynomial, a logarithm, or an inverse function. Integrate the factor that stays familiar. That is an exponential, a sine, or a cosine.

If the integrand is already exactly a derivative of a product, use the reverse product rule below and skip the parts table. If it is exactly a derivative of a quotient, use the reverse quotient rule and open unit 27.

## One step

On \([0,1]\),

\[
\int_0^1 x e^{2x}\,dx=\frac{e^2+1}{4}.
\]

Take \(u=x\) and \(dv=e^{2x}\,dx\), so \(du=dx\) and \(v=\frac12 e^{2x}\).

\[
\Bigl[\frac{x}{2}e^{2x}\Bigr]_0^1 - \int_0^1 \frac12 e^{2x}\,dx = \frac{e^2}{2} - \frac{e^2-1}{4} = \frac{e^2+1}{4}.
\]

Unit 03 stores the sibling \(\int_0^1 x e^x\,dx=1\) as `U03-D03`.

On \([1,2]\),

\[
\int_1^2 \ln x\,dx = 2\ln 2 - 1.
\]

Take \(u=\ln x\) and \(dv=dx\). The boundary term is \([x\ln x]_1^2=2\ln 2\), and the remaining integral is \(\int_1^2 1\,dx=1\). Unit 03 stores \(\int_1^e \ln x\,dx=1\) as `U03-D05`.

## Faded step

For \(\int_0^{\pi/2} x\cos x\,dx\), put \(x\) in the \(u\) slot. The boundary term is \([x\sin x]_0^{\pi/2}=\pi/2\). The remaining integral is \(\int_0^{\pi/2}\sin x\,dx=1\). The value is \(\pi/2-1\). Unit 15 stores that value as `U15-D04`.

## Two steps, then solve

\(\int e^x\sin x\,dx\) comes back after two steps. Call the integral \(I\). Differentiate \(e^x\) twice and integrate \(\sin x\) twice, keep the signs, and solve the equation \(I=\cdots - I\). Unit 15 stores the antiderivative \(\frac12 e^x(\sin x-\cos x)\) as `U15-D02`. Differentiate that expression if you want the check. The definite integral on \([0,\pi]\) is `U15-D03`.

## Reverse product rule

The product rule says \((fg)'=f'g+fg'\). An integrand that matches the right-hand side integrates to \(fg\).

Unit 07 stores

\[
\int_0^{\pi/2}(\sin x+x\cos x)\,dx=\frac{\pi}{2}
\]

as `U07-D04`, which is \([x\sin x]_0^{\pi/2}\). The faded drill `U07-D05` is the derivative of \(e^x\sin x\).

Name \(f\) and \(g\) before expanding. If you cannot name them, you are in ordinary parts.

## Reverse quotient rule

The quotient rule says \((f/g)'=(f'g-fg')/g^2\). Unit 27 stores

\[
\int\frac{x\cos x-\sin x}{x^2}\,dx=\frac{\sin x}{x}
\]

as `U27-D01`, with \(f=\sin x\) and \(g=x\).

On \((0,\pi/2]\) the same antiderivative has a limit at the missing endpoint, because \((\sin x)/x\to 1\). The definite value is

\[
\lim_{\varepsilon\to 0^+}\Bigl[\frac{\sin x}{x}\Bigr]_{\varepsilon}^{\pi/2}=\frac{2}{\pi}-1.
\]

That definite reading is original. The antiderivative is the stored one. A numerator that is only \(f'\), with no minus term, is a logarithmic derivative. That move is unit 24.

## A reduction

When the same shape carries an integer \(n\), parts produces a relation and a base, and you unroll. Two families are already written out.

Unit 14 defines \(J_n=\int_0^{\infty} x^n e^{-x}\,dx\). The base is \(J_0=1\), and \(J_n=n J_{n-1}\), so \(J_n=n!\). The unit stores \(J_2=2\) as `U14-D10` and \(J_4=24\) as `U14-D09`. A substitution that removes the power in one step finishes the integral. The reduction waits.

Unit 15 writes \(I_n=\int_0^1 x^n\ln x\,dx=-1/(n+1)^2\) for an integer \(n\ge 0\). The same identity, differentiated in a parameter, is `docs/techniques/introduce-constant.md`.

The trigonometric reduction \(I_n=\int_0^{\pi/2}\sin^n x\,dx\) is `trigonometric.md` and unit 20.

## Semi-parts

For \(p(x)e^x\) with \(p\) a polynomial, the answer has the shape \(q(x)e^x\) with \(\deg q=\deg p\). Assume the coefficients, differentiate, and match. Unit 03's value \(\int_0^1 x e^x\,dx=1\) is the degree-1 case: the antiderivative is \((x-1)e^x\). Unit 28 stores the longer polynomials. Teach that file once this match is familiar.

## Where this goes wrong

The exponential was differentiated and the polynomial was integrated. The remaining integral got harder. Swap \(u\) and \(dv\).

The boundary term was dropped on a definite integral. Write \([uv]\) even when it is zero, and say why it is zero.

A cyclic integral was expanded forever. Stop at the second return and solve for \(I\).

Parts was started on a pure \(du/u\) or on a derivative of a product. Those finish in one recognition.

## On a miss

Teach this file, then the unit in the table. Set `U03-D03` or `U03-D05` while the node is learning. Set `U15-D04` when the one-step case is solid. Leave `gamma` on its unit drills. A correct final answer that used the wrong factor in the \(u\) slot still needs the choice named.
