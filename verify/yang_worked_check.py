#!/usr/bin/env python3
"""Exact step checks for Yang worked solutions in sections 1.1, 1.2, and 1.3.

Differentiation uses the same zero test as verify/pack_gate.py. Definite steps
check each algebraic identity and the endpoint value. A wrong antiderivative
must fail. Run from the repository root:

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
SECTIONS = frozenset({"1.1", "1.2", "1.3"})

# final is the stored answer_sympy. lines are (plain, latex) without numbers.
# steps are ("diff", antiderivative), ("diff_of", antiderivative, piece),
# ("eq", left, right), ("odd", expression), or
# ("ends", antiderivative, lo, hi, factor, expected).
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


def parse(text: str):
    return pack_gate._parse(text, "x")


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
    delta = sp.diff(antiderivative, symbol) - integrand
    if pack_gate._zero(delta):
        return True
    dropped = pack_gate._drop_log_abs(antiderivative)
    if dropped != antiderivative and pack_gate._zero(sp.diff(dropped, symbol) - integrand):
        return True
    positive = sp.Symbol("x", positive=True)
    return pack_gate._zero(delta.subs(symbol, positive))


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
    raise AssertionError(f"{ident} unknown step {kind}")


def check_steps(row: dict, spec: dict) -> None:
    ident = row["id"]
    if fold(spec["final"]) != fold(row["answer_sympy"]):
        raise AssertionError(
            f"DISAGREE {ident}: stored {row['answer_sympy']} vs final {spec['final']}"
        )
    integrand = parse(row["sympy_expr"])
    if row["kind"] == "indefinite":
        matched = any(
            step[0] == "diff" and fold(step[1]) == fold(spec["final"]) for step in spec["steps"]
        )
        if not matched:
            raise AssertionError(f"{ident} final is not a differentiated antiderivative")
    elif row["kind"] == "definite":
        matched = any(
            step[0] == "ends" and fold(step[-1]) == fold(spec["final"]) for step in spec["steps"]
        )
        if not matched:
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
    integrand = parse("5*x**2 - 8*x + 5")
    if diff_ok(parse("5*x**3/3 - 4*x**2"), integrand):
        raise AssertionError("wrong antiderivative was accepted")
    if not diff_ok(parse("5*x**3/3 - 4*x**2 + 5*x"), integrand):
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
