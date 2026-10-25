# YANG-1.3-Ex02

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.3 Symmetry, Example 2
- The catalog row is `verify: unchecked` and stores no `answer_plain`. The guide prints the final in the sentence "The left term is an odd function, so the answer is just 2." This note copies that printed final. It does not invent one, and it does not change the catalog flag.

## Problem

The example is printed as

\[
\int_{-1}^{1} x\left(\frac{\sin^{-1} x}{\tan^{-1} x}+\frac1x\right)dx.
\]

That reading is the one the guide's next sentence describes: the left-hand term is odd, and what remains integrates to \(2\).

## Solution

\[
x\left(\frac{\arcsin x}{\arctan x}+\frac1x\right)=\frac{x\arcsin x}{\arctan x}+1.
\]

The first summand is an odd function of \(x\), because \(\arcsin\) and \(\arctan\) are odd, so their ratio is even and multiplication by \(x\) makes it odd. Its integral on \([-1,1]\) is \(0\). The constant term integrates to \(2\). Adding an integrand to its reflection gives \(2\) at every \(x\), which is the same conclusion.

## Final answer

\[
2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_yang_1_3_ex02`. SymPy simplifies the odd summand plus its reflection to \(0\), simplifies the full integrand plus its reflection to \(2\), and integrates the constant \(1\) from \(-1\) to \(1\) to \(2\).
