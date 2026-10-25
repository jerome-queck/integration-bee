# Substitution families

Coach card. Original examples on this page were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `basic-integration` | 1 | none | `units/01-foundations-substitution/teaching.tex` |
| `basic-u-substitution` | 1 | `basic-integration` | the same file |
| `basic-exponential` | 1 | `basic-integration` | `units/03-exponential-parts/teaching.tex` |
| `intermediate-u-substitution` | 2 | `basic-u-substitution` | `units/06-intermediate-u-sub/teaching.tex` |
| `forced-u-sub` | 2 | `intermediate-u-substitution` | `units/13-forced-u-sub/teaching.tex` |
| `power-substitution` | 3 | `intermediate-u-substitution` | `units/19-power-sneaky-usub/teaching.tex` |

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| The constant in \(du\) was omitted | `U01-D01`, stored \(\ln 2\). The higher power with the same constant is `U01-D03`, stored \((e-1)/2\). |
| The definite limits were left in \(x\) | `U06-D01`, stored \((e-1)/4\). |
| \(x e^x\) was treated as a substitution | `U03-D03`, stored \(1\). |
| The derivative was missing and \(x\) was not solved for | The worked example on this card, then `U13-D01`, after `intermediate-u-substitution` is solid. |
| A root was not cleared before dividing | The power example on this card, then a unit 19 drill. `U19-D08` stores \(\pi/2\) and stops. |

## When to use it

Use a substitution when one factor is a constant times the derivative of an inside function, and the rest of the integrand is a function of that inside function. On a definite integral, change the limits and leave the answer in the new variable.

The standard antiderivatives that need no substitution are the unit 01 warmup. \(\int_0^1 dx/(1+x^2)=\pi/4\) is `U01-D08`. \(\int x^n\,dx=x^{n+1}/(n+1)\) for \(n\neq -1\), and \(\int dx/x=\ln|x|\).

## Linear and \(du/u\)

On \([0,1]\),

\[
\int_0^1 e^{3x+1}\,dx=\frac{e^4-e}{3}.
\]

The inside is \(3x+1\), its derivative is 3, and the integrand is already a function of that inside. The same pattern is \(a^x\). Unit 03 stores \(\int_0^1 2^x\,dx=1/\ln 2\) as `U03-D07`.

A pure \(du/u\) has a numerator that is the derivative of the denominator. On \([1,e]\), \(\int_1^e dx/x=1\). On \([0,1]\),

\[
\int_0^1\frac{x^2}{x^3+1}\,dx=\frac{\ln 2}{3},
\]

because the derivative of \(x^3+1\) is \(3x^2\). The factor \(1/3\) is the whole extra step. Unit 01 stores the sibling \(\int_0^1 2x/(x^2+1)\,dx=\ln 2\) as `U01-D01`.

## A chain that is not linear

On \([0,2]\),

\[
\int_0^2\frac{2x+1}{x^2+x+1}\,dx=\ln 7.
\]

Let \(u=x^2+x+1\). Then \(du=(2x+1)\,dx\). The limits are \(u(0)=1\) and \(u(2)=7\). The integral is \(\int_1^7 du/u\).

Unit 01's faded drill `U01-D03` is \(\int_0^1 x e^{x^2}\,dx=(e-1)/2\). The derivative of the exponent is \(2x\), so the constant in front is \(1/2\). Unit 06 stores the higher power \(\int_0^1 x^3 e^{x^4}\,dx=(e-1)/4\) as `U06-D01`, and the log chain \(\int dx/(x\ln x)\) as `U06-D03`.

## Faded step

For \(\int_0^1 x^3/(x^4+1)\,dx\), name \(u\), name the constant in front of \(du\), and change both limits before integrating. The derivative of \(x^4+1\) is \(4x^3\), so the constant is \(1/4\). The value is \((\ln 2)/4\).

## Forced substitution

Sometimes the inside function's derivative is not sitting in the integrand. Solve for \(x\) and replace \(dx\).

On \([0,1]\),

\[
\int_0^1 e^{\sqrt{x}}\,dx=2.
\]

Let \(u=\sqrt{x}\), so \(x=u^2\) and \(dx=2u\,du\), with limits \(0\) and \(1\). The integral becomes \(2\int_0^1 u e^u\,du\). One parts step, \(u\) differentiated and \(e^u\) integrated, gives \(2[(u-1)e^u]_0^1=2\). The parts step is `integration-by-parts.md`. Unit 13 is the drill set for this shape. Teach the unit's stored drill after this example. Do not invent a further forced integral.

## Power substitution

A radical becomes a polynomial when \(x=u^n\) for an \(n\) that clears every root. After the substitution, divide the rational function before expanding.

On \([0,1]\),

\[
\int_0^1\frac{\sqrt{x}}{1+x}\,dx=2-\frac{\pi}{2}.
\]

Let \(x=u^2\), so \(dx=2u\,du\) and \(\sqrt{x}=u\), with limits still \(0\) and \(1\). The integral is

\[
\int_0^1\frac{2u^2}{1+u^2}\,du=\int_0^1 2\left(1-\frac{1}{1+u^2}\right)du=2\bigl[u-\arctan u\bigr]_0^1=2-\frac{\pi}{2}.
\]

Unit 19 stores the power drills. This example is the move. `sneaky-u-sub` is the next four drills in that file. The scaled fence is `habits.md`.

## Where this goes wrong

The constant in \(du\) was omitted, so a \(2x\) in the derivative became a missing factor of \(1/2\). Put the constant in before integrating.

The definite limits were left in \(x\). Write \(u\) at each endpoint, or back-substitute and then use the original limits. One of those two, and the same one throughout.

The leftover factor still depends on \(x\) after the substitution. That integral wants parts, a second substitution, or partial fractions.

The integrand is \(x e^x\). The exponential's derivative is itself, and the \(x\) is not the derivative of the exponent. That is parts. Unit 03 stores \(\int_0^1 x e^x\,dx=1\) as `U03-D03`.

## On a miss

Teach this file, then the unit in the table. Use the miss table. Set `U01-D01` at difficulty 1, `U06-D01` at difficulty 2, and the unit 13 or unit 19 drill only after those are solid. A correct value reached by the wrong substitution still needs the substitution named.
