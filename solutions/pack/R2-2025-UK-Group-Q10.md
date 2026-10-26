# R2-2025-UK-Group-Q10

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (p. 2, group 10)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p. 2, group 10)
- Worked source: derived in this note; the mark scheme prints the final value.
- Verification: `sympy`. The catalog retains the outer ceiling and the complete original integral, using the certificate already checked for the identical Singapore Group Q13.

## Source correction

Visual inspection of both PDFs confirms the ceiling in the problem and the
answer `1` under **Group Round**, question 10, on mark-scheme p. 2.
The former catalog Gamma expression came from **Relay Round**, question 10,
on mark-scheme p. 3. It was a catalog extraction mismatch, not a conflicting
printed Group answer. `answer_plain`, `answer_sympy`, and `answer_latex` now
all store `1`; the raw problem extraction remains available in the record.

## Problem

\[
\left\lceil\int_{1}^{\infty}\left(\frac{1}{\arctan x}-\frac{1+x^{2}}{1+\arctan x+x^{2}\arctan x}\right)dx\right\rceil.
\]

## Solution

The integrand simplifies to \(1/(\arctan x\cdot(1+(1+x^{2})\arctan x))\). The substitution \(x=\tan u\), with \(u\) running from \(\pi/4\) to \(\pi/2\), turns the integral into

\[
\int_{\pi/4}^{\pi/2}\frac{du}{u^{2}+u\cos^{2}u}.
\]

The integrand is positive. Since \(\cos^{2}u\geq 0\), it is at most \(1/u^{2}\), and the inequality is strict on a set of positive length. Therefore

\[
0<I<\int_{\pi/4}^{\pi/2}\frac{du}{u^{2}}=\frac{2}{\pi}.
\]

Since \(\pi>3\), \(2/\pi<1\). The ceiling of a number strictly between \(0\) and \(1\) is \(1\). The mark scheme prints \(1\).

## Final answer

\[
1.
\]

## SymPy self-check

`verify/pack_handoff_d_2024_2025.py` checks the original difference, the
tangent substitution and endpoints, the nonnegative upper-bound gap, and
the exact enclosure \(0<I\le 2/\pi<1\). Strict positivity follows from the
positive continuous reduced integrand; this enclosure alone certifies the
ceiling. The sharper strict upper inequality above also holds.

The catalog stores `Subs(ceiling(rounded_value), rounded_value, Integral(...))`
to preserve the source operation without triggering a numerical evaluation
of an unevaluated integral. The certificate checks its inner bounds against
the separate bound metadata. `verify/pack_certificates_check.py` checks the
round trip, the learner-facing grade, changed source shapes and bounds, and
rejects `0`, `2`, `2/pi`, and the misplaced Relay Gamma answer.
