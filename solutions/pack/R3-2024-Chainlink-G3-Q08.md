# R3-2024-Chainlink-G3-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf`, PDF page 2, problem 8.
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf`, PDF page 4, Game 3, problem 8.
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`, PDF pages 12-13, Game 3, problem 8.
- Visual comparison confirms that both answer sources print the final below. The old catalog text `pi` lost the entire denominator; this is a transcription error, not a source disagreement. The row now has a checked SymPy transcript.

## Problem

\[
\int_{0}^{\pi/2}\frac{1-\ln(\cos x)}{x^{2}+\bigl(1-\ln(\cos x)\bigr)^{2}}\cos(2x)\,dx.
\]

## Solution

Let \(a=1-\ln(\cos x)\). For \(0<x<\pi/2\) we have \(a\geq1\), and the Laplace transform gives

\[
\frac{a}{x^{2}+a^{2}}=\int_{0}^{\infty}e^{-at}\cos(xt)\,dt,
\]

Use \(e^{-at}=e^{-t}\cos^{t}x\). The absolute value of the resulting double-integral kernel is at most \(e^{-t}\), whose integral over \((0,\pi/2)\times(0,\infty)\) is \(\pi/2\). Fubini's theorem therefore gives

\[
\int_{0}^{\infty}e^{-t}\int_{0}^{\pi/2}\cos(2x)\cos^{t}x\cos(xt)\,dx\,dt.
\]

The first Laplace-transform line on worked page 12 prints \(\cos(t)\); the required factor is \(\cos(xt)\), as in its very next line and in the checked identity above.

Write the inner integral as \(J(t)\). Its integrand is even. On \((-\pi/2,\pi/2)\), the identity
\(2\cos x\,e^{ix}=1+e^{2ix}\) has positive \(\cos x\) and argument \(x\), so the principal complex powers agree without a branch change. With \(y=2x\),

\[
J(t)=2^{-t-2}\operatorname{Re}
\int_{-\pi}^{\pi}(1+e^{iy})^{t}\cos y\,dy.
\]

For \(0<r<1\), expand \((1+re^{iy})^t\) into its uniformly convergent binomial series. The coefficients \(c_n=\binom{t}{n}\) follow from
\((1+z)F'(z)=tF(z)\), \(F(0)=1\), or equivalently
\((n+1)c_{n+1}=(t-n)c_n\). Fourier orthogonality gives

\[
\int_{-\pi}^{\pi}e^{iny}\cos y\,dy
=\begin{cases}\pi,&n=1,\\0,&n=0\text{ or }n\geq2.\end{cases}
\]

Thus the integral at radius \(r\) is \(\pi tr\). For fixed \(t>0\), the bound
\(\lvert1+re^{iy}\rvert^t\leq2^t\) permits dominated convergence as \(r\uparrow1\). It follows that \(J(t)=t\pi/2^{t+2}\). Therefore the original integral is

\[
\frac{\pi}{4}\int_{0}^{\infty}t(2e)^{-t}\,dt=\frac{\pi}{4(1+\ln 2)^{2}}.
\]

## Final answer

\[
\dfrac{\pi}{4(1+\ln 2)^{2}}.
\]

## SymPy self-check

`verify/pack_gate.py::_laplace_log_cosine` first requires the exact printed integrand and bounds. It checks the Laplace kernel, the damping substitution, evenness, Euler's identity, the scale factor, the binomial coefficient recurrence for arbitrary nonnegative integer index, the three exhaustive Fourier-mode cases, and the Abel limit. SymPy then integrates the remaining decaying exponential moment. The returned value is compared with the answer using the strict certificate comparator. No quadrature or numerical equality is used to prove the row.
