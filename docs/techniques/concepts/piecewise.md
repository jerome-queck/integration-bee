# Absolute values and the floor

Coach card for absolute values. The floor lesson, with its checked fences, is `docs/techniques/floor.md`. Original absolute-value examples on this page were checked with SymPy. They are not catalog rows. A contest row is not a source for a new number.

The catalog id `floor` has no unit. The drills ride on `special-wildcard`. Teach the floor note. Leave `floor` unticked.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `absolute-values` | 2 | `symmetry` | `units/07-abs-reverse-product/teaching.tex` |
| `floor` | 2 | `absolute-values` | `docs/techniques/floor.md` |

`floor` is deferred in `trackers/catalog.json` because it has no unit. The teaching is ready. A tick of `floor` is not the goal of this card.

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

## When to split

An absolute value changes formula at each zero of its inside. Split the integral there, drop the bars on each piece, and add. A single endpoint does not change a definite integral.

On \([0,2]\),

\[
\int_0^2 |x-1|\,dx=\int_0^1(1-x)\,dx+\int_1^2(x-1)\,dx=\frac12+\frac12=1.
\]

On \([-1,2]\),

\[
\int_{-1}^{2}|x|\,dx=\int_{-1}^{0}(-x)\,dx+\int_0^2 x\,dx=\frac12+2=\frac52.
\]

Unit 07 stores \(\int_{-1}^{1}|x|\,dx=1\) as `U07-D01`. On a symmetric interval an even absolute value doubles, which is the symmetry card. The split is still available when the interval is not symmetric, as in the second example.

## Faded step

For \(\int_{-2}^{1}|x+1|\,dx\), name the zero, which is \(x=-1\). Write the left piece and the right piece, then add. The left piece is \(\int_{-2}^{-1}(-(x+1))\,dx=1/2\). The right piece is \(\int_{-1}^{1}(x+1)\,dx=2\). The value is \(5/2\).

## The floor, by pointer

The floor \(\lfloor x\rfloor\) is constant on each \([k,k+1)\), and that constant is \(k\). Split at the integers, pull the constant out, and add the areas. A piece that stops between integers contributes its actual length.

The worked fences, the negative argument, the fractional part \(\{x\}=x-\lfloor x\rfloor\), and the four drills `U11-D09` through `U11-D12` are `docs/techniques/floor.md`. Unit 11 teaches the same split beside the Gaussian cousins. An infinite upper limit becomes a series. The floor note does not quote a zeta value. This card does not either.

\(\lfloor x\rfloor\) and \(|x|\) agree on \([0,\infty)\) and disagree on the negatives. \(\lfloor -0.2\rfloor=-1\). Truncation toward zero is a third function. Name which one is in the integrand.

## Where this goes wrong

The bars were dropped on the whole interval. The sign is constant only between zeros.

A symmetric-interval shortcut was used for \(|x-1|\) on \([-1,1]\). The kink is at \(x=1\), on the endpoint, so the even shortcut about 0 still needs a reason. Splitting is the reason you can check.

A floor on a negative argument was replaced by \(-x\) or by \(|x|\). Use the greatest integer that is still \(\le x\), as the floor note does for `U11-D12`.

## On a miss

An absolute-value miss teaches this file, then unit 07. Set `U07-D01`. A floor miss teaches `docs/techniques/floor.md` and sets one of `U11-D09` through `U11-D12`. Leave `floor` unticked.
