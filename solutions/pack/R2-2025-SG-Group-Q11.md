# R2-2025-SG-Group-Q11

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 11)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\Biggl|\int_{0}^{1}\Biggl(\pi(e^{\pi x}-1)+(1+x)\sum_{k=0}^{998}(-x)^{k}\Biggr)\,dx\Biggr|.
\]

## Solution

The finite geometric sum is
\[
(1+x)\sum_{k=0}^{998}(-x)^{k}=1-(-x)^{999}=1+x^{999}
\]
for \(x\neq -1\), hence on \([0,1]\). The integral without the absolute value splits into
\[
\int_{0}^{1}\pi(e^{\pi x}-1)\,dx+\int_{0}^{1}(1+x^{999})\,dx=(e^{\pi}-1-\pi)+\Bigl(1+\frac{1}{1000}\Bigr)=e^{\pi}-\pi+\frac{1}{1000}.
\]
This number is positive, so the absolute value leaves it unchanged.

## Final answer

\[
e^{\pi}-\pi+\dfrac{1}{1000}.
\]

## SymPy self-check

SymPy checks the closed geometric identity \((1-(-x)^{999})/(1+x)=\sum_{k=0}^{998}(-x)^{k}\), and evaluates the two pieces \(\int_{0}^{1}\pi(e^{\pi x}-1)\,dx\) and \(\int_{0}^{1}(1+x^{999})\,dx\) as \(e^{\pi}-\pi+1/1000\) together.
