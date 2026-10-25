# Algebra before a technique

Coach card. These moves finish an integral, or they shorten it until substitution, parts, or partial fractions applies. Original examples were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

The longer writeup of adding and subtracting a constant, and of a small parameter, is `docs/techniques/introduce-constant.md`. This page is the decision to open that note.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `algebra-manipulation` | 2 | `basic-u-substitution` | `units/01-foundations-substitution/teaching.tex` |
| `sneaky-algebra` | 3 | `algebra-manipulation` | `units/12-modified-sneaky-algebra/teaching.tex` |
| `modified-textbook` | 3 | `algebra-manipulation` | the same file |
| `dutis` | 3 for a fixed interval, 4 for a moving endpoint | `basic-integration` | `docs/techniques/introduce-constant.md`, then `units/34-frullani-feynman/teaching.tex` |
| `feynman` | 4 | `basic-integration` | `units/34-frullani-feynman/teaching.tex` |

`dutis` is deferred in `trackers/catalog.json` because it has no unit. The fixed-interval drills are `U11-D13` through `U11-D15` on `special-wildcard`. A moving endpoint is unit 34. Leave `batis` unticked. `feynman` is the catalog node for that moving endpoint. The row above points at unit 34. It does not tick `batis`.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| An improper fraction was decomposed before the division | `docs/techniques/introduce-constant.md`, the worked split of \((x+1)/(x+2)\). |
| A quadratic with no completed square was integrated as \(1/x\) | The arctangent on this card, value \(\arctan 2-\pi/4\). |
| A parameter was built for a substitution that already finishes | `U34-D07`, stored \((\ln 2)^2/2\). |
| A moving endpoint was differentiated as a fixed interval | Unit 34. The worked case there has derivative \(6\) at \(t=2\). That case is not a drill. Leave `batis` unticked. |
| \(\pi/2\) was written for \((\cos x-\cos 2x)/x\) | `U34-D03`, stored \(\ln 2\). |
| \(-1/9\) was written for \((x^2-1)/\ln x\) | `U34-D04`, stored \(\ln 3\). |
| A fixed-interval parameter was the miss | `U11-D13`, stored \(-1/25\). Leave `batis` unticked. |

`sneaky-algebra` and `modified-textbook` are habits on top of this card. Their stored drills are unit 12. The scaled fences are `habits.md`.

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

## Add and subtract

When the numerator is a constant away from the denominator, or from its derivative, add and subtract that constant.

\[
\frac{x+1}{x+2}=1-\frac{1}{x+2}.
\]

`docs/techniques/introduce-constant.md` integrates that on \([0,1]\) and gets \(1+\ln(2/3)\). The same note does the coefficient \(3\) in \((3x+5)/(x+1)=3+2/(x+1)\), value \(3+2\ln 2\) on \([0,1]\). Use the note's fences. They are already checked.

Do this before a substitution and before partial fractions. After the split, the pieces are the integrals you actually compute.

## Complete the square

A quadratic \(x^2+bx+c\) with no real roots becomes a shift of \(u^2+a^2\), and the integral is an arctangent.

On \([0,1]\),

\[
\int_0^1\frac{dx}{x^2+2x+2}=\int_0^1\frac{dx}{(x+1)^2+1}=\arctan 2-\frac{\pi}{4}.
\]

The shift is \(u=x+1\). The limits move with it, from 1 to 2. \(\int du/(u^2+1)=\arctan u\).

## Rationalize a trig sum

Multiply by the conjugate when a sine or a cosine sits in a denominator next to 1.

On \([0,\pi/4]\),

\[
\int_0^{\pi/4}\frac{dx}{1+\sin x}=2-\sqrt{2}.
\]

The conjugate is \(1-\sin x\). The denominator becomes \(\cos^2 x\), and the integrand becomes \(\sec^2 x-\sec x\tan x\), whose antiderivative is \(\tan x-\sec x\). The endpoints are \((1-\sqrt{2})-(-1)\).

A rational function of sine and cosine that does not simplify this way opens `trigonometric.md` at the half-angle substitution.

## A fixed-interval parameter

Differentiating under the integral sign, on a fixed interval, is the syllabus form whose drills live on unit 11. The algebra note works \(\int_0^1 x^3\ln x\,dx=-1/16\) by differentiating \(\int_0^1 x^a\,dx=1/(a+1)\) at \(a=3\). The stored drill `U11-D13` is the same family at \(a=4\), value \(-1/25\). `U11-D14` differentiates \(\int_0^{\infty} e^{-ax}\,dx=1/a\) at \(a=2\). `U11-D15` integrates the parameter and stores \(\ln 4\).

Use a parameter when the integrand is a derivative, in that parameter, of a family you already know. A substitution that already finishes the integral does not need a parameter. Unit 34 stores that refusal as `U34-D07`.

## A moving endpoint

If the endpoints move with the parameter, the derivative picks up the fundamental theorem at the ends. Unit 34 states

\[
\frac{d}{dt}\int_{a(t)}^{b(t)} f(x,t)\,dx
=\int_{a(t)}^{b(t)}\partial_t f(x,t)\,dx
+f(b(t),t)\,b'(t)-f(a(t),t)\,a'(t).
\]

The unit's worked case is \(\int_0^t tx\,dx\). At \(t=2\) the integral equals 4 and the derivative equals 6. That case is not a drill, and it does not tick `dutis`. The stored parameter works `U34-D05`, fades `U34-D04`, and sets bare `U34-D08`. Frullani in the same file works `U34-D01`, fades `U34-D02`, and sets bare `U34-D03`. Teach both from `units/34-frullani-feynman/teaching.tex`.

## Faded step

Rewrite \((x^2+2x)/(x^2+2x+1)\) as a constant minus a square in the denominator, then integrate from 0 to 1. The algebra note already displays the value \(1/2\). The faded work is the rewrite, \(1-1/(x+1)^2\).

## Where this goes wrong

A substitution began while the numerator was still a sum of the derivative and a leftover. Split first. The leftover is a shorter integral.

A quadratic with no \(x\) term in the squared binomial was integrated as \(1/x\). Complete the square, then recognize \(u^2+a^2\).

A parameter was introduced for \(\int_0^1 2x/(x^2+1)\,dx\). That is `U01-D01`, a substitution.

An endpoint that moves was differentiated as if the interval were fixed. The two fundamental-theorem terms are unit 34.

## On a miss

An algebraic miss teaches `docs/techniques/introduce-constant.md` when the move is add-and-subtract or a fixed parameter, and this file when the move is completing the square or rationalizing. Use the miss table. A moving endpoint teaches unit 34 and the `feynman` row. That unit works `U34-D05`, fades `U34-D04`, and sets bare `U34-D08`. Frullani works `U34-D01`, fades `U34-D02`, and sets bare `U34-D03`. Set `U11-D13` for the fixed-interval parameter. Leave `dutis` unticked.
