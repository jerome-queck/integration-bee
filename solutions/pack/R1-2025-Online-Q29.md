# R1-2025-Online-Q29

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 29)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 29)
- The catalog row is not changed.

## Problem

\[
\int_0^{124}(f(x))^{2}\,dx,\qquad f(x)^{3}+x f(x)=125,\; f:[0,\infty)\to\mathbb{R}.
\]

## Solution

Differentiating the cubic relation gives \((3f^{2}+x)f'+f=0\). Since \(f\) is never \(0\),
\[
dx=-\Bigl(3f+\frac{x}{f}\Bigr)\,df.
\]
The endpoints are \(f(0)=5\) and \(f(124)=1\). Substituting and reversing the limits produces
\[
\int_1^{5}(3f^{3}+xf)\,df=\int_1^{5}(2f^{3}+125)\,df=\Bigl[\frac{f^{4}}{2}+125f\Bigr]_1^{5}=812,
\]
where \(f^{3}+xf=125\) was used. The solutions PDF writes the substituted integral from \(5\) to \(1\) without the minus sign in \(dx\); the mark-scheme value \(812\) is the evaluation above. Both the solutions PDF and the mark scheme print \(812\).

## Final answer

\[
812.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q29`. SymPy checks \(3f^{3}+xf=(2f^{3}+125)+(f^{3}+xf-125)\), the endpoints \(5^{3}=125\) and \(1+124\cdot 1=125\), and the antiderivative difference \(812\).
