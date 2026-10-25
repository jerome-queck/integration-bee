# Trigonometric integrals, trig substitution, and the half-angle

Coach card. Original examples on this page were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `basic-trig-integrals` | 1 | `basic-integration` | `units/02-symmetry-basic-trig/teaching.tex` |
| `basic-trig-substitution` | 2 | `basic-trig-integrals`, `basic-u-substitution` | `units/04-trig-sub-circle/teaching.tex` |
| `area-partial-circle` | 2 | `basic-trig-substitution` | the same file |
| `intermediate-trig-integrals` | 2 | `basic-trig-integrals` | `units/09-intermediate-trig/teaching.tex` |
| `intermediate-trig-substitution` | 3 | `basic-trig-substitution` | the same file |
| `trig-identities` | 3 | `intermediate-trig-integrals` | `units/16-trig-id-trig-sub/teaching.tex` |
| `intermediate-trig-sub-ch2` | 3 | `basic-trig-substitution` | the same file |
| `weierstrass` | 3 | `intermediate-trig-integrals` | `units/26-weierstrass/teaching.tex` |
| `wallis` | 3 | `intermediate-trig-integrals` | `units/20-wallis/teaching.tex` |
| `advanced-trig-integrals` | 3 | `trig-identities` | `units/29-advanced-trig/teaching.tex` |
| `advanced-trig-substitution` | 3 | `intermediate-trig-substitution` | `units/21-advanced-trig-sub/teaching.tex` |
| `periodicity` | 3 | `basic-trig-integrals` | `units/23-periodicity-speed/teaching.tex` |

`speed-bashing` shares unit 23. The unit's rule is to split a sum and integrate the pieces. The scaled fence is `habits.md`.

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| A standard secant-squared was expanded | `U02-D06`, stored \(1\). |
| A pure sine power was sent through \(t=\tan(x/2)\) | `U20-D01`, stored \(3\pi/16\), or `U29-D01`, stored \(5\pi/32\). |
| A leftover factor of \(\sin x\) was reduced | `U29-D04`, stored \(1/6\). The same refusal in unit 20 is `U20-D06`, stored \(2/15\). |
| \(\sec^2 x\) was already present and the half-angle was used | `U29-D08`, stored \(1\). `U29-D03` is the faded substitution, stored \(\frac12\tan^2 x\). |
| \(\tan^2 x\) was treated as a Wallis power | `U29-D02`, stored \(1-\pi/4\). `U09-D04` stores the same value. |
| Both powers were even and the reduction was skipped | Bare `U29-D06`, stored \(\pi/32\). |
| A radical was expanded as a binomial | `U04-D01`, stored \(\pi/2\). A later radical is `U21-D08`, stored \(\pi/4\). |
| A full-period cross term was given the value of the square | `U23-D01`, stored \(0\). The square of a sum is `U23-D02`, stored \(3\pi\). |
| The \([0,\pi]\) formula was quoted on a shorter interval | `U26-D07`, stored \(\frac{2\sqrt{3}}{3}\arctan\frac{1}{3}\). The full interval is `U26-D02`, stored \(\pi/\sqrt{3}\). |

## Basic antiderivatives

\(\int\sin x\,dx=-\cos x\), \(\int\cos x\,dx=\sin x\), \(\int\sec^2 x\,dx=\tan x\). Unit 02 stores \(\int_0^{\pi/4}\sec^2 x\,dx=1\) as `U02-D06`.

A tangent is a \(du/u\). Unit 02 stores

\[
\int_0^{\pi/4}\tan x\,dx=\frac{\ln 2}{2}
\]

as `U02-D08`, with \(u=\cos x\).

## Powers

An odd power of sine or cosine peels one factor and substitutes the other function.

On \([0,\pi/2]\),

\[
\int_0^{\pi/2}\sin^3 x\,dx=\frac{2}{3}.
\]

Write \(\sin^3 x=(1-\cos^2 x)\sin x\). Let \(u=\cos x\). The limits run from 1 to 0, and the sign from \(du\) flips them back:

\[
\int_0^1(1-u^2)\,du=\frac{2}{3}.
\]

An even power uses the double angle. Unit 09 stores \(\int_0^{\pi}\sin^2 x\,dx=\pi/2\) as `U09-D01`, from \(\sin^2 x=(1-\cos 2x)/2\). On \([0,\pi/2]\) the same identity plus the reflection in `symmetry-kings.md` gives \(\pi/4\), which unit 10 stores as `U10-D07`.

## A reduction for \(I_n\)

Define

\[
I_n=\int_0^{\pi/2}\sin^n x\,dx=\int_0^{\pi/2}\cos^n x\,dx.
\]

The two families agree by \(x\mapsto\pi/2-x\). The bases are \(I_0=\pi/2\) and \(I_1=1\). For \(n\ge 2\),

\[
I_n=\frac{n-1}{n}I_{n-2}.
\]

Then \(I_2=\pi/4\) and \(I_4=(3/4)I_2=3\pi/16\). Unit 20 stores \(I_4\) as `U20-D01`. The odd-power substitution above is \(I_3=(2/3)I_1=2/3\). The two methods agree. Use the substitution when one factor finishes the integral. Use the reduction when the index drops by 2 and you still want a number. `U20-D02` is the drill that refuses the reduction, because a double angle finishes it.

