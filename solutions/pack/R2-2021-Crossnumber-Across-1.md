# R2-2021-Crossnumber-Across-1

## Status: resolved by contest convention

- verify: sympy; kind: grid
- conflict: A8 asks for first publication, but the marked journal-volume year 1868 differs from the cited standalone edition dated 1867.
- derived / problem reading: Handoff N adopts the journal-volume year 1868 for grading; the earlier 1867 standalone edition remains acknowledged.
- printed mark: A8: \(1868\); the complete marked Across map is retained below.
- erratum: none claimed; Jerome's t636u override and Handoff N explicitly authorize this published grading convention.
- registry: docs/decisions/0016-pack-source-holds.md

## Source reading

The original clues were read visually from `sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf`, PDF pp.2-3 ([immutable problem copy](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf#page=2)). The completed lattice was read visually from `sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`, PDF p.3 ([immutable mark copy](https://github.com/jerome-queck/integration-bee/blob/db203fa3e4b9a96456993b85c49449ece4148cea/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf#page=3)). Its Across entries are:

| Clue | Printed entry |
|---|---:|
| 1 | 77177 |
| 3 | 27 |
| 6 | 53131 |
| 8 | 1868 |
| 10 | 20 |
| 11 | 46 |
| 12 | 4181 |
| 15 | 95791 |
| 16 | 230 |
| 17 | 343 |

These values and the full 11-by-15 lattice are retained in `verify/pack_grid_2021.py`, together with the explicit printed clue starts and source statements. All ten Across checks now pass under the declared contest convention for A8. The grid certificate checks the nine mathematical clues independently and checks A8 against the cited journal-volume year. The literal word **first** is retained in the clue transcript; the grading clarification is published separately in the problem manifest.

### A8: mark answer 1868 versus an earlier primary edition

The mark grid prints 1868. The [Göttingen journal-volume record](https://gdz.sub.uni-goettingen.de/id/PPN250442582_0013) identifies volume 13 as 1868, so the printed date has an identifiable bibliographical basis. However, the [Göttingen digitized standalone edition](https://gdz.sub.uni-goettingen.de/id/PPN309770033) of Riemann's *Ueber die Darstellbarkeit einer Function durch eine trigonometrische Reihe* is dated 1867; the [ETH Library's copy](https://www.e-rara.ch/zut/content/titleinfo/13665454) likewise records Göttingen, 1867. These are primary publication records, not an unsupported recollection of the history.

**Contest certificate adopts mark grid year 1868 = Abhandlungen vol. 13 dating; 1867 pamphlet is acknowledged but not graded.** This is the explicit contest convention authorised for this row. It resolves the grading contract without asserting that 1868 was the earliest public appearance of the work. A8 returns true exactly for the cited volume year; an answer of 1867 is rejected under this published convention. The original mark lattice is unchanged, and no organiser erratum is claimed.

## Derived mathematical clues

Write (A_j,D_j) for Across and Down entries. The sibling map from the same completed lattice is (D_1=77,D_2=77288,D_3=28,D_4=7134317,D_5=26564,D_7=12,D_8=14,D_9=85,D_{13}=1904,D_{14}=315). Its resolved D3 and D4 readings are documented in `solutions/pack/R2-2021-Crossnumber-Down-1.md`.

### A1: the next palindrome

The lower bound is

\[
A_{17}(D_8+1)^2=343\cdot15^2=77175.
\]

The first palindrome strictly above it is 77177. The exact check mirrors the central prefix, verifies strict inequality, and requires the first admissible palindrome.

### A3: linearity of the integral

Let (U=\int_0^1f(x)\,dx) and (V=\int_1^2f(x)\,dx). The source gives

\[
3V-5U=17,\qquad21U-7V=35.
\]

The solution is (U=8,V=19). Therefore (\int_0^2f=U+V=27). SymPy solves these equations exactly.

### A6 and A15: polynomial identities

For A6 substitute (a=A_{16}=230). The identity

\[
\frac{1+a^4+(a+1)^4}{1+a^2+(a+1)^2}=a^2+a+1
\]

gives (230^2+230+1=53131). The code checks the original numerator equals the claimed answer times its positive denominator.

For A15,

\[
\frac{1+310^2+310^4}{1+310+310^2}
=310^2-310+1=95791,
\]

using ((t^2+t+1)(t^2-t+1)=t^4+t^2+1). This too is checked by exact integer multiplication.

### A10: limit and two-significant-figure rounding

The original expression is

\[
\lim_{n\to\infty}\int_0^{14}\arctan(x^n)\,dx.
\]

The integrand tends to 0 for (0\le x<1), and to (\pi/2) for (1<x\le14). The exceptional point (x=1) has measure zero. The bound (0\le\arctan(x^n)\le\pi/2) on a finite interval permits dominated convergence. The limit is therefore

\[
\int_1^{14}\frac\pi2\,dx=\frac{13\pi}2.
\]

This lies between 19.5 and 20.5 and between 10 and 100, so rounding to two significant figures gives 20. The certificate evaluates the reduced integral with SymPy and checks these exact rational rounding boundaries; it does not use a floating-point decimal as the proof.

### A11, A12, A16, A17: exact grid constraints

The three smallest entries in the full grid are (12,14,20), giving A11 (=46). The entry (4181=F_{19}) is a Fibonacci number, verified by the integer recurrence (F_0=0,F_1=1). The source gives A16 (=D_7A_{10}-10=12\cdot20-10=230). Finally A17 (=343=7^3), an exact power of 7.

## Certificate outcome

All ten Across checks return true under the stated grading convention. The A8 check is a source-backed historical fact, with the same role as the cited book-publication date in D13; it is not a mathematical theorem proved by SymPy. A complete answer map is required, every crossing is checked against the original mark lattice, and altered entries are rejected. The row is certified as `kind: grid`, `verify: sympy`.

## Source audit and scope of the convention

Rechecked on 2026-10-27. Visual inspection of the original problem p.2
confirms that A8 explicitly asks when the integral was **first** published;
the completed grid on mark p.3 still gives 1868.

The new check goes beyond catalog metadata. In the
[ETH Library scan](https://www.e-rara.ch/zut/download/pdf/13665454), PDF p.2
is the original title page: it prints 1867 and identifies the work as taken
from volume 13 of the Göttingen proceedings. PDF p.4 contains Dedekind's
editorial notice dated July 1867. Both pages were rendered and read visually.
The [Göttingen archive record for Cod. Ms. B. Riemann 28 k](https://kalliope-verbund.info/de/ead?ead.id=DE-611-HS-3206244)
independently describes a printed 1867 offprint from that volume. Thus an
earlier issue cannot be dismissed merely because it has a separate title
page. These observations do not establish an exact distribution date, but
they do prevent certifying 1868 as an unambiguous first-publication year.

The prior Handoff J search of the [official contest homepage](https://integration.soc.srcf.net/)
and [2021 competition account](https://integration.soc.srcf.net/pastcomp.html),
together with targeted searches for a 2021 crossnumber correction or erratum,
supplied no clarification of A8. This is a bounded negative search, not a
claim that no correction exists. Handoff N resolves grading by declaring the
journal-volume convention above; the historical first-publication question
and evidence for the 1867 offprint remain visible.

The current [official resource pack](https://integration.soc.srcf.net/Resource%20pack.zip)
was also checked: all four PDFs in `Round 2/2021/` byte-match the committed
copies, including the crossnumber and mark scheme. That directory contains
no additional correction sheet.

On 2026-10-27 the Handoff N recheck again read the original problem and mark
pages visually and confirmed both dates from primary library records. The
[Göttingen volume record at Riemann's paper](https://gdz.sub.uni-goettingen.de/id/PPN250442582_0013?tify=%7B%22pages%22%3A%5B199%5D%7D)
labels the volume and article 1868; its [series catalogue](https://gdz.sub.uni-goettingen.de/id/PPN250442582)
also pairs volume 13 with 1868. The separately catalogued 1867 edition remains
part of the evidence. The former grading hold is resolved by the explicit
choice of publication event, with no change to any grid digit.
