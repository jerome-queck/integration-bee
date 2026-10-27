# R2-2021-Crossnumber-Down-1

## Status: ambiguous original clues held

The original Down clues are in `sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf`, PDF p.3, with Across clues and the same lattice on p.2. The completed grid was read visually from `sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`, PDF p.3.

| Down clue | Printed entry |
|---|---:|
| 1 | 77 |
| 2 | 77288 |
| 3 | 28 |
| 4 | 7134317 |
| 5 | 26564 |
| 7 | 12 |
| 8 | 14 |
| 9 | 85 |
| 13 | 1904 |
| 14 | 315 |

The row remains manual. Two source readings require clarification before every printed clue can be certified without silently changing its arithmetic. `verify/pack_grid_2021.py` keeps the literal checks, source text, full shared lattice, and explicit numbered starts. Every other mathematical clue has an exact certificate.

## Held readings

### D3: the modulus lacks necessary parentheses

The source asks for the (x)-th triangular number and prints

\[
x\text{ is }7^{9\ \mathrm{DOWN}}\bmod 7\ \mathrm{DOWN}+1.
\]

There are no parentheses around the modulus plus one. With the printed sibling entries (D_9=85,D_7=12), ordinary left-associated arithmetic gives

\[
x=(7^{85}\bmod12)+1=7+1=8,
\qquad \frac{x(x+1)}2=36.
\]

The mark grid instead prints 28. That answer can be recovered by changing the grouping to

\[
x=7^{85}\bmod(12+1)=7,
\qquad \frac{x(x+1)}2=28.
\]

The second reading is plausible authorial intent, but adding those parentheses changes the unparenthesized expression. The certificate reports the original reading's disagreement instead of treating the mark digits as permission to change the clue.

### D4: equality versus congruence

The source asks for a palindrome with digit product 1764, whose digit sum "is (x\bmod9)", where (x^2-D_7x+32=0). With (D_7=12), the roots are 4 and 8. The marked palindrome 7134317 has digit product 1764 and digit sum 26. Thus it does **not** have digit sum equal to either residue 4 or 8.

It does satisfy the likely intended congruence (26\equiv8\pmod9). The transcript records both readings. The literal equality checker remains false rather than silently turning an equality with a remainder into a congruence.

## Verified remaining clues

### D1 and D9: crossing arithmetic


\[
D_1=(A_{16}+1)/3=(230+1)/3=77,
\qquad D_9=D_{14}-A_{16}=315-230=85.
\]

### D2: a rounded improper integral

The source is the nearest integer to

\[
\frac{279^4+4}{279^2+2\cdot279+2}
+\int_0^\infty\frac{\log\sqrt{1+x}}{x\sqrt x}\,dx.
\]

The rational term is 77285. For the integral, use the exact primitive

\[
F(x)=-\frac{\log(1+x)}{\sqrt x}+2\arctan\sqrt x.
\]

Its derivative is (\log(1+x)/(2x\sqrt x)=\log\sqrt{1+x}/(x\sqrt x)). At zero, (F(x)\to0); at infinity, (F(x)\to\pi). Thus the integral is \(\pi\), and the total is \(77285+\pi\). It lies strictly between (77287.5) and (77288.5), proving the rounded answer 77288. SymPy checks the derivative, both improper limits, and the exact rational rounding bounds.

### D5: a large index proved by small inequalities

The problem asks for the greatest integer (n) with

\[
I_n=\int_0^1\frac{x^n}{1+x}\,dx>\frac1{A_6-1}=\frac1{53130}.
\]

For (0<x<1), the inequalities (1+x<2) and (1+x>2\sqrt x) imply

\[
\frac1{2(n+1)}<I_n<\frac1{2n+1}.
\]

The inequalities are strict on a set of positive measure. At (n=26564), the lower bound equals (1/53130), so (I_{26564}) is larger than the threshold. For the next index,

\[
I_{26565}<\frac1{53131}<\frac1{53130}.
\]

Since (I_n) decreases strictly with (n), the greatest index is 26564. The code checks these exact rational inequalities and uses the stated monotonicity proof; it does not ask SymPy to integrate a polynomial with more than 26,000 terms.

### D7: linear equations

Write (U=\int_0^1f) and (T=\int_0^2f). The printed conditions are

\[
5T+4U=143,\qquad7T+11(T-U)=210.
\]

