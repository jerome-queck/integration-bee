# R2-2021-Crossnumber-Across-1

## Status: source reading held

The original clues were read visually from `sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf`, PDF pp.2-3. The completed lattice was read visually from `sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`, PDF p.3. Its Across entries are:

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

These values and the full 11-by-15 lattice are retained in `verify/pack_grid_2021.py`, together with the explicit printed clue starts and source statements. The completed grid is not by itself a proof of every clue. The entry remains manual because A8 asks for the year the Riemann integral was **first** published, while the marked 1868 is not an unambiguous first-publication date.

### A8: mark answer 1868 versus an earlier primary edition

The mark grid prints 1868. The [Göttingen journal-volume record](https://gdz.sub.uni-goettingen.de/id/PPN250442582_0013) identifies volume 13 as 1868, so the printed date has an identifiable bibliographical basis. However, the [Göttingen digitized standalone edition](https://gdz.sub.uni-goettingen.de/id/PPN309770033) of Riemann's *Ueber die Darstellbarkeit einer Function durch eine trigonometrische Reihe* is dated 1867; the [ETH Library's copy](https://www.e-rara.ch/zut/content/titleinfo/13665454) likewise records Göttingen, 1867. These are primary publication records, not an unsupported recollection of the history.

Consequently this certificate does not silently replace "first published" with "journal volume dated". A8 returns false and the Across row remains held. The mark grid is preserved, and no substitute digits are invented. This is a source-disambiguation issue, not a claim that the other mathematical clues lack answers.

## Derived mathematical clues

Write (A_j,D_j) for Across and Down entries. The sibling map from the same completed lattice is (D_1=77,D_2=77288,D_3=28,D_4=7134317,D_5=26564,D_7=12,D_8=14,D_9=85,D_{13}=1904,D_{14}=315). Its own held readings are documented in `solutions/pack/R2-2021-Crossnumber-Down-1.md`.

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

The nine mathematical Across checks return true; the historical A8 check is deliberately false pending clarification of the source wording. A complete map is still required by the grid contract, and it checks every crossing against the printed sibling map. This transcript never upgrades a grid-equality check into a claim that the publication-date conflict has been resolved.

## Handoff J source recheck

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

The [official contest homepage](https://integration.soc.srcf.net/) and
[2021 competition account](https://integration.soc.srcf.net/pastcomp.html),
together with targeted searches for a 2021 crossnumber correction or
erratum, supplied no clarification of A8. This is a bounded negative search,
not a claim that no correction exists. The Across map remains manual and
the coupled Down holds remain separate obligations.

The current [official resource pack](https://integration.soc.srcf.net/Resource%20pack.zip)
was also checked: all four PDFs in `Round 2/2021/` byte-match the committed
copies, including the crossnumber and mark scheme. That directory contains
no additional correction sheet.

### Escalation: R2-2021-Crossnumber-Across-1

- Obstacle: The marked 1868 has a journal-volume basis, but the clue's word
  "first" remains in conflict with the original 1867 offprint title and
  its archived publication record. No located contest correction resolves
  that conflict; substituting 1867 would also change the supplied lattice.
- PDF problem: [p.2 at 6ac8f7d1552e32b6007bed7e8206ab3c284ab10b](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf#page=2)
- PDF mark: [p.3 at 6ac8f7d1552e32b6007bed7e8206ab3c284ab10b](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf#page=3)
- What a follow-up agent should try next:

  ```text
  Re-open the original 2021 A8 clue and completed crossnumber lattice.
  Seek an official contest correction defining the intended publication event.
  Compare the ETH scan's original title (PDF p.2) and Dedekind notice (p.4).
  Check the Göttingen offprint record Cod. Ms. B. Riemann 28 k.
  Distinguish a volume's cover year from evidence of first public distribution.
  If authority resolves the clue, recheck all Across clues and Down crossings.
  Otherwise retain the mark digits and manual status, with the unresolved source reading.
  ```

- Do not mark impossible.
