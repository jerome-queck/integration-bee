#!/usr/bin/env python3
"""Exact step checks for Yang worked solutions.

Sections 1.1 through 1.5, 1.8, 1.9, 1.11, 1.12, 2.3, 2.4, 2.5, and 2.6. Differentiation uses the same zero test
as verify/pack_gate.py. An improper endpoint is a limit. A wrong antiderivative must fail. Run from the repository root:

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
SECTIONS = frozenset({"1.1", "1.2", "1.3", "1.4", "1.5", "1.8", "1.9", "2.3", "2.4", "2.5", "2.6"})

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
    "YANG-1.4-P01": {
        "final": "log(exp(x) + 2024)",
        "lines": [
            (
                "Substitution. The derivative of exp(x) + 2024 is exp(x).",
                r"Substitution. The derivative of \(e^{x}+2024\) is \(e^{x}\).",
            ),
            (
                "The integrand exp(x)/(exp(x) + 2024) becomes 1/u.",
                r"The integrand becomes \(1/u\).",
            ),
        ],
        "steps": [
            ("diff_of", "exp(x) + 2024", "exp(x)"),
            ("diff", "log(exp(x) + 2024)"),
        ],
    },
    "YANG-1.4-P02": {
        "final": "-1/(exp(x) + 1)",
        "lines": [
            (
                "Substitution u = exp(x) + 1. Then exp(x)/(exp(x) + 1)**2 is u**(-2).",
                r"Substitution \(u=e^{x}+1\). The integrand is \(u^{-2}\).",
            ),
        ],
        "steps": [
            ("diff", "-1/(exp(x) + 1)"),
        ],
    },
    "YANG-1.4-P03": {
        "final": "1/(-log(2) + log(5)) + 1/(-log(3) + log(5))",
        "lines": [
            (
                "Split the quotient. (2**x + 3**x)/5**x = (2/5)**x + (3/5)**x.",
                r"Split the quotient into \((2/5)^{x}+(3/5)^{x}\).",
            ),
            (
                "Write the powers as exponentials. (2/5)**x = exp(x*log(2/5)) and (3/5)**x = exp(x*log(3/5)).",
                r"Write \((2/5)^{x}=\exp(x\log(2/5))\) and \((3/5)^{x}=\exp(x\log(3/5))\).",
            ),
            (
                "The antiderivative of exp(x*log(2/5)) is exp(x*log(2/5))/log(2/5). The antiderivative of exp(x*log(3/5)) is exp(x*log(3/5))/log(3/5).",
                r"Each exponential ray has antiderivative \(e^{cx}/c\).",
            ),
            (
                "Evaluate exp(x*log(2/5))/log(2/5) + exp(x*log(3/5))/log(3/5) from 0 to oo.",
                r"Evaluate the sum of those antiderivatives from \(0\) to \(\infty\).",
            ),
        ],
        "steps": [
            ("eq", "(2**x + 3**x)/5**x", "(2/5)**x + (3/5)**x"),
            ("eq", "(2/5)**x", "exp(x*log(2/5))"),
            ("eq", "(3/5)**x", "exp(x*log(3/5))"),
            ("diff_of", "exp(x*log(2/5))/log(2/5)", "exp(x*log(2/5))"),
            ("diff_of", "exp(x*log(3/5))/log(3/5)", "exp(x*log(3/5))"),
            (
                "ends",
                "exp(x*log(2/5))/log(2/5) + exp(x*log(3/5))/log(3/5)",
                "0",
                "oo",
                "1",
                "1/(-log(2) + log(5)) + 1/(-log(3) + log(5))",
            ),
        ],
    },
    "YANG-1.4-P04": {
        "final": "x - log(exp(x) + 1)",
        "lines": [
            (
                "Split the fraction. 1/(exp(x) + 1) = 1 - exp(x)/(exp(x) + 1).",
                r"Split \(1/(e^{x}+1)=1-e^{x}/(e^{x}+1)\).",
            ),
            (
                "The second term has antiderivative log(exp(x) + 1), so the signed term is -log(exp(x) + 1) and its integrand is -exp(x)/(exp(x) + 1).",
                r"The second term is a logarithm.",
            ),
        ],
        "steps": [
            ("eq", "1/(exp(x) + 1)", "1 - exp(x)/(exp(x) + 1)"),
            ("diff_of", "-log(exp(x) + 1)", "-exp(x)/(exp(x) + 1)"),
            ("diff", "x - log(exp(x) + 1)"),
        ],
    },
    "YANG-1.4-P05": {
        "final": "log(x + exp(x) + 1)",
        "lines": [
            (
                "The numerator of (exp(x) + 1)/(x + exp(x) + 1) is the derivative of the denominator.",
                r"The numerator is the derivative of the denominator.",
            ),
            (
                "The derivative of x + exp(x) + 1 is exp(x) + 1.",
                r"The derivative of \(x+e^{x}+1\) is \(e^{x}+1\).",
            ),
        ],
        "steps": [
            ("diff_of", "x + exp(x) + 1", "exp(x) + 1"),
            ("diff", "log(x + exp(x) + 1)"),
        ],
    },
    "YANG-1.4-P06": {
        "final": "6*x + exp(4*x)/4 + 2*exp(2*x) - 2*exp(-2*x) - exp(-4*x)/4",
        "lines": [
            (
                "Expand the power. (exp(x) + exp(-x))**4 = exp(4*x) + 4*exp(2*x) + 6 + 4*exp(-2*x) + exp(-4*x).",
                r"Expand \((e^{x}+e^{-x})^{4}\).",
            ),
        ],
        "steps": [
            (
                "eq",
                "(exp(x) + exp(-x))**4",
                "exp(4*x) + 4*exp(2*x) + 6 + 4*exp(-2*x) + exp(-4*x)",
            ),
            ("diff", "6*x + exp(4*x)/4 + 2*exp(2*x) - 2*exp(-2*x) - exp(-4*x)/4"),
        ],
    },
    "YANG-1.4-P07": {
        "final": "2**x*E*exp(x)/(2*log(2) + 2)",
        "lines": [
            (
                "Combine the bases. 2**(x - 1)*exp(x + 1) = (E/2)*exp(x*(1 + log(2))).",
                r"Combine the bases into one exponential.",
            ),
            (
                "Divide by the exponent constant. (E/2)*exp(x*(1 + log(2)))/(1 + log(2)) is that antiderivative.",
                r"Divide by the constant in the exponent.",
            ),
        ],
        "steps": [
            ("eq", "2**(x - 1)*exp(x + 1)", "(E/2)*exp(x*(1 + log(2)))"),
            ("diff_of", "(E/2)*exp(x*(1 + log(2)))/(1 + log(2))", "(E/2)*exp(x*(1 + log(2)))"),
            ("eq", "(E/2)*exp(x*(1 + log(2)))/(1 + log(2))", "2**x*E*exp(x)/(2*log(2) + 2)"),
            ("diff", "2**x*E*exp(x)/(2*log(2) + 2)"),
        ],
    },
    "YANG-1.4-P08": {
        "final": "-cos(exp(x))",
        "lines": [
            (
                "Substitution u = exp(x). Then exp(x)*sin(exp(x)) becomes sin(u).",
                r"Substitution \(u=e^{x}\). The integrand becomes \(\sin u\).",
            ),
        ],
        "steps": [
            ("diff", "-cos(exp(x))"),
        ],
    },
    "YANG-1.4-P09": {
        "final": "exp(2*x)/2",
        "lines": [
            (
                "Cancel the common factor. (exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x)) = exp(2*x).",
                r"Cancel \(e^{3x}+1\). The quotient is \(e^{2x}\).",
            ),
        ],
        "steps": [
            ("eq", "(exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x))", "exp(2*x)"),
            ("diff_of", "exp(2*x)/2", "exp(2*x)"),
            ("diff", "exp(2*x)/2"),
        ],
    },
    "YANG-1.4-P10": {
        "final": "asin(exp(x))",
        "lines": [
            (
                "Substitution u = exp(x). Then exp(x)/sqrt(1 - exp(2*x)) becomes 1/sqrt(1 - u**2).",
                r"Substitution \(u=e^{x}\). The integrand becomes \(1/\sqrt{1-u^{2}}\).",
            ),
        ],
        "steps": [
            ("diff", "asin(exp(x))"),
        ],
    },
    "YANG-1.4-P11": {
        "final": "log(exp(2*x) + 1)/2 + atan(exp(x))",
        "lines": [
            (
                "Split the integrand. (exp(2*x) + exp(x))/(exp(2*x) + 1) = exp(2*x)/(exp(2*x) + 1) + exp(x)/(exp(2*x) + 1).",
                r"Split the integrand into two terms.",
            ),
            (
                "The first antiderivative is log(exp(2*x) + 1)/2. Substitution u = exp(x) gives atan(exp(x)).",
                r"The first term is a logarithm and the second is an arctangent.",
            ),
        ],
        "steps": [
            (
                "eq",
                "(exp(2*x) + exp(x))/(exp(2*x) + 1)",
                "exp(2*x)/(exp(2*x) + 1) + exp(x)/(exp(2*x) + 1)",
            ),
            ("diff_of", "log(exp(2*x) + 1)/2", "exp(2*x)/(exp(2*x) + 1)"),
            ("diff_of", "atan(exp(x))", "exp(x)/(exp(2*x) + 1)"),
            ("diff", "log(exp(2*x) + 1)/2 + atan(exp(x))"),
        ],
    },
    "YANG-1.4-P12": {
        "final": "2*x + exp(x) - exp(-x)",
        "lines": [
            (
                "Expand the product. (1 + exp(-x))*(exp(x) + 1) = exp(x) + 2 + exp(-x).",
                r"Expand \((1+e^{-x})(e^{x}+1)\).",
            ),
        ],
        "steps": [
            ("eq", "(1 + exp(-x))*(exp(x) + 1)", "exp(x) + 2 + exp(-x)"),
            ("diff_of", "2*x + exp(x) - exp(-x)", "exp(x) + 2 + exp(-x)"),
            ("diff", "2*x + exp(x) - exp(-x)"),
        ],
    },
    "YANG-1.4-P13": {
        "final": "atan(exp(x))",
        "lines": [
            (
                "Clear the negative power. 1/(exp(x) + exp(-x)) = exp(x)/(exp(2*x) + 1).",
                r"Multiply numerator and denominator by \(e^{x}\).",
            ),
        ],
        "steps": [
            ("eq", "1/(exp(x) + exp(-x))", "exp(x)/(exp(2*x) + 1)"),
            ("diff_of", "atan(exp(x))", "exp(x)/(exp(2*x) + 1)"),
            ("diff", "atan(exp(x))"),
        ],
    },
    "YANG-1.4-P14": {
        "final": "log(log(exp(x) - 1))",
        "lines": [
            (
                "Substitution u = log(exp(x) - 1). The integrand exp(x)/((exp(x) - 1)*log(exp(x) - 1)) becomes 1/u.",
                r"Substitution \(u=\log(e^{x}-1)\).",
            ),
        ],
        "steps": [
            ("diff", "log(log(exp(x) - 1))"),
        ],
    },
    "YANG-1.4-P15": {
        "final": "tan(exp(2*x))/2",
        "lines": [
            (
                "Substitution u = exp(2*x). Then exp(2*x)/cos(exp(2*x))**2 becomes sec(u)**2 / 2.",
                r"Substitution \(u=e^{2x}\). The integrand becomes \(\sec^{2}(u)/2\).",
            ),
        ],
        "steps": [
            ("diff", "tan(exp(2*x))/2"),
        ],
    },
    "YANG-1.4-P16": {
        "final": "exp(x)*exp(exp(x))",
        "lines": [
            (
                "The integrand (exp(2*x) + exp(x))*exp(exp(x)) is the derivative of exp(x)*exp(exp(x)).",
                r"The integrand is the derivative of \(e^{x}e^{e^{x}}\).",
            ),
        ],
        "steps": [
            ("diff", "exp(x)*exp(exp(x))"),
        ],
    },
    "YANG-1.4-P17": {
        "final": "4*exp(3*x/4)/3",
        "lines": [
            (
                "The printed root simplifies. sqrt(exp(x)*sqrt(exp(x))) = exp(3*x/4).",
                r"The printed root is \(e^{3x/4}\).",
            ),
        ],
        "steps": [
            ("eq", "sqrt(exp(x)*sqrt(exp(x)))", "exp(3*x/4)"),
            ("diff_of", "4*exp(3*x/4)/3", "exp(3*x/4)"),
            ("diff", "4*exp(3*x/4)/3"),
        ],
    },
    "YANG-1.4-P18": {
        "final": "5/3",
        "lines": [
            (
                "Substitution t = exp(-x). The derivative of exp(-x) is -exp(-x), and the limit at oo is 0.",
                r"Substitution \(t=e^{-x}\). Then \(dt=-e^{-x}\,dx\).",
            ),
            (
                "The integrand matches that differential. (sqrt(1 - exp(-x)) + 1)*exp(-x) = -(1 + sqrt(1 - exp(-x)))*(-exp(-x)).",
                r"The integrand becomes \(-(1+\sqrt{1-t})\,dt\).",
            ),
            (
                "An antiderivative is -exp(-x) + (2/3)*(1 - exp(-x))**(3/2). Evaluate it from 0 to oo.",
                r"Evaluate \(-e^{-x}+(2/3)(1-e^{-x})^{3/2}\) from \(0\) to \(\infty\).",
            ),
        ],
        "steps": [
            ("diff_of", "exp(-x)", "-exp(-x)"),
            (
                "eq",
                "(sqrt(1 - exp(-x)) + 1)*exp(-x)",
                "-(1 + sqrt(1 - exp(-x)))*(-exp(-x))",
            ),
            (
                "diff_of",
                "-exp(-x) + (2/3)*(1 - exp(-x))**(3/2)",
                "(sqrt(1 - exp(-x)) + 1)*exp(-x)",
            ),
            (
                "ends",
                "-exp(-x) + (2/3)*(1 - exp(-x))**(3/2)",
                "0",
                "oo",
                "1",
                "5/3",
            ),
        ],
    },
    "YANG-1.5-P01": {
        "final": "x - log(cos(x))",
        "lines": [
            (
                "Split the quotient. (sin(x) + cos(x))/cos(x) = tan(x) + 1.",
                r"Split the quotient into \(\tan x+1\).",
            ),
        ],
        "steps": [
            ("eq", "(sin(x) + cos(x))/cos(x)", "tan(x) + 1"),
            ("diff_of", "x - log(cos(x))", "tan(x) + 1"),
            ("diff", "x - log(cos(x))"),
        ],
    },
    "YANG-1.5-P02": {
        "final": "sin(x)**3/3",
        "lines": [
            (
                "Substitution u = sin(x). Then sin(x)**2*cos(x) becomes u**2.",
                r"Substitution \(u=\sin x\).",
            ),
        ],
        "steps": [
            ("diff", "sin(x)**3/3"),
        ],
    },
    "YANG-1.5-P03": {
        "final": "-sin(x)**5/5 + sin(x)**3/3",
        "lines": [
            (
                "Save one cosine. sin(x)**2*cos(x)**3 = sin(x)**2*(1 - sin(x)**2)*cos(x).",
                r"Write \(\cos^{2}x=1-\sin^{2}x\) and keep one factor of \(\cos x\).",
            ),
        ],
        "steps": [
            ("eq", "sin(x)**2*cos(x)**3", "sin(x)**2*(1 - sin(x)**2)*cos(x)"),
            ("diff_of", "-sin(x)**5/5 + sin(x)**3/3", "sin(x)**2*(1 - sin(x)**2)*cos(x)"),
            ("diff", "-sin(x)**5/5 + sin(x)**3/3"),
        ],
    },
    "YANG-1.5-P04": {
        "final": "tan(x)**3/3",
        "lines": [
            (
                "Substitution u = tan(x). Then tan(x)**2*sec(x)**2 becomes u**2.",
                r"Substitution \(u=\tan x\).",
            ),
        ],
        "steps": [
            ("diff", "tan(x)**3/3"),
        ],
    },
    "YANG-1.5-P05": {
        "final": "sec(x)**3/3",
        "lines": [
            (
                "Substitution u = sec(x). Then tan(x)*sec(x)**3 becomes u**2.",
                r"Substitution \(u=\sec x\).",
            ),
        ],
        "steps": [
            ("diff", "sec(x)**3/3"),
        ],
    },
    "YANG-1.5-P06": {
        "final": "-x + tan(x)",
        "lines": [
            (
                "Pythagorean rewrite. tan(x)**2 = sec(x)**2 - 1.",
                r"Write \(\tan^{2}x=\sec^{2}x-1\).",
            ),
        ],
        "steps": [
            ("eq", "tan(x)**2", "sec(x)**2 - 1"),
            ("diff_of", "-x + tan(x)", "sec(x)**2 - 1"),
            ("diff", "-x + tan(x)"),
        ],
    },
    "YANG-1.5-P07": {
        "final": "atan(sin(x))",
        "lines": [
            (
                "Substitution u = sin(x). Then cos(x)/(sin(x)**2 + 1) becomes 1/(u**2 + 1).",
                r"Substitution \(u=\sin x\).",
            ),
        ],
        "steps": [
            ("diff", "atan(sin(x))"),
        ],
    },
    "YANG-1.5-P08": {
        "final": "-log(csc(x) + 1)",
        "lines": [
            (
                "Substitution u = csc(x). Then cot(x)*csc(x)/(csc(x) + 1) leads to -1/(u + 1).",
                r"Substitution \(u=\csc x\).",
            ),
        ],
        "steps": [
            ("diff", "-log(csc(x) + 1)"),
        ],
    },
    "YANG-1.5-P09": {
        "final": "-log(sin(x) + cos(x))",
        "lines": [
            (
                "The numerator of (sin(x) - cos(x))/(sin(x) + cos(x)) is the negative derivative of the denominator.",
                r"The numerator is the negative derivative of \(\sin x+\cos x\).",
            ),
        ],
        "steps": [
            ("diff", "-log(sin(x) + cos(x))"),
        ],
    },
    "YANG-1.5-P10": {
        "final": "cos(x)**3/3 - cos(x)",
        "lines": [
            (
                "Save one sine. sin(x)**3 = sin(x)*(1 - cos(x)**2).",
                r"Write \(\sin^{2}x=1-\cos^{2}x\) and keep one factor of \(\sin x\).",
            ),
        ],
        "steps": [
            ("eq", "sin(x)**3", "sin(x)*(1 - cos(x)**2)"),
            ("diff_of", "cos(x)**3/3 - cos(x)", "sin(x)*(1 - cos(x)**2)"),
            ("diff", "cos(x)**3/3 - cos(x)"),
        ],
    },
    "YANG-1.5-P11": {
        "final": "tan(x) - cot(x)",
        "lines": [
            (
                "Simplify the quotient. (tan(x) + cot(x))/(sin(x)*cos(x)) = sec(x)**2 + csc(x)**2.",
                r"The quotient equals \(\sec^{2}x+\csc^{2}x\).",
            ),
        ],
        "steps": [
            ("eq", "(tan(x) + cot(x))/(sin(x)*cos(x))", "sec(x)**2 + csc(x)**2"),
            ("diff_of", "tan(x) - cot(x)", "sec(x)**2 + csc(x)**2"),
            ("diff", "tan(x) - cot(x)"),
        ],
    },
    "YANG-1.5-P12": {
        "final": "x - cos(2*x)/2",
        "lines": [
            (
                "Double angle. (sin(x) + cos(x))**2 = 1 + sin(2*x).",
                r"Expand and use \(\sin(2x)=2\sin x\cos x\).",
            ),
        ],
        "steps": [
            ("eq", "(sin(x) + cos(x))**2", "1 + sin(2*x)"),
            ("diff_of", "x - cos(2*x)/2", "1 + sin(2*x)"),
            ("diff", "x - cos(2*x)/2"),
        ],
    },
    "YANG-1.5-P13": {
        "final": "-x + 2*tan(x) + 2*sec(x)",
        "lines": [
            (
                "Expand and replace tan(x)**2. (tan(x) + sec(x))**2 = 2*sec(x)**2 + 2*sec(x)*tan(x) - 1.",
                r"Expand and replace \(\tan^{2}x\) by \(\sec^{2}x-1\).",
            ),
        ],
        "steps": [
            ("eq", "(tan(x) + sec(x))**2", "2*sec(x)**2 + 2*sec(x)*tan(x) - 1"),
            ("diff_of", "-x + 2*tan(x) + 2*sec(x)", "2*sec(x)**2 + 2*sec(x)*tan(x) - 1"),
            ("diff", "-x + 2*tan(x) + 2*sec(x)"),
        ],
    },
    "YANG-1.5-P14": {
        "final": "x + sin(x)**2/2 + sin(x) - cos(x)",
        "lines": [
            (
                "Expand the product. (sin(x) + 1)*(cos(x) + 1) = sin(x)*cos(x) + sin(x) + cos(x) + 1.",
                r"Expand the product.",
            ),
        ],
        "steps": [
            ("eq", "(sin(x) + 1)*(cos(x) + 1)", "sin(x)*cos(x) + sin(x) + cos(x) + 1"),
            ("diff_of", "x + sin(x)**2/2 + sin(x) - cos(x)", "sin(x)*cos(x) + sin(x) + cos(x) + 1"),
            ("diff", "x + sin(x)**2/2 + sin(x) - cos(x)"),
        ],
    },
    "YANG-1.5-P15": {
        "final": "tan(tan(x))",
        "lines": [
            (
                "Substitution u = tan(x). Then sec(x)**2*sec(tan(x))**2 becomes sec(u)**2.",
                r"Substitution \(u=\tan x\).",
            ),
        ],
        "steps": [
            ("diff", "tan(tan(x))"),
        ],
    },
    "YANG-1.5-P16": {
        "final": "log(sin(x) + 1)",
        "lines": [
            (
                "Rationalize by the conjugate. 1/(tan(x) + sec(x)) = sec(x) - tan(x).",
                r"Multiply by \(\sec x-\tan x\). The denominator becomes 1.",
            ),
        ],
        "steps": [
            ("eq", "1/(tan(x) + sec(x))", "sec(x) - tan(x)"),
            ("diff_of", "log(sin(x) + 1)", "sec(x) - tan(x)"),
            ("diff", "log(sin(x) + 1)"),
        ],
    },
    "YANG-1.5-P17": {
        "final": "sin(x) - cos(x)",
        "lines": [
            (
                "Cancel the secant. (tan(x) + 1)/sec(x) = sin(x) + cos(x).",
                r"Multiply through by \(\cos x\).",
            ),
        ],
        "steps": [
            ("eq", "(tan(x) + 1)/sec(x)", "sin(x) + cos(x)"),
            ("diff_of", "sin(x) - cos(x)", "sin(x) + cos(x)"),
            ("diff", "sin(x) - cos(x)"),
        ],
    },
    "YANG-1.5-P18": {
        "final": "x - cos(x) + tan(x) + sec(x)",
        "lines": [
            (
                "Expand the product. (sin(x) + 1)*(sec(x)**2 + 1) = 1 + sin(x) + sec(x)**2 + sec(x)*tan(x).",
                r"Expand, then replace \(\sin x\sec^{2}x\) by \(\sec x\tan x\).",
            ),
        ],
        "steps": [
            ("eq", "(sin(x) + 1)*(sec(x)**2 + 1)", "1 + sin(x) + sec(x)**2 + sec(x)*tan(x)"),
            ("diff_of", "x - cos(x) + tan(x) + sec(x)", "1 + sin(x) + sec(x)**2 + sec(x)*tan(x)"),
            ("diff", "x - cos(x) + tan(x) + sec(x)"),
        ],
    },
    "YANG-1.5-P19": {
        "final": "-log(sin(2*x))",
        "lines": [
            (
                "Difference of squares. (-csc(x) + sec(x))*(csc(x) + sec(x))/(tan(x) + cot(x)) = -2*cot(2*x).",
                r"The quotient simplifies to \(-2\cot(2x)\).",
            ),
        ],
        "steps": [
            (
                "eq",
                "(-csc(x) + sec(x))*(csc(x) + sec(x))/(tan(x) + cot(x))",
                "-2*cot(2*x)",
            ),
            ("diff_of", "-log(sin(2*x))", "-2*cot(2*x)"),
            ("diff", "-log(sin(2*x))"),
        ],
    },
    "YANG-1.5-P20": {
        "final": "sin(x)**2/2",
        "lines": [
            (
                "Cancel sin(x) + cos(x). (sin(x) + cos(x))/(csc(x) + sec(x)) = sin(x)*cos(x).",
                r"Write \(\sec x+\csc x=(\sin x+\cos x)/(\sin x\cos x)\) and cancel.",
            ),
        ],
        "steps": [
            ("eq", "(sin(x) + cos(x))/(csc(x) + sec(x))", "sin(x)*cos(x)"),
            ("diff_of", "sin(x)**2/2", "sin(x)*cos(x)"),
            ("diff", "sin(x)**2/2"),
        ],
    },
    "YANG-1.8-P01": {
        "final": "log(Abs(x)) - log(Abs(x + 1))",
        "lines": [
            (
                "Partial fractions. 1/(x*(x + 1)) = 1/x - 1/(x + 1).",
                r"Partial fractions. \(1/(x(x+1))=1/x-1/(x+1)\).",
            ),
            (
                "The antiderivative of 1/x is log(Abs(x)). The antiderivative of -1/(x + 1) is -log(Abs(x + 1)).",
                r"The antiderivative of \(1/x\) is \(\log|x|\). The antiderivative of \(-1/(x+1)\) is \(-\log|x+1|\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x*(x + 1))", "1/x - 1/(x + 1)"),
            ("diff_of", "log(Abs(x))", "1/x"),
            ("diff_of", "-log(Abs(x + 1))", "-1/(x + 1)"),
            ("diff", "log(Abs(x)) - log(Abs(x + 1))"),
        ],
    },
    "YANG-1.8-P02": {
        "final": "-log(Abs(x)) + log(Abs(x + 1)) - 1/x",
        "lines": [
            (
                "Partial fractions with a repeated factor. 1/(x**2*(x + 1)) = -1/x + 1/x**2 + 1/(x + 1).",
                r"Partial fractions with a repeated factor. \(1/(x^{2}(x+1))=-1/x+1/x^{2}+1/(x+1)\).",
            ),
            (
                "The antiderivative of -1/x is -log(Abs(x)). The antiderivative of 1/x**2 is -1/x. The antiderivative of 1/(x + 1) is log(Abs(x + 1)).",
                r"The antiderivatives are \(-\log|x|\), \(-1/x\), and \(\log|x+1|\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x**2*(x + 1))", "-1/x + 1/x**2 + 1/(x + 1)"),
            ("diff_of", "-log(Abs(x))", "-1/x"),
            ("diff_of", "-1/x", "1/x**2"),
            ("diff_of", "log(Abs(x + 1))", "1/(x + 1)"),
            ("diff", "-log(Abs(x)) + log(Abs(x + 1)) - 1/x"),
        ],
    },
    "YANG-1.8-P03": {
        "final": "log(Abs(x + 1)) - log(Abs(x + 2))",
        "lines": [
            (
                "Partial fractions. 1/((x + 1)*(x + 2)) = 1/(x + 1) - 1/(x + 2).",
                r"Partial fractions. \(1/((x+1)(x+2))=1/(x+1)-1/(x+2)\).",
            ),
            (
                "The antiderivative of 1/(x + 1) is log(Abs(x + 1)). The antiderivative of -1/(x + 2) is -log(Abs(x + 2)).",
                r"The antiderivatives are \(\log|x+1|\) and \(-\log|x+2|\).",
            ),
        ],
        "steps": [
            ("eq", "1/((x + 1)*(x + 2))", "1/(x + 1) - 1/(x + 2)"),
            ("diff_of", "log(Abs(x + 1))", "1/(x + 1)"),
            ("diff_of", "-log(Abs(x + 2))", "-1/(x + 2)"),
            ("diff", "log(Abs(x + 1)) - log(Abs(x + 2))"),
        ],
    },
    "YANG-1.8-P04": {
        "final": "-log(Abs(x)) + log(Abs(2*x - 1))",
        "lines": [
            (
                "Partial fractions. 1/(x*(2*x - 1)) = -1/x + 2/(2*x - 1).",
                r"Partial fractions. \(1/(x(2x-1))=-1/x+2/(2x-1)\).",
            ),
            (
                "The antiderivative of -1/x is -log(Abs(x)). The antiderivative of 2/(2*x - 1) is log(Abs(2*x - 1)), since the derivative of 2*x - 1 is 2.",
                r"The antiderivative of \(-1/x\) is \(-\log|x|\). The antiderivative of \(2/(2x-1)\) is \(\log|2x-1|\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x*(2*x - 1))", "-1/x + 2/(2*x - 1)"),
            ("diff_of", "-log(Abs(x))", "-1/x"),
            ("diff_of", "log(Abs(2*x - 1))", "2/(2*x - 1)"),
            ("diff", "-log(Abs(x)) + log(Abs(2*x - 1))"),
        ],
    },
    "YANG-1.8-P05": {
        "final": "log(Abs(x - 1))/2 - log(Abs(x + 1))/2",
        "lines": [
            (
                "Partial fractions. 1/(x**2 - 1) = (1/2)/(x - 1) - (1/2)/(x + 1).",
                r"Partial fractions. \(1/(x^{2}-1)=(1/2)/(x-1)-(1/2)/(x+1)\).",
            ),
            (
                "The antiderivative of (1/2)/(x - 1) is log(Abs(x - 1))/2. The antiderivative of -(1/2)/(x + 1) is -log(Abs(x + 1))/2.",
                r"The antiderivatives are \(\frac12\log|x-1|\) and \(-\frac12\log|x+1|\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x**2 - 1)", "(1/2)/(x - 1) - (1/2)/(x + 1)"),
            ("diff_of", "log(Abs(x - 1))/2", "(1/2)/(x - 1)"),
            ("diff_of", "-log(Abs(x + 1))/2", "-(1/2)/(x + 1)"),
            ("diff", "log(Abs(x - 1))/2 - log(Abs(x + 1))/2"),
        ],
    },
    "YANG-1.8-P06": {
        "final": "log(Abs(x**2 + 4*x + 3))/2",
        "lines": [
            (
                "Logarithmic derivative. (x + 2)/(x**2 + 4*x + 3) = (2*x + 4)/(2*(x**2 + 4*x + 3)).",
                r"Logarithmic derivative. \((x+2)/(x^{2}+4x+3)=(2x+4)/(2(x^{2}+4x+3))\).",
            ),
            (
                "The antiderivative is log(Abs(x**2 + 4*x + 3))/2.",
                r"The antiderivative is \(\frac12\log|x^{2}+4x+3|\).",
            ),
        ],
        "steps": [
            ("eq", "(x + 2)/(x**2 + 4*x + 3)", "(2*x + 4)/(2*(x**2 + 4*x + 3))"),
            ("diff", "log(Abs(x**2 + 4*x + 3))/2"),
        ],
    },
    "YANG-1.8-P07": {
        "final": "-log(Abs(x)) + log(Abs(x - 1))/2 + log(Abs(x + 1))/2",
        "lines": [
            (
                "Partial fractions. 1/(x**3 - x) = -1/x + (1/2)/(x - 1) + (1/2)/(x + 1).",
                r"Partial fractions. \(1/(x^{3}-x)=-1/x+(1/2)/(x-1)+(1/2)/(x+1)\).",
            ),
            (
                "The antiderivative of -1/x is -log(Abs(x)). The antiderivative of (1/2)/(x - 1) is log(Abs(x - 1))/2. The antiderivative of (1/2)/(x + 1) is log(Abs(x + 1))/2.",
                r"The antiderivatives are \(-\log|x|\), \(\frac12\log|x-1|\), and \(\frac12\log|x+1|\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x**3 - x)", "-1/x + (1/2)/(x - 1) + (1/2)/(x + 1)"),
            ("diff_of", "-log(Abs(x))", "-1/x"),
            ("diff_of", "log(Abs(x - 1))/2", "(1/2)/(x - 1)"),
            ("diff_of", "log(Abs(x + 1))/2", "(1/2)/(x + 1)"),
            ("diff", "-log(Abs(x)) + log(Abs(x - 1))/2 + log(Abs(x + 1))/2"),
        ],
    },
    "YANG-1.8-P08": {
        "final": "-log(Abs(x + 1))/2 + 2*log(Abs(x + 2)) - 3*log(Abs(x + 3))/2",
        "lines": [
            (
                "Partial fractions. x/((x + 1)*(x + 2)*(x + 3)) = -1/(2*(x + 1)) + 2/(x + 2) - 3/(2*(x + 3)).",
                r"Partial fractions. \(x/((x+1)(x+2)(x+3))=-1/(2(x+1))+2/(x+2)-3/(2(x+3))\).",
            ),
            (
                "The antiderivative of -1/(2*(x + 1)) is -log(Abs(x + 1))/2. The antiderivative of 2/(x + 2) is 2*log(Abs(x + 2)). The antiderivative of -3/(2*(x + 3)) is -3*log(Abs(x + 3))/2.",
                r"The antiderivatives are \(-\frac12\log|x+1|\), \(2\log|x+2|\), and \(-\frac32\log|x+3|\).",
            ),
        ],
        "steps": [
            ("eq", "x/((x + 1)*(x + 2)*(x + 3))", "-1/(2*(x + 1)) + 2/(x + 2) - 3/(2*(x + 3))"),
            ("diff_of", "-log(Abs(x + 1))/2", "-1/(2*(x + 1))"),
            ("diff_of", "2*log(Abs(x + 2))", "2/(x + 2)"),
            ("diff_of", "-3*log(Abs(x + 3))/2", "-3/(2*(x + 3))"),
            ("diff", "-log(Abs(x + 1))/2 + 2*log(Abs(x + 2)) - 3*log(Abs(x + 3))/2"),
        ],
    },
    "YANG-1.8-P09": {
        "final": "-atan(x) - 1/x",
        "lines": [
            (
                "Partial fractions. 1/(x**2*(x**2 + 1)) = 1/x**2 - 1/(x**2 + 1).",
                r"Partial fractions. \(1/(x^{2}(x^{2}+1))=1/x^{2}-1/(x^{2}+1)\).",
            ),
            (
                "The antiderivative of 1/x**2 is -1/x. The antiderivative of -1/(x**2 + 1) is -atan(x).",
                r"The antiderivatives are \(-1/x\) and \(-\arctan x\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x**2*(x**2 + 1))", "1/x**2 - 1/(x**2 + 1)"),
            ("diff_of", "-1/x", "1/x**2"),
            ("diff_of", "-atan(x)", "-1/(x**2 + 1)"),
            ("diff", "-atan(x) - 1/x"),
        ],
    },
    "YANG-1.8-P10": {
        "final": "log(Abs(x)) - log(Abs(x + 1)) + 1/(x + 1)",
        "lines": [
            (
                "Partial fractions with a repeated factor. 1/(x*(x + 1)**2) = 1/x - 1/(x + 1) - 1/(x + 1)**2.",
                r"Partial fractions with a repeated factor. \(1/(x(x+1)^{2})=1/x-1/(x+1)-1/(x+1)^{2}\).",
            ),
            (
                "The antiderivative of 1/x is log(Abs(x)). The antiderivative of -1/(x + 1) is -log(Abs(x + 1)). The antiderivative of -1/(x + 1)**2 is 1/(x + 1).",
                r"The antiderivatives are \(\log|x|\), \(-\log|x+1|\), and \(1/(x+1)\).",
            ),
        ],
        "steps": [
            ("eq", "1/(x*(x + 1)**2)", "1/x - 1/(x + 1) - 1/(x + 1)**2"),
            ("diff_of", "log(Abs(x))", "1/x"),
            ("diff_of", "-log(Abs(x + 1))", "-1/(x + 1)"),
            ("diff_of", "1/(x + 1)", "-1/(x + 1)**2"),
            ("diff", "log(Abs(x)) - log(Abs(x + 1)) + 1/(x + 1)"),
        ],
    },
    "YANG-1.8-P11": {
        "final": "x - 2*log(Abs(x + 2)) + 2*log(Abs(x + 3))",
        "lines": [
            (
                "Polynomial division, then partial fractions. (x + 1)*(x + 4)/((x + 2)*(x + 3)) = 1 - 2/((x + 2)*(x + 3)).",
                r"Polynomial division, then partial fractions. \((x+1)(x+4)/((x+2)(x+3))=1-2/((x+2)(x+3))\).",
            ),
            (
                "2/((x + 2)*(x + 3)) = 2/(x + 2) - 2/(x + 3).",
                r"\(2/((x+2)(x+3))=2/(x+2)-2/(x+3)\).",
            ),
            (
                "The antiderivative of 1 is x. The antiderivative of -2/(x + 2) is -2*log(Abs(x + 2)). The antiderivative of 2/(x + 3) is 2*log(Abs(x + 3)).",
                r"The antiderivatives are \(x\), \(-2\log|x+2|\), and \(2\log|x+3|\).",
            ),
        ],
        "steps": [
            ("eq", "(x + 1)*(x + 4)/((x + 2)*(x + 3))", "1 - 2/((x + 2)*(x + 3))"),
            ("eq", "2/((x + 2)*(x + 3))", "2/(x + 2) - 2/(x + 3)"),
            ("diff_of", "x", "1"),
            ("diff_of", "-2*log(Abs(x + 2))", "-2/(x + 2)"),
            ("diff_of", "2*log(Abs(x + 3))", "2/(x + 3)"),
            ("diff", "x - 2*log(Abs(x + 2)) + 2*log(Abs(x + 3))"),
        ],
    },
    "YANG-1.8-P12": {
        "final": "-log(exp(x) + 1) + 2*log(exp(x) + 2)",
        "lines": [
            (
                "Substitution u = exp(x). exp(2*x)/(exp(2*x) + 3*exp(x) + 2) = exp(x)*exp(x)/((exp(x) + 1)*(exp(x) + 2)).",
                r"Substitution \(u=e^{x}\). \(e^{2x}/(e^{2x}+3e^{x}+2)=e^{x}e^{x}/((e^{x}+1)(e^{x}+2))\).",
            ),
            (
                "Partial fractions. exp(x)/((exp(x) + 1)*(exp(x) + 2)) = -1/(exp(x) + 1) + 2/(exp(x) + 2).",
                r"Partial fractions. \(e^{x}/((e^{x}+1)(e^{x}+2))=-1/(e^{x}+1)+2/(e^{x}+2)\).",
            ),
            (
                "The antiderivative of -exp(x)/(exp(x) + 1) is -log(exp(x) + 1). The antiderivative of 2*exp(x)/(exp(x) + 2) is 2*log(exp(x) + 2). Both exp(x) + 1 and exp(x) + 2 stay positive.",
                r"The antiderivatives are \(-\log(e^{x}+1)\) and \(2\log(e^{x}+2)\). Both factors stay positive.",
            ),
        ],
        "steps": [
            ("eq", "exp(2*x)/(exp(2*x) + 3*exp(x) + 2)", "exp(x)*exp(x)/((exp(x) + 1)*(exp(x) + 2))"),
            ("eq", "exp(x)/((exp(x) + 1)*(exp(x) + 2))", "-1/(exp(x) + 1) + 2/(exp(x) + 2)"),
            ("diff_of", "-log(exp(x) + 1)", "-exp(x)/(exp(x) + 1)"),
            ("diff_of", "2*log(exp(x) + 2)", "2*exp(x)/(exp(x) + 2)"),
            ("diff", "-log(exp(x) + 1) + 2*log(exp(x) + 2)"),
        ],
    },
    "YANG-1.8-P13": {
        "final": "log(Abs(x + 1)) - atan(x)",
        "lines": [
            (
                "Partial fractions. (x**2 - x)/(x**3 + x**2 + x + 1) = 1/(x + 1) - 1/(x**2 + 1).",
                r"Partial fractions. \((x^{2}-x)/(x^{3}+x^{2}+x+1)=1/(x+1)-1/(x^{2}+1)\).",
            ),
            (
                "The antiderivative of 1/(x + 1) is log(Abs(x + 1)). The antiderivative of -1/(x**2 + 1) is -atan(x).",
                r"The antiderivatives are \(\log|x+1|\) and \(-\arctan x\).",
            ),
        ],
        "steps": [
            ("eq", "(x**2 - x)/(x**3 + x**2 + x + 1)", "1/(x + 1) - 1/(x**2 + 1)"),
            ("diff_of", "log(Abs(x + 1))", "1/(x + 1)"),
            ("diff_of", "-atan(x)", "-1/(x**2 + 1)"),
            ("diff", "log(Abs(x + 1)) - atan(x)"),
        ],
    },
    "YANG-1.8-P14": {
        "final": "log(Abs(x - 2)) + 2*log(Abs(x + 4))",
        "lines": [
            (
                "Partial fractions. 3*x/(x**2 + 2*x - 8) = 1/(x - 2) + 2/(x + 4).",
                r"Partial fractions. \(3x/(x^{2}+2x-8)=1/(x-2)+2/(x+4)\).",
            ),
            (
                "The antiderivative of 1/(x - 2) is log(Abs(x - 2)). The antiderivative of 2/(x + 4) is 2*log(Abs(x + 4)).",
                r"The antiderivatives are \(\log|x-2|\) and \(2\log|x+4|\).",
            ),
        ],
        "steps": [
            ("eq", "3*x/(x**2 + 2*x - 8)", "1/(x - 2) + 2/(x + 4)"),
            ("diff_of", "log(Abs(x - 2))", "1/(x - 2)"),
            ("diff_of", "2*log(Abs(x + 4))", "2/(x + 4)"),
            ("diff", "log(Abs(x - 2)) + 2*log(Abs(x + 4))"),
        ],
    },
    "YANG-1.8-P15": {
        "final": "2*log(Abs(x - 1)) - log(Abs(x + 2))",
        "lines": [
            (
                "Partial fractions. (x + 5)/(x**2 + x - 2) = 2/(x - 1) - 1/(x + 2).",
                r"Partial fractions. \((x+5)/(x^{2}+x-2)=2/(x-1)-1/(x+2)\).",
            ),
            (
                "The antiderivative of 2/(x - 1) is 2*log(Abs(x - 1)). The antiderivative of -1/(x + 2) is -log(Abs(x + 2)).",
                r"The antiderivatives are \(2\log|x-1|\) and \(-\log|x+2|\).",
            ),
        ],
        "steps": [
            ("eq", "(x + 5)/(x**2 + x - 2)", "2/(x - 1) - 1/(x + 2)"),
            ("diff_of", "2*log(Abs(x - 1))", "2/(x - 1)"),
            ("diff_of", "-log(Abs(x + 2))", "-1/(x + 2)"),
            ("diff", "2*log(Abs(x - 1)) - log(Abs(x + 2))"),
        ],
    },
    "YANG-1.8-P16": {
        "final": "log(3)/2",
        "lines": [
            (
                "Partial fractions on [2, 4]. (x - 4)/(x**2 - 6*x + 5) = (3/4)/(x - 1) + (1/4)/(x - 5).",
                r"Partial fractions on \([2,4]\). \((x-4)/(x^{2}-6x+5)=(3/4)/(x-1)+(1/4)/(x-5)\).",
            ),
            (
                "The antiderivative of (3/4)/(x - 1) is (3/4)*log(Abs(x - 1)). The antiderivative of (1/4)/(x - 5) is (1/4)*log(Abs(x - 5)).",
                r"The antiderivatives are \(\frac34\log|x-1|\) and \(\frac14\log|x-5|\).",
            ),
            (
                "The antiderivative (3/4)*log(Abs(x - 1)) + (1/4)*log(Abs(x - 5)) from 2 to 4 equals log(3)/2.",
                r"That antiderivative from \(2\) to \(4\) equals \(\frac12\log 3\).",
            ),
        ],
        "steps": [
            ("eq", "(x - 4)/(x**2 - 6*x + 5)", "(3/4)/(x - 1) + (1/4)/(x - 5)"),
            ("diff_of", "(3/4)*log(Abs(x - 1))", "(3/4)/(x - 1)"),
            ("diff_of", "(1/4)*log(Abs(x - 5))", "(1/4)/(x - 5)"),
            ("ends", "(3/4)*log(Abs(x - 1)) + (1/4)*log(Abs(x - 5))", "2", "4", "1", "log(3)/2"),
        ],
    },
    "YANG-1.8-P17": {
        "final": "log(3)/4",
        "lines": [
            (
                "Partial fractions. 1/((x - 2)*(x + 6)) = (1/8)/(x - 2) - (1/8)/(x + 6).",
                r"Partial fractions. \(1/((x-2)(x+6))=(1/8)/(x-2)-(1/8)/(x+6)\).",
            ),
            (
                "For x > 0, (x - 2)/(x + 6) = (1 - 2/x)/(1 + 6/x). The antiderivative (1/8)*log(Abs((1 - 2/x)/(1 + 6/x))) equals 0 at oo and -log(3)/4 at 3.",
                r"For \(x>0\), \((x-2)/(x+6)=(1-2/x)/(1+6/x)\). The antiderivative is \(0\) at infinity and \(-\frac14\log 3\) at \(3\).",
            ),
        ],
        "steps": [
            ("eq", "1/((x - 2)*(x + 6))", "(1/8)/(x - 2) - (1/8)/(x + 6)"),
            ("eq", "(x - 2)/(x + 6)", "(1 - 2/x)/(1 + 6/x)"),
            ("diff_of", "(1/8)*log(Abs((1 - 2/x)/(1 + 6/x)))", "1/((x - 2)*(x + 6))"),
            ("ends", "(1/8)*log(Abs((1 - 2/x)/(1 + 6/x)))", "3", "oo", "1", "log(3)/4"),
        ],
    },
    "YANG-1.9-P01a": {
        "final": "9*pi/4",
        "lines": [
            (
                "Complete the square, as in the guide's Substitution Example. sqrt(-x**2 + 6*x) = sqrt(9-(x-3)**2).",
                r"Complete the square, as in the guide's Substitution Example. \(\sqrt{6x-x^{2}}=\sqrt{9-(x-3)^{2}}\).",
            ),
            (
                "The antiderivative (1/2)*((x-3)*sqrt(9-(x-3)**2) + 9*asin((x-3)/3)) from 0 to 3 is a quarter disk of radius 3.",
                r"The antiderivative from \(0\) to \(3\) is a quarter disk of radius \(3\).",
            ),
        ],
        "steps": [
            ("eq", "sqrt(-x**2 + 6*x)", "sqrt(9-(x-3)**2)"),
            ("diff_of", "(1/2)*((x-3)*sqrt(9-(x-3)**2) + 9*asin((x-3)/3))", "sqrt(9-(x-3)**2)"),
            ("ends", "(1/2)*((x-3)*sqrt(9-(x-3)**2) + 9*asin((x-3)/3))", "0", "3", "1", "9*pi/4"),
        ],
    },
    "YANG-1.9-P01b": {
        "final": "pi/4",
        "lines": [
            (
                "Factor the radicand, as in the guide's Exponential Example. sqrt(exp(-2*x) - exp(-4*x)) = exp(-x)*sqrt(1 - exp(-2*x)).",
                r"Factor the radicand, as in the guide's Exponential Example. \(\sqrt{e^{-2x}-e^{-4x}}=e^{-x}\sqrt{1-e^{-2x}}\).",
            ),
            (
                "exp(-2*x) = exp(-x)**2, and the derivative of exp(-x) is -exp(-x), so u = exp(-x) carries the integral to sqrt(1 - x**2) from 0 to 1.",
                r"\(e^{-2x}=(e^{-x})^{2}\), and \(u=e^{-x}\) carries the integral to \(\sqrt{1-x^{2}}\) from \(0\) to \(1\).",
            ),
            (
                "The antiderivative (1/2)*(x*sqrt(1 - x**2) + asin(x)) from 0 to 1 is a quarter disk of radius 1.",
                r"That antiderivative from \(0\) to \(1\) is a quarter disk of radius \(1\).",
            ),
        ],
        "steps": [
            ("eq", "sqrt(exp(-2*x) - exp(-4*x))", "exp(-x)*sqrt(1 - exp(-2*x))"),
            ("eq", "exp(-2*x)", "exp(-x)**2"),
            ("diff_of", "exp(-x)", "-exp(-x)"),
            ("diff_of", "(1/2)*(x*sqrt(1 - x**2) + asin(x))", "sqrt(1 - x**2)"),
            ("ends", "(1/2)*(x*sqrt(1 - x**2) + asin(x))", "0", "1", "1", "pi/4"),
        ],
    },
    "YANG-1.9-P01c": {
        "final": "3*pi/2",
        "lines": [
            (
                "Algebraic split, as in the guide's Hybrid Example. (2 - x**2)/sqrt(1 - x**2) = 1/sqrt(1 - x**2) + sqrt(1 - x**2).",
                r"Algebraic split, as in the guide's Hybrid Example. \((2-x^{2})/\sqrt{1-x^{2}}=1/\sqrt{1-x^{2}}+\sqrt{1-x^{2}}\).",
            ),
            (
                "(2 - x**2)*(x**3 + 1)/sqrt(1 - x**2) = (1/sqrt(1 - x**2) + sqrt(1 - x**2))*(1 + x**3).",
                r"\((2-x^{2})(1+x^{3})/\sqrt{1-x^{2}}=(1/\sqrt{1-x^{2}}+\sqrt{1-x^{2}})(1+x^{3})\).",
            ),
            (
                "The odd part (1/sqrt(1 - x**2) + sqrt(1 - x**2))*x**3 satisfies f(-x) + f(x) = 0 on [-1, 1].",
                r"The odd part with \(x^{3}\) integrates to \(0\) on \([-1,1]\).",
            ),
            (
                "The even antiderivative (3/2)*asin(x) + (1/2)*x*sqrt(1 - x**2) from -1 to 1 equals 3*pi/2.",
                r"The even antiderivative from \(-1\) to \(1\) equals \(3\pi/2\).",
            ),
        ],
        "steps": [
            ("eq", "(2 - x**2)/sqrt(1 - x**2)", "1/sqrt(1 - x**2) + sqrt(1 - x**2)"),
            ("eq", "(2 - x**2)*(x**3 + 1)/sqrt(1 - x**2)", "(1/sqrt(1 - x**2) + sqrt(1 - x**2))*(1 + x**3)"),
            ("odd", "(1/sqrt(1 - x**2) + sqrt(1 - x**2))*x**3"),
            ("diff_of", "(3/2)*asin(x) + (1/2)*x*sqrt(1 - x**2)", "1/sqrt(1 - x**2) + sqrt(1 - x**2)"),
            ("ends", "(3/2)*asin(x) + (1/2)*x*sqrt(1 - x**2)", "-1", "1", "1", "3*pi/2"),
        ],
    },
    "YANG-1.9-P04a": {
        "final": "pi",
        "lines": [
            (
                "Hidden symmetry, as in the guide. sqrt(4 - x**2)*(x**3*cos(x/2) + 1/2) = x**3*cos(x/2)*sqrt(4 - x**2) + (1/2)*sqrt(4 - x**2).",
                r"Hidden symmetry, as in the guide. The integrand splits into an odd term and \(\frac12\sqrt{4-x^{2}}\).",
            ),
            (
                "The odd part x**3*cos(x/2)*sqrt(4 - x**2) satisfies f(-x) + f(x) = 0 on [-2, 2].",
                r"The odd part \(x^{3}\cos(x/2)\sqrt{4-x^{2}}\) integrates to \(0\) on \([-2,2]\).",
            ),
            (
                "The antiderivative (1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2)) of sqrt(4 - x**2), from 0 to 2, is a quarter disk of radius 2.",
                r"The antiderivative of \(\sqrt{4-x^{2}}\) from \(0\) to \(2\) is a quarter disk of radius \(2\).",
            ),
        ],
        "steps": [
            ("eq", "sqrt(4 - x**2)*(x**3*cos(x/2) + 1/2)", "x**3*cos(x/2)*sqrt(4 - x**2) + (1/2)*sqrt(4 - x**2)"),
            ("odd", "x**3*cos(x/2)*sqrt(4 - x**2)"),
            ("diff_of", "(1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2))", "sqrt(4 - x**2)"),
            ("ends", "(1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2))", "0", "2", "1", "pi"),
        ],
    },
    "YANG-1.9-P04b": {
        "final": "sqrt(3)*pi",
        "lines": [
            (
                "Factor the radicand, as in the guide's Ellipse Example. sqrt(12 - 3*x**2) = sqrt(3)*sqrt(4 - x**2).",
                r"Factor the radicand, as in the guide's Ellipse Example. \(\sqrt{12-3x^{2}}=\sqrt{3}\sqrt{4-x^{2}}\).",
            ),
            (
                "The antiderivative (1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2)) of sqrt(4 - x**2) from 0 to 2 is a quarter disk of radius 2. Multiply by sqrt(3).",
                r"The integral of \(\sqrt{4-x^{2}}\) from \(0\) to \(2\) is a quarter disk of radius \(2\). Multiply by \(\sqrt{3}\).",
            ),
        ],
        "steps": [
            ("eq", "sqrt(12 - 3*x**2)", "sqrt(3)*sqrt(4 - x**2)"),
            ("diff_of", "(1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2))", "sqrt(4 - x**2)"),
            ("ends", "(1/2)*(x*sqrt(4 - x**2) + 4*asin(x/2))", "0", "2", "sqrt(3)", "sqrt(3)*pi"),
        ],
    },
}


def _add(ident: str, final: str, lines: list, steps: list) -> None:
    SPECS[ident] = {"final": final, "lines": lines, "steps": steps}


_add(
    "YANG-2.3-P01",
    "2*sqrt(x)*exp(sqrt(x)) - 2*exp(sqrt(x))",
    [
        (
            "Forced substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)), and 2*sqrt(x)*(1/(2*sqrt(x))) equals 1, so dx = 2*sqrt(x)*du.",
            r"Forced substitution \(u=\sqrt{x}\). The derivative of \(\sqrt{x}\) is \(1/(2\sqrt{x})\), and \(2\sqrt{x}\cdot(1/(2\sqrt{x}))\) equals \(1\), so \(dx=2\sqrt{x}\,du\).",
        ),
        (
            "The integrand becomes 2*u*exp(u). Integration by parts gives 2*exp(sqrt(x))*(sqrt(x) - 1).",
            r"The integrand becomes \(2ue^{u}\). Integration by parts gives \(2e^{\sqrt{x}}(\sqrt{x}-1)\).",
        ),
        (
            "That equals 2*sqrt(x)*exp(sqrt(x)) - 2*exp(sqrt(x)).",
            r"That equals \(2\sqrt{x}e^{\sqrt{x}}-2e^{\sqrt{x}}\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "2*sqrt(x)*(1/(2*sqrt(x)))", "1"),
        ("eq", "2*exp(sqrt(x))*(sqrt(x) - 1)", "2*sqrt(x)*exp(sqrt(x)) - 2*exp(sqrt(x))"),
        ("diff", "2*exp(sqrt(x))*(sqrt(x) - 1)"),
        ("diff", "2*sqrt(x)*exp(sqrt(x)) - 2*exp(sqrt(x))"),
    ],
)

_add(
    "YANG-2.3-P02",
    "x*sin(log(x))/2 - x*cos(log(x))/2",
    [
        (
            "Forced substitution u = log(x). The derivative of log(x) is 1/x, and exp(log(x)) equals x, so dx = x*du.",
            r"Forced substitution \(u=\log x\). The derivative of \(\log x\) is \(1/x\), and \(e^{\log x}=x\), so \(dx=x\,du\).",
        ),
        (
            "The integrand becomes x*sin(u) in u, that is exp(u)*sin(u). Two integrations by parts give x*(sin(log(x)) - cos(log(x)))/2.",
            r"The integrand becomes \(e^{u}\sin u\). Two integrations by parts give \(x(\sin(\log x)-\cos(\log x))/2\).",
        ),
        (
            "That equals x*sin(log(x))/2 - x*cos(log(x))/2.",
            r"That equals \(\frac{x\sin(\log x)}{2}-\frac{x\cos(\log x)}{2}\).",
        ),
    ],
    [
        ("diff_of", "log(x)", "1/x"),
        ("eq", "exp(log(x))", "x"),
        ("eq", "x*(sin(log(x)) - cos(log(x)))/2", "x*sin(log(x))/2 - x*cos(log(x))/2"),
        ("diff", "x*(sin(log(x)) - cos(log(x)))/2"),
        ("diff", "x*sin(log(x))/2 - x*cos(log(x))/2"),
    ],
)

_add(
    "YANG-2.3-P03",
    "4097/45",
    [
        (
            "Forced substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)), so dx = 2*u*du.",
            r"Forced substitution \(u=\sqrt{x}\). The derivative of \(\sqrt{x}\) is \(1/(2\sqrt{x})\), so \(dx=2u\,du\).",
        ),
        (
            "Let t = 1 + u. The antiderivative is 2*((sqrt(x)+1)**10/10 - (sqrt(x)+1)**9/9).",
            r"Let \(t=1+u\). The antiderivative is \(2(( \sqrt{x}+1)^{10}/10-(\sqrt{x}+1)^{9}/9)\).",
        ),
        (
            "The endpoints u = 0 and u = 1 give 2*(2**10/10 - 2**9/9 - 1/10 + 1/9), which equals 4097/45.",
            r"The endpoints \(u=0\) and \(u=1\) give \(2(2^{10}/10-2^{9}/9-1/10+1/9)\), which equals \(4097/45\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("diff", "2*((sqrt(x)+1)**10/10 - (sqrt(x)+1)**9/9)"),
        ("eq", "2*(2**10/10 - 2**9/9 - 1/10 + 1/9)", "4097/45"),
        ("ends", "2*((sqrt(x)+1)**10/10 - (sqrt(x)+1)**9/9)", "0", "1", "1", "4097/45"),
    ],
)

_add(
    "YANG-2.3-P04",
    "4*sqrt(x)*sqrt(sqrt(x) + 1)/3 - 8*sqrt(sqrt(x) + 1)/3",
    [
        (
            "Forced substitution u = sqrt(sqrt(x) + 1), after t = sqrt(x). Then 4*(sqrt(sqrt(x)+1))**3/3 - 4*sqrt(sqrt(x)+1) is an antiderivative.",
            r"Forced substitution \(u=\sqrt{\sqrt{x}+1}\), after \(t=\sqrt{x}\). Then \(\frac{4}{3}(\sqrt{\sqrt{x}+1})^{3}-4\sqrt{\sqrt{x}+1}\) is an antiderivative.",
        ),
        (
            "Expand u**3 = (sqrt(x) + 1)*u. That form equals 4*sqrt(x)*sqrt(sqrt(x) + 1)/3 - 8*sqrt(sqrt(x) + 1)/3.",
            r"Expand \(u^{3}=(\sqrt{x}+1)u\). That form equals \(\frac{4\sqrt{x}\sqrt{\sqrt{x}+1}}{3}-\frac{8\sqrt{\sqrt{x}+1}}{3}\).",
        ),
    ],
    [
        ("diff", "4*(sqrt(sqrt(x)+1))**3/3 - 4*sqrt(sqrt(x)+1)"),
        ("eq", "4*(sqrt(sqrt(x)+1))**3/3 - 4*sqrt(sqrt(x)+1)", "4*sqrt(x)*sqrt(sqrt(x) + 1)/3 - 8*sqrt(sqrt(x) + 1)/3"),
        ("diff", "4*sqrt(x)*sqrt(sqrt(x) + 1)/3 - 8*sqrt(sqrt(x) + 1)/3"),
    ],
)

_add(
    "YANG-2.3-P05",
    "x*asin(x)**2 - 2*x + 2*sqrt(1 - x**2)*asin(x)",
    [
        (
            "Integration by parts on asin(x)**2, then t = asin(x). The combined antiderivative is x*asin(x)**2 - 2*(-asin(x)*sqrt(1-x**2) + x).",
            r"Integration by parts on \((\arcsin x)^{2}\), then \(t=\arcsin x\). The combined antiderivative is \(x(\arcsin x)^{2}-2(-\arcsin x\sqrt{1-x^{2}}+x)\).",
        ),
        (
            "That equals x*asin(x)**2 - 2*x + 2*sqrt(1 - x**2)*asin(x).",
            r"That equals \(x(\arcsin x)^{2}-2x+2\sqrt{1-x^{2}}\arcsin x\).",
        ),
    ],
    [
        ("eq", "x*asin(x)**2 - 2*(-asin(x)*sqrt(1-x**2) + x)", "x*asin(x)**2 - 2*x + 2*sqrt(1 - x**2)*asin(x)"),
        ("diff", "x*asin(x)**2 - 2*x + 2*sqrt(1 - x**2)*asin(x)"),
    ],
)

_add(
    "YANG-2.3-P06",
    "3*x**2*(2*x - 1)**(1/3)/7 - 3*x*(2*x - 1)**(1/3)/56 - 9*(2*x - 1)**(1/3)/112",
    [
        (
            "Forced substitution u = 2*x - 1, so x = (u + 1)/2 and dx = du/2. The antiderivative in u is 3*(2*x - 1)**(7/3)/28 + 3*(2*x - 1)**(4/3)/16.",
            r"Forced substitution \(u=2x-1\), so \(x=(u+1)/2\) and \(dx=du/2\). The antiderivative in \(u\) is \(\frac{3}{28}(2x-1)^{7/3}+\frac{3}{16}(2x-1)^{4/3}\).",
        ),
        (
            "Factor u**(1/3). That equals 3*x**2*(2*x - 1)**(1/3)/7 - 3*x*(2*x - 1)**(1/3)/56 - 9*(2*x - 1)**(1/3)/112.",
            r"Factor \(u^{1/3}\). That equals \(\frac{3x^{2}(2x-1)^{1/3}}{7}-\frac{3x(2x-1)^{1/3}}{56}-\frac{9(2x-1)^{1/3}}{112}\).",
        ),
    ],
    [
        ("diff", "3*(2*x - 1)**(7/3)/28 + 3*(2*x - 1)**(4/3)/16"),
        ("eq", "3*(2*x - 1)**(7/3)/28 + 3*(2*x - 1)**(4/3)/16", "3*x**2*(2*x - 1)**(1/3)/7 - 3*x*(2*x - 1)**(1/3)/56 - 9*(2*x - 1)**(1/3)/112"),
        ("diff", "3*x**2*(2*x - 1)**(1/3)/7 - 3*x*(2*x - 1)**(1/3)/56 - 9*(2*x - 1)**(1/3)/112"),
    ],
)

_add(
    "YANG-2.3-P07",
    "4*sqrt(2)/3 + 8/3",
    [
        (
            "Forced substitution t = sqrt(1 + x), then u = sqrt(1 + t). The antiderivative is 4*((sqrt(1+sqrt(1+x)))**3/3 - sqrt(1+sqrt(1+x))).",
            r"Forced substitution \(t=\sqrt{1+x}\), then \(u=\sqrt{1+t}\). The antiderivative is \(4((\sqrt{1+\sqrt{1+x}})^{3}/3-\sqrt{1+\sqrt{1+x}})\).",
        ),
        (
            "On [0, 8], u runs from sqrt(2) to 2. The evaluation equals 4*sqrt(2)/3 + 8/3.",
            r"On \([0,8]\), \(u\) runs from \(\sqrt{2}\) to \(2\). The evaluation equals \(\frac{4\sqrt{2}}{3}+\frac{8}{3}\).",
        ),
    ],
    [
        ("diff", "4*((sqrt(1+sqrt(1+x)))**3/3 - sqrt(1+sqrt(1+x)))"),
        ("ends", "4*((sqrt(1+sqrt(1+x)))**3/3 - sqrt(1+sqrt(1+x)))", "0", "8", "1", "4*sqrt(2)/3 + 8/3"),
    ],
)

_add(
    "YANG-2.3-P08",
    "-sqrt(x) + x*atan(sqrt(x)) + atan(sqrt(x))",
    [
        (
            "Forced substitution u = sqrt(x), so the integral is 2*u*atan(u). Integration by parts gives sqrt(x)**2*atan(sqrt(x)) - sqrt(x) + atan(sqrt(x)).",
            r"Forced substitution \(u=\sqrt{x}\), so the integral is \(2u\arctan u\). Integration by parts gives \(x\arctan\sqrt{x}-\sqrt{x}+\arctan\sqrt{x}\).",
        ),
        (
            "That equals -sqrt(x) + x*atan(sqrt(x)) + atan(sqrt(x)).",
            r"That equals \(-\sqrt{x}+x\arctan\sqrt{x}+\arctan\sqrt{x}\).",
        ),
    ],
    [
        ("eq", "sqrt(x)**2*atan(sqrt(x)) - sqrt(x) + atan(sqrt(x))", "-sqrt(x) + x*atan(sqrt(x)) + atan(sqrt(x))"),
        ("diff", "sqrt(x)**2*atan(sqrt(x)) - sqrt(x) + atan(sqrt(x))"),
        ("diff", "-sqrt(x) + x*atan(sqrt(x)) + atan(sqrt(x))"),
    ],
)

_add(
    "YANG-2.3-P09",
    "x*log(x)**3 - 3*x*log(x)**2 + 6*x*log(x) - 6*x",
    [
        (
            "The derivative of x*log(x)**3 is log(x)**3 + 3*log(x)**2. Repeat the reduction twice.",
            r"The derivative of \(x(\log x)^{3}\) is \((\log x)^{3}+3(\log x)^{2}\). Repeat the reduction twice.",
        ),
        (
            "The nested form x*log(x)**3 - 3*(x*log(x)**2 - 2*(x*log(x) - x)) equals x*log(x)**3 - 3*x*log(x)**2 + 6*x*log(x) - 6*x.",
            r"The nested form \(x(\log x)^{3}-3(x(\log x)^{2}-2(x\log x-x))\) equals \(x(\log x)^{3}-3x(\log x)^{2}+6x\log x-6x\).",
        ),
    ],
    [
        ("diff_of", "x*log(x)**3", "log(x)**3 + 3*log(x)**2"),
        ("eq", "x*log(x)**3 - 3*(x*log(x)**2 - 2*(x*log(x) - x))", "x*log(x)**3 - 3*x*log(x)**2 + 6*x*log(x) - 6*x"),
        ("diff", "x*log(x)**3 - 3*x*log(x)**2 + 6*x*log(x) - 6*x"),
    ],
)

_add(
    "YANG-2.3-P10",
    "2*log(sqrt(x) + 1) + 2/(sqrt(x) + 1)",
    [
        (
            "Forced substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)).",
            r"Forced substitution \(u=\sqrt{x}\). The derivative of \(\sqrt{x}\) is \(1/(2\sqrt{x})\).",
        ),
        (
            "Then 2*sqrt(x)/(sqrt(x)+1)**2 equals 2*(1/(sqrt(x)+1) - 1/(sqrt(x)+1)**2).",
            r"Then \(2\sqrt{x}/(\sqrt{x}+1)^{2}\) equals \(2(1/(\sqrt{x}+1)-1/(\sqrt{x}+1)^{2})\).",
        ),
        (
            "The antiderivative is 2*log(sqrt(x) + 1) + 2/(sqrt(x) + 1).",
            r"The antiderivative is \(2\log(\sqrt{x}+1)+2/(\sqrt{x}+1)\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "2*sqrt(x)/(sqrt(x)+1)**2", "2*(1/(sqrt(x)+1) - 1/(sqrt(x)+1)**2)"),
        ("diff", "2*log(sqrt(x) + 1) + 2/(sqrt(x) + 1)"),
    ],
)

_add(
    "YANG-2.3-P11",
    "6 - 3*pi/2",
    [
        (
            "Forced substitution t = sqrt(exp(x)-1). Then sqrt(exp(x)-1)**2 + 1 equals exp(x), and the integrand becomes 2*t**2/(t**2 + 9).",
            r"Forced substitution \(t=\sqrt{e^{x}-1}\). Then \(t^{2}+1=e^{x}\), and the integrand becomes \(2t^{2}/(t^{2}+9)\).",
        ),
        (
            "Write that as 2*(1 - 9/(t**2 + 9)). The antiderivative is 2*(sqrt(exp(x)-1) - 3*atan(sqrt(exp(x)-1)/3)).",
            r"Write that as \(2(1-9/(t^{2}+9))\). The antiderivative is \(2(\sqrt{e^{x}-1}-3\arctan(\sqrt{e^{x}-1}/3))\).",
        ),
        (
            "From 0 to log(10), t runs from 0 to 3. Then 2*(3 - 3*atan(1)) equals 6 - 3*pi/2.",
            r"From \(0\) to \(\log 10\), \(t\) runs from \(0\) to \(3\). Then \(2(3-3\arctan 1)\) equals \(6-3\pi/2\).",
        ),
    ],
    [
        ("eq", "sqrt(exp(x)-1)**2 + 1", "exp(x)"),
        ("eq", "2*(3 - 3*atan(1))", "6 - 3*pi/2"),
        ("diff", "2*(sqrt(exp(x)-1) - 3*atan(sqrt(exp(x)-1)/3))"),
        ("ends", "2*(sqrt(exp(x)-1) - 3*atan(sqrt(exp(x)-1)/3))", "0", "log(10)", "1", "6 - 3*pi/2"),
    ],
)

_add(
    "YANG-2.3-P12",
    "2*atan(sqrt(2021**x - 1))/log(2021)",
    [
        (
            "Forced substitution u = sqrt(2021**x - 1). Then sqrt(2021**x - 1)**2 + 1 equals 2021**x.",
            r"Forced substitution \(u=\sqrt{2021^{x}-1}\). Then \(u^{2}+1=2021^{x}\).",
        ),
        (
            "The derivative of log(2021**x) is log(2021), so dx = 2*u*du/(u**2 + 1)/log(2021). The integral in u is 2*atan(u)/log(2021).",
            r"The derivative of \(\log(2021^{x})\) is \(\log 2021\), so \(dx=2u\,du/((u^{2}+1)\log 2021)\). The integral in \(u\) is \(2\arctan(u)/\log 2021\).",
        ),
        (
            "The antiderivative is 2*atan(sqrt(2021**x - 1))/log(2021).",
            r"The antiderivative is \(2\arctan(\sqrt{2021^{x}-1})/\log 2021\).",
        ),
    ],
    [
        ("eq", "sqrt(2021**x - 1)**2 + 1", "2021**x"),
        ("diff_of", "log(2021**x)", "log(2021)"),
        ("diff", "2*atan(sqrt(2021**x - 1))/log(2021)"),
    ],
)

_add(
    "YANG-2.3-P13",
    "3*(x + 1)**(2/3)/2 + 3*(x + 1)**(1/3) + 3*log((x + 1)**(1/3) - 1)",
    [
        (
            "Forced substitution u = (x + 1)**(1/3), so dx = 3*u**2*du. Division gives (x+1)**(2/3)/((x+1)**(1/3)-1) = (x+1)**(1/3) + 1 + 1/((x+1)**(1/3)-1).",
            r"Forced substitution \(u=(x+1)^{1/3}\), so \(dx=3u^{2}\,du\). Division gives \(u^{2}/(u-1)=u+1+1/(u-1)\).",
        ),
        (
            "Integrate termwise. The antiderivative is 3*(x + 1)**(2/3)/2 + 3*(x + 1)**(1/3) + 3*log((x + 1)**(1/3) - 1).",
            r"Integrate termwise. The antiderivative is \(\frac{3}{2}(x+1)^{2/3}+3(x+1)^{1/3}+3\log((x+1)^{1/3}-1)\).",
        ),
    ],
    [
        ("eq", "(x+1)**(2/3)/((x+1)**(1/3)-1)", "(x+1)**(1/3) + 1 + 1/((x+1)**(1/3)-1)"),
        ("diff", "3*(x + 1)**(2/3)/2 + 3*(x + 1)**(1/3) + 3*log((x + 1)**(1/3) - 1)"),
    ],
)

_add(
    "YANG-2.3-P14",
    "log(x + 2*sqrt(x + 3)) - log(sqrt(x + 3) - 1)/2 + log(sqrt(x + 3) + 3)/2",
    [
        (
            "Forced substitution t = sqrt(x + 3). Then x + 2*sqrt(x + 3) equals (sqrt(x + 3) + 3)*(sqrt(x + 3) - 1).",
            r"Forced substitution \(t=\sqrt{x+3}\). Then \(x+2\sqrt{x+3}=(\sqrt{x+3}+3)(\sqrt{x+3}-1)\).",
        ),
        (
            "Partial fractions give 2*sqrt(x+3)/((sqrt(x+3)+3)*(sqrt(x+3)-1)) = (3/2)/(sqrt(x+3)+3) + (1/2)/(sqrt(x+3)-1).",
            r"Partial fractions give \(2t/((t+3)(t-1))=(3/2)/(t+3)+(1/2)/(t-1)\).",
        ),
        (
            "The logarithmic form (3/2)*log(sqrt(x+3)+3) + (1/2)*log(sqrt(x+3)-1) differentiates to 1/(x + 2*sqrt(x + 3)), and so does log(x + 2*sqrt(x + 3)) - log(sqrt(x + 3) - 1)/2 + log(sqrt(x + 3) + 3)/2.",
            r"Both \(\frac{3}{2}\log(t+3)+\frac{1}{2}\log(t-1)\) and \(\log(x+2\sqrt{x+3})-\frac{1}{2}\log(\sqrt{x+3}-1)+\frac{1}{2}\log(\sqrt{x+3}+3)\) differentiate to the integrand.",
        ),
    ],
    [
        ("eq", "x + 2*sqrt(x + 3)", "(sqrt(x + 3) + 3)*(sqrt(x + 3) - 1)"),
        ("eq", "2*sqrt(x+3)/((sqrt(x+3)+3)*(sqrt(x+3)-1))", "(3/2)/(sqrt(x+3)+3) + (1/2)/(sqrt(x+3)-1)"),
        ("diff_of", "(3/2)*log(sqrt(x+3)+3) + (1/2)*log(sqrt(x+3)-1)", "1/(x + 2*sqrt(x + 3))"),
        ("diff", "log(x + 2*sqrt(x + 3)) - log(sqrt(x + 3) - 1)/2 + log(sqrt(x + 3) + 3)/2"),
    ],
)

_add(
    "YANG-2.3-P15",
    "3**(sqrt(2*x + 1))*sqrt(2*x + 1)/log(3) - 3**(sqrt(2*x + 1))/log(3)**2",
    [
        (
            "Forced substitution u = sqrt(2*x + 1). The derivative of sqrt(2*x + 1) is 1/sqrt(2*x + 1), so dx = u*du.",
            r"Forced substitution \(u=\sqrt{2x+1}\). The derivative of \(\sqrt{2x+1}\) is \(1/\sqrt{2x+1}\), so \(dx=u\,du\).",
        ),
        (
            "The integral becomes u*3**u. Integration by parts gives 3**(sqrt(2*x + 1))*sqrt(2*x + 1)/log(3) - 3**(sqrt(2*x + 1))/log(3)**2.",
            r"The integral becomes \(u\cdot 3^{u}\). Integration by parts gives \(3^{\sqrt{2x+1}}\sqrt{2x+1}/\log 3-3^{\sqrt{2x+1}}/(\log 3)^{2}\).",
        ),
    ],
    [
        ("diff_of", "sqrt(2*x + 1)", "1/sqrt(2*x + 1)"),
        ("diff", "3**(sqrt(2*x + 1))*sqrt(2*x + 1)/log(3) - 3**(sqrt(2*x + 1))/log(3)**2"),
    ],
)

_add(
    "YANG-2.3-P16",
    "-log(2)**2/2",
    [
        (
            "The factor exp(-x)/(1 - exp(-x)) equals 1/(exp(x) - 1), so log(1 - exp(-x))**2/2 is an antiderivative.",
            r"The factor \(e^{-x}/(1-e^{-x})\) equals \(1/(e^{x}-1)\), so \((\log(1-e^{-x}))^{2}/2\) is an antiderivative.",
        ),
        (
            "Evaluate from log(2) to oo. The limit at oo is 0, and the value at log(2) leaves -log(2)**2/2.",
            r"Evaluate from \(\log 2\) to \(\infty\). The limit at infinity is \(0\), and the value at \(\log 2\) leaves \(-\frac{1}{2}(\log 2)^{2}\).",
        ),
    ],
    [
        ("eq", "exp(-x)/(1 - exp(-x))", "1/(exp(x) - 1)"),
        ("diff", "log(1 - exp(-x))**2/2"),
        ("ends", "log(1 - exp(-x))**2/2", "log(2)", "oo", "1", "-log(2)**2/2"),
    ],
)

_add(
    "YANG-2.3-P17",
    "x**2*log(x)**5/2 - 5*x**2*log(x)**4/4 + 5*x**2*log(x)**3/2 - 15*x**2*log(x)**2/4 + 15*x**2*log(x)/4 - 15*x**2/8",
    [
        (
            "Substitution u = log(x). Then exp(2*log(x)) equals x**2, and the integral becomes u**5*exp(2*u).",
            r"Substitution \(u=\log x\). Then \(e^{2\log x}=x^{2}\), and the integral becomes \(u^{5}e^{2u}\).",
        ),
        (
            "Five integrations by parts. The antiderivative is x**2*log(x)**5/2 - 5*x**2*log(x)**4/4 + 5*x**2*log(x)**3/2 - 15*x**2*log(x)**2/4 + 15*x**2*log(x)/4 - 15*x**2/8.",
            r"Five integrations by parts. The antiderivative is \(\frac{x^{2}(\log x)^{5}}{2}-\frac{5x^{2}(\log x)^{4}}{4}+\frac{5x^{2}(\log x)^{3}}{2}-\frac{15x^{2}(\log x)^{2}}{4}+\frac{15x^{2}\log x}{4}-\frac{15x^{2}}{8}\).",
        ),
    ],
    [
        ("eq", "exp(2*log(x))", "x**2"),
        ("diff", "x**2*log(x)**5/2 - 5*x**2*log(x)**4/4 + 5*x**2*log(x)**3/2 - 15*x**2*log(x)**2/4 + 15*x**2*log(x)/4 - 15*x**2/8"),
    ],
)

_add(
    "YANG-2.3-P18",
    "-4*sqrt(x)*sqrt(1 - sqrt(x))/15 + 4*x*sqrt(1 - sqrt(x))/5 - 8*sqrt(1 - sqrt(x))/15",
    [
        (
            "Forced substitution t = 1 - sqrt(x), after u = sqrt(x). Then 4*(1 - sqrt(x))**(5/2)/5 - 4*(1 - sqrt(x))**(3/2)/3 is an antiderivative.",
            r"Forced substitution \(t=1-\sqrt{x}\), after \(u=\sqrt{x}\). Then \(\frac{4}{5}(1-\sqrt{x})^{5/2}-\frac{4}{3}(1-\sqrt{x})^{3/2}\) is an antiderivative.",
        ),
        (
            "Factor sqrt(1 - sqrt(x)). That equals -4*sqrt(x)*sqrt(1 - sqrt(x))/15 + 4*x*sqrt(1 - sqrt(x))/5 - 8*sqrt(1 - sqrt(x))/15.",
            r"Factor \(\sqrt{1-\sqrt{x}}\). That equals \(-\frac{4\sqrt{x}\sqrt{1-\sqrt{x}}}{15}+\frac{4x\sqrt{1-\sqrt{x}}}{5}-\frac{8\sqrt{1-\sqrt{x}}}{15}\).",
        ),
    ],
    [
        ("diff", "4*(1 - sqrt(x))**(5/2)/5 - 4*(1 - sqrt(x))**(3/2)/3"),
        ("eq", "4*(1 - sqrt(x))**(5/2)/5 - 4*(1 - sqrt(x))**(3/2)/3", "-4*sqrt(x)*sqrt(1 - sqrt(x))/15 + 4*x*sqrt(1 - sqrt(x))/5 - 8*sqrt(1 - sqrt(x))/15"),
        ("diff", "-4*sqrt(x)*sqrt(1 - sqrt(x))/15 + 4*x*sqrt(1 - sqrt(x))/5 - 8*sqrt(1 - sqrt(x))/15"),
    ],
)

_add(
    "YANG-2.4-P01",
    "120",
    [
        (
            "The guide's factorial integral says the integral of x**n*exp(-x) from 0 to oo is n!. Here n = 5, and 5*4*3*2*1 equals 120.",
            r"The guide's factorial integral says \(\int_0^\infty x^{n}e^{-x}\,dx=n!\). Here \(n=5\), and \(5\cdot4\cdot3\cdot2\cdot1=120\).",
        ),
        (
            "The antiderivative -exp(-x)*(x**5 + 5*x**4 + 20*x**3 + 60*x**2 + 120*x + 120), from 0 to oo, equals 120.",
            r"The antiderivative \(-e^{-x}(x^{5}+5x^{4}+20x^{3}+60x^{2}+120x+120)\), from \(0\) to \(\infty\), equals \(120\).",
        ),
    ],
    [
        ("eq", "5*4*3*2*1", "120"),
        ("diff", "-exp(-x)*(x**5 + 5*x**4 + 20*x**3 + 60*x**2 + 120*x + 120)"),
        ("ends", "-exp(-x)*(x**5 + 5*x**4 + 20*x**3 + 60*x**2 + 120*x + 120)", "0", "oo", "1", "120"),
    ],
)

_add(
    "YANG-2.4-P02",
    "720",
    [
        (
            "Substitution x = exp(-u) sends log(x)**6 on [0, 1] to u**6*exp(-u) on [0, oo]. The factorial integral gives 6*5*4*3*2*1, which equals 720.",
            r"Substitution \(x=e^{-u}\) sends \((\log x)^{6}\) on \([0,1]\) to \(u^{6}e^{-u}\) on \([0,\infty)\). The factorial integral gives \(6!\), which equals \(720\).",
        ),
        (
            "The antiderivative x*(log(x)**6 - 6*log(x)**5 + 30*log(x)**4 - 120*log(x)**3 + 360*log(x)**2 - 720*log(x) + 720), from 0 to 1, equals 720.",
            r"The antiderivative \(x((\log x)^{6}-6(\log x)^{5}+30(\log x)^{4}-120(\log x)^{3}+360(\log x)^{2}-720\log x+720)\), from \(0\) to \(1\), equals \(720\).",
        ),
    ],
    [
        ("eq", "6*5*4*3*2*1", "720"),
        ("diff", "x*(log(x)**6 - 6*log(x)**5 + 30*log(x)**4 - 120*log(x)**3 + 360*log(x)**2 - 720*log(x) + 720)"),
        ("ends", "x*(log(x)**6 - 6*log(x)**5 + 30*log(x)**4 - 120*log(x)**3 + 360*log(x)**2 - 720*log(x) + 720)", "0", "1", "1", "720"),
    ],
)

_add(
    "YANG-2.4-P03",
    "19",
    [
        (
            "Substitution t = -x. The polynomial (-x)**4 + (-x)**3 + (-x)**2 + (-x) equals x**4 - x**3 + x**2 - x.",
            r"Substitution \(t=-x\). The polynomial \((-x)^{4}+(-x)^{3}+(-x)^{2}+(-x)\) equals \(x^{4}-x^{3}+x^{2}-x\).",
        ),
        (
            "The factorial integral gives 4*3*2*1 - 3*2*1 + 2*1 - 1, and 24 - 6 + 2 - 1 equals 19.",
            r"The factorial integral gives \(4!-3!+2!-1!\), and \(24-6+2-1=19\).",
        ),
        (
            "The antiderivative (x**4 - 3*x**3 + 10*x**2 - 19*x + 19)*exp(x), from -oo to 0, equals 19.",
            r"The antiderivative \((x^{4}-3x^{3}+10x^{2}-19x+19)e^{x}\), from \(-\infty\) to \(0\), equals \(19\).",
        ),
    ],
    [
        ("eq", "(-x)**4 + (-x)**3 + (-x)**2 + (-x)", "x**4 - x**3 + x**2 - x"),
        ("eq", "4*3*2*1 - 3*2*1 + 2*1 - 1", "19"),
        ("eq", "24 - 6 + 2 - 1", "19"),
        ("diff", "(x**4 - 3*x**3 + 10*x**2 - 19*x + 19)*exp(x)"),
        ("ends", "(x**4 - 3*x**3 + 10*x**2 - 19*x + 19)*exp(x)", "-oo", "0", "1", "19"),
    ],
)

_add(
    "YANG-2.4-P04",
    "1",
    [
        (
            "Substitution u = x**2. Then (x**2)**2 equals x**4, and x**5*exp(-x**2) dx becomes u**2*exp(-u) du/2. So 2*1/2 equals 1.",
            r"Substitution \(u=x^{2}\). Then \((x^{2})^{2}=x^{4}\), and \(x^{5}e^{-x^{2}}\,dx\) becomes \(u^{2}e^{-u}\,du/2\). So \(2!/2=1\).",
        ),
        (
            "The antiderivative -exp(-x**2)*(x**4 + 2*x**2 + 2)/2, from 0 to oo, equals 1.",
            r"The antiderivative \(-\frac{1}{2}e^{-x^{2}}(x^{4}+2x^{2}+2)\), from \(0\) to \(\infty\), equals \(1\).",
        ),
    ],
    [
        ("eq", "(x**2)**2", "x**4"),
        ("eq", "2*1/2", "1"),
        ("diff", "-exp(-x**2)*(x**4 + 2*x**2 + 2)/2"),
        ("ends", "-exp(-x**2)*(x**4 + 2*x**2 + 2)/2", "0", "oo", "1", "1"),
    ],
)

_add(
    "YANG-2.4-P05",
    "65",
    [
        (
            "Expand (x+1)**4 as x**4 + 4*x**3 + 6*x**2 + 4*x + 1. The factorial integral gives 24 + 4*6 + 6*2 + 4*1 + 1, which equals 65.",
            r"Expand \((x+1)^{4}\) as \(x^{4}+4x^{3}+6x^{2}+4x+1\). The factorial integral gives \(24+4\cdot6+6\cdot2+4\cdot1+1\), which equals \(65\).",
        ),
        (
            "The antiderivative (-x**4 - 8*x**3 - 30*x**2 - 64*x - 65)*exp(-x), from 0 to oo, equals 65.",
            r"The antiderivative \((-x^{4}-8x^{3}-30x^{2}-64x-65)e^{-x}\), from \(0\) to \(\infty\), equals \(65\).",
        ),
    ],
    [
        ("eq", "(x+1)**4", "x**4 + 4*x**3 + 6*x**2 + 4*x + 1"),
        ("eq", "24 + 4*6 + 6*2 + 4*1 + 1", "65"),
        ("diff", "(-x**4 - 8*x**3 - 30*x**2 - 64*x - 65)*exp(-x)"),
        ("ends", "(-x**4 - 8*x**3 - 30*x**2 - 64*x - 65)*exp(-x)", "0", "oo", "1", "65"),
    ],
)

_add(
    "YANG-2.4-P06",
    "4",
    [
        (
            "Forced substitution u = sqrt(x). The derivative of sqrt(x) is 1/(2*sqrt(x)), and the integrand becomes 2*u**2*exp(-u). Then 2*2 equals 4.",
            r"Forced substitution \(u=\sqrt{x}\). The derivative of \(\sqrt{x}\) is \(1/(2\sqrt{x})\), and the integrand becomes \(2u^{2}e^{-u}\). Then \(2\cdot2!=4\).",
        ),
        (
            "The antiderivative -2*exp(-sqrt(x))*(x + 2*sqrt(x) + 2), from 0 to oo, equals 4.",
            r"The antiderivative \(-2e^{-\sqrt{x}}(x+2\sqrt{x}+2)\), from \(0\) to \(\infty\), equals \(4\).",
        ),
    ],
    [
        ("diff_of", "sqrt(x)", "1/(2*sqrt(x))"),
        ("eq", "2*2", "4"),
        ("diff", "-2*exp(-sqrt(x))*(x + 2*sqrt(x) + 2)"),
        ("ends", "-2*exp(-sqrt(x))*(x + 2*sqrt(x) + 2)", "0", "oo", "1", "4"),
    ],
)

_add(
    "YANG-2.4-P07",
    "3",
    [
        (
            "Forced substitution u = x**(1/3). The derivative of x**(1/3) is 1/(3*x**(2/3)), so the integral becomes 3*u*exp(-u). Then 3*1 equals 3.",
            r"Forced substitution \(u=x^{1/3}\). The derivative of \(x^{1/3}\) is \(1/(3x^{2/3})\), so the integral becomes \(3ue^{-u}\). Then \(3\cdot1!=3\).",
        ),
        (
            "The antiderivative -3*exp(-x**(1/3))*(x**(1/3) + 1), from 0 to oo, equals 3.",
            r"The antiderivative \(-3e^{-x^{1/3}}(x^{1/3}+1)\), from \(0\) to \(\infty\), equals \(3\).",
        ),
    ],
    [
        ("diff_of", "x**(1/3)", "1/(3*x**(2/3))"),
        ("eq", "3*1", "3"),
        ("diff", "-3*exp(-x**(1/3))*(x**(1/3) + 1)"),
        ("ends", "-3*exp(-x**(1/3))*(x**(1/3) + 1)", "0", "oo", "1", "3"),
    ],
)

_add(
    "YANG-2.4-P08",
    "12",
    [
        (
            "Forced substitution u = sqrt(x). The integrand becomes 2*u**3*exp(-u), and 2*6 equals 12.",
            r"Forced substitution \(u=\sqrt{x}\). The integrand becomes \(2u^{3}e^{-u}\), and \(2\cdot3!=12\).",
        ),
        (
            "The antiderivative -2*exp(-sqrt(x))*(sqrt(x)**3 + 3*x + 6*sqrt(x) + 6), from 0 to oo, equals 12.",
            r"The antiderivative \(-2e^{-\sqrt{x}}(x^{3/2}+3x+6\sqrt{x}+6)\), from \(0\) to \(\infty\), equals \(12\).",
        ),
    ],
    [
        ("eq", "2*6", "12"),
        ("diff", "-2*exp(-sqrt(x))*(sqrt(x)**3 + 3*x + 6*sqrt(x) + 6)"),
        ("ends", "-2*exp(-sqrt(x))*(sqrt(x)**3 + 3*x + 6*sqrt(x) + 6)", "0", "oo", "1", "12"),
    ],
)

_add(
    "YANG-2.4-P09",
    "2",
    [
        (
            "Substitution u = exp(x). Then exp(3*x - exp(x))/exp(x) equals exp(2*x - exp(x)), which is u**2*exp(-u). The factorial integral gives 2*1, which equals 2.",
            r"Substitution \(u=e^{x}\). Then \(e^{3x-e^{x}}/e^{x}=e^{2x-e^{x}}\), which is \(u^{2}e^{-u}\). The factorial integral gives \(2!\), which equals \(2\).",
        ),
        (
            "The antiderivative -exp(-exp(x))*(exp(2*x) + 2*exp(x) + 2), from -oo to oo, equals 2.",
            r"The antiderivative \(-e^{-e^{x}}(e^{2x}+2e^{x}+2)\), from \(-\infty\) to \(\infty\), equals \(2\).",
        ),
    ],
    [
        ("eq", "exp(3*x - exp(x))/exp(x)", "exp(2*x - exp(x))"),
        ("eq", "2*1", "2"),
        ("diff", "-exp(-exp(x))*(exp(2*x) + 2*exp(x) + 2)"),
        ("ends", "-exp(-exp(x))*(exp(2*x) + 2*exp(x) + 2)", "-oo", "oo", "1", "2"),
    ],
)

_add(
    "YANG-2.4-P10",
    "8/81",
    [
        (
            "Substitution u = log(x) gives the integral of u**4*exp(-3*u) from 0 to oo, which is 4!/3**5. Then 24/3**5 equals 8/81.",
            r"Substitution \(u=\log x\) gives \(\int_0^\infty u^{4}e^{-3u}\,du=4!/3^{5}\). Then \(24/3^{5}=8/81\).",
        ),
        (
            "The antiderivative -log(x)**4/(3*x**3) - 4*log(x)**3/(9*x**3) - 4*log(x)**2/(9*x**3) - 8*log(x)/(27*x**3) - 8/(81*x**3), from 1 to oo, equals 8/81.",
            r"The antiderivative \(-\frac{(\log x)^{4}}{3x^{3}}-\frac{4(\log x)^{3}}{9x^{3}}-\frac{4(\log x)^{2}}{9x^{3}}-\frac{8\log x}{27x^{3}}-\frac{8}{81x^{3}}\), from \(1\) to \(\infty\), equals \(8/81\).",
        ),
    ],
    [
        ("eq", "24/3**5", "8/81"),
        ("diff", "-log(x)**4/(3*x**3) - 4*log(x)**3/(9*x**3) - 4*log(x)**2/(9*x**3) - 8*log(x)/(27*x**3) - 8/(81*x**3)"),
        ("ends", "-log(x)**4/(3*x**3) - 4*log(x)**3/(9*x**3) - 4*log(x)**2/(9*x**3) - 8*log(x)/(27*x**3) - 8/(81*x**3)", "1", "oo", "1", "8/81"),
    ],
)

_add(
    "YANG-2.4-P11",
    "120",
    [
        (
            "Substitution u = 1/x turns exp(-1/x)/x**7 into u**5*exp(-u). The factorial integral gives 5*4*3*2*1, which equals 120.",
            r"Substitution \(u=1/x\) turns \(e^{-1/x}/x^{7}\) into \(u^{5}e^{-u}\). The factorial integral gives \(5!\), which equals \(120\).",
        ),
        (
            "The antiderivative exp(-1/x)*(120 + 120/x + 60/x**2 + 20/x**3 + 5/x**4 + 1/x**5), from 0 to oo, equals 120.",
            r"The antiderivative \(e^{-1/x}(120+120/x+60/x^{2}+20/x^{3}+5/x^{4}+1/x^{5})\), from \(0\) to \(\infty\), equals \(120\).",
        ),
    ],
    [
        ("eq", "5*4*3*2*1", "120"),
        ("diff", "exp(-1/x)*(120 + 120/x + 60/x**2 + 20/x**3 + 5/x**4 + 1/x**5)"),
        ("ends", "exp(-1/x)*(120 + 120/x + 60/x**2 + 20/x**3 + 5/x**4 + 1/x**5)", "0", "oo", "1", "120"),
    ],
)

_add(
    "YANG-2.4-P12",
    "29",
    [
        (
            "Substitution u = tan(x). Then sec(x)**2 equals 1 + tan(x)**2, and (1 + tan(x)**2)**2*sec(x)**2 equals sec(x)**6.",
            r"Substitution \(u=\tan x\). Then \(\sec^{2}x=1+\tan^{2}x\), and \((1+\tan^{2}x)^{2}\sec^{2}x=\sec^{6}x\).",
        ),
        (
            "The integral becomes (1 + 2*u**2 + u**4)*exp(-u) on [0, oo]. The factorial integral gives 1 + 4 + 24, which equals 29.",
            r"The integral becomes \((1+2u^{2}+u^{4})e^{-u}\) on \([0,\infty)\). The factorial integral gives \(0!+2\cdot2!+4!=1+4+24\), which equals \(29\).",
        ),
        (
            "The antiderivative -exp(-tan(x))*(tan(x)**4 + 4*tan(x)**3 + 14*tan(x)**2 + 28*tan(x) + 29), from 0 to pi/2, equals 29.",
            r"The antiderivative \(-e^{-\tan x}(\tan^{4}x+4\tan^{3}x+14\tan^{2}x+28\tan x+29)\), from \(0\) to \(\pi/2\), equals \(29\).",
        ),
    ],
    [
        ("eq", "sec(x)**2", "1 + tan(x)**2"),
        ("eq", "(1 + tan(x)**2)**2*sec(x)**2", "sec(x)**6"),
        ("eq", "1 + 4 + 24", "29"),
        ("diff", "-exp(-tan(x))*(tan(x)**4 + 4*tan(x)**3 + 14*tan(x)**2 + 28*tan(x) + 29)"),
        ("ends", "-exp(-tan(x))*(tan(x)**4 + 4*tan(x)**3 + 14*tan(x)**2 + 28*tan(x) + 29)", "0", "pi/2", "1", "29"),
    ],
)

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


def _bad_value(value) -> bool:
    if value in (sp.nan, sp.zoo, sp.oo, -sp.oo):
        return True
    has = getattr(value, "has", None)
    if has is None:
        return False
    return bool(has(sp.nan, sp.zoo, sp.oo, -sp.oo))


def _at(primitive, symbol, bound: str, side: str):
    point = parse(bound)
    if bound in {"oo", "-oo"}:
        return sp.limit(primitive, symbol, point)
    value = primitive.subs(symbol, point)
    if not _bad_value(value):
        return value
    direction = "-" if side == "hi" else "+"
    return sp.limit(primitive, symbol, point, dir=direction)


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
        got = parse(factor) * (_at(primitive, symbol, hi, "hi") - _at(primitive, symbol, lo, "lo"))
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


def _main_core(argv: list[str]) -> int:
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


LANE_MAINS = []


# ---- folded from yang_worked_1_11.py ----
_s111_SECTIONS = frozenset({"1.11", "1.12"})

# final matches answer_sympy. lines are (plain, latex) without numbers.
_s111_SPECS: dict[str, dict] = {}


def _s111__add(ident, final, lines, steps):
    _s111_SPECS[ident] = {"final": final, "lines": lines, "steps": steps}


_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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
_s111__add(
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


def _s111_parse(text: str):
    return pack_gate._parse(text, "x")


def _s111_fold(text: str) -> str:
    return "".join(str(text).split())


def _s111_symbol():
    return pack_gate.namespace("x")["x"]


def _s111_same(left, right) -> bool:
    if pack_gate._zero(left - right):
        return True
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero((left - right).subs(_s111_symbol(), positive))


def _s111_diff_ok(antiderivative, integrand) -> bool:
    delta = sp.diff(antiderivative, _s111_symbol()) - integrand
    if pack_gate._zero(delta):
        return True
    dropped = pack_gate._drop_log_abs(antiderivative)
    if dropped != antiderivative and pack_gate._zero(sp.diff(dropped, _s111_symbol()) - integrand):
        return True
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero(delta.subs(_s111_symbol(), positive))


def _s111_must_show(token: str) -> bool:
    return any(char.isalpha() for char in token) or "**" in token or "/" in token


def _s111__ge0(value) -> bool:
    if value == sp.oo:
        return True
    if value == -sp.oo:
        return False
    simplified = sp.simplify(value)
    if simplified == 0 or simplified.is_nonnegative is True:
        return True
    return simplified >= 0


def _s111__le0(value) -> bool:
    return _s111__ge0(sp.simplify(-value))


def _s111_interval_sign(expr, lo, hi):
    expanded = sp.expand(expr)
    if expanded == 0:
        return "nonneg"
    if not expanded.is_polynomial(_s111_symbol()):
        return None
    polynomial = sp.Poly(expanded, _s111_symbol())
    degree = polynomial.degree()
    if degree is None or degree < 0 or degree > 2:
        return None
    points = [lo, hi]
    if degree == 2:
        vertex = sp.simplify(-polynomial.nth(1) / (2 * polynomial.LC()))
        if _s111__ge0(vertex - lo) and _s111__ge0(hi - vertex):
            points.append(vertex)
    values = []
    for point in points:
        if point == sp.oo:
            values.append(sp.oo if _s111__ge0(polynomial.LC()) else -sp.oo)
        elif point == -sp.oo:
            sign = sp.oo if _s111__ge0(polynomial.LC()) else -sp.oo
            values.append(sign if degree % 2 == 0 else -sign)
        else:
            values.append(sp.simplify(expanded.subs(_s111_symbol(), point)))
    if all(_s111__ge0(item) for item in values):
        return "nonneg"
    if all(_s111__le0(item) for item in values):
        return "nonpos"
    return None


def _s111_load_rows() -> list[dict]:
    return [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]


def _s111_section_rows(rows: list[dict]) -> list[dict]:
    chosen = []
    for row in rows:
        if row.get("source") != "yang_book" or row.get("kind") == "reference":
            continue
        if row.get("section") not in _s111_SECTIONS:
            continue
        if row.get("worked_solution_origin") == "pdf_copy":
            continue
        plain = row.get("worked_solution_plain")
        if plain not in (None, "") and row.get("id") not in _s111_SPECS:
            continue
        chosen.append(row)
    return chosen


def _s111_compose(row: dict, spec: dict) -> tuple[str, str]:
    plain = "\n".join(f"{index}. {text}" for index, (text, _) in enumerate(spec["lines"], 1))
    latex = "\n".join(f"{index}. {text}" for index, (_, text) in enumerate(spec["lines"], 1))
    plain += f"\nThe answer is {row['answer_sympy']}."
    latex += f"\nThe answer is \\({row['answer_latex']}\\)."
    return plain, latex


def _s111_shown_text(spec: dict) -> str:
    body = "\n".join(text for text, _ in spec["lines"])
    return body + "\n" + spec["final"]


def _s111_assert_shown(ident: str, spec: dict) -> None:
    folded = _s111_fold(_s111_shown_text(spec))
    for step in spec["steps"]:
        for token in step[1:]:
            if _s111_must_show(token) and _s111_fold(token) not in folded:
                raise AssertionError(f"{ident} prose omits {token}")


def _s111__at(primitive, point):
    if point in (sp.oo, -sp.oo):
        return sp.limit(primitive, _s111_symbol(), point)
    return primitive.subs(_s111_symbol(), point)


def _s111_run_step(ident: str, step: tuple, integrand) -> None:
    kind = step[0]
    if kind == "diff":
        if not _s111_diff_ok(_s111_parse(step[1]), integrand):
            raise AssertionError(f"{ident} derivative {step[1]}")
        return
    if kind == "diff_of":
        if not _s111_diff_ok(_s111_parse(step[1]), _s111_parse(step[2])):
            raise AssertionError(f"{ident} derivative {step[1]} vs {step[2]}")
        return
    if kind == "eq":
        if not _s111_same(_s111_parse(step[1]), _s111_parse(step[2])):
            raise AssertionError(f"{ident} equality {step[1]} vs {step[2]}")
        return
    if kind == "odd":
        expr = _s111_parse(step[1])
        if not pack_gate._zero(expr.subs(_s111_symbol(), -_s111_symbol()) + expr):
            raise AssertionError(f"{ident} odd part {step[1]}")
        return
    if kind == "ends":
        _, ant, lo, hi, factor, expected = step
        primitive = _s111_parse(ant)
        got = _s111_parse(factor) * (_s111__at(primitive, _s111_parse(hi)) - _s111__at(primitive, _s111_parse(lo)))
        if not _s111_same(sp.simplify(got), _s111_parse(expected)):
            raise AssertionError(f"{ident} endpoints {ant} on [{lo}, {hi}] gave {got}")
        return
    if kind == "sum":
        total = _s111_parse(step[-1])
        got = _s111_parse(step[1])
        for term in step[2:-1]:
            got += _s111_parse(term)
        if not _s111_same(got, total):
            raise AssertionError(f"{ident} sum {step[1:-1]}")
        return
    if kind == "abs_on":
        _, inside, form, lo, hi = step
        form_v = _s111_parse(form)
        if _s111_interval_sign(form_v, _s111_parse(lo), _s111_parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {form} is not nonnegative on [{lo}, {hi}]")
        if not (_s111_same(form_v, _s111_parse(inside)) or _s111_same(form_v, -_s111_parse(inside))):
            raise AssertionError(f"{ident} {form} is not a sign of {inside}")
        return
    if kind == "abs_prod":
        _, left, right, lo, hi = step
        if _s111_interval_sign(_s111_parse(left), _s111_parse(lo), _s111_parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {left} leaves [{lo}, {hi}]")
        if _s111_interval_sign(_s111_parse(right), _s111_parse(lo), _s111_parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} {right} leaves [{lo}, {hi}]")
        return
    if kind == "atan_pos":
        positive = sp.symbols("t", positive=True)
        delta = (_s111_parse(step[1]) - _s111_parse(step[2])).subs(_s111_symbol(), sp.atan(positive))
        if not pack_gate._zero(sp.simplify(delta)):
            raise AssertionError(f"{ident} atan branch {step[1]}")
        return
    if kind == "assume_abs":
        _, lo, hi, form = step
        expr = sp.Abs(_s111_symbol() - sp.Abs(_s111_symbol() - sp.Abs(_s111_symbol())))
        if _s111_parse(lo) >= 0:
            sample = sp.symbols("s", nonnegative=True)
        elif _s111_parse(hi) <= 0:
            sample = sp.symbols("s", negative=True)
        else:
            raise AssertionError(f"{ident} nested interval")
        got = sp.simplify(expr.subs(_s111_symbol(), sample))
        want = sp.simplify(_s111_parse(form).subs(_s111_symbol(), sample))
        if not pack_gate._zero(got - want):
            raise AssertionError(f"{ident} nested absolute value on [{lo}, {hi}] is {got}")
        return
    if kind == "replace_abs":
        _, integrand_text, inside, deriv, reduced, lo, hi = step
        if not _s111_diff_ok(_s111_parse(inside), _s111_parse(deriv)):
            raise AssertionError(f"{ident} slope of {inside}")
        numerator, denominator = sp.fraction(sp.together(_s111_parse(deriv)))
        if _s111_interval_sign(numerator, _s111_parse(lo), _s111_parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} numerator sign")
        if _s111_interval_sign(denominator, _s111_parse(lo), _s111_parse(hi)) != "nonneg":
            raise AssertionError(f"{ident} denominator sign")
        if not _s111__ge0(sp.simplify(_s111_parse(inside).subs(_s111_symbol(), _s111_parse(lo)))):
            raise AssertionError(f"{ident} value at {lo}")
        replaced = _s111_parse(integrand_text).subs(sp.Abs(_s111_parse(inside)), _s111_parse(inside))
        if not _s111_same(replaced, _s111_parse(reduced)):
            raise AssertionError(f"{ident} cleared absolute value")
        return
    if kind == "exp_parts":
        _s111__exp_parts(ident, step[1], step[2])
        return
    if kind == "shift":
        _s111__shift(ident, step[1])
        return
    if kind == "sine_pull":
        _s111__sine_pull(ident, step[1])
        return
    if kind == "hyperbolic":
        _s111__hyperbolic(ident, step[1])
        return
    raise AssertionError(f"{ident} unknown step {kind}")


def _s111__exp_parts(ident: str, right_text: str, left_text: str) -> None:
    step = sp.Dummy("s", real=True)
    height = sp.symbols("h", nonnegative=True)
    rise = sp.integrate(sp.exp(step), (step, 0, height))
    if not pack_gate._zero(rise - (sp.exp(height) - 1)) or sp.exp(step).is_positive is not True:
        raise AssertionError(f"{ident} exponential rise")
    primitive = sp.exp(_s111_symbol()) - _s111_symbol()
    if not pack_gate._zero(sp.diff(primitive, _s111_symbol()) - (sp.exp(_s111_symbol()) - 1)):
        raise AssertionError(f"{ident} right derivative")
    right = sp.simplify(primitive.subs(_s111_symbol(), 1) - primitive.subs(_s111_symbol(), 0))
    if not _s111_same(right, _s111_parse(right_text)):
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
    if not _s111_same(left, _s111_parse(left_text)):
        raise AssertionError(f"{ident} left value {left}")


def _s111__shift(ident: str, index_text: str) -> None:
    index = _s111_parse(index_text)
    angle = sp.Dummy("t", real=True)
    sign = sp.Integer(-1) ** index
    if not pack_gate._zero(sp.sin(index * sp.pi + angle) - sign * sp.sin(angle)):
        raise AssertionError(f"{ident} angle addition {index_text}")
    if sp.calculus.util.minimum(sp.sin(angle), angle, sp.Interval(0, sp.pi)) != 0:
        raise AssertionError(f"{ident} sine minimum")
    nonnegative = sp.Dummy("s", nonnegative=True)
    if sp.Abs(sign * nonnegative) != nonnegative:
        raise AssertionError(f"{ident} absolute sign")
    primitive = -sign * sp.cos(_s111_symbol())
    integrand = sign * sp.sin(_s111_symbol())
    if not pack_gate._zero(sp.diff(primitive, _s111_symbol()) - integrand):
        raise AssertionError(f"{ident} signed sine")
    value = sp.simplify(
        primitive.subs(_s111_symbol(), (index + 1) * sp.pi) - primitive.subs(_s111_symbol(), index * sp.pi)
    )
    if value != 2:
        raise AssertionError(f"{ident} period {index_text} gave {value}")


def _s111__sine_pull(ident: str, target: str) -> None:
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
    if not _s111_same(_s111_parse(target), _s111_parse("cos(x)/(1 + cos(x))")):
        raise AssertionError(f"{ident} sine target")


def _s111__hyperbolic(ident: str, expected: str) -> None:
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
    if not _s111_same(wanted, _s111_parse(expected)):
        raise AssertionError(f"{ident} outer expression")


def _s111_closes(spec: dict, kind: str) -> bool:
    final = _s111_fold(spec["final"])
    if kind == "indefinite":
        return any(step[0] == "diff" and _s111_fold(step[1]) == final for step in spec["steps"])
    return any(step[0] in {"ends", "sum", "eq"} and _s111_fold(step[-1]) == final for step in spec["steps"])


def _s111_check_steps(row: dict, spec: dict) -> None:
    ident = row["id"]
    if _s111_fold(spec["final"]) != _s111_fold(row["answer_sympy"]):
        raise AssertionError(f"DISAGREE {ident}: stored {row['answer_sympy']} vs final {spec['final']}")
    integrand = _s111_parse(row["sympy_expr"])
    if not _s111_closes(spec, row["kind"]):
        raise AssertionError(f"{ident} final is not checked against the stored answer")
    for step in spec["steps"]:
        _s111_run_step(ident, step, integrand)
    _s111_assert_shown(ident, spec)
    if not _s111_same(_s111_parse(spec["final"]), _s111_parse(row["answer_sympy"])):
        raise AssertionError(f"DISAGREE {ident}: simplified final does not match answer_sympy")


def _s111_check_prose(row: dict, spec: dict) -> None:
    plain, latex = _s111_compose(row, spec)
    if row.get("worked_solution_plain") != plain:
        raise AssertionError(f"{row['id']} plain text drifted")
    if row.get("worked_solution_latex") != latex:
        raise AssertionError(f"{row['id']} latex drifted")
    if row.get("worked_solution_origin") != "missing":
        raise AssertionError(f"{row['id']} origin changed")


def _s111_reject_wrong_derivative() -> None:
    integrand = _s111_parse("x/(x**4 + 1)")
    if _s111_diff_ok(_s111_parse("atan(x**2)"), integrand):
        raise AssertionError("wrong antiderivative was accepted")
    if not _s111_diff_ok(_s111_parse("atan(x**2)/2"), integrand):
        raise AssertionError("stored antiderivative was rejected")


def _s111_write_rows(rows: list[dict]) -> None:
    by_id = {row["id"]: row for row in rows}
    for ident, spec in _s111_SPECS.items():
        row = by_id[ident]
        plain, latex = _s111_compose(row, spec)
        row["worked_solution_plain"] = plain
        row["worked_solution_latex"] = latex
    body = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    RECORDS.write_text(body, encoding="utf-8")


def _s111_main(argv: list[str]) -> int:
    _s111_reject_wrong_derivative()
    rows = _s111_load_rows()
    chosen = _s111_section_rows(rows)
    ids = [row["id"] for row in chosen]
    if ids != list(_s111_SPECS):
        missing = [ident for ident in ids if ident not in _s111_SPECS]
        extra = [ident for ident in _s111_SPECS if ident not in ids]
        print(f"FAIL section rows missing={missing} extra={extra}", file=sys.stderr)
        return 1
    try:
        for row in chosen:
            _s111_check_steps(row, _s111_SPECS[row["id"]])
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    if "--write" in argv:
        _s111_write_rows(rows)
        print(f"WROTE {len(chosen)}")
        return 0
    try:
        for row in chosen:
            _s111_check_prose(row, _s111_SPECS[row["id"]])
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(f"PASS {len(chosen)} yang worked solutions")
    return 0


LANE_MAINS.append(_s111_main)


def main(argv: list[str]) -> int:
    status = _main_core(argv)
    for lane_main in LANE_MAINS:
        status = lane_main(argv) or status
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
