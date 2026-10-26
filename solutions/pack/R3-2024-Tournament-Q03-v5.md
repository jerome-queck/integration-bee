# R3-2024-Tournament-Q03-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 1, problem 3, slide 65)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 67)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (page 7, section 2.1, problem 3)
- The catalog now uses the visually checked source reading and a SymPy certificate.

## Problem

\[
\int_1^\infty\frac{1}{x\sqrt{\sqrt[e]{x}-1}}\,dx.
\]

The small \(e\) is the index of the inner radical, so \(\sqrt[e]{x}=x^{1/e}\).
The earlier transcription as \(e^{\sqrt{x}}\) was incorrect; the original
problem and its worked solution agree. The answer-slide rows refer to this same integral.

## Solution

Set \(u=\sqrt{x^{1/e}-1}\), so \(x=(1+u^2)^e\) and

\[
\frac{dx}{du}=2eu(1+u^2)^{e-1},
\qquad
\frac{1}{x\sqrt{x^{1/e}-1}}\frac{dx}{du}
=\frac{2e}{1+u^2}.
\]

This increasing substitution sends \(x=1\) to \(u=0\) and \(x\to\infty\)
to \(u\to\infty\). Hence

\[
2e\int_0^\infty\frac{du}{1+u^2}
=2e[\arctan u]_0^\infty=e\pi.
\]

## Final answer

\[
e\pi.
\]

This is the value printed on slide 67 and in the worked solutions on page 7.

## SymPy self-check

`verify/pack_handoff_e_tournament.py` checks the exact positive real e-th root,
the substitution derivative, its endpoints and orientation, and the arctangent
primitive. `pack_gate.proven` accepts \(e\pi\) and rejects an altered answer.
