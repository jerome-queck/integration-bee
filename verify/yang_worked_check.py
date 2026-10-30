#!/usr/bin/env python3
"""Exact step checks for Yang worked solutions.

Sections 1.1, 1.2, 1.3, 2.5, and 2.6. Differentiation uses the same zero test
as verify/pack_gate.py. A wrong antiderivative must fail. Run from the repository root:

    python3 verify/yang_worked_check.py
    python3 verify/yang_worked_check.py --write
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

import pack_gate

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
SECTIONS = frozenset({"1.1", "1.2", "1.3", "2.5", "2.6"})

# final is the stored answer_sympy. lines are (plain, latex) without numbers.
# steps are ("diff", antiderivative), ("diff_of", antiderivative, piece),
# ("dvar", variable, antiderivative, piece), ("eq", left, right),
# ("odd", expression), ("ends", antiderivative, lo, hi, factor, expected),
# ("branch", antiderivative), ("limit", expr, point, dir, expected),
# ("at", expr, point, expected), ("nested", ...), or ("elliptic", ...).
SPECS: dict[str, dict] = {
    "YANG-1.1-P01": {
        "final": "5*x**3/3 - 4*x**2 + 5*x",
        "lines": [
            (
                "Power rule on each term of 5*x**2 - 8*x + 5.",
                r"Power rule on each term of \(5x^{2}-8x+5\).",
            ),
            (
                "The antiderivative is 5*x**3/3 - 4*x**2 + 5*x.",
                r"The antiderivative is \(\frac{5x^{3}}{3}-4x^{2}+5x\).",
            ),
        ],
        "steps": [
            ("diff", "5*x**3/3 - 4*x**2 + 5*x"),
        ],
    },
    "YANG-1.1-P02": {
        "final": "x**2/2 + exp(x) - exp(-x)",
        "lines": [
            (
                "Integrate x, exp(x), and exp(-x) separately.",
                r"Integrate \(x\), \(e^{x}\), and \(e^{-x}\) separately.",
            ),
            (
                "The antiderivative is x**2/2 + exp(x) - exp(-x).",
                r"The antiderivative is \(\frac{x^{2}}{2}+e^{x}-e^{-x}\).",
            ),
        ],
        "steps": [
            ("diff", "x**2/2 + exp(x) - exp(-x)"),
        ],
    },
    "YANG-1.1-P03": {
        "final": "2*sqrt(x) + log(Abs(x))",
        "lines": [
            (
                "Rewrite (sqrt(x) + 1)/x as x**(-1) + x**(-1/2).",
                r"Rewrite \((\sqrt{x}+1)/x\) as \(x^{-1}+x^{-1/2}\).",
            ),
            (
                "Power rule. The antiderivative is 2*sqrt(x) + log(Abs(x)).",
                r"Power rule. The antiderivative is \(2\sqrt{x}+\log|x|\).",
            ),
        ],
        "steps": [
            ("eq", "(sqrt(x) + 1)/x", "x**(-1) + x**(-1/2)"),
            ("diff", "2*sqrt(x) + log(Abs(x))"),
        ],
    },
    "YANG-1.1-P04": {
        "final": "-12*cos(x/3)",
        "lines": [
            (
                "Chain rule with u = x/3. The derivative of x/3 is 1/3, and 4/(1/3) = 12.",
                r"Chain rule with \(u=x/3\). The derivative of \(x/3\) is \(1/3\), and \(4/(1/3)=12\).",
            ),
            (
                "The antiderivative is -12*cos(x/3).",
                r"The antiderivative is \(-12\cos(x/3)\).",
            ),
        ],
        "steps": [
            ("diff_of", "x/3", "1/3"),
            ("eq", "4/(1/3)", "12"),
            ("diff", "-12*cos(x/3)"),
        ],
    },
    "YANG-1.1-P05": {
        "final": "4*atan(x)",
        "lines": [
            (
                "The derivative of atan(x) is 1/(x**2 + 1).",
                r"The derivative of \(\arctan x\) is \(1/(x^{2}+1)\).",
            ),
            (
                "Scale by 4. The antiderivative is 4*atan(x).",
                r"Scale by 4. The antiderivative is \(4\arctan x\).",
            ),
        ],
        "steps": [
            ("diff_of", "atan(x)", "1/(x**2 + 1)"),
            ("diff", "4*atan(x)"),
        ],
    },
    "YANG-1.1-P06": {
        "final": "7*asin(x)",
        "lines": [
            (
                "The derivative of asin(x) is 1/sqrt(1 - x**2).",
                r"The derivative of \(\arcsin x\) is \(1/\sqrt{1-x^{2}}\).",
            ),
            (
                "Scale by 7. The antiderivative is 7*asin(x).",
                r"Scale by 7. The antiderivative is \(7\arcsin x\).",
            ),
        ],
        "steps": [
            ("diff_of", "asin(x)", "1/sqrt(1 - x**2)"),
            ("diff", "7*asin(x)"),
        ],
    },
    "YANG-1.2-P01": {
        "final": "log(x**2 + 1)/2",
        "lines": [
            (
                "Substitution u = x**2 + 1. The derivative of x**2 + 1 is 2*x.",
                r"Substitution \(u=x^{2}+1\). The derivative of \(x^{2}+1\) is \(2x\).",
            ),
            (
                "The integral is log(u)/2. The antiderivative is log(x**2 + 1)/2.",
                r"The integral is \(\log(u)/2\). The antiderivative is \(\log(x^{2}+1)/2\).",
            ),
        ],
        "steps": [
            ("diff_of", "x**2 + 1", "2*x"),
            ("diff", "log(x**2 + 1)/2"),
        ],
    },
    "YANG-1.2-P02": {
        "final": "tan(x)**2/2",
        "lines": [
            (
                "Substitution u = tan(x). The derivative of tan(x) is sec(x)**2.",
                r"Substitution \(u=\tan x\). The derivative of \(\tan x\) is \(\sec^{2}x\).",
            ),
            (
                "The integral is u**2/2. The antiderivative is tan(x)**2/2.",
                r"The integral is \(u^{2}/2\). The antiderivative is \(\tan^{2}(x)/2\).",
            ),
        ],
        "steps": [
            ("diff_of", "tan(x)", "sec(x)**2"),
            ("diff", "tan(x)**2/2"),
        ],
    },
    "YANG-1.2-P03": {
        "final": "x**2/2 + x*exp(x) + exp(2*x)/2",
        "lines": [
            (
                "Substitution u = exp(x) + x. The derivative of exp(x) + x is exp(x) + 1.",
                r"Substitution \(u=e^{x}+x\). The derivative of \(e^{x}+x\) is \(e^{x}+1\).",
            ),
            (
                "The integral is u**2/2, so (exp(x) + x)**2/2.",
                r"The integral is \(u^{2}/2\), so \((e^{x}+x)^{2}/2\).",
            ),
            (
                "Expand. The antiderivative is x**2/2 + x*exp(x) + exp(2*x)/2.",
                r"Expand. The antiderivative is \(\frac{x^{2}}{2}+xe^{x}+\frac{e^{2x}}{2}\).",
            ),
        ],
        "steps": [
            ("diff_of", "exp(x) + x", "exp(x) + 1"),
            ("diff", "(exp(x) + x)**2/2"),
            ("eq", "(exp(x) + x)**2/2", "x**2/2 + x*exp(x) + exp(2*x)/2"),
            ("diff", "x**2/2 + x*exp(x) + exp(2*x)/2"),
        ],
    },
    "YANG-1.2-P04": {
        "final": "-cos(sin(x) + 1)",
        "lines": [
            (
                "Substitution u = sin(x) + 1. The derivative of sin(x) + 1 is cos(x).",
                r"Substitution \(u=\sin x+1\). The derivative of \(\sin x+1\) is \(\cos x\).",
            ),
            (
                "The integral is -cos(u). The antiderivative is -cos(sin(x) + 1).",
                r"The integral is \(-\cos u\). The antiderivative is \(-\cos(\sin x+1)\).",
            ),
        ],
        "steps": [
            ("diff_of", "sin(x) + 1", "cos(x)"),
            ("diff", "-cos(sin(x) + 1)"),
        ],
    },
    "YANG-1.2-P05": {
        "final": "x**2*sqrt(x - 1)*sqrt(x + 1)/3 - sqrt(x - 1)*sqrt(x + 1)/3",
        "lines": [
            (
                "Substitution t = sqrt(x - 1)*sqrt(x + 1). Then (sqrt(x - 1)*sqrt(x + 1))**2 = (x - 1)*(x + 1).",
                r"Substitution \(t=\sqrt{x-1}\sqrt{x+1}\). Then \((\sqrt{x-1}\sqrt{x+1})^{2}=(x-1)(x+1)\).",
            ),
            (
                "The antiderivative in t is t**3/3, so (sqrt(x - 1)*sqrt(x + 1))**3/3.",
                r"The antiderivative in \(t\) is \(t^{3}/3\), so \((\sqrt{x-1}\sqrt{x+1})^{3}/3\).",
            ),
            (
                "That equals x**2*sqrt(x - 1)*sqrt(x + 1)/3 - sqrt(x - 1)*sqrt(x + 1)/3.",
                r"That equals \(\frac{x^{2}\sqrt{x-1}\sqrt{x+1}}{3}-\frac{\sqrt{x-1}\sqrt{x+1}}{3}\).",
            ),
        ],
        "steps": [
            ("eq", "(sqrt(x - 1)*sqrt(x + 1))**2", "(x - 1)*(x + 1)"),
            ("diff", "(sqrt(x - 1)*sqrt(x + 1))**3/3"),
            (
                "eq",
                "(sqrt(x - 1)*sqrt(x + 1))**3/3",
                "x**2*sqrt(x - 1)*sqrt(x + 1)/3 - sqrt(x - 1)*sqrt(x + 1)/3",
            ),
            ("diff", "x**2*sqrt(x - 1)*sqrt(x + 1)/3 - sqrt(x - 1)*sqrt(x + 1)/3"),
        ],
    },
    "YANG-1.2-P06": {
        "final": "exp(exp(x))",
        "lines": [
            (
                "Rewrite exp(x + exp(x)) as exp(x)*exp(exp(x)).",
                r"Rewrite \(e^{x+e^{x}}\) as \(e^{x}e^{e^{x}}\).",
            ),
            (
                "Substitution u = exp(x). The derivative of exp(x) is exp(x).",
                r"Substitution \(u=e^{x}\). The derivative of \(e^{x}\) is \(e^{x}\).",
            ),
            (
                "The integral is exp(u). The antiderivative is exp(exp(x)).",
                r"The integral is \(e^{u}\). The antiderivative is \(e^{e^{x}}\).",
            ),
        ],
        "steps": [
            ("eq", "exp(x + exp(x))", "exp(x)*exp(exp(x))"),
            ("diff_of", "exp(x)", "exp(x)"),
            ("diff", "exp(exp(x))"),
        ],
    },
    "YANG-1.2-P07": {
        "final": "sin(5*x - 4)/(5*cos(5*x - 4))",
        "lines": [
            (
                "Substitution u = 5*x - 4. The derivative of 5*x - 4 is 5.",
                r"Substitution \(u=5x-4\). The derivative of \(5x-4\) is \(5\).",
            ),
            (
                "tan(5*x - 4)/5 equals sin(5*x - 4)/(5*cos(5*x - 4)).",
                r"\(\tan(5x-4)/5\) equals \(\sin(5x-4)/(5\cos(5x-4))\).",
            ),
            (
                "The antiderivative is sin(5*x - 4)/(5*cos(5*x - 4)).",
                r"The antiderivative is \(\sin(5x-4)/(5\cos(5x-4))\).",
            ),
        ],
        "steps": [
            ("diff_of", "5*x - 4", "5"),
            ("eq", "tan(5*x - 4)/5", "sin(5*x - 4)/(5*cos(5*x - 4))"),
            ("diff", "sin(5*x - 4)/(5*cos(5*x - 4))"),
        ],
    },
    "YANG-1.2-P08": {
        "final": "log(x)**2/2 + log(Abs(log(x)))",
        "lines": [
            (
                "Substitution u = log(x). The derivative of log(x) is 1/x.",
                r"Substitution \(u=\log x\). The derivative of \(\log x\) is \(1/x\).",
            ),
            (
                "The derivative of log(x)**2/2 is log(x)/x, and the derivative of log(Abs(log(x))) is 1/(x*log(x)).",
                r"The derivative of \((\log x)^{2}/2\) is \((\log x)/x\), and the derivative of \(\log|\log x|\) is \(1/(x\log x)\).",
            ),
            (
                "log(x)/x + 1/(x*log(x)) equals (log(x) + 1/log(x))/x. The antiderivative is log(x)**2/2 + log(Abs(log(x))).",
                r"\((\log x)/x+1/(x\log x)\) equals \((\log x+1/\log x)/x\). The antiderivative is \((\log x)^{2}/2+\log|\log x|\).",
            ),
        ],
        "steps": [
            ("diff_of", "log(x)", "1/x"),
            ("diff_of", "log(x)**2/2", "log(x)/x"),
            ("diff_of", "log(Abs(log(x)))", "1/(x*log(x))"),
            ("eq", "log(x)/x + 1/(x*log(x))", "(log(x) + 1/log(x))/x"),
            ("diff", "log(x)**2/2 + log(Abs(log(x)))"),
        ],
    },
    "YANG-1.2-P09": {
        "final": "x**4/2 + x**3 + 3*x**2/2 + x + 1/2",
        "lines": [
            (
                "Substitution u = x**2 + x + 1. The derivative of x**2 + x + 1 is 2*x + 1.",
                r"Substitution \(u=x^{2}+x+1\). The derivative of \(x^{2}+x+1\) is \(2x+1\).",
            ),
            (
                "The integral is u**2/2, so (x**2 + x + 1)**2/2.",
                r"The integral is \(u^{2}/2\), so \((x^{2}+x+1)^{2}/2\).",
            ),
            (
                "Expand. The antiderivative is x**4/2 + x**3 + 3*x**2/2 + x + 1/2.",
                r"Expand. The antiderivative is \(\frac{x^{4}}{2}+x^{3}+\frac{3x^{2}}{2}+x+\frac{1}{2}\).",
            ),
        ],
        "steps": [
            ("diff_of", "x**2 + x + 1", "2*x + 1"),
            ("diff", "(x**2 + x + 1)**2/2"),
            ("eq", "(x**2 + x + 1)**2/2", "x**4/2 + x**3 + 3*x**2/2 + x + 1/2"),
            ("diff", "x**4/2 + x**3 + 3*x**2/2 + x + 1/2"),
        ],
    },
    "YANG-1.2-P10": {
        "final": "(x + 1)**2025/2025",
        "lines": [
            (
                "Substitution u = x + 1. The derivative of x + 1 is 1.",
                r"Substitution \(u=x+1\). The derivative of \(x+1\) is \(1\).",
            ),
            (
                "The antiderivative is (x + 1)**2025/2025.",
                r"The antiderivative is \((x+1)^{2025}/2025\).",
            ),
        ],
        "steps": [
            ("diff_of", "x + 1", "1"),
            ("diff", "(x + 1)**2025/2025"),
        ],
    },
    "YANG-1.2-P11": {
        "final": "3*(x - 2024)**(2/3)/2",
        "lines": [
            (
                "Substitution u = x - 2024. The derivative of x - 2024 is 1.",
                r"Substitution \(u=x-2024\). The derivative of \(x-2024\) is \(1\).",
            ),
            (
                "(x - 2024)**(2/3)/(2/3) equals 3*(x - 2024)**(2/3)/2.",
                r"\((x-2024)^{2/3}/(2/3)\) equals \(3(x-2024)^{2/3}/2\).",
            ),
            (
                "The antiderivative is 3*(x - 2024)**(2/3)/2.",
                r"The antiderivative is \(3(x-2024)^{2/3}/2\).",
            ),
        ],
        "steps": [
            ("diff_of", "x - 2024", "1"),
            ("eq", "(x - 2024)**(2/3)/(2/3)", "3*(x - 2024)**(2/3)/2"),
            ("diff", "3*(x - 2024)**(2/3)/2"),
        ],
    },
    "YANG-1.2-P12": {
        "final": "atan(exp(x))",
        "lines": [
            (
                "Substitution u = exp(x). The derivative of exp(x) is exp(x), and exp(2*x) equals exp(x)**2.",
                r"Substitution \(u=e^{x}\). The derivative of \(e^{x}\) is \(e^{x}\), and \(e^{2x}\) equals \((e^{x})^{2}\).",
            ),
            (
                "exp(x)/(exp(2*x) + 1) equals exp(x)/(exp(x)**2 + 1).",
                r"\(e^{x}/(e^{2x}+1)\) equals \(e^{x}/((e^{x})^{2}+1)\).",
            ),
            (
                "The integral is atan(u). The antiderivative is atan(exp(x)).",
                r"The integral is \(\arctan u\). The antiderivative is \(\arctan(e^{x})\).",
            ),
        ],
        "steps": [
            ("diff_of", "exp(x)", "exp(x)"),
            ("eq", "exp(2*x)", "exp(x)**2"),
            ("eq", "exp(x)/(exp(2*x) + 1)", "exp(x)/(exp(x)**2 + 1)"),
            ("diff", "atan(exp(x))"),
        ],
    },
    "YANG-1.2-P13": {
        "final": "log(Abs(x + exp(x) + sin(x)))",
        "lines": [
            (
                "Substitution u = x + exp(x) + sin(x). The derivative of x + exp(x) + sin(x) is exp(x) + cos(x) + 1.",
                r"Substitution \(u=x+e^{x}+\sin x\). The derivative of \(x+e^{x}+\sin x\) is \(e^{x}+\cos x+1\).",
            ),
            (
                "The integral is log(Abs(u)). The antiderivative is log(Abs(x + exp(x) + sin(x))).",
                r"The integral is \(\log|u|\). The antiderivative is \(\log|x+e^{x}+\sin x|\).",
            ),
        ],
        "steps": [
            ("diff_of", "x + exp(x) + sin(x)", "exp(x) + cos(x) + 1"),
            ("diff", "log(Abs(x + exp(x) + sin(x)))"),
        ],
    },
    "YANG-1.2-P14": {
        "final": "log(sin(x)**2 + 1)/2",
        "lines": [
            (
                "Substitution u = sin(x)**2 + 1. The derivative of sin(x)**2 + 1 is 2*sin(x)*cos(x).",
                r"Substitution \(u=\sin^{2}x+1\). The derivative of \(\sin^{2}x+1\) is \(2\sin x\cos x\).",
            ),
            (
                "The integral is log(u)/2. The antiderivative is log(sin(x)**2 + 1)/2.",
                r"The integral is \(\log(u)/2\). The antiderivative is \(\log(\sin^{2}x+1)/2\).",
            ),
        ],
        "steps": [
            ("diff_of", "sin(x)**2 + 1", "2*sin(x)*cos(x)"),
            ("diff", "log(sin(x)**2 + 1)/2"),
        ],
    },
    "YANG-1.2-P15": {
        "final": "exp(2*x)*exp(x**2)/2",
        "lines": [
            (
                "Substitution u = x**2 + 2*x. The derivative of x**2 + 2*x is 2*x + 2, which equals 2*(x + 1).",
                r"Substitution \(u=x^{2}+2x\). The derivative of \(x^{2}+2x\) is \(2x+2\), which equals \(2(x+1)\).",
            ),
            (
                "The integral is exp(u)/2, so exp(x**2 + 2*x)/2.",
                r"The integral is \(e^{u}/2\), so \(e^{x^{2}+2x}/2\).",
            ),
            (
                "That equals exp(2*x)*exp(x**2)/2.",
                r"That equals \(e^{2x}e^{x^{2}}/2\).",
            ),
        ],
        "steps": [
            ("diff_of", "x**2 + 2*x", "2*x + 2"),
            ("eq", "2*x + 2", "2*(x + 1)"),
            ("diff", "exp(x**2 + 2*x)/2"),
            ("eq", "exp(x**2 + 2*x)/2", "exp(2*x)*exp(x**2)/2"),
            ("diff", "exp(2*x)*exp(x**2)/2"),
        ],
    },
    "YANG-1.2-P16": {
        "final": "-cos(log(x))",
        "lines": [
            (
                "Substitution u = log(x). The derivative of log(x) is 1/x.",
                r"Substitution \(u=\log x\). The derivative of \(\log x\) is \(1/x\).",
            ),
            (
                "The integral is -cos(u). The antiderivative is -cos(log(x)).",
                r"The integral is \(-\cos u\). The antiderivative is \(-\cos(\log x)\).",
            ),
        ],
        "steps": [
            ("diff_of", "log(x)", "1/x"),
            ("diff", "-cos(log(x))"),
        ],
    },
    "YANG-1.2-P17": {
        "final": "-log(Abs(cos(x)))",
        "lines": [
            (
                "Write tan(x) as sin(x)/cos(x). Substitution u = cos(x). The derivative of cos(x) is -sin(x).",
                r"Write \(\tan x\) as \(\sin x/\cos x\). Substitution \(u=\cos x\). The derivative of \(\cos x\) is \(-\sin x\).",
            ),
            (
                "The integral is -log(Abs(u)). The antiderivative is -log(Abs(cos(x))).",
                r"The integral is \(-\log|u|\). The antiderivative is \(-\log|\cos x|\).",
            ),
        ],
        "steps": [
            ("eq", "tan(x)", "sin(x)/cos(x)"),
            ("diff_of", "cos(x)", "-sin(x)"),
            ("diff", "-log(Abs(cos(x)))"),
        ],
    },
    "YANG-1.2-P18": {
        "final": "-x + 2*log(exp(x) + 1)",
        "lines": [
            (
                "Multiply numerator and denominator by exp(x/2). (exp(x/2) - exp(-x/2))/(exp(x/2) + exp(-x/2)) equals (exp(x) - 1)/(exp(x) + 1).",
                r"Multiply numerator and denominator by \(e^{x/2}\). \((e^{x/2}-e^{-x/2})/(e^{x/2}+e^{-x/2})\) equals \((e^{x}-1)/(e^{x}+1)\).",
            ),
            (
                "Rewrite (exp(x) - 1)/(exp(x) + 1) as 1 - 2/(exp(x) + 1).",
                r"Rewrite \((e^{x}-1)/(e^{x}+1)\) as \(1-2/(e^{x}+1)\).",
            ),
            (
                "The derivative of x - log(exp(x) + 1) is 1/(exp(x) + 1).",
                r"The derivative of \(x-\log(e^{x}+1)\) is \(1/(e^{x}+1)\).",
            ),
            (
                "x - 2*(x - log(exp(x) + 1)) equals -x + 2*log(exp(x) + 1).",
                r"\(x-2(x-\log(e^{x}+1))\) equals \(-x+2\log(e^{x}+1)\).",
            ),
        ],
        "steps": [
            (
                "eq",
                "(exp(x/2) - exp(-x/2))/(exp(x/2) + exp(-x/2))",
                "(exp(x) - 1)/(exp(x) + 1)",
            ),
            ("eq", "(exp(x) - 1)/(exp(x) + 1)", "1 - 2/(exp(x) + 1)"),
            ("diff_of", "x - log(exp(x) + 1)", "1/(exp(x) + 1)"),
            ("eq", "x - 2*(x - log(exp(x) + 1))", "-x + 2*log(exp(x) + 1)"),
            ("diff", "-x + 2*log(exp(x) + 1)"),
        ],
    },
    "YANG-1.2-P19": {
        "final": "x**2/2 + x*log(x) + log(x)**2/2",
        "lines": [
            (
                "Rewrite log(x*exp(x)) as x + log(x). The derivative of x + log(x) is 1 + 1/x.",
                r"Rewrite \(\log(xe^{x})\) as \(x+\log x\). The derivative of \(x+\log x\) is \(1+1/x\).",
            ),
            (
                "The integral is u**2/2, so (x + log(x))**2/2.",
                r"The integral is \(u^{2}/2\), so \((x+\log x)^{2}/2\).",
            ),
            (
                "Expand. The antiderivative is x**2/2 + x*log(x) + log(x)**2/2.",
                r"Expand. The antiderivative is \(\frac{x^{2}}{2}+x\log x+\frac{(\log x)^{2}}{2}\).",
            ),
        ],
        "steps": [
            ("eq", "log(x*exp(x))", "x + log(x)"),
            ("diff_of", "x + log(x)", "1 + 1/x"),
            ("diff", "(x + log(x))**2/2"),
            ("eq", "(x + log(x))**2/2", "x**2/2 + x*log(x) + log(x)**2/2"),
            ("diff", "x**2/2 + x*log(x) + log(x)**2/2"),
        ],
    },
    "YANG-1.2-P20": {
        "final": "-csc(x - 1)",
        "lines": [
            (
                "csc(1 - x)*cot(1 - x) equals cot(x - 1)*csc(x - 1), since each factor is odd.",
                r"\(\csc(1-x)\cot(1-x)\) equals \(\cot(x-1)\csc(x-1)\), since each factor is odd.",
            ),
            (
                "Substitution u = x - 1. The derivative of x - 1 is 1.",
                r"Substitution \(u=x-1\). The derivative of \(x-1\) is \(1\).",
            ),
            (
                "The integral of csc(u)*cot(u) is -csc(u). The antiderivative is -csc(x - 1).",
                r"The integral of \(\csc u\cot u\) is \(-\csc u\). The antiderivative is \(-\csc(x-1)\).",
            ),
        ],
        "steps": [
            ("eq", "csc(1 - x)*cot(1 - x)", "cot(x - 1)*csc(x - 1)"),
            ("diff_of", "x - 1", "1"),
            ("diff", "-csc(x - 1)"),
        ],
    },
    "YANG-1.3-Ex01": {
        "final": "8/3",
        "lines": [
            (
                "The guide expands (x + 1)*(x**2 + 1) as x**3 + x**2 + x + 1.",
                r"The guide expands \((x+1)(x^{2}+1)\) as \(x^{3}+x^{2}+x+1\).",
            ),
            (
                "The odd part x**3 + x satisfies f(-x) + f(x) = 0, so its integral on [-1, 1] is 0.",
                r"The odd part \(x^{3}+x\) satisfies \(f(-x)+f(x)=0\), so its integral on \([-1,1]\) is \(0\).",
            ),
            (
                "x**3 + x**2 + x + 1 = (x**3 + x) + (x**2 + 1). The even part is x**2 + 1, with antiderivative x**3/3 + x.",
                r"\(x^{3}+x^{2}+x+1=(x^{3}+x)+(x^{2}+1)\). The even part is \(x^{2}+1\), with antiderivative \(x^{3}/3+x\).",
            ),
            (
                "Twice the evaluation from 0 to 1 is 2*((1/3) + 1), which equals 8/3.",
                r"Twice the evaluation from \(0\) to \(1\) is \(2(1/3+1)\), which equals \(8/3\).",
            ),
        ],
        "steps": [
            ("eq", "(x + 1)*(x**2 + 1)", "x**3 + x**2 + x + 1"),
            ("odd", "x**3 + x"),
            ("eq", "x**3 + x**2 + x + 1", "(x**3 + x) + (x**2 + 1)"),
            ("diff_of", "x**3/3 + x", "x**2 + 1"),
            ("eq", "2*((1/3) + 1)", "8/3"),
            ("ends", "x**3/3 + x", "0", "1", "2", "8/3"),
        ],
    },
}



def _add(ident: str, final: str, lines: list, steps: list) -> None:
    SPECS[ident] = {"final": final, "lines": lines, "steps": steps}


_add(
    "YANG-2.5-P01",
    "x**2*log(x + 1)/2 - x**2/4 + x/2 - log(x + 1)/2",
    [
        (
            "Integration by parts with u = log(x + 1). The derivative of log(x + 1) is 1/(x + 1), and the derivative of x**2/2 is x.",
            r"Integration by parts with \(u=\log(x+1)\). The derivative of \(\log(x+1)\) is \(1/(x+1)\), and the derivative of \(x^{2}/2\) is \(x\).",
        ),
        (
            "The quotient x**2/(x + 1) equals x - 1 + 1/(x + 1).",
            r"The quotient \(x^{2}/(x+1)\) equals \(x-1+1/(x+1)\).",
        ),
        (
            "Subtracting that integral gives x**2*log(x + 1)/2 - (x**2/4 - x/2 + log(x + 1)/2).",
            r"Subtracting that integral gives \(\frac{x^{2}\log(x+1)}{2}-\left(\frac{x^{2}}{4}-\frac{x}{2}+\frac{\log(x+1)}{2}\right)\).",
        ),
    ],
    [
        ("diff_of", "log(x + 1)", "1/(x + 1)"),
        ("diff_of", "x**2/2", "x"),
        ("eq", "x**2/(x + 1)", "x - 1 + 1/(x + 1)"),
        (
            "eq",
            "x**2*log(x + 1)/2 - (x**2/4 - x/2 + log(x + 1)/2)",
            "x**2*log(x + 1)/2 - x**2/4 + x/2 - log(x + 1)/2",
        ),
        ("diff", "x**2*log(x + 1)/2 - x**2/4 + x/2 - log(x + 1)/2"),
    ],
)

_add(
    "YANG-2.5-P02",
    "exp(x)*sin(2*x)/10 - exp(x)*cos(2*x)/5",
    [
        (
            "Double angle: sin(x)*cos(x) = sin(2*x)/2, so exp(x)*sin(x)*cos(x) = exp(x)*sin(2*x)/2.",
            r"Double angle: \(\sin x\cos x=\sin(2x)/2\), so \(e^{x}\sin x\cos x=e^{x}\sin(2x)/2\).",
        ),
        (
            "The formula for exp(x)*sin(2*x) gives exp(x)*(sin(2*x) - 2*cos(2*x))/10.",
            r"The formula for \(e^{x}\sin(2x)\) gives \(e^{x}(\sin(2x)-2\cos(2x))/10\).",
        ),
    ],
    [
        ("eq", "sin(x)*cos(x)", "sin(2*x)/2"),
        ("eq", "exp(x)*sin(x)*cos(x)", "exp(x)*sin(2*x)/2"),
        ("diff_of", "exp(x)*(sin(2*x) - 2*cos(2*x))/10", "exp(x)*sin(2*x)/2"),
        (
            "eq",
            "exp(x)*(sin(2*x) - 2*cos(2*x))/10",
            "exp(x)*sin(2*x)/10 - exp(x)*cos(2*x)/5",
        ),
        ("diff", "exp(x)*sin(2*x)/10 - exp(x)*cos(2*x)/5"),
    ],
)

_add(
    "YANG-2.5-P03",
    "-log(x)**2/(2*x**2) - log(x)/(2*x**2) - 1/(4*x**2)",
    [
        (
            "Parts twice, differentiating the logarithm. The remainder log(x)/x**3 has antiderivative -log(x)/(2*x**2) - 1/(4*x**2).",
            r"Parts twice, differentiating the logarithm. The remainder \(\log(x)/x^{3}\) has antiderivative \(-\log(x)/(2x^{2})-1/(4x^{2})\).",
        ),
        (
            "Adding -log(x)**2/(2*x**2) produces -log(x)**2/(2*x**2) + (-log(x)/(2*x**2) - 1/(4*x**2)).",
            r"Adding \(-\log(x)^{2}/(2x^{2})\) produces that sum.",
        ),
    ],
    [
        ("diff_of", "-log(x)/(2*x**2) - 1/(4*x**2)", "log(x)/x**3"),
        (
            "eq",
            "-log(x)**2/(2*x**2) + (-log(x)/(2*x**2) - 1/(4*x**2))",
            "-log(x)**2/(2*x**2) - log(x)/(2*x**2) - 1/(4*x**2)",
        ),
        ("diff", "-log(x)**2/(2*x**2) - log(x)/(2*x**2) - 1/(4*x**2)"),
    ],
)

_add(
    "YANG-2.5-P04",
    "x*tan(x) - x*sec(x) + log(Abs(tan(x) + sec(x))) - log(Abs(sec(x)))",
    [
        (
            "Multiply by 1 - sin(x). Since (sec(x) - tan(x))*(sec(x) + tan(x)) = 1, x/(sin(x) + 1) = x*(sec(x)**2 - sec(x)*tan(x)).",
            r"Multiply by \(1-\sin x\). Since \((\sec x-\tan x)(\sec x+\tan x)=1\), \(x/(\sin x+1)=x(\sec^{2}x-\sec x\tan x)\).",
        ),
        (
            "The derivative of tan(x) - sec(x) is sec(x)**2 - sec(x)*tan(x). The integral of tan(x) - sec(x) is log(Abs(sec(x))) - log(Abs(tan(x) + sec(x))).",
            r"The derivative of \(\tan x-\sec x\) is \(\sec^{2}x-\sec x\tan x\). The integral of \(\tan x-\sec x\) is \(\log|\sec x|-\log|\tan x+\sec x|\).",
        ),
        (
            "Parts gives x*(tan(x) - sec(x)) - (log(Abs(sec(x))) - log(Abs(tan(x) + sec(x)))).",
            r"Parts gives \(x(\tan x-\sec x)-(\log|\sec x|-\log|\tan x+\sec x|)\).",
        ),
    ],
    [
        ("eq", "(sec(x) - tan(x))*(sec(x) + tan(x))", "1"),
        ("eq", "x/(sin(x) + 1)", "x*(sec(x)**2 - sec(x)*tan(x))"),
        ("diff_of", "tan(x) - sec(x)", "sec(x)**2 - sec(x)*tan(x)"),
        (
            "diff_of",
            "log(Abs(sec(x))) - log(Abs(tan(x) + sec(x)))",
            "tan(x) - sec(x)",
        ),
        (
            "eq",
            "x*(tan(x) - sec(x)) - (log(Abs(sec(x))) - log(Abs(tan(x) + sec(x))))",
            "x*tan(x) - x*sec(x) + log(Abs(tan(x) + sec(x))) - log(Abs(sec(x)))",
        ),
        (
            "diff",
            "x*tan(x) - x*sec(x) + log(Abs(tan(x) + sec(x))) - log(Abs(sec(x)))",
        ),
    ],
)

_add(
    "YANG-2.5-P05",
    "log(Abs(tan(x) + sec(x)))/2 + tan(x)*sec(x)/2",
    [
        (
            "Write tan(x)**2 = sec(x)**2 - 1 and integrate sec(x)**3 by parts.",
            r"Write \(\tan^{2}x=\sec^{2}x-1\) and integrate \(\sec^{3}x\) by parts.",
        ),
        (
            "The reduction is (tan(x)*sec(x) + log(Abs(tan(x) + sec(x))))/2.",
            r"The reduction is \((\tan x\sec x+\log|\tan x+\sec x|)/2\).",
        ),
    ],
    [
        ("eq", "tan(x)**2", "sec(x)**2 - 1"),
        (
            "eq",
            "(tan(x)*sec(x) + log(Abs(tan(x) + sec(x))))/2",
            "log(Abs(tan(x) + sec(x)))/2 + tan(x)*sec(x)/2",
        ),
        ("diff", "log(Abs(tan(x) + sec(x)))/2 + tan(x)*sec(x)/2"),
    ],
)

_add(
    "YANG-2.5-P06",
    "4*atan(sqrt(x)) - 2*log(x + 1)/sqrt(x)",
    [
        (
            "Parts with u = log(x + 1). The remainder is 2*x**(-1/2)/(x + 1), which equals 2/(sqrt(x)*(x + 1)).",
            r"Parts with \(u=\log(x+1)\). The remainder is \(2x^{-1/2}/(x+1)\), which equals \(2/(\sqrt{x}(x+1))\).",
        ),
        (
            "The substitution t = sqrt(x) integrates that remainder to 4*atan(sqrt(x)).",
            r"The substitution \(t=\sqrt{x}\) integrates that remainder to \(4\arctan\sqrt{x}\).",
        ),
    ],
    [
        ("eq", "2*x**(-1/2)/(x + 1)", "2/(sqrt(x)*(x + 1))"),
        ("diff_of", "4*atan(sqrt(x))", "2/(sqrt(x)*(x + 1))"),
        ("diff", "4*atan(sqrt(x)) - 2*log(x + 1)/sqrt(x)"),
    ],
)

_add(
    "YANG-2.5-P07",
    "-log(x**2 + 1)/2 + log(Abs(x)) - atan(x)/x",
    [
        (
            "Parts with u = atan(x). Partial fractions give 1/(x*(1 + x**2)) = 1/x - x/(1 + x**2).",
            r"Parts with \(u=\arctan x\). Partial fractions give \(1/(x(1+x^{2}))=1/x-x/(1+x^{2})\).",
        ),
        (
            "That integrates to log(Abs(x)) - log(x**2 + 1)/2.",
            r"That integrates to \(\log|x|-\log(x^{2}+1)/2\).",
        ),
    ],
    [
        ("eq", "1/(x*(1 + x**2))", "1/x - x/(1 + x**2)"),
        ("diff_of", "log(Abs(x)) - log(x**2 + 1)/2", "1/x - x/(1 + x**2)"),
        ("diff", "-log(x**2 + 1)/2 + log(Abs(x)) - atan(x)/x"),
    ],
)

_add(
    "YANG-2.5-P08",
    "-exp(x)*sin(2*x)/5 - exp(x)*cos(2*x)/10 + exp(x)/2",
    [
        (
            "Write sin(x)**2 = (1 - cos(2*x))/2, so exp(x)*sin(x)**2 = exp(x)*(1 - cos(2*x))/2.",
            r"Write \(\sin^{2}x=(1-\cos(2x))/2\), so \(e^{x}\sin^{2}x=e^{x}(1-\cos(2x))/2\).",
        ),
        (
            "The cosine formula gives exp(x)/2 - exp(x)*(cos(2*x) + 2*sin(2*x))/10.",
            r"The cosine formula gives \(e^{x}/2-e^{x}(\cos(2x)+2\sin(2x))/10\).",
        ),
    ],
    [
        ("eq", "sin(x)**2", "(1 - cos(2*x))/2"),
        ("eq", "exp(x)*sin(x)**2", "exp(x)*(1 - cos(2*x))/2"),
        (
            "eq",
            "exp(x)/2 - exp(x)*(cos(2*x) + 2*sin(2*x))/10",
            "-exp(x)*sin(2*x)/5 - exp(x)*cos(2*x)/10 + exp(x)/2",
        ),
        ("diff", "-exp(x)*sin(2*x)/5 - exp(x)*cos(2*x)/10 + exp(x)/2"),
    ],
)

_add(
    "YANG-2.5-P09",
    "x - sqrt(1 - x**2)*asin(x)",
    [
        (
            "Substitution x = sin(u), using cos(asin(x)) = sqrt(1 - x**2). The integral becomes u*sin(u).",
            r"Substitution \(x=\sin u\), using \(\cos(\arcsin x)=\sqrt{1-x^{2}}\). The integral becomes \(u\sin u\).",
        ),
        (
            "Parts gives sin(u) - u*cos(u), which is sin(asin(x)) - asin(x)*sqrt(1 - x**2).",
            r"Parts gives \(\sin u-u\cos u\), which is \(\sin(\arcsin x)-\arcsin(x)\sqrt{1-x^{2}}\).",
        ),
    ],
    [
        ("eq", "cos(asin(x))", "sqrt(1 - x**2)"),
        ("eq", "sin(asin(x)) - asin(x)*sqrt(1 - x**2)", "x - sqrt(1 - x**2)*asin(x)"),
        ("diff", "x - sqrt(1 - x**2)*asin(x)"),
    ],
)

_add(
    "YANG-2.5-P10",
    "2*x*sqrt(exp(x) - 1) - 4*sqrt(exp(x) - 1) + 4*atan(sqrt(exp(x) - 1))",
    [
        (
            "Set t = sqrt(exp(x) - 1). Then (sqrt(exp(x) - 1))**2 + 1 = exp(x), and the integral becomes 2*log(t**2 + 1).",
            r"Set \(t=\sqrt{e^{x}-1}\). Then \((\sqrt{e^{x}-1})^{2}+1=e^{x}\), and the integral becomes \(2\log(t^{2}+1)\).",
        ),
        (
            "The derivative of t*log(t**2 + 1) - 2*t + 2*atan(t) is log(t**2 + 1).",
            r"The derivative of \(t\log(t^{2}+1)-2t+2\arctan t\) is \(\log(t^{2}+1)\).",
        ),
        (
            "Doubling and restoring t gives 2*(sqrt(exp(x) - 1)*x - 2*sqrt(exp(x) - 1) + 2*atan(sqrt(exp(x) - 1))).",
            r"Doubling and restoring \(t\) gives \(2(\sqrt{e^{x}-1}\,x-2\sqrt{e^{x}-1}+2\arctan\sqrt{e^{x}-1})\).",
        ),
    ],
    [
        ("eq", "(sqrt(exp(x) - 1))**2 + 1", "exp(x)"),
        ("dvar", "t", "t*log(t**2 + 1) - 2*t + 2*atan(t)", "log(t**2 + 1)"),
        (
            "eq",
            "2*(sqrt(exp(x) - 1)*x - 2*sqrt(exp(x) - 1) + 2*atan(sqrt(exp(x) - 1)))",
            "2*x*sqrt(exp(x) - 1) - 4*sqrt(exp(x) - 1) + 4*atan(sqrt(exp(x) - 1))",
        ),
        (
            "diff",
            "2*x*sqrt(exp(x) - 1) - 4*sqrt(exp(x) - 1) + 4*atan(sqrt(exp(x) - 1))",
        ),
    ],
)

_add(
    "YANG-2.5-P11",
    "-2*sin(log(x))/(5*x**2) - cos(log(x))/(5*x**2)",
    [
        (
            "Set u = log(x). The integral becomes exp(-2*u)*sin(u), with antiderivative -exp(-2*u)*(2*sin(u) + cos(u))/5.",
            r"Set \(u=\log x\). The integral becomes \(e^{-2u}\sin u\), with antiderivative \(-e^{-2u}(2\sin u+\cos u)/5\).",
        ),
        (
            "Back-substitution gives -exp(-2*log(x))*(2*sin(log(x)) + cos(log(x)))/5.",
            r"Back-substitution gives \(-e^{-2\log x}(2\sin(\log x)+\cos(\log x))/5\).",
        ),
    ],
    [
        ("dvar", "u", "-exp(-2*u)*(2*sin(u) + cos(u))/5", "exp(-2*u)*sin(u)"),
        (
            "eq",
            "-exp(-2*log(x))*(2*sin(log(x)) + cos(log(x)))/5",
            "-2*sin(log(x))/(5*x**2) - cos(log(x))/(5*x**2)",
        ),
        ("diff", "-2*sin(log(x))/(5*x**2) - cos(log(x))/(5*x**2)"),
    ],
)

_add(
    "YANG-2.5-P12",
    "x**3*asec(x)/3 - x*sqrt(x**2 - 1)/6 - log(x + sqrt(x**2 - 1))/6",
    [
        (
            "Parts with u = asec(x). For x > 1 the derivative of asec(x) is 1/(x*sqrt(x**2 - 1)), so the remainder is x**2/(3*sqrt(x**2 - 1)).",
            r"Parts with \(u=\operatorname{arcsec} x\). For \(x>1\) the derivative of \(\operatorname{arcsec} x\) is \(1/(x\sqrt{x^{2}-1})\), so the remainder is \(x^{2}/(3\sqrt{x^{2}-1})\).",
        ),
        (
            "x**3/(3*x*sqrt(x**2 - 1)) equals that remainder. Its antiderivative is x*sqrt(x**2 - 1)/6 + log(x + sqrt(x**2 - 1))/6.",
            r"\(x^{3}/(3x\sqrt{x^{2}-1})\) equals that remainder. Its antiderivative is \(x\sqrt{x^{2}-1}/6+\log(x+\sqrt{x^{2}-1})/6\).",
        ),
    ],
    [
        ("diff_of", "asec(x)", "1/(x*sqrt(x**2 - 1))"),
        ("eq", "x**3/(3*x*sqrt(x**2 - 1))", "x**2/(3*sqrt(x**2 - 1))"),
        (
            "diff_of",
            "x*sqrt(x**2 - 1)/6 + log(x + sqrt(x**2 - 1))/6",
            "x**2/(3*sqrt(x**2 - 1))",
        ),
        (
            "diff",
            "x**3*asec(x)/3 - x*sqrt(x**2 - 1)/6 - log(x + sqrt(x**2 - 1))/6",
        ),
    ],
)

_add(
    "YANG-2.5-P13",
    "log(Abs(tan(x) + sec(x)))",
    [
        (
            "The derivative of log(Abs(tan(x) + sec(x))) is sec(x).",
            r"The derivative of \(\log|\tan x+\sec x|\) is \(\sec x\).",
        ),
    ],
    [
        ("diff_of", "log(Abs(tan(x) + sec(x)))", "sec(x)"),
        ("diff", "log(Abs(tan(x) + sec(x)))"),
    ],
)

_add(
    "YANG-2.5-P14",
    "sqrt(x**2 - 1)*log(x) - sqrt(x**2 - 1) + asec(x)",
    [
        (
            "Parts with u = log(x). The derivative of sqrt(x**2 - 1) is x/sqrt(x**2 - 1).",
            r"Parts with \(u=\log x\). The derivative of \(\sqrt{x^{2}-1}\) is \(x/\sqrt{x^{2}-1}\).",
        ),
        (
            "For x > 1 the remainder sqrt(x**2 - 1)/x has antiderivative sqrt(x**2 - 1) - asec(x).",
            r"For \(x>1\) the remainder \(\sqrt{x^{2}-1}/x\) has antiderivative \(\sqrt{x^{2}-1}-\operatorname{arcsec} x\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x**2 - 1)", "x/sqrt(x**2 - 1)"),
        ("diff_of", "sqrt(x**2 - 1) - asec(x)", "sqrt(x**2 - 1)/x"),
        ("diff", "sqrt(x**2 - 1)*log(x) - sqrt(x**2 - 1) + asec(x)"),
    ],
)

_add(
    "YANG-2.5-P15",
    "-log(sin(x))*cos(x) - log(Abs(cot(x) + csc(x))) + cos(x)",
    [
        (
            "Parts with u = log(sin(x)). Then cos(x)**2/sin(x) = csc(x) - sin(x).",
            r"Parts with \(u=\log(\sin x)\). Then \(\cos^{2}x/\sin x=\csc x-\sin x\).",
        ),
        (
            "The derivative of -log(Abs(cot(x) + csc(x))) is csc(x).",
            r"The derivative of \(-\log|\cot x+\csc x|\) is \(\csc x\).",
        ),
    ],
    [
        ("eq", "cos(x)**2/sin(x)", "csc(x) - sin(x)"),
        ("diff_of", "-log(Abs(cot(x) + csc(x)))", "csc(x)"),
        ("diff", "-log(sin(x))*cos(x) - log(Abs(cot(x) + csc(x))) + cos(x)"),
    ],
)

_add(
    "YANG-2.5-P16",
    "x*exp(x)*sin(x)/2 - x*exp(x)*cos(x)/2 + exp(x)*cos(x)/2",
    [
        (
            "The antiderivative of exp(x)*sin(x) is exp(x)*(sin(x) - cos(x))/2, and the antiderivative of exp(x)*cos(x) is exp(x)*(sin(x) + cos(x))/2.",
            r"The antiderivative of \(e^{x}\sin x\) is \(e^{x}(\sin x-\cos x)/2\), and the antiderivative of \(e^{x}\cos x\) is \(e^{x}(\sin x+\cos x)/2\).",
        ),
        (
            "Parts on x subtracts exp(x)*(sin(x) - cos(x))/4 - exp(x)*(sin(x) + cos(x))/4, which equals -exp(x)*cos(x)/2.",
            r"Parts on \(x\) subtracts \(e^{x}(\sin x-\cos x)/4-e^{x}(\sin x+\cos x)/4\), which equals \(-e^{x}\cos x/2\).",
        ),
        (
            "The sum is x*exp(x)*(sin(x) - cos(x))/2 + exp(x)*cos(x)/2.",
            r"The sum is \(xe^{x}(\sin x-\cos x)/2+e^{x}\cos x/2\).",
        ),
    ],
    [
        ("diff_of", "exp(x)*(sin(x) - cos(x))/2", "exp(x)*sin(x)"),
        ("diff_of", "exp(x)*(sin(x) + cos(x))/2", "exp(x)*cos(x)"),
        (
            "eq",
            "exp(x)*(sin(x) - cos(x))/4 - exp(x)*(sin(x) + cos(x))/4",
            "-exp(x)*cos(x)/2",
        ),
        (
            "eq",
            "x*exp(x)*(sin(x) - cos(x))/2 + exp(x)*cos(x)/2",
            "x*exp(x)*sin(x)/2 - x*exp(x)*cos(x)/2 + exp(x)*cos(x)/2",
        ),
        (
            "diff",
            "x*exp(x)*sin(x)/2 - x*exp(x)*cos(x)/2 + exp(x)*cos(x)/2",
        ),
    ],
)

_add(
    "YANG-2.5-P17",
    "atan(x**2) - log(x**4 + 1)/(2*x**2)",
    [
        (
            "Parts leaves 2*x/(x**4 + 1). The substitution u = x**2 integrates that to atan(x**2).",
            r"Parts leaves \(2x/(x^{4}+1)\). The substitution \(u=x^{2}\) integrates that to \(\arctan(x^{2})\).",
        ),
    ],
    [
        ("diff_of", "atan(x**2)", "2*x/(x**4 + 1)"),
        ("diff", "atan(x**2) - log(x**4 + 1)/(2*x**2)"),
    ],
)

_add(
    "YANG-2.5-P18",
    "-x + log(tan(x))*sin(x)*cos(x)",
    [
        (
            "The derivative of sin(x)*cos(x) is cos(2*x), and the derivative of log(tan(x)) is 1/(sin(x)*cos(x)).",
            r"The derivative of \(\sin x\cos x\) is \(\cos(2x)\), and the derivative of \(\log(\tan x)\) is \(1/(\sin x\cos x)\).",
        ),
        (
            "Parts cancels the logarithm factor and leaves the integral of 1, which is x.",
            r"Parts cancels the logarithm factor and leaves the integral of \(1\), which is \(x\).",
        ),
    ],
    [
        ("diff_of", "sin(x)*cos(x)", "cos(2*x)"),
        ("diff_of", "log(tan(x))", "1/(sin(x)*cos(x))"),
        ("diff", "-x + log(tan(x))*sin(x)*cos(x)"),
    ],
)

_add(
    "YANG-2.6-P01",
    "2*sqrt(2)*sin(x/2)",
    [
        (
            "Half-angle: 1 + cos(x) = 2*cos(x/2)**2, so sqrt(2*cos(x/2)**2) = sqrt(2)*Abs(cos(x/2)).",
            r"Half-angle: \(1+\cos x=2\cos^{2}(x/2)\), so \(\sqrt{2\cos^{2}(x/2)}=\sqrt{2}|\cos(x/2)|\).",
        ),
        (
            "Where cos(x/2) > 0 the integrand is sqrt(2)*cos(x/2), and the derivative of 2*sqrt(2)*sin(x/2) is that factor.",
            r"Where \(\cos(x/2)>0\) the integrand is \(\sqrt{2}\cos(x/2)\), and the derivative of \(2\sqrt{2}\sin(x/2)\) is that factor.",
        ),
        (
            "The squares of the two sides agree, and sqrt(2)*cos(0) = sqrt(1 + cos(0)) = sqrt(2).",
            r"The squares of the two sides agree, and \(\sqrt{2}\cos 0=\sqrt{1+\cos 0}=\sqrt{2}\).",
        ),
    ],
    [
        ("eq", "1 + cos(x)", "2*cos(x/2)**2"),
        ("eq", "sqrt(2*cos(x/2)**2)", "sqrt(2)*Abs(cos(x/2))"),
        ("diff_of", "2*sqrt(2)*sin(x/2)", "sqrt(2)*cos(x/2)"),
        ("eq", "sqrt(2)*cos(0)", "sqrt(2)"),
        ("eq", "sqrt(1 + cos(0))", "sqrt(2)"),
        ("branch", "2*sqrt(2)*sin(x/2)"),
    ],
)

_add(
    "YANG-2.6-P02",
    "tan(x) + sec(x)",
    [
        (
            "(sec(x) - tan(x))*(sec(x) + tan(x)) = 1, so sec(x)/(sec(x) - tan(x)) = sec(x)*(sec(x) + tan(x)).",
            r"\((\sec x-\tan x)(\sec x+\tan x)=1\), so \(\sec x/(\sec x-\tan x)=\sec x(\sec x+\tan x)\).",
        ),
        (
            "That product is sec(x)**2 + sec(x)*tan(x), the derivative of tan(x) + sec(x).",
            r"That product is \(\sec^{2}x+\sec x\tan x\), the derivative of \(\tan x+\sec x\).",
        ),
    ],
    [
        ("eq", "(sec(x) - tan(x))*(sec(x) + tan(x))", "1"),
        ("eq", "sec(x)/(sec(x) - tan(x))", "sec(x)*(sec(x) + tan(x))"),
        ("eq", "sec(x)*(sec(x) + tan(x))", "sec(x)**2 + sec(x)*tan(x)"),
        ("diff_of", "tan(x) + sec(x)", "sec(x)**2 + sec(x)*tan(x)"),
        ("diff", "tan(x) + sec(x)"),
    ],
)

_add(
    "YANG-2.6-P03",
    "tan(x) - cot(x)",
    [
        (
            "1/(sin(x)**2*cos(x)**2) = sec(x)**2 + csc(x)**2.",
            r"\(1/(\sin^{2}x\cos^{2}x)=\sec^{2}x+\csc^{2}x\).",
        ),
        (
            "The derivative of tan(x) - cot(x) is sec(x)**2 + csc(x)**2.",
            r"The derivative of \(\tan x-\cot x\) is \(\sec^{2}x+\csc^{2}x\).",
        ),
    ],
    [
        ("eq", "1/(sin(x)**2*cos(x)**2)", "sec(x)**2 + csc(x)**2"),
        ("diff_of", "tan(x) - cot(x)", "sec(x)**2 + csc(x)**2"),
        ("diff", "tan(x) - cot(x)"),
    ],
)

_add(
    "YANG-2.6-P04",
    "-sin(x)**3/3 + sin(x) + cos(x)**3/3 - cos(x)",
    [
        (
            "Split the cubes: sin(x)**3 + cos(x)**3 = sin(x)*(1 - cos(x)**2) + cos(x)*(1 - sin(x)**2).",
            r"Split the cubes: \(\sin^{3}x+\cos^{3}x=\sin x(1-\cos^{2}x)+\cos x(1-\sin^{2}x)\).",
        ),
        (
            "Integrate termwise. The antiderivative is -sin(x)**3/3 + sin(x) + cos(x)**3/3 - cos(x).",
            r"Integrate termwise. The antiderivative is \(-\sin^{3}x/3+\sin x+\cos^{3}x/3-\cos x\).",
        ),
    ],
    [
        (
            "eq",
            "sin(x)**3 + cos(x)**3",
            "sin(x)*(1 - cos(x)**2) + cos(x)*(1 - sin(x)**2)",
        ),
        ("diff", "-sin(x)**3/3 + sin(x) + cos(x)**3/3 - cos(x)"),
    ],
)

_add(
    "YANG-2.6-P05",
    "-sin(2*x)/4",
    [
        (
            "sin(x - pi/4) = -cos(x + pi/4), so the printed product sin(x + pi/4)*sin(x - pi/4) equals the stored integrand -sin(x + pi/4)*cos(x + pi/4).",
            r"\(\sin(x-\pi/4)=-\cos(x+\pi/4)\), so the printed product \(\sin(x+\pi/4)\sin(x-\pi/4)\) equals the stored integrand \(-\sin(x+\pi/4)\cos(x+\pi/4)\).",
        ),
        (
            "Both equal -cos(2*x)/2, whose antiderivative is -sin(2*x)/4.",
            r"Both equal \(-\cos(2x)/2\), whose antiderivative is \(-\sin(2x)/4\).",
        ),
    ],
    [
        ("eq", "sin(x - pi/4)", "-cos(x + pi/4)"),
        ("eq", "sin(x + pi/4)*sin(x - pi/4)", "-cos(2*x)/2"),
        ("eq", "-sin(x + pi/4)*cos(x + pi/4)", "-cos(2*x)/2"),
        ("diff_of", "-sin(2*x)/4", "-cos(2*x)/2"),
        ("diff", "-sin(2*x)/4"),
    ],
)

_add(
    "YANG-2.6-P06",
    "1/(2*sin(x))",
    [
        (
            "cos(2*x) - 1 = -2*sin(x)**2, so cos(x)/(cos(2*x) - 1) = cos(x)/(-2*sin(x)**2).",
            r"\(\cos(2x)-1=-2\sin^{2}x\), so \(\cos x/(\cos(2x)-1)=\cos x/(-2\sin^{2}x)\).",
        ),
        (
            "The substitution u = sin(x) gives 1/(2*sin(x)).",
            r"The substitution \(u=\sin x\) gives \(1/(2\sin x)\).",
        ),
    ],
    [
        ("eq", "cos(2*x) - 1", "-2*sin(x)**2"),
        ("eq", "cos(x)/(cos(2*x) - 1)", "cos(x)/(-2*sin(x)**2)"),
        ("diff", "1/(2*sin(x))"),
    ],
)

_add(
    "YANG-2.6-P07",
    "sin(x) + cos(x)",
    [
        (
            "cos(2*x) = (cos(x) - sin(x))*(cos(x) + sin(x)), so cos(2*x)/(sin(x) + cos(x)) = cos(x) - sin(x).",
            r"\(\cos(2x)=(\cos x-\sin x)(\cos x+\sin x)\), so \(\cos(2x)/(\sin x+\cos x)=\cos x-\sin x\).",
        ),
        (
            "The derivative of sin(x) + cos(x) is cos(x) - sin(x).",
            r"The derivative of \(\sin x+\cos x\) is \(\cos x-\sin x\).",
        ),
    ],
    [
        ("eq", "cos(2*x)", "(cos(x) - sin(x))*(cos(x) + sin(x))"),
        ("eq", "cos(2*x)/(sin(x) + cos(x))", "cos(x) - sin(x)"),
        ("diff_of", "sin(x) + cos(x)", "cos(x) - sin(x)"),
        ("diff", "sin(x) + cos(x)"),
    ],
)

_add(
    "YANG-2.6-P08",
    "sin(x)*sqrt(cos(2*x))/2 + sqrt(2)*asin(sqrt(2)*sin(x))/4",
    [
        (
            "Set u = sin(x). Then cos(2*x) = 1 - 2*sin(x)**2, and the integral is sqrt(1 - 2*u**2).",
            r"Set \(u=\sin x\). Then \(\cos(2x)=1-2\sin^{2}x\), and the integral is \(\sqrt{1-2u^{2}}\).",
        ),
        (
            "The standard square-root integral has coefficient 1/(2*sqrt(2)), which equals sqrt(2)/4.",
            r"The standard square-root integral has coefficient \(1/(2\sqrt{2})\), which equals \(\sqrt{2}/4\).",
        ),
    ],
    [
        ("eq", "cos(2*x)", "1 - 2*sin(x)**2"),
        ("eq", "1/(2*sqrt(2))", "sqrt(2)/4"),
        ("diff", "sin(x)*sqrt(cos(2*x))/2 + sqrt(2)*asin(sqrt(2)*sin(x))/4"),
    ],
)

_add(
    "YANG-2.6-P09",
    "atan(tan(x)/3)/3",
    [
        (
            "The derivative of atan(tan(x)/3) is 3/(1 + 8*cos(x)**2).",
            r"The derivative of \(\arctan(\tan(x)/3)\) is \(3/(1+8\cos^{2}x)\).",
        ),
        (
            "Dividing by 3 gives (3/(1 + 8*cos(x)**2))/3 = 1/(8*cos(x)**2 + 1).",
            r"Dividing by 3 gives \((3/(1+8\cos^{2}x))/3=1/(8\cos^{2}x+1)\).",
        ),
    ],
    [
        ("diff_of", "atan(tan(x)/3)", "3/(1 + 8*cos(x)**2)"),
        ("eq", "(3/(1 + 8*cos(x)**2))/3", "1/(8*cos(x)**2 + 1)"),
        ("diff", "atan(tan(x)/3)/3"),
    ],
)

_add(
    "YANG-2.6-P10",
    "8*sec(x)**(15/8)/15",
    [
        (
            "The nest sqrt(sqrt(sqrt(sin(x)*tan(x))*tan(x))*tan(x)) and tan(x)**7*sin(x) have the same eighth power.",
            r"The nest \(\sqrt{\sqrt{\sqrt{\sin x\tan x}\,\tan x}\,\tan x}\) and \(\tan^{7}x\sin x\) have the same eighth power.",
        ),
        (
            "For positive factors the nest equals tan(x)**(7/8)*sin(x)**(1/8). With the outer secant square this is sec(x)**2*tan(x)**(7/8)*sin(x)**(1/8).",
            r"For positive factors the nest equals \(\tan^{7/8}x\sin^{1/8}x\). With the outer secant square this is \(\sec^{2}x\tan^{7/8}x\sin^{1/8}x\).",
        ),
        (
            "The derivative of the antiderivative is tan(x)*sec(x)**(15/8). On positive sine and cosine that equals the denested integrand.",
            r"The derivative of the antiderivative is \(\tan x\sec^{15/8}x\). On positive sine and cosine that equals the denested integrand.",
        ),
    ],
    [
        (
            "nested",
            "sqrt(sqrt(sqrt(sin(x)*tan(x))*tan(x))*tan(x))",
            "tan(x)**7*sin(x)",
            "tan(x)**(7/8)*sin(x)**(1/8)",
            "tan(x)*sec(x)**(15/8)",
            "sec(x)**2*tan(x)**(7/8)*sin(x)**(1/8)",
            "8*sec(x)**(15/8)/15",
        ),
    ],
)

_add(
    "YANG-2.6-P11",
    "-log(Abs(cos(2*x)))/2",
    [
        (
            "2*tan(x)/(1 - tan(x)**2) = tan(2*x).",
            r"\(2\tan x/(1-\tan^{2}x)=\tan(2x)\).",
        ),
        (
            "The derivative of -log(Abs(cos(2*x)))/2 is tan(2*x).",
            r"The derivative of \(-\log|\cos(2x)|/2\) is \(\tan(2x)\).",
        ),
    ],
    [
        ("eq", "2*tan(x)/(1 - tan(x)**2)", "tan(2*x)"),
        ("diff_of", "-log(Abs(cos(2*x)))/2", "tan(2*x)"),
        ("diff", "-log(Abs(cos(2*x)))/2"),
    ],
)

_add(
    "YANG-2.6-P12",
    "2**(1/4)*5**(3/4)*elliptic_f(2*atan(sqrt(tan(x/2 + atan(1/3)/2))), 1/2)/5",
    [
        (
            "Phase shift: 3*sin(x) + cos(x) = sqrt(10)*sin(x + atan(1/3)).",
            r"Phase shift: \(3\sin x+\cos x=\sqrt{10}\sin(x+\arctan(1/3))\).",
        ),
        (
            "In s, the derivative of sqrt(2)*elliptic_f(2*atan(s), 1/2) times ((1 + s**4)/2)/(2*s) equals 1/sqrt(2*s**2/(1 + s**4)).",
            r"In \(s\), the derivative of \(\sqrt{2}F(2\arctan s\mid 1/2)\) times \(((1+s^{4})/2)/(2s)\) equals \(1/\sqrt{2s^{2}/(1+s^{4})}\).",
        ),
        (
            "s = sqrt(tan(theta/2)) has that theta derivative, and 2*s**2/(1 + s**4) equals sin(theta).",
            r"\(s=\sqrt{\tan(\theta/2)}\) has that \(\theta\) derivative, and \(2s^{2}/(1+s^{4})\) equals \(\sin\theta\).",
        ),
        (
            "Scale by 10**(-1/4) and set theta = x + atan(1/3). The composed antiderivative is the stored answer.",
            r"Scale by \(10^{-1/4}\) and set \(\theta=x+\arctan(1/3)\). The composed antiderivative is the stored answer.",
        ),
    ],
    [
        (
            "elliptic",
            "sqrt(10)*sin(x + atan(1/3))",
            "3*sin(x) + cos(x)",
            "sqrt(2)*elliptic_f(2*atan(s), 1/2)",
            "((1 + s**4)/2)/(2*s)",
            "2*s**2/(1 + s**4)",
            "sqrt(tan(theta/2))",
            "10**(-1/4)",
            "2**(1/4)*5**(3/4)*elliptic_f(2*atan(sqrt(tan(x/2 + atan(1/3)/2))), 1/2)/5",
        ),
    ],
)

_add(
    "YANG-2.6-P13",
    "x/2 - sin(2*x)/4",
    [
        (
            "tan(x)/(tan(x) + cot(x)) = sin(x)**2, and sin(x)**2 = (1 - cos(2*x))/2.",
            r"\(\tan x/(\tan x+\cot x)=\sin^{2}x\), and \(\sin^{2}x=(1-\cos(2x))/2\).",
        ),
        (
            "The derivative of x/2 - sin(2*x)/4 is (1 - cos(2*x))/2.",
            r"The derivative of \(x/2-\sin(2x)/4\) is \((1-\cos(2x))/2\).",
        ),
    ],
    [
        ("eq", "tan(x)/(tan(x) + cot(x))", "sin(x)**2"),
        ("eq", "sin(x)**2", "(1 - cos(2*x))/2"),
        ("diff_of", "x/2 - sin(2*x)/4", "(1 - cos(2*x))/2"),
        ("diff", "x/2 - sin(2*x)/4"),
    ],
)

_add(
    "YANG-2.6-P14",
    "-sqrt(2) + sqrt(2)*log(2)",
    [
        (
            "2*cos(x)**2 - 1 = 1 - 2*sin(x)**2. Set u = sin(x) and F(u) = u*log(1 - 2*u**2) - 2*u + log((1 + sqrt(2)*u)/(1 - sqrt(2)*u))/sqrt(2).",
            r"\(2\cos^{2}x-1=1-2\sin^{2}x\). Set \(u=\sin x\) and \(F(u)=u\log(1-2u^{2})-2u+\log((1+\sqrt{2}u)/(1-\sqrt{2}u))/\sqrt{2}\).",
        ),
        (
            "In x, F is sin(x)*log(1 - 2*sin(x)**2) - 2*sin(x) + log((1 + sqrt(2)*sin(x))/(1 - sqrt(2)*sin(x)))/sqrt(2). Its derivative is the integrand, and F(0) = 0.",
            r"In \(x\), \(F\) is that composition. Its derivative is the integrand, and \(F(0)=0\).",
        ),
        (
            "The limit of F as x approaches pi/4 from the left is -sqrt(2) + sqrt(2)*log(2).",
            r"The limit of \(F\) as \(x\) approaches \(\pi/4\) from the left is \(-\sqrt{2}+\sqrt{2}\log 2\).",
        ),
    ],
    [
        ("eq", "2*cos(x)**2 - 1", "1 - 2*sin(x)**2"),
        (
            "diff",
            "sin(x)*log(1 - 2*sin(x)**2) - 2*sin(x) + log((1 + sqrt(2)*sin(x))/(1 - sqrt(2)*sin(x)))/sqrt(2)",
        ),
        (
            "at",
            "sin(x)*log(1 - 2*sin(x)**2) - 2*sin(x) + log((1 + sqrt(2)*sin(x))/(1 - sqrt(2)*sin(x)))/sqrt(2)",
            "0",
            "0",
        ),
        (
            "limit",
            "sin(x)*log(1 - 2*sin(x)**2) - 2*sin(x) + log((1 + sqrt(2)*sin(x))/(1 - sqrt(2)*sin(x)))/sqrt(2)",
            "pi/4",
            "-",
            "-sqrt(2) + sqrt(2)*log(2)",
        ),
    ],
)

_add(
    "YANG-2.6-P15",
    "-cos(sin(x)*cos(x))",
    [
        (
            "The derivative of sin(x)*cos(x) is cos(2*x), so the integrand is the chain-rule derivative of -cos(sin(x)*cos(x)).",
            r"The derivative of \(\sin x\cos x\) is \(\cos(2x)\), so the integrand is the chain-rule derivative of \(-\cos(\sin x\cos x)\).",
        ),
    ],
    [
        ("diff_of", "sin(x)*cos(x)", "cos(2*x)"),
        ("diff", "-cos(sin(x)*cos(x))"),
    ],
)

_add(
    "YANG-2.6-P16",
    "log(Abs(tan(x)))",
    [
        (
            "The derivative of log(Abs(tan(x))) is csc(x)*sec(x).",
            r"The derivative of \(\log|\tan x|\) is \(\csc x\sec x\).",
        ),
    ],
    [
        ("diff_of", "log(Abs(tan(x)))", "csc(x)*sec(x)"),
        ("diff", "log(Abs(tan(x)))"),
    ],
)


def parse(text: str, variable: str = "x"):
    return pack_gate._parse(text, variable)


def fold(text: str) -> str:
    return "".join(str(text).split())


def same(left, right) -> bool:
    if pack_gate._zero(left - right):
        return True
    symbol = pack_gate.namespace("x")["x"]
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero((left - right).subs(symbol, positive))


def diff_ok(antiderivative, integrand) -> bool:
    symbol = pack_gate.namespace("x")["x"]
    return diff_expr(antiderivative, integrand, symbol)


def diff_expr(antiderivative, integrand, symbol) -> bool:
    delta = sp.diff(antiderivative, symbol) - integrand
    if pack_gate._zero(delta):
        return True
    dropped = pack_gate._drop_log_abs(antiderivative)
    if dropped != antiderivative and pack_gate._zero(sp.diff(dropped, symbol) - integrand):
        return True
    positive = sp.Symbol(symbol.name, positive=True)
    return pack_gate._zero(delta.subs(symbol, positive))


def branch_ok(antiderivative, integrand) -> bool:
    """Match pack_gate._radical_branch. The sample picks the sign after the squares agree."""
    symbol = pack_gate.namespace("x")["x"]
    slope = sp.diff(antiderivative, symbol)
    if not pack_gate._zero(slope**2 - integrand**2):
        return False
    return pack_gate._zero((slope - integrand).subs(symbol, 0))


def must_show(token: str) -> bool:
    return any(char.isalpha() for char in token) or "**" in token or "/" in token


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


def run_nested(step) -> None:
    nest_s, eighth, power, slope_s, denested, final = step[1:]
    x = pack_gate.namespace("x")["x"]
    nest = parse(nest_s)
    if not same(nest**8, parse(eighth)):
        raise AssertionError("eighth power")
    t, s = sp.symbols("t s", positive=True)
    if nest.subs({sp.tan(x): t, sp.sin(x): s}) != parse(power).subs({sp.tan(x): t, sp.sin(x): s}):
        raise AssertionError("positive denest")
    if not same(parse(denested), parse("sec(x)**2") * parse(power)):
        raise AssertionError("denested product")
    slope = parse(slope_s)
    den = parse(denested)
    sine, cosine = sp.symbols("sine cosine", positive=True)
    replaced_slope = slope.subs({sp.tan(x): sine / cosine, sp.sec(x): 1 / cosine})
    replaced_denested = den.subs({
        sp.tan(x): sine / cosine,
        sp.sec(x): 1 / cosine,
        sp.sin(x): sine,
    })
    if sp.expand_power_exp(replaced_slope) != sp.expand_power_exp(replaced_denested):
        raise AssertionError("sine cosine reduction")
    if not diff_ok(parse(final), slope):
        raise AssertionError("nested derivative")


def run_elliptic(step) -> None:
    phase, linear, prim, jac, sine_s, s_of, scale, final = step[1:]
    if not same(parse(phase), parse(linear)):
        raise AssertionError("phase")
    s = pack_gate.namespace("s")["s"]
    primitive = parse(prim, "s")
    jacobian = parse(jac, "s")
    sine = parse(sine_s, "s")
    if not pack_gate._zero(sp.diff(primitive, s) * jacobian - 1 / sp.sqrt(sine)):
        raise AssertionError("elliptic s derivative")
    theta = pack_gate.namespace("theta")["theta"]
    s_expr = parse(s_of, "theta")
    if not pack_gate._zero(sp.diff(s_expr, theta) - jacobian.subs(s, s_expr)):
        raise AssertionError("ds")
    if not pack_gate._zero(sine.subs(s, s_expr) - sp.sin(theta)):
        raise AssertionError("sine in s")
    scale_e = parse(scale, "x")
    rate = scale_e / sp.sqrt(sp.sin(theta))
    if not pack_gate._zero(rate - 1 / sp.sqrt(sp.sqrt(10) * sp.sin(theta))):
        raise AssertionError("scale")
    x = pack_gate.namespace("x")["x"]
    alpha = sp.atan(sp.Rational(1, 3))
    if not pack_gate._zero(sp.diff(x + alpha, x) - 1):
        raise AssertionError("dtheta")
    composed = primitive.subs(s, sp.sqrt(sp.tan((x + alpha) / 2))) * scale_e
    if not same(composed, parse(final)):
        raise AssertionError("composed antiderivative")
    if not same(1 / sp.sqrt(parse(linear)), 1 / sp.sqrt(parse(phase))):
        raise AssertionError("integrand scale")


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
    if kind == "dvar":
        variable = step[1]
        symbol = pack_gate.namespace(variable)[variable]
        if not diff_expr(parse(step[2], variable), parse(step[3], variable), symbol):
            raise AssertionError(f"{ident} derivative in {variable}")
        return
    if kind == "eq":
        if not same(parse(step[1]), parse(step[2])):
            raise AssertionError(f"{ident} equality {step[1]} vs {step[2]}")
        return
    if kind == "odd":
        symbol = pack_gate.namespace("x")["x"]
        expr = parse(step[1])
        if not pack_gate._zero(expr.subs(symbol, -symbol) + expr):
            raise AssertionError(f"{ident} odd part {step[1]}")
        return
    if kind == "ends":
        _, ant, lo, hi, factor, expected = step
        symbol = pack_gate.namespace("x")["x"]
        primitive = parse(ant)
        got = parse(factor) * (primitive.subs(symbol, parse(hi)) - primitive.subs(symbol, parse(lo)))
        if not same(sp.simplify(got), parse(expected)):
            raise AssertionError(f"{ident} endpoints {ant} on [{lo}, {hi}]")
        return
    if kind == "branch":
        if not branch_ok(parse(step[1]), integrand):
            raise AssertionError(f"{ident} branch {step[1]}")
        return
    if kind == "at":
        symbol = pack_gate.namespace("x")["x"]
        got = parse(step[1]).subs(symbol, parse(step[2]))
        if not same(got, parse(step[3])):
            raise AssertionError(f"{ident} value at {step[2]}")
        return
    if kind == "limit":
        symbol = pack_gate.namespace("x")["x"]
        got = sp.limit(parse(step[1]), symbol, parse(step[2]), dir=step[3])
        if not same(got, parse(step[4])):
            raise AssertionError(f"{ident} limit {step[2]}")
        return
    if kind == "nested":
        try:
            run_nested(step)
        except AssertionError as exc:
            raise AssertionError(f"{ident} {exc}") from exc
        return
    if kind == "elliptic":
        try:
            run_elliptic(step)
        except AssertionError as exc:
            raise AssertionError(f"{ident} {exc}") from exc
        return
    raise AssertionError(f"{ident} unknown step {kind}")


def proves_final(spec: dict) -> bool:
    final = fold(spec["final"])
    for step in spec["steps"]:
        if step[0] in {"diff", "branch"} and fold(step[1]) == final:
            return True
        if step[0] in {"limit", "ends"} and fold(step[-1]) == final:
            return True
        if step[0] in {"nested", "elliptic"} and any(fold(token) == final for token in step[1:]):
            return True
    return False


def check_steps(row: dict, spec: dict) -> None:
    ident = row["id"]
    if fold(spec["final"]) != fold(row["answer_sympy"]):
        raise AssertionError(
            f"DISAGREE {ident}: stored {row['answer_sympy']} vs final {spec['final']}"
        )
    integrand = parse(row["sympy_expr"])
    if row["kind"] == "indefinite":
        if not proves_final(spec):
            raise AssertionError(f"{ident} final is not a differentiated antiderivative")
    elif row["kind"] == "definite":
        if not proves_final(spec):
            raise AssertionError(f"{ident} final is not an endpoint value")
    else:
        raise AssertionError(f"{ident} kind {row['kind']}")
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
    early = parse("5*x**2 - 8*x + 5")
    if diff_ok(parse("5*x**3/3 - 4*x**2"), early):
        raise AssertionError("wrong antiderivative was accepted")
    if not diff_ok(parse("5*x**3/3 - 4*x**2 + 5*x"), early):
        raise AssertionError("stored antiderivative was rejected")
    integrand = parse("x*log(x + 1)")
    if diff_ok(parse("x**2*log(x + 1)/2"), integrand):
        raise AssertionError("wrong antiderivative was accepted")
    good = "x**2*log(x + 1)/2 - x**2/4 + x/2 - log(x + 1)/2"
    if not diff_ok(parse(good), integrand):
        raise AssertionError("stored antiderivative was rejected")
    radical = parse("sqrt(cos(x) + 1)")
    if branch_ok(parse("-2*sqrt(2)*sin(x/2)"), radical):
        raise AssertionError("wrong sign was accepted")
    if not branch_ok(parse("2*sqrt(2)*sin(x/2)"), radical):
        raise AssertionError("half-angle antiderivative was rejected")


def write_rows(rows: list[dict]) -> None:
    by_id = {row["id"]: row for row in rows}
    for ident, spec in SPECS.items():
        row = by_id[ident]
        plain, latex = compose(row, spec)
        row["worked_solution_plain"] = plain
        row["worked_solution_latex"] = latex
    body = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
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
