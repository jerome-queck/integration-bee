#!/usr/bin/env python3
"""Exact step checks for Yang worked solutions in sections 1.11 and 1.12.

The guide lists these practice integrals and does not print their solutions.
Differentiation uses the same zero test as verify/pack_gate.py. Definite steps
check each algebraic identity and the endpoint value. A wrong antiderivative
must fail. Run from the repository root:

    python3 verify/yang_worked_1_11.py
    python3 verify/yang_worked_1_11.py --write
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

import pack_gate

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
SECTIONS = frozenset({"1.11", "1.12"})

# final matches answer_sympy. lines are (plain, latex) without numbers.
SPECS: dict[str, dict] = {}


def _add(ident, final, lines, steps):
    SPECS[ident] = {"final": final, "lines": lines, "steps": steps}


_add(
    "YANG-1.11-P01",
    "atan(x**2)/2",
    [
        (
            "Substitution u = x**2. The derivative of x**2 is 2*x.",
            r"Substitution \(u=x^{2}\). The derivative of \(x^{2}\) is \(2x\).",
        ),
        (
            "Then x/(x**4 + 1) = (1/2)*2*x/(1 + (x**2)**2). The antiderivative is atan(x**2)/2.",
            r"Then \(x/(1+x^{4})=(1/2)\cdot 2x/(1+(x^{2})^{2})\). The antiderivative is \(\arctan(x^{2})/2\).",
        ),
    ],
    [
        ("diff_of", "x**2", "2*x"),
        ("eq", "x/(x**4 + 1)", "(1/2)*2*x/(1 + (x**2)**2)"),
        ("diff", "atan(x**2)/2"),
    ],
)
_add(
    "YANG-1.11-P02",
    "2*atan(sqrt(x))",
    [
        (
            "Substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)).",
            r"Substitution \(u=\sqrt{x}\). The derivative of \(\sqrt{x}\) is \(1/(2\sqrt{x})\).",
        ),
        (
            "Then 1/(sqrt(x)*(x + 1)) = 2*(1/(2*sqrt(x)))/(1 + sqrt(x)**2). The antiderivative is 2*atan(sqrt(x)).",
            r"Then \(1/(\sqrt{x}(x+1))=2\cdot(1/(2\sqrt{x}))/(1+x)\). The antiderivative is \(2\arctan\sqrt{x}\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "1/(sqrt(x)*(x + 1))", "2*(1/(2*sqrt(x)))/(1 + sqrt(x)**2)"),
        ("diff", "2*atan(sqrt(x))"),
    ],
)
_add(
    "YANG-1.11-P03",
    "x**2*exp(x**2)/2 - exp(x**2)/2",
    [
        (
            "Substitution u = x**2. The derivative of x**2 is 2*x, and x**3*exp(x**2) = (1/2)*x**2*exp(x**2)*(2*x).",
            r"Substitution \(u=x^{2}\). Then \(x^{3}e^{x^{2}}=(1/2)u e^{u}\,du\) after the chain rule.",
        ),
        (
            "Integration by parts in u gives (1/2)*exp(x**2)*(x**2 - 1) = x**2*exp(x**2)/2 - exp(x**2)/2.",
            r"Integration by parts gives \((1/2)e^{x^{2}}(x^{2}-1)\).",
        ),
    ],
    [
        ("diff_of", "x**2", "2*x"),
        ("eq", "x**3*exp(x**2)", "(1/2)*x**2*exp(x**2)*(2*x)"),
        ("eq", "(1/2)*exp(x**2)*(x**2 - 1)", "x**2*exp(x**2)/2 - exp(x**2)/2"),
        ("diff", "x**2*exp(x**2)/2 - exp(x**2)/2"),
    ],
)
_add(
    "YANG-1.11-P04",
    "2*x**(3/2)/3 + 2*sqrt(x) + x + 2*log(Abs(sqrt(x) - 1))",
    [
        (
            "Substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)).",
            r"Substitution \(u=\sqrt{x}\).",
        ),
        (
            "Then x/(sqrt(x) - 1) = 2*sqrt(x)**3/(sqrt(x) - 1)*(1/(2*sqrt(x))). Polynomial division gives sqrt(x)**3/(sqrt(x) - 1) = sqrt(x)**2 + sqrt(x) + 1 + 1/(sqrt(x) - 1).",
            r"Divide \(u^{3}/(u-1)\) to get \(u^{2}+u+1+1/(u-1)\).",
        ),
        (
            "Termwise integration gives 2*(sqrt(x)**3/3 + sqrt(x)**2/2 + sqrt(x) + log(Abs(sqrt(x) - 1))) = 2*x**(3/2)/3 + 2*sqrt(x) + x + 2*log(Abs(sqrt(x) - 1)).",
            r"The antiderivative is \(\frac{2}{3}x^{3/2}+x+2\sqrt{x}+2\log|\sqrt{x}-1|\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "x/(sqrt(x) - 1)", "2*sqrt(x)**3/(sqrt(x) - 1)*(1/(2*sqrt(x)))"),
        ("eq", "sqrt(x)**3/(sqrt(x) - 1)", "sqrt(x)**2 + sqrt(x) + 1 + 1/(sqrt(x) - 1)"),
        (
            "eq",
            "2*(sqrt(x)**3/3 + sqrt(x)**2/2 + sqrt(x) + log(Abs(sqrt(x) - 1)))",
            "2*x**(3/2)/3 + 2*sqrt(x) + x + 2*log(Abs(sqrt(x) - 1))",
        ),
        ("diff", "2*x**(3/2)/3 + 2*sqrt(x) + x + 2*log(Abs(sqrt(x) - 1))"),
    ],
)
_add(
    "YANG-1.11-P05",
    "2*sin(sqrt(x))",
    [
        (
            "Substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)).",
            r"Substitution \(u=\sqrt{x}\).",
        ),
        (
            "Then cos(sqrt(x))/sqrt(x) = 2*cos(sqrt(x))*(1/(2*sqrt(x))). The antiderivative is 2*sin(sqrt(x)).",
            r"The integral is \(2\int\cos u\,du=2\sin\sqrt{x}\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "cos(sqrt(x))/sqrt(x)", "2*cos(sqrt(x))*(1/(2*sqrt(x)))"),
        ("diff", "2*sin(sqrt(x))"),
    ],
)
_add(
    "YANG-1.11-P06",
    "-exp(1/x)",
    [
        (
            "Substitution u = 1/x. The derivative of 1/x is -1/x**2.",
            r"Substitution \(u=1/x\). Then \(du=-dx/x^{2}\).",
        ),
        (
            "Then exp(1/x)/x**2 = -exp(1/x)*(-1/x**2). The antiderivative is -exp(1/x).",
            r"The integral is \(-\int e^{u}\,du=-e^{1/x}\).",
        ),
    ],
    [
        ("diff_of", "1/x", "-1/x**2"),
        ("eq", "exp(1/x)/x**2", "-exp(1/x)*(-1/x**2)"),
        ("diff", "-exp(1/x)"),
    ],
)
_add(
    "YANG-1.11-P07",
    "asin(2*x - 1)",
    [
        (
            "Complete the square. x - x**2 = 1/4 - (x - 1/2)**2, and 1 - (2*x - 1)**2 = 4*(x - x**2).",
            r"Complete the square. \(x-x^{2}=1/4-(x-1/2)^{2}\).",
        ),
        (
            "The antiderivative is asin(2*x - 1).",
            r"The antiderivative is \(\arcsin(2x-1)\).",
        ),
    ],
    [
        ("eq", "x - x**2", "1/4 - (x - 1/2)**2"),
        ("eq", "1 - (2*x - 1)**2", "4*(x - x**2)"),
        ("diff", "asin(2*x - 1)"),
    ],
)
_add(
    "YANG-1.11-P08",
    "-2*cos(x**(3/2))/3",
    [
        (
            "Substitution u = x**(3/2). The derivative of x**(3/2) is (3/2)*sqrt(x).",
            r"Substitution \(u=x^{3/2}\). Then \(du=(3/2)\sqrt{x}\,dx\).",
        ),
        (
            "Then sqrt(x)*sin(x**(3/2)) = (2/3)*sin(x**(3/2))*((3/2)*sqrt(x)). The antiderivative is -2*cos(x**(3/2))/3.",
            r"The integral is \((2/3)\int\sin u\,du=-2\cos(x^{3/2})/3\).",
        ),
    ],
    [
        ("diff_of", "x**(3/2)", "(3/2)*sqrt(x)"),
        ("eq", "sqrt(x)*sin(x**(3/2))", "(2/3)*sin(x**(3/2))*((3/2)*sqrt(x))"),
        ("diff", "-2*cos(x**(3/2))/3"),
    ],
)
_add(
    "YANG-1.11-P09",
    "1/18",
    [
        (
            "Substitution u = 2*x - 1. Then 2*0 - 1 = -1 and 2*1 - 1 = 1, and 2*(2*x)**2*(2*x - 1)**7/8 = x**2*(2*x - 1)**7.",
            r"Substitution \(u=2x-1\) runs from \(-1\) to \(1\).",
        ),
        (
            "Expand ((x + 1)**2)*x**7/8 = (x**9 + 2*x**8 + x**7)/8 = (x**9 + x**7)/8 + x**8/4. The odd part x**9 + x**7 integrates to 0 on [-1, 1].",
            r"Only the even part \(x^{8}/4\) survives on \([-1,1]\).",
        ),
        (
            "The antiderivative of (x**9 + x**7)/8 is x**10/80 + x**8/64, and the antiderivative of x**8/4 is x**9/36. The second evaluation is 1/18.",
            r"The even integral equals \(1/18\).",
        ),
    ],
    [
        ("eq", "2*0 - 1", "-1"),
        ("eq", "2*1 - 1", "1"),
        ("eq", "2*(2*x)**2*(2*x - 1)**7/8", "x**2*(2*x - 1)**7"),
        ("eq", "((x + 1)**2)*x**7/8", "(x**9 + 2*x**8 + x**7)/8"),
        ("eq", "(x**9 + 2*x**8 + x**7)/8", "(x**9 + x**7)/8 + x**8/4"),
        ("odd", "x**9 + x**7"),
        ("diff_of", "x**10/80 + x**8/64", "(x**9 + x**7)/8"),
        ("ends", "x**10/80 + x**8/64", "-1", "1", "1", "0"),
        ("diff_of", "x**9/36", "x**8/4"),
        ("ends", "x**9/36", "-1", "1", "1", "1/18"),
        ("sum", "0", "1/18", "1/18"),
    ],
)
_add(
    "YANG-1.11-P10",
    "-sqrt(x**4 + 1)/(6*x**2) - sqrt(x**4 + 1)/(6*x**6)",
    [
        (
            "Substitution t = 1/x**4. The derivative of 1/x**4 is -4/x**5.",
            r"Substitution \(t=1/x^{4}\).",
        ),
        (
            "For positive x, sqrt((x**4 + 1)/x**4)/x**5 = sqrt(x**4 + 1)/x**7 = -sqrt(1 + 1/x**4)*(-4/x**5)/4.",
            r"The integrand is \(\sqrt{1+t}\) times \(-dt/4\).",
        ),
        (
            "The compact antiderivative -(1 + 1/x**4)**(3/2)/6 equals -sqrt(x**4 + 1)/(6*x**2) - sqrt(x**4 + 1)/(6*x**6).",
            r"That integral is \(-(1+1/x^{4})^{3/2}/6\).",
        ),
    ],
    [
        ("diff_of", "1/x**4", "-4/x**5"),
        ("eq", "sqrt((x**4 + 1)/x**4)/x**5", "sqrt(x**4 + 1)/x**7"),
        ("eq", "sqrt((x**4 + 1)/x**4)/x**5", "-sqrt(1 + 1/x**4)*(-4/x**5)/4"),
        (
            "eq",
            "-(1 + 1/x**4)**(3/2)/6",
            "-sqrt(x**4 + 1)/(6*x**2) - sqrt(x**4 + 1)/(6*x**6)",
        ),
        ("diff", "-sqrt(x**4 + 1)/(6*x**2) - sqrt(x**4 + 1)/(6*x**6)"),
    ],
)
_add(
    "YANG-1.11-P11",
    "2*x**3*sqrt(x - 1)/7 - 2*x**2*sqrt(x - 1)/35 - 8*x*sqrt(x - 1)/105 - 16*sqrt(x - 1)/105",
    [
        (
            "Substitution u = sqrt(x - 1). The derivative of sqrt(x - 1) is 1/(2*sqrt(x - 1)).",
            r"Substitution \(u=\sqrt{x-1}\). Then \(x=u^{2}+1\) and \(dx=2u\,du\).",
        ),
        (
            "The chain-rule form is 2*((sqrt(x - 1)**2 + 1)**2)*sqrt(x - 1)**2*(1/(2*sqrt(x - 1))) = x**2*sqrt(x - 1).",
            r"The integral becomes \(2\int(u^{2}+1)^{2}u^{2}\,du\).",
        ),
        (
            "Integrate the powers. 2*(sqrt(x - 1)**7/7 + 2*sqrt(x - 1)**5/5 + sqrt(x - 1)**3/3) = 2*x**3*sqrt(x - 1)/7 - 2*x**2*sqrt(x - 1)/35 - 8*x*sqrt(x - 1)/105 - 16*sqrt(x - 1)/105.",
            r"Back-substitute \(u=\sqrt{x-1}\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x - 1)", "1/(2*sqrt(x - 1))"),
        (
            "eq",
            "2*((sqrt(x - 1)**2 + 1)**2)*sqrt(x - 1)**2*(1/(2*sqrt(x - 1)))",
            "x**2*sqrt(x - 1)",
        ),
        (
            "eq",
            "2*(sqrt(x - 1)**7/7 + 2*sqrt(x - 1)**5/5 + sqrt(x - 1)**3/3)",
            "2*x**3*sqrt(x - 1)/7 - 2*x**2*sqrt(x - 1)/35 - 8*x*sqrt(x - 1)/105 - 16*sqrt(x - 1)/105",
        ),
        (
            "diff",
            "2*x**3*sqrt(x - 1)/7 - 2*x**2*sqrt(x - 1)/35 - 8*x*sqrt(x - 1)/105 - 16*sqrt(x - 1)/105",
        ),
    ],
)
_add(
    "YANG-1.11-P12",
    "sqrt(x**2 + 10*x + 16)",
    [
        (
            "Substitution u = x + 5. The derivative of x + 5 is 1, and (x + 2)*(x + 8) = (x + 5)**2 - 9.",
            r"Substitution \(u=x+5\). Then \((x+2)(x+8)=u^{2}-9\).",
        ),
        (
            "The standard integral is sqrt((x + 5)**2 - 9) = sqrt(x**2 + 10*x + 16).",
            r"The antiderivative is \(\sqrt{u^{2}-9}=\sqrt{x^{2}+10x+16}\).",
        ),
    ],
    [
        ("diff_of", "x + 5", "1"),
        ("eq", "(x + 2)*(x + 8)", "(x + 5)**2 - 9"),
        ("eq", "sqrt((x + 5)**2 - 9)", "sqrt(x**2 + 10*x + 16)"),
        ("diff", "sqrt(x**2 + 10*x + 16)"),
    ],
)
_add(
    "YANG-1.11-P13",
    "atan(exp(2*x))/2",
    [
        (
            "Substitution u = exp(2*x). The derivative of exp(2*x) is 2*exp(2*x).",
            r"Substitution \(u=e^{2x}\). Then \(du=2e^{2x}\,dx\).",
        ),
        (
            "Then exp(2*x)/(exp(4*x) + 1) = (1/2)*2*exp(2*x)/(1 + exp(2*x)**2). The antiderivative is atan(exp(2*x))/2.",
            r"The integral is \((1/2)\arctan(e^{2x})\).",
        ),
    ],
    [
        ("diff_of", "exp(2*x)", "2*exp(2*x)"),
        ("eq", "exp(2*x)/(exp(4*x) + 1)", "(1/2)*2*exp(2*x)/(1 + exp(2*x)**2)"),
        ("diff", "atan(exp(2*x))/2"),
    ],
)
_add(
    "YANG-1.11-P14",
    "-2 - log(2)",
    [
        (
            "Substitution u = x - 2. Then x**2/(x - 2)**3 = ((x - 2) + 2)**2/(x - 2)**3 = 1/(x - 2) + 4/(x - 2)**2 + 4/(x - 2)**3.",
            r"Substitution \(u=x-2\) on \([1,3/2]\) gives \(1/u+4/u^{2}+4/u^{3}\).",
        ),
        (
            "The antiderivative is log(Abs(x - 2)) - 4/(x - 2) - 2/(x - 2)**2. From 1 to 3/2 it equals -2 - log(2).",
            r"Evaluating \(\log|u|-4/u-2/u^{2}\) from \(-1\) to \(-1/2\) gives \(-2-\log 2\).",
        ),
    ],
    [
        ("eq", "x**2/(x - 2)**3", "((x - 2) + 2)**2/(x - 2)**3"),
        ("eq", "((x - 2) + 2)**2/(x - 2)**3", "1/(x - 2) + 4/(x - 2)**2 + 4/(x - 2)**3"),
        ("diff_of", "log(Abs(x - 2)) - 4/(x - 2) - 2/(x - 2)**2", "1/(x - 2) + 4/(x - 2)**2 + 4/(x - 2)**3"),
        ("ends", "log(Abs(x - 2)) - 4/(x - 2) - 2/(x - 2)**2", "1", "3/2", "1", "-2 - log(2)"),
    ],
)
_add(
    "YANG-1.11-P15",
    "2*sin(x)**(3/2)/(3*cos(x)**(3/2))",
    [
        (
            "Where tan(x) > 0, sqrt(sin(x))/cos(x)**(5/2) = sqrt(tan(x))*sec(x)**2. The derivative of tan(x) is sec(x)**2.",
            r"Write the integrand as \(\sqrt{\tan x}\sec^{2}x\).",
        ),
        (
            "The integral of sqrt(u) is (2/3)*tan(x)**(3/2) = 2*sin(x)**(3/2)/(3*cos(x)**(3/2)).",
            r"Then \(\int\sqrt{u}\,du=(2/3)\tan^{3/2}x\).",
        ),
    ],
    [
        ("diff_of", "tan(x)", "sec(x)**2"),
        ("atan_pos", "sqrt(sin(x))/cos(x)**(5/2)", "sqrt(tan(x))*sec(x)**2"),
        ("atan_pos", "(2/3)*tan(x)**(3/2)", "2*sin(x)**(3/2)/(3*cos(x)**(3/2))"),
        ("diff", "2*sin(x)**(3/2)/(3*cos(x)**(3/2))"),
    ],
)
_add(
    "YANG-1.11-P16",
    "log(tan(x) + sec(x))**2/2",
    [
        (
            "Substitution u = log(tan(x) + sec(x)). The derivative of log(tan(x) + sec(x)) is sec(x).",
            r"Substitution \(u=\log(\tan x+\sec x)\). Then \(du=\sec x\,dx\).",
        ),
        (
            "The integral of u is u**2/2. The antiderivative is log(tan(x) + sec(x))**2/2.",
            r"The antiderivative is \(\log(\tan x+\sec x)^{2}/2\).",
        ),
    ],
    [
        ("diff_of", "log(tan(x) + sec(x))", "sec(x)"),
        ("diff", "log(tan(x) + sec(x))**2/2"),
    ],
)
_add(
    "YANG-1.11-P17",
    "-2/(sqrt(x) + 1)",
    [
        (
            "The inside is a square. 1 + 2*sqrt(x) + x = (1 + sqrt(x))**2. The derivative of sqrt(x) is 1/(2*sqrt(x)).",
            r"Factor \(1+2\sqrt{x}+x=(1+\sqrt{x})^{2}\).",
        ),
        (
            "Then 1/(sqrt(x)*(1 + 2*sqrt(x) + x)) = 2*(1/(2*sqrt(x)))/(1 + sqrt(x))**2. The antiderivative is -2/(sqrt(x) + 1).",
            r"Substitution \(u=\sqrt{x}\) gives \(2\int du/(1+u)^{2}=-2/(1+\sqrt{x})\).",
        ),
    ],
    [
        ("eq", "1 + 2*sqrt(x) + x", "(1 + sqrt(x))**2"),
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "1/(sqrt(x)*(1 + 2*sqrt(x) + x))", "2*(1/(2*sqrt(x)))/(1 + sqrt(x))**2"),
        ("diff", "-2/(sqrt(x) + 1)"),
    ],
)
_add(
    "YANG-1.11-P18",
    "atan(tan(x)/3)/3",
    [
        (
            "Substitution u = tan(x). The derivative of tan(x) is sec(x)**2, and sec(x)**2 + 8 = tan(x)**2 + 9.",
            r"Substitution \(u=\tan x\). Then \(8+\sec^{2}x=9+u^{2}\).",
        ),
        (
            "The antiderivative is atan(tan(x)/3)/3.",
            r"The antiderivative is \(\arctan(u/3)/3\).",
        ),
    ],
    [
        ("diff_of", "tan(x)", "sec(x)**2"),
        ("eq", "sec(x)**2 + 8", "tan(x)**2 + 9"),
        ("diff", "atan(tan(x)/3)/3"),
    ],
)
_add(
    "YANG-1.11-P19",
    "2*asin(x**(3/2))/3",
    [
        (
            "Write sqrt(x/(1 - x**3)) = sqrt(x)/sqrt(1 - x**3). The derivative of x**(3/2) is (3/2)*sqrt(x).",
            r"Set \(s=x^{3/2}\). Then \(ds=(3/2)\sqrt{x}\,dx\).",
        ),
        (
            "Then sqrt(x)/sqrt(1 - x**3) = (2/3)*((3/2)*sqrt(x))/sqrt(1 - (x**(3/2))**2). The antiderivative is 2*asin(x**(3/2))/3.",
            r"The integral is \((2/3)\arcsin(x^{3/2})\).",
        ),
    ],
    [
        ("eq", "sqrt(x/(1 - x**3))", "sqrt(x)/sqrt(1 - x**3)"),
        ("diff_of", "x**(3/2)", "(3/2)*sqrt(x)"),
        ("eq", "sqrt(x)/sqrt(1 - x**3)", "(2/3)*((3/2)*sqrt(x))/sqrt(1 - (x**(3/2))**2)"),
        ("diff", "2*asin(x**(3/2))/3"),
    ],
)
_add(
    "YANG-1.11-P20",
    "log(Abs(x*log(x) + 1))",
    [
        (
            "The numerator is the derivative of the denominator. The derivative of x*log(x) + 1 is log(x) + 1.",
            r"The derivative of \(x\log x+1\) is \(\log x+1\).",
        ),
        (
            "The antiderivative is log(Abs(x*log(x) + 1)).",
            r"The antiderivative is \(\log|x\log x+1|\).",
        ),
    ],
    [
        ("diff_of", "x*log(x) + 1", "log(x) + 1"),
        ("diff", "log(Abs(x*log(x) + 1))"),
    ],
)
_add(
    "YANG-1.12-P01",
    "4",
    [
        (
            "Split at the roots of x**2 - 1. On [-2, -1] and [1, 2], Abs(x**2 - 1) = x**2 - 1. On [-1, 1], Abs(x**2 - 1) = 1 - x**2.",
            r"Split at \(x=\pm 1\).",
        ),
        (
            "The antiderivative of x**2 - 1 is x**3/3 - x, and each outer piece equals 4/3. The antiderivative of 1 - x**2 is x - x**3/3, and the middle piece equals 4/3.",
            r"The three polynomial evaluations are each \(4/3\).",
        ),
    ],
    [
        ("abs_on", "x**2 - 1", "x**2 - 1", "-2", "-1"),
        ("abs_on", "x**2 - 1", "1 - x**2", "-1", "1"),
        ("abs_on", "x**2 - 1", "x**2 - 1", "1", "2"),
        ("diff_of", "x**3/3 - x", "x**2 - 1"),
        ("diff_of", "x - x**3/3", "1 - x**2"),
        ("ends", "x**3/3 - x", "-2", "-1", "1", "4/3"),
        ("ends", "x - x**3/3", "-1", "1", "1", "4/3"),
        ("ends", "x**3/3 - x", "1", "2", "1", "4/3"),
        ("sum", "4/3", "4/3", "4/3", "4"),
    ],
)
_add(
    "YANG-1.12-P02",
    "1 + log(3)",
    [
        (
            "On [0, 1], Abs(x - 1) = 1 - x, so the denominator x + (1 - x) equals 1. On [1, 5], Abs(x - 1) = x - 1, so the denominator x + (x - 1) equals 2*x - 1.",
            r"Split at \(x=1\).",
        ),
        (
            "The first piece is the integral of 1, with antiderivative x, and equals 1. The second integrates 1/(2*x - 1), with antiderivative log(2*x - 1)/2, and equals log(9)/2 = log(3).",
            r"The pieces are \(1\) and \(\log 3\).",
        ),
    ],
    [
        ("abs_on", "x - 1", "1 - x", "0", "1"),
        ("abs_on", "x - 1", "x - 1", "1", "5"),
        ("eq", "x + (1 - x)", "1"),
        ("eq", "x + (x - 1)", "2*x - 1"),
        ("diff_of", "x", "1"),
        ("ends", "x", "0", "1", "1", "1"),
        ("diff_of", "log(2*x - 1)/2", "1/(2*x - 1)"),
        ("ends", "log(2*x - 1)/2", "1", "5", "1", "log(9)/2"),
        ("eq", "log(9)/2", "log(3)"),
        ("sum", "1", "log(3)", "1 + log(3)"),
    ],
)
_add(
    "YANG-1.12-P03",
    "-2 + exp(-1) + E",
    [
        (
            "On [0, 1], exp(x) - 1 stays nonnegative because the integral of exp from 0 to a nonnegative height is exp(h) - 1. The antiderivative exp(x) - x evaluates to E - 2.",
            r"On \([0,1]\), \(|e^{x}-1|=e^{x}-1\), and the piece is \(e-2\).",
        ),
        (
            "The reflection u = -x turns [-1, 0] into [0, 1]. There the integrand is 1 - exp(-x), with antiderivative x + exp(-x), and the piece equals exp(-1).",
            r"The reflected piece is \(e^{-1}\).",
        ),
    ],
    [
        ("exp_parts", "E - 2", "exp(-1)"),
        ("diff_of", "exp(x) - x", "exp(x) - 1"),
        ("ends", "exp(x) - x", "0", "1", "1", "E - 2"),
        ("diff_of", "x + exp(-x)", "1 - exp(-x)"),
        ("ends", "x + exp(-x)", "0", "1", "1", "exp(-1)"),
        ("sum", "E - 2", "exp(-1)", "-2 + exp(-1) + E"),
    ],
)
_add(
    "YANG-1.12-P04",
    "2",
    [
        (
            "For nonnegative x the nested absolute value Abs(x - Abs(x - Abs(x))) equals x. For negative x it equals -3*x.",
            r"For \(x\ge 0\) the integrand is \(x\). For \(x<0\) it is \(-3x\).",
        ),
        (
            "The antiderivative -3*x**2/2 on [-1, 0] equals 3/2. The antiderivative x**2/2 on [0, 1] equals 1/2.",
            r"The pieces are \(3/2\) and \(1/2\).",
        ),
    ],
    [
        ("assume_abs", "0", "1", "x"),
        ("assume_abs", "-1", "0", "-3*x"),
        ("diff_of", "-3*x**2/2", "-3*x"),
        ("ends", "-3*x**2/2", "-1", "0", "1", "3/2"),
        ("diff_of", "x**2/2", "x"),
        ("ends", "x**2/2", "0", "1", "1", "1/2"),
        ("sum", "3/2", "1/2", "2"),
    ],
)
_add(
    "YANG-1.12-P05",
    "8",
    [
        (
            "On [0, pi], the minimum of sin(x) is 0, so Abs(sin(x)) = sin(x). The antiderivative -cos(x) increases by 2.",
            r"On \([0,\pi]\), \(|\sin x|=\sin x\), and the integral is \(2\).",
        ),
        (
            "Each shift by an integer multiple of pi, namely -2, -1, 0, and 1, pulls one period back to that interval. Four copies of 2 add to 8.",
            r"Four periods from \(-2\pi\) to \(2\pi\) add to \(8\).",
        ),
    ],
    [
        ("diff_of", "-cos(x)", "sin(x)"),
        ("ends", "-cos(x)", "0", "pi", "1", "2"),
        ("shift", "-2"),
        ("shift", "-1"),
        ("shift", "0"),
        ("shift", "1"),
        ("sum", "2", "2", "2", "2", "8"),
    ],
)
_add(
    "YANG-1.12-P06",
    "-3*log(5)/4 + 2 + 9*log(3)/4",
    [
        (
            "On [0, 1], Abs(x - 1) = 1 - x, Abs(x - 2) = 2 - x, and Abs(x - 3) = 3 - x. The quotient (1 - x)/((2 - x) + (3 - x)) equals (1 - x)/(5 - 2*x).",
            r"On \([0,1]\) the quotient is \((1-x)/(5-2x)\).",
        ),
        (
            "Its antiderivative x/2 + 3*log(Abs(5 - 2*x))/4 from 0 to 1 equals 1/2 + 3*log(3)/4 - 3*log(5)/4.",
            r"The first piece is \(1/2+3\log 3/4-3\log 5/4\).",
        ),
        (
            "On [1, 2], Abs(x - 1) = x - 1, Abs(x - 2) = 2 - x, and Abs(x - 3) = 3 - x. The quotient (x - 1)/((2 - x) + (3 - x)) equals (x - 1)/(5 - 2*x).",
            r"On \([1,2]\) the quotient is \((x-1)/(5-2x)\).",
        ),
        (
            "Its antiderivative -x/2 - 3*log(Abs(5 - 2*x))/4 from 1 to 2 equals -1/2 + 3*log(3)/4.",
            r"The second piece is \(-1/2+3\log 3/4\).",
        ),
        (
            "On [2, 3], Abs(x - 1) = x - 1, Abs(x - 2) = x - 2, and Abs(x - 3) = 3 - x. The quotient (x - 1)/((x - 2) + (3 - x)) equals x - 1. The antiderivative x**2/2 - x from 2 to 3 equals 3/2.",
            r"On \([2,3]\) the integrand is \(x-1\), and the piece is \(3/2\).",
        ),
        (
            "On [3, 4], Abs(x - 1) = x - 1, Abs(x - 2) = x - 2, and Abs(x - 3) = x - 3. The quotient (x - 1)/((x - 2) + (x - 3)) equals (x - 1)/(2*x - 5), which equals (1 - x)/(5 - 2*x). The same antiderivative x/2 + 3*log(Abs(5 - 2*x))/4 from 3 to 4 equals 1/2 + 3*log(3)/4.",
            r"On \([3,4]\) the piece is \(1/2+3\log 3/4\).",
        ),
    ],
    [
        ("abs_on", "x - 1", "1 - x", "0", "1"),
        ("abs_on", "x - 2", "2 - x", "0", "1"),
        ("abs_on", "x - 3", "3 - x", "0", "1"),
        ("eq", "(1 - x)/((2 - x) + (3 - x))", "(1 - x)/(5 - 2*x)"),
        ("diff_of", "x/2 + 3*log(Abs(5 - 2*x))/4", "(1 - x)/(5 - 2*x)"),
        ("ends", "x/2 + 3*log(Abs(5 - 2*x))/4", "0", "1", "1", "1/2 + 3*log(3)/4 - 3*log(5)/4"),
        ("abs_on", "x - 1", "x - 1", "1", "2"),
        ("abs_on", "x - 2", "2 - x", "1", "2"),
        ("abs_on", "x - 3", "3 - x", "1", "2"),
        ("eq", "(x - 1)/((2 - x) + (3 - x))", "(x - 1)/(5 - 2*x)"),
        ("diff_of", "-x/2 - 3*log(Abs(5 - 2*x))/4", "(x - 1)/(5 - 2*x)"),
        ("ends", "-x/2 - 3*log(Abs(5 - 2*x))/4", "1", "2", "1", "-1/2 + 3*log(3)/4"),
        ("abs_on", "x - 1", "x - 1", "2", "3"),
        ("abs_on", "x - 2", "x - 2", "2", "3"),
        ("abs_on", "x - 3", "3 - x", "2", "3"),
        ("eq", "(x - 1)/((x - 2) + (3 - x))", "x - 1"),
        ("diff_of", "x**2/2 - x", "x - 1"),
        ("ends", "x**2/2 - x", "2", "3", "1", "3/2"),
        ("abs_on", "x - 1", "x - 1", "3", "4"),
        ("abs_on", "x - 2", "x - 2", "3", "4"),
        ("abs_on", "x - 3", "x - 3", "3", "4"),
        ("eq", "(x - 1)/((x - 2) + (x - 3))", "(x - 1)/(2*x - 5)"),
        ("eq", "(x - 1)/(2*x - 5)", "(1 - x)/(5 - 2*x)"),
        ("ends", "x/2 + 3*log(Abs(5 - 2*x))/4", "3", "4", "1", "1/2 + 3*log(3)/4"),
        (
            "sum",
            "1/2 + 3*log(3)/4 - 3*log(5)/4",
            "-1/2 + 3*log(3)/4",
            "3/2",
            "1/2 + 3*log(3)/4",
            "-3*log(5)/4 + 2 + 9*log(3)/4",
        ),
    ],
)
_add(
    "YANG-1.12-P07",
    "2",
    [
        (
            "The integrand is even, since exp(-Abs(-x)) = exp(-Abs(x)), and the derivative of -x is -1.",
            r"The integrand is even, so the line is twice the integral on \([0,\infty)\).",
        ),
        (
            "On [0, oo], Abs(x) = x, so the integrand is exp(-x). The antiderivative -exp(-x), doubled, equals 2.",
            r"Twice \(\int_0^\infty e^{-x}\,dx\) is \(2\).",
        ),
    ],
    [
        ("eq", "exp(-Abs(-x))", "exp(-Abs(x))"),
        ("diff_of", "-x", "-1"),
        ("abs_on", "x", "x", "0", "oo"),
        ("diff_of", "-exp(-x)", "exp(-x)"),
        ("ends", "-exp(-x)", "0", "oo", "2", "2"),
    ],
)
_add(
    "YANG-1.12-P08",
    "E",
    [
        (
            "The derivative of x - log(x) is (x - 1)/x, which stays nonnegative on [1, E]. The value at 1 is 1, so x - log(x) stays positive and the absolute value drops.",
            r"On \([1,e]\), \(x-\log x\) increases from \(1\).",
        ),
        (
            "Clearing it gives (x + 1)/(Abs(x - log(x)) + log(x)) = (x + 1)/x. The antiderivative x + log(x) from 1 to E equals E.",
            r"The integrand simplifies to \((x+1)/x\), and the evaluation is \(e\).",
        ),
    ],
    [
        (
            "replace_abs",
            "(x + 1)/(Abs(x - log(x)) + log(x))",
            "x - log(x)",
            "(x - 1)/x",
            "(x + 1)/x",
            "1",
            "E",
        ),
        ("diff_of", "x + log(x)", "(x + 1)/x"),
        ("ends", "x + log(x)", "1", "E", "1", "E"),
    ],
)
_add(
    "YANG-1.12-P09",
    "16",
    [
        (
            "Squaring compares the roots. sqrt(4) = 2 and sqrt(x)**2 = x. On [0, 4], Abs(x - 4) = 4 - x, so sqrt(x) <= 2. On [4, 16], x - 4 stays nonnegative, so sqrt(x) >= 2.",
            r"Then \(\sqrt{x}\le 2\) on \([0,4]\) and \(\sqrt{x}\ge 2\) on \([4,16]\).",
        ),
        (
            "The antiderivative 2*x - 2*x**(3/2)/3 of 2 - sqrt(x) from 0 to 4 equals 8/3. The antiderivative 2*x**(3/2)/3 - 2*x of sqrt(x) - 2 from 4 to 16 equals 40/3.",
            r"The pieces are \(8/3\) and \(40/3\).",
        ),
    ],
    [
        ("eq", "sqrt(4)", "2"),
        ("eq", "sqrt(x)**2", "x"),
        ("abs_on", "x - 4", "4 - x", "0", "4"),
        ("abs_on", "x - 4", "x - 4", "4", "16"),
        ("diff_of", "2*x - 2*x**(3/2)/3", "2 - sqrt(x)"),
        ("ends", "2*x - 2*x**(3/2)/3", "0", "4", "1", "8/3"),
        ("diff_of", "2*x**(3/2)/3 - 2*x", "sqrt(x) - 2"),
        ("ends", "2*x**(3/2)/3 - 2*x", "4", "16", "1", "40/3"),
        ("sum", "8/3", "40/3", "16"),
    ],
)
_add(
    "YANG-1.12-P10",
    "-2 - sqrt(2)*log(sqrt(2) + sqrt(3)) + 2*log(sqrt(3) + 2) + pi",
    [
        (
            "The integrand is even. 1/(sqrt(Abs(1 - (-x)**2)) + 1) = 1/(sqrt(Abs(1 - x**2)) + 1), and the derivative of -x is -1, so the integral is twice the integral on [0, 2].",
            r"Evenness reduces the integral to twice the integral on \([0,2]\).",
        ),
        (
            "On [0, 1], both 1 - x and 1 + x stay nonnegative, and (1 - x)*(1 + x) = 1 - x**2. The substitution x = sin(theta) produces cos(x)/(1 + cos(x)) = 1 - (1/2)/cos(x/2)**2.",
            r"On \([0,1]\), \(x=\sin\theta\) produces \(1-(1/2)\sec^{2}(\theta/2)\).",
        ),
        (
            "The antiderivative x - tan(x/2) from 0 to pi/2 equals pi/2 - 1.",
            r"That piece equals \(\pi/2-1\).",
        ),
        (
            "On [1, 2], both x - 1 and x + 1 stay nonnegative, and (x - 1)*(x + 1) = x**2 - 1. The hyperbolic substitution produces sinh(x)/(1 + sinh(x)), whose evaluated antiderivative is log(2 + sqrt(3)) - log(sqrt(2) + sqrt(3))/sqrt(2).",
            r"On \([1,2]\), \(x=\cosh u\) evaluates to \(\log(2+\sqrt{3})-\log(\sqrt{2}+\sqrt{3})/\sqrt{2}\).",
        ),
        (
            "Doubling the sum gives 2*((pi/2 - 1) + (log(2 + sqrt(3)) - log(sqrt(2) + sqrt(3))/sqrt(2))).",
            r"Twice the sum is the stored value.",
        ),
    ],
    [
        ("eq", "1/(sqrt(Abs(1 - (-x)**2)) + 1)", "1/(sqrt(Abs(1 - x**2)) + 1)"),
        ("diff_of", "-x", "-1"),
        ("abs_prod", "1 - x", "1 + x", "0", "1"),
        ("eq", "(1 - x)*(1 + x)", "1 - x**2"),
        ("sine_pull", "cos(x)/(1 + cos(x))"),
        ("eq", "cos(x)/(1 + cos(x))", "1 - (1/2)/cos(x/2)**2"),
        ("diff_of", "x - tan(x/2)", "1 - (1/2)/cos(x/2)**2"),
        ("ends", "x - tan(x/2)", "0", "pi/2", "1", "pi/2 - 1"),
        ("abs_prod", "x - 1", "x + 1", "1", "2"),
        ("eq", "(x - 1)*(x + 1)", "x**2 - 1"),
        ("hyperbolic", "log(2 + sqrt(3)) - log(sqrt(2) + sqrt(3))/sqrt(2)"),
        (
            "eq",
            "2*((pi/2 - 1) + (log(2 + sqrt(3)) - log(sqrt(2) + sqrt(3))/sqrt(2)))",
            "-2 - sqrt(2)*log(sqrt(2) + sqrt(3)) + 2*log(sqrt(3) + 2) + pi",
        ),
    ],
)


def parse(text: str):
    return pack_gate._parse(text, "x")


def fold(text: str) -> str:
    return "".join(str(text).split())


def symbol():
    return pack_gate.namespace("x")["x"]


def same(left, right) -> bool:
    if pack_gate._zero(left - right):
        return True
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero((left - right).subs(symbol(), positive))


def diff_ok(antiderivative, integrand) -> bool:
    delta = sp.diff(antiderivative, symbol()) - integrand
    if pack_gate._zero(delta):
        return True
    dropped = pack_gate._drop_log_abs(antiderivative)
    if dropped != antiderivative and pack_gate._zero(sp.diff(dropped, symbol()) - integrand):
        return True
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero(delta.subs(symbol(), positive))


def must_show(token: str) -> bool:
    return any(char.isalpha() for char in token) or "**" in token or "/" in token


def _ge0(value) -> bool:
    if value == sp.oo:
        return True
    if value == -sp.oo:
        return False
    simplified = sp.simplify(value)
    if simplified == 0 or simplified.is_nonnegative is True:
        return True
    return simplified >= 0


def _le0(value) -> bool:
    return _ge0(sp.simplify(-value))


def interval_sign(expr, lo, hi):
    expanded = sp.expand(expr)
    if expanded == 0:
        return "nonneg"
    if not expanded.is_polynomial(symbol()):
        return None
    polynomial = sp.Poly(expanded, symbol())
    degree = polynomial.degree()
    if degree is None or degree < 0 or degree > 2:
        return None
    points = [lo, hi]
    if degree == 2:
        vertex = sp.simplify(-polynomial.nth(1) / (2 * polynomial.LC()))
        if _ge0(vertex - lo) and _ge0(hi - vertex):
            points.append(vertex)
    values = []
    for point in points:
        if point == sp.oo:
            values.append(sp.oo if _ge0(polynomial.LC()) else -sp.oo)
        elif point == -sp.oo:
            sign = sp.oo if _ge0(polynomial.LC()) else -sp.oo
            values.append(sign if degree % 2 == 0 else -sign)
        else:
            values.append(sp.simplify(expanded.subs(symbol(), point)))
    if all(_ge0(item) for item in values):
        return "nonneg"
    if all(_le0(item) for item in values):
        return "nonpos"
    return None


def load_rows() -> list[dict]:
    return [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]


def section_rows(rows: list[dict]) -> list[dict]:
    chosen = []
    for row in rows:
        if row.get("source") != "yang_book" or row.get("kind") == "reference":
            continue
        if row.get("section") not in SECTIONS:
            continue
        if row.get("worked_solution_origin") == "pdf_copy":
            continue
        plain = row.get("worked_solution_plain")
        if plain not in (None, "") and row.get("id") not in SPECS:
            continue
        chosen.append(row)
    return chosen


def compose(row: dict, spec: dict) -> tuple[str, str]:
    plain = "\n".join(f"{index}. {text}" for index, (text, _) in enumerate(spec["lines"], 1))
    latex = "\n".join(f"{index}. {text}" for index, (_, text) in enumerate(spec["lines"], 1))
    plain += f"\nThe answer is {row['answer_sympy']}."
    latex += f"\nThe answer is \\({row['answer_latex']}\\)."
    return plain, latex


def shown_text(spec: dict) -> str:
    body = "\n".join(text for text, _ in spec["lines"])
    return body + "\n" + spec["final"]


def assert_shown(ident: str, spec: dict) -> None:
    folded = fold(shown_text(spec))
    for step in spec["steps"]:
        for token in step[1:]:
            if must_show(token) and fold(token) not in folded:
                raise AssertionError(f"{ident} prose omits {token}")


def _at(primitive, point):
    if point in (sp.oo, -sp.oo):
        return sp.limit(primitive, symbol(), point)
    return primitive.subs(symbol(), point)


def run_step(ident: str, step: tuple, integrand) -> None:
    kind = step[0]
    if kind == "diff":
        if not diff_ok(parse(step[1]), integrand):
            raise AssertionError(f"{ident} derivative {step[1]}")
        return
    if kind == "diff_of":
        if not diff_ok(parse(step[1]), parse(step[2])):
            raise AssertionError(f"{ident} derivative {step[1]} vs {step[2]}")
        return
    if kind == "eq":
        if not same(parse(step[1]), parse(step[2])):
            raise AssertionError(f"{ident} equality {step[1]} vs {step[2]}")
        return
    if kind == "odd":
        expr = parse(step[1])
        if not pack_gate._zero(expr.subs(symbol(), -symbol()) + expr):
            raise AssertionError(f"{ident} odd part {step[1]}")
        return
    if kind == "ends":
        _, ant, lo, hi, factor, expected = step
        primitive = parse(ant)
        got = parse(factor) * (_at(primitive, parse(hi)) - _at(primitive, parse(lo)))
        if not same(sp.simplify(got), parse(expected)):
            raise AssertionError(f"{ident} endpoints {ant} on [{lo}, {hi}] gave {got}")
        return
    if kind == "sum":
        total = parse(step[-1])
        got = parse(step[1])
        for term in step[2:-1]:
            got += parse(term)
        if not same(got, total):
            raise AssertionError(f"{ident} sum {step[1:-1]}")
        return
    if kind == "abs_on":
        _, inside, form, lo, hi = step
        form_v = parse(form)
        if interval_sign(form_v, parse(lo), parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {form} is not nonnegative on [{lo}, {hi}]")
        if not (same(form_v, parse(inside)) or same(form_v, -parse(inside))):
            raise AssertionError(f"{ident} {form} is not a sign of {inside}")
        return
    if kind == "abs_prod":
        _, left, right, lo, hi = step
        if interval_sign(parse(left), parse(lo), parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {left} leaves [{lo}, {hi}]")
        if interval_sign(parse(right), parse(lo), parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {right} leaves [{lo}, {hi}]")
        return
    if kind == "atan_pos":
        positive = sp.symbols("t", positive=True)
        delta = (parse(step[1]) - parse(step[2])).subs(symbol(), sp.atan(positive))
        if not pack_gate._zero(sp.simplify(delta)):
            raise AssertionError(f"{ident} atan branch {step[1]}")
        return
    if kind == "assume_abs":
        _, lo, hi, form = step
        expr = sp.Abs(symbol() - sp.Abs(symbol() - sp.Abs(symbol())))
        if parse(lo) >= 0:
            sample = sp.symbols("s", nonnegative=True)
        elif parse(hi) <= 0:
            sample = sp.symbols("s", negative=True)
        else:
            raise AssertionError(f"{ident} nested interval")
        got = sp.simplify(expr.subs(symbol(), sample))
        want = sp.simplify(parse(form).subs(symbol(), sample))
        if not pack_gate._zero(got - want):
            raise AssertionError(f"{ident} nested absolute value on [{lo}, {hi}] is {got}")
        return
    if kind == "replace_abs":
        _, integrand_text, inside, deriv, reduced, lo, hi = step
        if not diff_ok(parse(inside), parse(deriv)):
            raise AssertionError(f"{ident} slope of {inside}")
        numerator, denominator = sp.fraction(sp.together(parse(deriv)))
        if interval_sign(numerator, parse(lo), parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} numerator sign")
        if interval_sign(denominator, parse(lo), parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} denominator sign")
        if not _ge0(sp.simplify(parse(inside).subs(symbol(), parse(lo)))):
            raise AssertionError(f"{ident} value at {lo}")
        replaced = parse(integrand_text).subs(sp.Abs(parse(inside)), parse(inside))
        if not same(replaced, parse(reduced)):
            raise AssertionError(f"{ident} cleared absolute value")
        return
    if kind == "exp_parts":
        _exp_parts(ident, step[1], step[2])
        return
    if kind == "shift":
        _shift(ident, step[1])
        return
    if kind == "sine_pull":
        _sine_pull(ident, step[1])
        return
    if kind == "hyperbolic":
        _hyperbolic(ident, step[1])
        return
    raise AssertionError(f"{ident} unknown step {kind}")


def _exp_parts(ident: str, right_text: str, left_text: str) -> None:
    step = sp.Dummy("s", real=True)
    height = sp.symbols("h", nonnegative=True)
    rise = sp.integrate(sp.exp(step), (step, 0, height))
    if not pack_gate._zero(rise - (sp.exp(height) - 1)) or sp.exp(step).is_positive is not True:
        raise AssertionError(f"{ident} exponential rise")
    primitive = sp.exp(symbol()) - symbol()
    if not pack_gate._zero(sp.diff(primitive, symbol()) - (sp.exp(symbol()) - 1)):
        raise AssertionError(f"{ident} right derivative")
    right = sp.simplify(primitive.subs(symbol(), 1) - primitive.subs(symbol(), 0))
    if not same(right, parse(right_text)):
        raise AssertionError(f"{ident} right value {right}")
    decay = sp.integrate(sp.exp(-step), (step, 0, height))
    if not pack_gate._zero(decay - (1 - sp.exp(-height))):
        raise AssertionError(f"{ident} exponential decay")
    line = sp.Dummy("u", real=True)
    if sp.diff(-line, line) != -1:
        raise AssertionError(f"{ident} reflection")
    left_primitive = line + sp.exp(-line)
    if not pack_gate._zero(sp.diff(left_primitive, line) - (1 - sp.exp(-line))):
        raise AssertionError(f"{ident} left derivative")
    left = sp.simplify(left_primitive.subs(line, 1) - left_primitive.subs(line, 0))
    if not same(left, parse(left_text)):
        raise AssertionError(f"{ident} left value {left}")


def _shift(ident: str, index_text: str) -> None:
    index = parse(index_text)
    angle = sp.Dummy("t", real=True)
    sign = sp.Integer(-1) ** index
    if not pack_gate._zero(sp.sin(index * sp.pi + angle) - sign * sp.sin(angle)):
        raise AssertionError(f"{ident} angle addition {index_text}")
    if sp.calculus.util.minimum(sp.sin(angle), angle, sp.Interval(0, sp.pi)) != 0:
        raise AssertionError(f"{ident} sine minimum")
    nonnegative = sp.Dummy("s", nonnegative=True)
    if sp.Abs(sign * nonnegative) != nonnegative:
        raise AssertionError(f"{ident} absolute sign")
    primitive = -sign * sp.cos(symbol())
    integrand = sign * sp.sin(symbol())
    if not pack_gate._zero(sp.diff(primitive, symbol()) - integrand):
        raise AssertionError(f"{ident} signed sine")
    value = sp.simplify(
        primitive.subs(symbol(), (index + 1) * sp.pi) - primitive.subs(symbol(), index * sp.pi)
    )
    if value != 2:
        raise AssertionError(f"{ident} period {index_text} gave {value}")


def _sine_pull(ident: str, target: str) -> None:
    theta = sp.symbols("theta", real=True)
    if sp.calculus.util.minimum(sp.cos(theta), theta, sp.Interval(0, sp.pi / 2)) != 0:
        raise AssertionError(f"{ident} cosine minimum")
    if sp.sin(0) != 0 or sp.sin(sp.pi / 2) != 1:
        raise AssertionError(f"{ident} sine endpoints")
    if not pack_gate._zero(sp.cos(theta) ** 2 - (1 - sp.sin(theta) ** 2)):
        raise AssertionError(f"{ident} pythagoras")
    nonnegative = sp.Dummy("s", nonnegative=True)
    if sp.sqrt(nonnegative ** 2) != nonnegative:
        raise AssertionError(f"{ident} square root of a square")
    pulled = sp.cos(theta) / (sp.sqrt(1 - sp.sin(theta) ** 2) + 1)
    reduced = sp.cos(theta) / (1 + sp.cos(theta))
    replaced = pulled.subs(sp.sqrt(1 - sp.sin(theta) ** 2), sp.cos(theta))
    if not pack_gate._zero(replaced - reduced):
        raise AssertionError(f"{ident} sine pullback")
    if not same(parse(target), parse("cos(x)/(1 + cos(x))")):
        raise AssertionError(f"{ident} sine target")


def _hyperbolic(ident: str, expected: str) -> None:
    parameter = sp.Dummy("u", real=True, nonnegative=True)
    if parameter.is_nonnegative is not True or sp.sinh(parameter).is_nonnegative is not True:
        raise AssertionError(f"{ident} sinh sign")
    if not pack_gate._zero(sp.cosh(parameter) ** 2 - sp.sinh(parameter) ** 2 - 1):
        raise AssertionError(f"{ident} cosh identity")
    if sp.sqrt(sp.sinh(parameter) ** 2) != sp.sinh(parameter):
        raise AssertionError(f"{ident} sqrt sinh")
    if sp.diff(sp.cosh(parameter), parameter) != sp.sinh(parameter):
        raise AssertionError(f"{ident} derivative of cosh")
    reduced = sp.sinh(parameter) / (1 + sp.sinh(parameter))
    half = sp.sqrt(2) / 2
    slope = sp.tanh(parameter / 2)
    primitive = (
        parameter
        - half * sp.log(slope + sp.sqrt(2) - 1)
        + half * sp.log(sp.sqrt(2) + 1 - slope)
    )
    if not pack_gate._zero(sp.diff(primitive, parameter) - reduced):
        raise AssertionError(f"{ident} hyperbolic derivative")
    upper = sp.log(2 + sp.sqrt(3))
    if upper.is_positive is not True:
        raise AssertionError(f"{ident} upper log")
    hyperbolic = (sp.exp(upper) + sp.exp(-upper)) / 2
    if sp.cosh(upper).rewrite(sp.exp) != hyperbolic or not pack_gate._zero(hyperbolic - 2):
        raise AssertionError(f"{ident} cosh of the upper limit")
    if not pack_gate._zero(sp.acosh(sp.cosh(upper)) - upper):
        raise AssertionError(f"{ident} acosh")
    angle = upper / 2
    if angle.is_positive is not True:
        raise AssertionError(f"{ident} half angle")
    if sp.cosh(2 * angle).rewrite(sp.exp) != hyperbolic:
        raise AssertionError(f"{ident} double angle")
    if not pack_gate._zero((2 * sp.cosh(angle) ** 2 - 1).rewrite(sp.exp) - hyperbolic):
        raise AssertionError(f"{ident} cosh double")
    if not pack_gate._zero(sp.cosh(angle).rewrite(sp.exp) ** 2 - (hyperbolic + 1) / 2):
        raise AssertionError(f"{ident} cosh half")
    if not pack_gate._zero((hyperbolic + 1) / 2 - sp.Rational(3, 2)):
        raise AssertionError(f"{ident} three halves")
    if not pack_gate._zero(sp.sinh(angle).rewrite(sp.exp) ** 2 - (sp.cosh(angle).rewrite(sp.exp) ** 2 - 1)):
        raise AssertionError(f"{ident} sinh square")
    if not pack_gate._zero(sp.sinh(angle).rewrite(sp.exp) ** 2 - sp.Rational(1, 2)):
        raise AssertionError(f"{ident} sinh half")
    if sp.sinh(angle).rewrite(sp.exp) != (sp.exp(angle) - sp.exp(-angle)) / 2:
        raise AssertionError(f"{ident} sinh exp")
    if sp.exp(upper) != 2 + sp.sqrt(3) or not (2 + sp.sqrt(3) > 1):
        raise AssertionError(f"{ident} exp upper")
    ratio = sp.sqrt(sp.Rational(1, 2)) / sp.sqrt(sp.Rational(3, 2))
    if not pack_gate._zero(ratio - 1 / sp.sqrt(3)):
        raise AssertionError(f"{ident} tanh ratio")
    if sp.tanh(0) != 0:
        raise AssertionError(f"{ident} tanh zero")
    end = 1 / sp.sqrt(3)
    if (sp.sqrt(2) - 1).is_positive is not True or (sp.sqrt(2) + 1).is_positive is not True:
        raise AssertionError(f"{ident} sqrt two shift")
    if (end + sp.sqrt(2) - 1).is_positive is not True or (sp.sqrt(2) + 1 - end).is_positive is not True:
        raise AssertionError(f"{ident} log arguments")

    def _value(height, tangent):
        return (
            height
            - half * sp.log(tangent + sp.sqrt(2) - 1)
            + half * sp.log(sp.sqrt(2) + 1 - tangent)
        )

    outer = sp.expand_log(_value(upper, end) - _value(0, 0), force=True)
    wanted = upper - sp.log(sp.sqrt(2) + sp.sqrt(3)) / sp.sqrt(2)
    if not pack_gate._zero(sp.expand_log(outer - wanted, force=True)):
        raise AssertionError(f"{ident} outer value")
    if not same(wanted, parse(expected)):
        raise AssertionError(f"{ident} outer expression")


def closes(spec: dict, kind: str) -> bool:
    final = fold(spec["final"])
    if kind == "indefinite":
        return any(step[0] == "diff" and fold(step[1]) == final for step in spec["steps"])
    return any(step[0] in {"ends", "sum", "eq"} and fold(step[-1]) == final for step in spec["steps"])


def check_steps(row: dict, spec: dict) -> None:
    ident = row["id"]
    if fold(spec["final"]) != fold(row["answer_sympy"]):
        raise AssertionError(f"DISAGREE {ident}: stored {row['answer_sympy']} vs final {spec['final']}")
    integrand = parse(row["sympy_expr"])
    if not closes(spec, row["kind"]):
        raise AssertionError(f"{ident} final is not checked against the stored answer")
    for step in spec["steps"]:
        run_step(ident, step, integrand)
    assert_shown(ident, spec)
    if not same(parse(spec["final"]), parse(row["answer_sympy"])):
        raise AssertionError(f"DISAGREE {ident}: simplified final does not match answer_sympy")


def check_prose(row: dict, spec: dict) -> None:
    plain, latex = compose(row, spec)
    if row.get("worked_solution_plain") != plain:
        raise AssertionError(f"{row['id']} plain text drifted")
    if row.get("worked_solution_latex") != latex:
        raise AssertionError(f"{row['id']} latex drifted")
    if row.get("worked_solution_origin") != "missing":
        raise AssertionError(f"{row['id']} origin changed")


def reject_wrong_derivative() -> None:
    integrand = parse("x/(x**4 + 1)")
    if diff_ok(parse("atan(x**2)"), integrand):
        raise AssertionError("wrong antiderivative was accepted")
    if not diff_ok(parse("atan(x**2)/2"), integrand):
        raise AssertionError("stored antiderivative was rejected")


def write_rows(rows: list[dict]) -> None:
    by_id = {row["id"]: row for row in rows}
    for ident, spec in SPECS.items():
        row = by_id[ident]
        plain, latex = compose(row, spec)
        row["worked_solution_plain"] = plain
        row["worked_solution_latex"] = latex
    body = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    RECORDS.write_text(body, encoding="utf-8")


def main(argv: list[str]) -> int:
    reject_wrong_derivative()
    rows = load_rows()
    chosen = section_rows(rows)
    ids = [row["id"] for row in chosen]
    if ids != list(SPECS):
        missing = [ident for ident in ids if ident not in SPECS]
        extra = [ident for ident in SPECS if ident not in ids]
        print(f"FAIL section rows missing={missing} extra={extra}", file=sys.stderr)
        return 1
    try:
        for row in chosen:
            check_steps(row, SPECS[row["id"]])
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    if "--write" in argv:
        write_rows(rows)
        print(f"WROTE {len(chosen)}")
        return 0
    try:
        for row in chosen:
            check_prose(row, SPECS[row["id"]])
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(f"PASS {len(chosen)} yang worked solutions")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