The speed unrolls are in unit 20: the even line through `U20-D05`, the odd line through `U20-D04`, and the alternating line through `U15-D11`. Unit 14 times the factorial line. Each check is a stored drill.

## Trig substitution and circle area

| Radical | Substitution |
|---|---|
| \(\sqrt{a^2-x^2}\) | \(x=a\sin\theta\), or read a circle area |
| \(\sqrt{a^2+x^2}\) | \(x=a\tan\theta\), or \(x=a\sinh u\) |
| \(\sqrt{x^2-a^2}\) | \(x=a\sec\theta\) |

On \([0,1/2]\),

\[
\int_0^{1/2}\frac{dx}{\sqrt{1-x^2}}=\arcsin\frac12=\frac{\pi}{6}.
\]

Unit 04 stores the full quarter \(\int_0^1 dx/\sqrt{1-x^2}=\pi/2\) as `U04-D01`, and the area \(\int_0^1\sqrt{1-x^2}\,dx=\pi/4\) as `U04-D02`. The area is a quarter unit disk. The substitution \(x=\sin\theta\) reproduces it, and the geometry is enough when the limits are the obvious radii. `U04-D03` is the radius-2 form, value \(\pi/2\).

Unit 09 stores \(\int_0^1 dx/\sqrt{x^2+1}=\ln(1+\sqrt{2})\) as `U09-D05`. Unit 21 chooses \(\sec\), \(\sinh\), or \(\tan\) from the radicand and changes limits first. Open it when the three-row table is solid.

## Half-angle substitution

When the integrand is rational in \(\sin x\) and \(\cos x\), and no shorter substitution works,

\[
t=\tan\frac{x}{2},\qquad
\sin x=\frac{2t}{1+t^2},\qquad
\cos x=\frac{1-t^2}{1+t^2},\qquad
dx=\frac{2\,dt}{1+t^2}.
\]

\(\tan x=2t/(1-t^2)\) is the quotient of the first two. Use it when a tangent is already present. The map is continuous on \((-\pi,\pi)\). An odd multiple of \(\pi\) in the interior is a split. An endpoint at \(\pi\) makes the \(t\)-integral improper.

On \([0,\pi/2]\),

\[
\int_0^{\pi/2}\frac{dx}{2+\cos x}=\frac{\pi\sqrt{3}}{9}.
\]

The limits are \(t=0\) and \(t=1\). Then \(2+\cos x=(3+t^2)/(1+t^2)\), so the integrand collapses to \(2/(t^2+3)\). 

\[
\int_0^1\frac{2\,dt}{t^2+3}=\frac{2}{\sqrt{3}}\arctan\frac{1}{\sqrt{3}}=\frac{2}{\sqrt{3}}\cdot\frac{\pi}{6}=\frac{\pi}{3\sqrt{3}}=\frac{\pi\sqrt{3}}{9}.
\]

This integral is original exposition. It is not a stored drill.

Unit 09 works \(\int_0^{\pi/3} dx/(1+\cos x)=\sqrt{3}/3\), whose antiderivative is \(\tan(x/2)\). That pass is not a drill. Unit 26 stores \(\int_0^{\pi/2} dx/(1+\sin x)=1\) as `U26-D01`. The limits there are \(0\) and \(1\), not \(0\) and \(\infty\). Unit 26 works `U26-D01`, fades the limits on `U26-D08` (stored \(\sqrt{3}\pi/9\)), and sets bare `U26-D02` (stored \(\pi/\sqrt{3}\)). That file is the note a miss of this substitution names.

## Periodicity

On \([0,2\pi]\), for positive integers \(m\neq n\),

\[
\int_0^{2\pi}\sin(mx)\sin(nx)\,dx=0,
\]

and the cosine product does the same. The square \(\int_0^{2\pi}\sin^2(mx)\,dx=\pi\).

The product-to-sum check for \(m=1\), \(n=2\) is \(\sin x\sin 2x=\frac12(\cos x-\cos 3x)\), whose integral on a full period is 0. Unit 23 stores \(\int_0^{2\pi}\sin(3x)\sin(5x)\,dx=0\) as `U23-D01`, and the square of a sum of three sines as \(3\pi\) in `U23-D02`. Cross terms die. Diagonal squares remain.

## Where this goes wrong

A pure power of sine was sent through \(t=\tan(x/2)\). The reduction in unit 20, or one peeled factor, is the shorter path.

A rational function of \(\tan x\) that already contains \(\sec^2 x\) was sent through the half-angle. The substitution is \(u=\tan x\). Unit 09 stores that as `U09-D04` and `U09-D08`.

The half-angle was used across \(x=\pi\) without a split. The tangent of the half-angle is discontinuous there.

\(\sqrt{a^2-x^2}\) was expanded as a binomial. The substitution or the circle area finishes it.

A full-period cross term was given the value of the square. The square is the case \(m=n\).

## On a miss

Teach this file. Use the miss table. A half-angle miss then opens unit 26. A power miss opens unit 09, unit 20, or unit 29. Set `U02-D06` at difficulty 1, `U04-D01` at difficulty 2, `U29-D04` when a factor should have been saved, and `U26-D01` only after the early pass in unit 09 is familiar. A shorter interval than \([0,\pi]\) sets `U26-D07`. A correct value from the wrong substitution still needs the substitution named.
