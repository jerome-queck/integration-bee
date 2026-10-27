# R2-2023-Crossnumber-Down-1

## Status: source hold (print-vs-math)

- verify: manual
- conflict: Down 7's integral limit does not determine \(f(0)\) without an additional hypothesis such as continuity at zero.
- derived / problem reading: Changing \(f(0)\) alone preserves every printed integral, so \(f(0)\) is undetermined.
- printed mark: Down 7: \(250\); the complete marked Down map is retained below.
- erratum: none documented in the cited repository sources as of 2026-10-27.
- registry: docs/decisions/0016-pack-source-holds.md

## Sources and manual status

The numbered lattice and Down clues were read visually from
`sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf`,
p.3. The completed grid is in
`sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf`,
p.3. Its map is

`{1:115, 2:14183, 4:376, 6:4320, 7:250, 10:69134, 11:27, 13:721, 14:394, 15:856}`.

**This row stays manual.** Down 7's printed hypothesis does not determine
`f(0)`. The literal statement is a limit of integrals equal to `50*pi`;
it gives no continuity assumption at zero. The problem's cover contains
only its title and sponsor, and the two clue pages supply no general
regularity assumption. Its intended answer 250 follows under continuity,
but adding that hypothesis would change the source.

## Down 7: exact obstruction

For any real number `c`, set `f(x)=250` for `x!=0` and `f(0)=c`.
This is Riemann-integrable on `[-1,1]`. Changing one point does not alter
any integral, and for `n>0`,

`integral_-1^1 n*f(x)/(25*n^2+x^2) dx`
`=100*atan(1/(5*n)) -> 50*pi`.

Thus every `c` satisfies the printed integral limit. In particular,
the source hypotheses hold with `f(0)=0` as well as with the completed
grid's 250. There is no disagreement about the mark-grid digits; the
unresolved issue is the missing hypothesis. If `f` is continuous at zero,
the Cauchy approximate identity gives `(pi/5)f(0)=50*pi`, and then
`f(0)=250`. The implemented `D7` check deliberately returns false instead
of silently imposing continuity.

## Other Down derivations

1. Put `u=integral_0^1 f`, `v=integral_1^2 f`. The equations are
   `-4u+3v=23`, `3u-2v=0`, so `u=46,v=69` and the requested sum is 115.

2. Across 1 gives `c=10`. Substitute `x=exp(-t)`:
   `integral_0^1 x(log x)^10 dx=10!/2^11=14175/8`.
   The numerator and denominator are coprime, giving `14175+8=14183`.

4. Let `I=integral_-1^1 f`. Integration of
   `f(x)+I=3x^2+x+8` gives `3I=18`, hence `I=6` and
   `f(11)=3*121+11+8-6=376`.

6. The three smallest marked entries are 10,16,27. Their product is 4320.

10. The identity
    `d/dx[f'(x)sin(x)-f(x)cos(x)]=(f''(x)+f(x))sin(x)`
    gives `f(pi)+f(0)=70000`. Since `f(pi)=866`, `f(0)=69134`.
    The symbolic derivative is checked directly, with the endpoint sine
    factors zero and the endpoint cosine factors `-1,1`.

11. The nested integral uses every letter from `a` through `z`, hence
    26 integrations of the initial function `z`. Repeated integration of
    `t^m/m!` from 0 to the next upper variable gives
    `t^(m+1)/(m+1)!`. The outer upper endpoint is 1, so the result is
    `1/27!` and `A=27`. The checker executes this finite recurrence.

13. `721=6!+1`.

14. The digits of 394 have product 108 and sum 16.

15. The digits of 856 alternate even, odd, even.

The entries in Down 13,14,15 concatenate to `721394856`, which contains
every digit 1 through 9 exactly once. The shared grid contract checks
the crossings, but cannot turn the deficient Down 7 hypothesis into a
point-value theorem. All other Down checks pass independently.

## Handoff J source recheck (2026-10-27)

The complete problem PDF (pp.1-3) and complete mark PDF (pp.1-4) were
rendered and reread visually. Down 7 on problem p.3 explicitly has
`n -> 0+`; it still gives no continuity condition. The cover and Across
page add none. Mark p.3 gives the completed lattice and digit-by-digit
marking instructions, without supplementing the function hypothesis.

The [current official resource pack](https://integration.soc.srcf.net/Resource%20pack.zip)
was downloaded for this recheck. Its 2023 Crossnumber and Mark Scheme
PDFs are byte-for-byte identical to the committed copies. Its Round 2/2023
directory contains only the problem, blank grid, group round, mark scheme,
and relay PDFs; it supplies no separate 2023 participant or marker guide.
The [official 2023/24 syllabus](https://integration.soc.srcf.net/UK_University_Integration_Bee_Syllabus.pdf),
pp.1-2, also supplies no general continuity assumption. Its statement
setting aside convergence questions concerns interchanging infinite
series and integrals, not recovering a function's value at an isolated
point. The [official contest page](https://integration.soc.srcf.net/)
and [past-competitions page](https://integration.soc.srcf.net/pastcomp.html),
and targeted searches for a crossnumber correction, provided no applicable
erratum. This records the scope of the search, not a claim that no
unpublished clarification exists.

The counterexample above was rechecked symbolically: for positive `n`,
the integral is exactly `100*atan(1/(5*n))`, and its right-hand limit at
zero is `50*pi`. Any finite change to `f(0)` preserves each integral.
Thus neither ordinary Riemann integrability nor the syllabus's convergence
convention supplies the missing point-value information. The row remains
manual; no answer, sibling-map constraint, or certificate was changed.

### Escalation: R2-2023-Crossnumber-Down-1

- Obstacle: Down 7 asks for `f(0)` from an integral limit unchanged by
  altering `f` at zero. The marked 250 follows if continuity at zero is
  assumed, but the complete printed problem, mark scheme, and checked
  official supplementary material do not state that assumption. A source
  correction or an applicable official regularity convention is still
  needed before this clue can be certified.
- PDF problem: [Crossnumber, pp.1-3; Down 7 on p.3](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf)
- PDF mark: [Mark Scheme, pp.1-4; completed grid on p.3](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf)
- What a follow-up agent should try next:

  ```text
  Revisit R2-2023-Crossnumber-Down-1, specifically Down 7.
  Seek an official 2023/24 event instruction or dated organizer erratum.
  It must state continuity at zero, or another sufficient hypothesis,
  and explicitly apply to this paper; retain its URL and exact page.
  Recheck f(x)=250 for x!=0 with arbitrary finite f(0) against that wording.
  If authority resolves it, derive 250 and recheck every Down clue/crossing.
  Otherwise retain manual status and record precisely what remains missing.
  Do not silently add continuity and do not mark impossible.
  ```

- Do not mark impossible.
