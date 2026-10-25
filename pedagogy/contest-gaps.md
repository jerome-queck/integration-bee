# Teaching the six contest gaps

Yang is one source. The Techniques Guide files reflection, a recurrence \(I_n\), the half-angle substitution, floor, and introducing a constant in sections 1.2, 1.3, 1.6, 1.7, and 1.9. The syllabus adds both forms of differentiation under the integral sign, and it lists the floor. The 2024 participant guides are the source for the Round 2 and Round 3 games. A contest row is not a source of a new answer.

The six headings in `docs/techniques/beyond-yang.md` are the only gap ids. A study session does not edit a teaching note. Teach the one file the mark names. Read the worked example, then the faded step, then set the integral again. Match `coach.detail` when it is present: worked, faded, or bare.

Before a gap id, a Round 1 node opens the coach card in `pedagogy/concept-map.md`. Match the card to the tick using `pedagogy/round1-coach.md`. A missing or learning prerequisite is taught first. A solid node skips the lecture and takes the next drill. The six headings stay the only `extract.gap` values.

## Answer shape before technique

Name the object the blank wants before any substitution.

| Blank | Object | Then |
|---|---|---|
| Round 1 paper, or the group round | the value | the unit note |
| Crossnumber square | one digit, one attempt | `docs/techniques/formats.md` |
| Relay or shuttle | the current problem only | the same file, then a unit drill |
| Chainlink | the value, then bank or continue | the same file |
| Dichotomy | the chosen problem only | the same file |
| Tournament | a boxed value, gamble only before the fight | the same file |

A full antiderivative in a digit blank is a format miss. A right value from the wrong method is a method miss. Say which, and open one file.

## Reflection

File: `units/10-inverse-kings/teaching.tex`. Catalog node `kings-queens-rule`.

1. Worked. The identity is \(x \mapsto a+b-x\). If the two integrands add to a constant, half the constant times the length is the value. `U10-D04` and `U10-D07` are that case. The log-sine evaluation in the same file is a derivation, not a drill id.
2. Faded. For `U10-D05`, the learner writes the reflected integrand, then adds.
3. Bare. Set `U10-D04` again.
4. Later. Unit 25 is the same identity on an exponential, a tangent, and a factor of \(x\).

## Recurrence

File: `units/20-wallis/teaching.tex`. Catalog node `wallis`.

1. Worked. Define \(I_n\), write the relation, write the base, then unroll. `U20-D01` is \(I_4 = 3\pi/16\). The factorial family \(J_n = n!\) is the same index drop. Unit 14 stores \(J_2\) and \(J_4\) as `U14-D10` and `U14-D09`.
2. Second family, still in that file. \(\int_0^1 x^n/(1+x)\,dx\) alternates: \(I_n + I_{n-1} = 1/n\). The base uses the add-and-subtract move. \(I_3 = 5/6 - \ln 2\) is stored as `U15-D11`. The factorial drop \(J_n = n J_{n-1}\) is unit 14, drills `U14-D09` and `U14-D10`.
3. Faded. `U20-D02` is a double-angle, so the learner should refuse the general reduction.
4. Do not start a reduction when one substitution finishes the integral. `U20-D06` is that refusal.

## Half-angle substitution, early

First pass: `units/09-intermediate-trig/teaching.tex`. The note a miss names: `units/26-weierstrass/teaching.tex`. Catalog node `weierstrass`.

1. In unit 09, work \(\int_0^{\pi/3} dx/(1+\cos x)\). The substitutions collapse it to \(dt\), and the value is \(\sqrt{3}/3\). The antiderivative is \(\tan(x/2)\). This is not a drill.
2. Faded. The learner writes the three limits and the new denominator for `U26-D01`, then reads unit 26.
3. Unit 26 adds \(\tan x = 2t/(1-t^2)\), the pattern on \([0,\pi]\), and the warning that \(t=\tan(x/2)\) is unbounded at \(x=\pi\).
4. Refuse the substitution when a sine power is a reduction (unit 20) or when \(\sec^2 x\) is already the derivative of \(\tan x\) (unit 09's ordinary substitution).

## Floor

File: `docs/techniques/floor.md`. Drills: `U11-D09` through `U11-D12` on unit 11. Do not tick `floor`.

1. Worked. Split at the integers, pull out the constant, add the areas. The checked fences are piecewise. `U11-D09` is four steps on \([0, 4]\), value 6.
2. Faded. Ask where \(\lfloor x\rfloor\) jumps on \([0, 5/2]\), and what length the last piece has. `U11-D11` stores 2.
3. Name the two traps: a negative argument steps down (`U11-D12` stores \(-3\)), and a non-constant factor stays inside the piece.
4. `U11-D10` is three teeth of the fractional part, value \(3/2\). An infinite upper limit becomes a series. Do not quote a zeta value from this note.

## Introducing a constant, and DUTIS

Algebra file: `docs/techniques/introduce-constant.md`. Parameter file: `units/34-frullani-feynman/teaching.tex`. Drills: `U11-D13` through `U11-D15`. Do not tick `dutis`.

1. If the numerator is almost the denominator or almost its derivative, teach the algebra file. Work \((x+1)/(x+2)\), then the faded multiple \((3x+5)/(x+1)\).
2. If a constant independent of \(x\) lets an addition formula split the integrand, stay in the algebra file. The cosine product on \([0, \pi/3]\) is the worked case.
3. If the integrand is a derivative in a parameter on a fixed interval, set `U11-D13` (value \(-1/25\)) or teach unit 34. The algebra file keeps the smaller parameter at \(a=3\), which is a fence, not a drill id.
4. `U11-D14` is the exponential family at \(a=2\), value \(1/4\). `U11-D15` integrates the parameter from 0 to 3 and stores \(\ln 4\).
5. If an endpoint moves with the parameter, teach the second syllabus formula in unit 34. The worked case is \(\int_0^t tx\,dx\). Its derivative at \(t=2\) is 6. That is not a drill, and it does not tick `dutis`.
6. If a substitution already finishes the integral, do not build a parameter. `U34-D07` is that refusal.

## Formats

File: `docs/techniques/formats.md`.

1. Name the format and the object.
2. State the rule the attempt broke, using the 2024 scoring in that file. The relay bonus counts correct problems. It is not a consecutive streak. A failed chainlink chain pays the safety net, not the bank row of the number solved.
3. Set one ordinary unit drill and score it with that format's points: 6 or 0 in a group set, one digit once in a crossnumber, 3 then 1 in a relay, bank or continue after a chainlink solve, 6 then 2 in a dichotomy, a boxed line in a tournament.
4. Do not invent a contest answer, and do not open a past-paper file as the lesson.

## What the session does not do

The session does not edit the note and does not add a drill id. Do not tick `floor` or `dutis`: those catalog ids have no unit. A later commit is what adds an example, and only to the file the mark named.
