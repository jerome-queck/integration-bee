# R3-2024-Tournament-Q01-v10

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 4, Fight 1, problem 1, slide 153)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 155)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 4.1, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{3^{-\lfloor x\rfloor}\tan\bigl(3^{-\lfloor x\rfloor}\bigr)}{3-\tan^{2}\bigl(3^{-\lfloor x\rfloor}\bigr)}\,dx.
\]

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

`solutions/self_check.py` runs `check_r3_2024_tournament_q01_v10`. SymPy checks the tangent identity, the limit \(a\cot a\to 1\), and \(\tan(\pi/2-3)=\cot 3\).
