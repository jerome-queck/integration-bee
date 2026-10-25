# R3-2024-Tournament-Q01-v12

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 1, problem 1, answer slide 155)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 155)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.1, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 155, not the integral. Slide 155 is the answer reveal for Battle 4, Fight 1, problem 1:

\[
\int_{0}^{\infty}\frac{3^{-\lfloor x\rfloor}\tan\bigl(3^{-\lfloor x\rfloor}\bigr)}{3-\tan^{2}\bigl(3^{-\lfloor x\rfloor}\bigr)}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q01-v10`.

## Solution

The triple-angle formula for tangent rearranges to

\[
\frac{\tan a}{3-\tan^{2}a}=\frac18\bigl(\cot a-3\cot(3a)\bigr).
\]

On the interval \([n,n+1)\) the integrand is constant. With \(a=3^{-n}\),

\[
\frac{a\tan a}{3-\tan^{2}a}=\frac18\Bigl(3^{-n}\cot(3^{-n})-3^{-(n-1)}\cot\bigl(3^{-(n-1)}\bigr)\Bigr).
\]

The series telescopes. The limit \(a\cot a\to 1\) as \(a\to 0\) leaves

\[
\frac18\bigl(1-3\cot 3\bigr).
\]

The answer slide also prints \(\frac18\bigl(1-3\tan(\pi/2-3)\bigr)\). Those two expressions agree because \(\tan(\pi/2-3)=\cot 3\).

## Final answer

\[
\dfrac{1}{8}(1-3\cot 3).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q01_v12`. That check runs `check_r3_2024_tournament_q01_v11` for `R3-2024-Tournament-Q01-v11`: the tangent identity for `R3-2024-Tournament-Q01-v10`, and the equality of the two forms printed on slide 155.