They give (U=12,T=19), hence D7 (=12). These are a separate function's integral equations from A3; the two clues must not be combined as if they referred to one shared function.

### D8: three consecutive heads

Let (E_j) be the expected remaining number of fair-coin flips when the current run has (j) consecutive heads, for (j=0,1,2,3). Then (E_3=0) and first-step conditioning gives

\[
E_0=1+\frac{E_0+E_1}2,\qquad
E_1=1+\frac{E_0+E_2}2,\qquad
E_2=1+\frac{E_0}2.
\]

Solving yields (E_0=14). The certificate solves this finite rational system. Finiteness follows, for example, from checking disjoint blocks of three flips: each block succeeds with probability (1/8), so the waiting time is bounded by three times a geometric waiting time.

### D13: a cited publication fact

The mark grid prints 1904. The [Bibliotheque nationale de France record](https://catalogue.bnf.fr/ark:/12148/cb30759541r) dates Lebesgue's *Lecons sur l'integration et la recherche des fonctions primitives* to Paris, Gauthier-Villars, 1904. This supports a book-publication interpretation of the printed clue. The checker treats that as a cited source fact, not a theorem proved by SymPy and not a claim that the integral was first introduced in 1904.

### D14: another integral-defined function

Put (C=\int_2^5f(t)\,dt). Integrating (f(x)+C=12x^2) from 2 to 5 gives

\[
C+3C=\int_2^5 12x^2\,dx=468,
\]

so (C=117), and (f(6)=12\cdot36-117=315). SymPy checks the polynomial integral exactly.

## Certificate outcome

Eight Down checks pass; D3 and D4 remain false under their literal readings. The preserved mark map is useful evidence, but it does not erase those two differences. The common map contract separately rejects missing keys, scalar answers, digit mutations, and inconsistent crossings. Neither this note nor the helper claims a fully proved Down row.

## Handoff J typography recheck

Rechecked on 2026-10-27 by rendering problem pp.2-3 and mark p.3. In D3,
`9 DOWN` is visibly the exponent of 7, while `mod 7 DOWN + 1` is on the
baseline, with no parentheses around `7 DOWN + 1`. This rules out an OCR
loss of printed parentheses; it does not resolve the author's intended
operator grouping. D4 visibly says that the digit sum "is x mod 9".
There is no printed congruence sign or instruction to reduce the digit
sum modulo 9 first. Consequently D4 is an independent blocker even if
an authoritative convention were to settle D3.

The [official contest homepage](https://integration.soc.srcf.net/) and
[2021 competition account](https://integration.soc.srcf.net/pastcomp.html)
provide no convention or correction for these two clues. Targeted searches
for the 2021 crossnumber, errata, and the modular wording located no public
clarification. This bounded search does not establish that none exists.
The original digits and both failed literal checks are retained.

The current [official resource pack](https://integration.soc.srcf.net/Resource%20pack.zip)
contains the same four `Round 2/2021/` PDFs as the repository, verified
byte-for-byte, and no additional correction sheet in that directory.

### Escalation: R2-2021-Crossnumber-Down-1

- Obstacle: D3's unparenthesized modulus admits the known reading yielding
  36 rather than marked 28. Obtaining 28 requires putting `D7 + 1` inside
  the modulus. Independently, D4's marked palindrome has digit sum 26,
  whereas the quadratic roots have residues 4 and 8; only a congruence
  interpretation yields agreement. The visual recheck found no missing
  punctuation or explicit convention that resolves both readings.
- PDF problem: [p.3 at 6ac8f7d1552e32b6007bed7e8206ab3c284ab10b](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf#page=3)
- PDF mark: [p.3 at 6ac8f7d1552e32b6007bed7e8206ab3c284ab10b](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf#page=3)
- What a follow-up agent should try next:

  ```text
  Inspect original 2021 Down clues 3 and 4 together with the marked lattice.
  Seek an official correction or a published contest notation convention.
  For D3, establish whether the modulus is D7 or the complete expression D7 + 1.
  For D4, establish whether the digit-sum condition is equality or congruence.
  Require authority for both readings; resolving D3 alone does not certify this row.
  Preserve 28 and 7134317 as the printed marks until a source resolves the wording.
  Recheck every Down clue and the sibling Across crossings before any status flip.
  ```

- Do not mark impossible.
