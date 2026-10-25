# Symmetry, reflection, and inverses

Coach card. Original examples on this page were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `symmetry` | 1 | none | `units/02-symmetry-basic-trig/teaching.tex` |
| `kings-queens-rule` | 2 | `symmetry` | `units/10-inverse-kings/teaching.tex` |
| `inverse-functions` | 2 | `basic-integration-by-parts` | the same file |
| `advanced-kings-queens` | 3 | `kings-queens-rule` | `units/25-advanced-kings/teaching.tex` |
| `sneaky-symmetry` | 3 | `symmetry`, `kings-queens-rule` | `units/18-sneaky-symmetry-product/teaching.tex` |

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| Oddness was quoted on an interval that is not symmetric about 0 | `U02-D01`, stored \(0\), then the split `U02-D03`, stored \(2/3\). |
| The two copies were added when they do not form a constant | `U10-D06`, stored \(1-\ln 2\). The faded drill that does add is `U10-D05`, stored \(\pi/4\). |
| The area identity was skipped for a bare inverse | `U10-D01`, stored \(\pi/2-1\). `U31-D01` stores the same value. |
| A definite number was written as an antiderivative | Unit 31 refusal. Set `U31-D08`. |
| An inverse times \(x\) was given the no-factor value | `U31-D07`, stored \(\pi/8\). The faded boundary is `U31-D05`, stored \(\pi/12+\sqrt{3}/2-1\). |
| An advanced copy was quoted as \(\pi/4\) when the sum is not 1 | `U25-D04`, stored \(\pi/8+(\ln 2)/4\). |

`inverse-jailbreaking` has no separate card. The unit note is the lesson. This table only points at its stored drills.

## Odd and even

On an interval \([-a,a]\), an odd integrand that possesses an integral contributes 0. An even integrand doubles the half-interval.

\[
\int_{-2}^{2} x^3\,dx=0, \qquad \int_{-2}^{2} x^2\,dx=\frac{16}{3}.
\]

Unit 02 stores \(\int_{-\pi}^{\pi}\sin x\,dx=0\) as `U02-D01` and \(\int_{-1}^{1}x^2\,dx=2/3\) as `U02-D02`. A sum splits into odd plus even. `U02-D03` is \(x^3+x^2\) on \([-1,1]\), and only the even part survives, value \(2/3\).

The integral has to exist. A singularity in the middle is a separate question. Split there and take limits before you quote 0.

## Reflection

For a continuous \(f\),

\[
\int_a^b f(x)\,dx=\int_a^b f(a+b-x)\,dx.
\]

The substitution \(u=a+b-x\) swaps the limits, and the sign of \(du\) swaps them back. If \(f(x)+f(a+b-x)\) equals a constant \(c\), the integral equals \(c(b-a)/2\).

On \([0,\pi/2]\),

\[
\int_0^{\pi/2}\frac{dx}{1+\tan x}=\frac{\pi}{4}.
\]

The reflection \(x\mapsto \pi/2-x\) replaces \(\tan x\) by \(\cot x\). The new integrand is \(\tan x/(1+\tan x)\). The two integrands add to 1, so twice the integral is the length \(\pi/2\).

Unit 11 stores the sibling \(\int_0^{\pi/2}\sin x/(\sin x+\cos x)\,dx=\pi/4\) as `U11-D07`. Unit 10 stores \(\int_0^{\pi/2}\sin^2 x\,dx=\pi/4\) as `U10-D07`, because the reflection swaps sine and cosine and the squares add to 1. `U10-D04` and `U10-D05` are the same identity on other integrands.

Queen's rule, in the usual contest wording, is this identity on \([0,a]\) with \(u=a-x\). King's rule is the same identity on \([a,b]\). There is one identity. Unit 10 writes it.

## Faded step

For \(\int_0^1 x/(x+1)\,dx\), the reflection \(x\mapsto 1-x\) produces \((1-x)/(2-x)\), and the two integrands do not add to a constant. Compute the integral directly. It is \(1-\ln 2\). The faded lesson is the test, which this integrand fails. `U10-D05` is the drill where the learner writes the reflected integrand and then adds.

## Inverses

An inverse with no extra factor has an area reading. If \(f\) is increasing and continuous,

\[
\int_a^b f^{-1}(y)\,dy = b\,f^{-1}(b)-a\,f^{-1}(a)-\int_{f^{-1}(a)}^{f^{-1}(b)} f(x)\,dx,
\]

when the integrals exist. Unit 10 works \(\int_0^1\arcsin x\,dx=\pi/2-1\) as `U10-D01`, both by parts and by that area identity. `U10-D02` is \(\arctan\) on \([0,1]\), value \(\pi/4-(\ln 2)/2\). `U10-D03` is \(\arccos\) on \([0,1]\), value \(1\).

An inverse multiplied by another factor goes to parts. Put the inverse in the \(u\) slot. Unit 31 is that later drill set. Teach unit 10 first.

## Later reflections

Unit 25 is the same identity on an exponential, a tangent, and a factor of \(x\). Open it when `kings-queens-rule` is solid. The constant-complement test stays the unit 10 test. Unit 25 times that test: `U25-D01`, `U25-D03`, and `U25-D05` add to a constant. `U25-D04` does not, and its stored value stays \(\pi/8+(\ln 2)/4\).

Unit 18 centers a product with a shift so an odd part cancels, and it spots a hidden product rule. Those drills stay in that file. The scaled fences are `habits.md`.

Unit 10 also names \(x\mapsto 1/x\) as the same idea on a half-line. The worked pattern is unit 33. Teach that file's stored drill. The finite fence is `habits.md`.

## Where this goes wrong

Oddness was used on \([0,1]\). The interval has to be symmetric about the point the substitution fixes. On \([0,1]\) the useful reflection is \(x\mapsto 1-x\), when it simplifies the integrand.

The two reflected copies were added when they did not form a constant or a short sum. Write both integrands. Add them only after the sum is easier than either one.

A value of \(\pi/4\) was quoted because the interval was \([0,\pi/2]\). The length of that interval is \(\pi/2\), and \(\pi/4\) is what you get when the two integrands add to 1. Check the sum.

## On a miss

Teach this file, then unit 02 or unit 10. Use the miss table. Set `U02-D01` at difficulty 1 and `U10-D07` at difficulty 2. Advanced copies wait until unit 25. A product \(x f^{-1}(x)\) waits until unit 31. A right value from an even/odd shortcut on the wrong interval still needs the interval named.
