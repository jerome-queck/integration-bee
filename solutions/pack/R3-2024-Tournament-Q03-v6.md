# R3-2024-Tournament-Q03-v6

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 1, problem 3, answer slide 67)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 67)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.1, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 67, not the integral. Slide 67 is the answer reveal for Battle 2, Fight 1, problem 3:

\[
\int_{1}^{\infty}\frac{1}{x\sqrt{e^{\sqrt{x}}-1}}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q03-v4`.

Slide 67 prints \(e\pi\), and the solutions PDF reaches that same line. The derivative used there is false: the ratio of the true derivative to the claimed derivative is \(e\sqrt{x}/2\). The printed line is not the value of the integral.

## Solution

The solutions PDF sets \(u=\sqrt{e^{\sqrt{x}}-1}\) and claims

\[
u'=\frac{u^{2}+1}{2e\,x\,u},
\]

then concludes that the integral equals

\[
2e\int_{0}^{\infty}\frac{1}{1+u^{2}}\,du=e\pi.
\]

The answer slide prints the same value \(e\pi\). Differentiating the chosen \(u\) gives a different derivative. The ratio of the true derivative to the claimed derivative is \(e\sqrt{x}/2\), which is not \(1\). The arithmetic \(2e\cdot(\pi/2)=e\pi\) is the value of that false substitution, not the value of the printed integrand.

The same substitution done with the true derivative is elementary in a different variable. From \(u^{2}+1=e^{\sqrt{x}}\) one has \(\sqrt{x}=\ln(1+u^{2})\) and \(x=\bigl(\ln(1+u^{2})\bigr)^{2}\), and

\[
\frac{1}{x u}\frac{dx}{du}=\frac{4}{(1+u^{2})\ln(1+u^{2})}.
\]

Then \(u=\tan t\) uses \(1+\tan^{2}t=\sec^{2}t\). On \((0,\pi/2)\), where \(\sec t>1\),

\[
\frac{4}{\ln(\sec^{2}t)}=\frac{2}{\ln(\sec t)}.
\]

The limits \(x=1\) and \(x\to\infty\) become \(t=\arctan\sqrt{e-1}\) and \(t=\pi/2\).

## Final answer

\[
\int_{\arctan\sqrt{e-1}}^{\pi/2}\frac{2}{\ln(\sec t)}\,dt.
\]

The solutions PDF and the answer slide both print \(e\pi\). That printed line is the result of the false derivative above. It is not the value of the integral.

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q03_v6`. That check runs `check_r3_2024_tournament_q03_v4` for `R3-2024-Tournament-Q03-v4`. SymPy checks that the claimed derivative is off by the factor \(e\sqrt{x}/2\), that the false substitution would produce \(e\pi\), that high-precision quadrature of the printed integrand differs from \(e\pi\) by more than \(1\), and that the corrected substitution equals \(4\,du/\bigl((1+u^{2})\ln(1+u^{2})\bigr)\), which is \(2\,dt/\ln(\sec t)\) on \((0,\pi/2)\).
