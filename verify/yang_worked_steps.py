#!/usr/bin/env python3
"""Re-check worked steps for Yang sections 1.4 and 1.5.

Each indefinite antiderivative is differentiated and simplified to its stated
piece. Each definite ray is evaluated with limits, including infinity, and the
values must add to the stored answer. Numeric agreement is not used.

    python3 verify/yang_worked_steps.py
    python3 verify/yang_worked_steps.py --write
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
SECTIONS = frozenset({"1.4", "1.5"})
ANSWER = "@@ANSWER@@"


def _steps(plain_steps, latex_steps, **rest):
    plain = "\n".join(f"{index}. {text}" for index, text in enumerate(plain_steps, 1))
    latex = "\n".join(f"{index}. {text}" for index, text in enumerate(latex_steps, 1))
    rest["plain"] = plain + "\nThe answer is " + ANSWER + "."
    rest["latex"] = latex + "\nThe answer is \\(" + ANSWER + "\\)."
    rest.setdefault("equations", ())
    rest.setdefault("parts", ())
    rest.setdefault("rays", ())
    rest.setdefault("derivatives", ())
    rest.setdefault("ends", ())
    return rest


def _indefinite(answer, integrand, plain_steps, latex_steps, equations=()):
    return _steps(
        plain_steps,
        latex_steps,
        kind="indefinite",
        equations=tuple(equations),
        parts=((answer, integrand),),
        final=answer,
    )


SOLUTIONS = {
    "YANG-1.4-P01": _indefinite(
        "log(exp(x) + 2024)",
        "exp(x)/(exp(x) + 2024)",
        [
            "Substitution. In exp(x)/(exp(x) + 2024), the factor exp(x) is the derivative of exp(x) + 2024.",
            "The integral is the logarithm of that inside.",
        ],
        [
            r"Substitution. In \(e^{x}/(e^{x}+2024)\), the factor \(e^{x}\) is the derivative of \(e^{x}+2024\).",
            r"The integral is \(\log(e^{x}+2024)\).",
        ],
    ),
    "YANG-1.4-P02": _indefinite(
        "-1/(exp(x) + 1)",
        "exp(x)/(exp(x) + 1)**2",
        [
            "Substitution u = exp(x) + 1. Then du = exp(x) dx, and exp(x)/(exp(x) + 1)**2 becomes u**(-2).",
            "Integrate the power. The antiderivative is -1/u.",
        ],
        [
            r"Substitution \(u=e^{x}+1\). Then \(du=e^{x}\,dx\), and the integrand becomes \(u^{-2}\).",
            r"The antiderivative is \(-1/u\).",
        ],
    ),
    "YANG-1.4-P03": _steps(
        [
            "Split the quotient. (2**x + 3**x)/5**x = (2/5)**x + (3/5)**x.",
            "Write the powers as exponentials. (2/5)**x = exp(x*log(2/5)) and (3/5)**x = exp(x*log(3/5)).",
            "The antiderivative of exp(x*log(2/5)) is exp(x*log(2/5))/log(2/5). The limit at oo is 0 and the value at 0 is 1/log(2/5), so the ray equals -1/log(2/5).",
            "The antiderivative of exp(x*log(3/5)) is exp(x*log(3/5))/log(3/5). The same evaluation gives -1/log(3/5).",
        ],
        [
            r"Split the quotient into \((2/5)^{x}+(3/5)^{x}\).",
            r"Write \((2/5)^{x}=\exp(x\log(2/5))\) and \((3/5)^{x}=\exp(x\log(3/5))\).",
            r"Each ray \(\int_0^\infty e^{cx}\,dx\) with \(c<0\) equals \(-1/c\).",
        ],
        kind="definite",
        equations=(
            ("(2**x + 3**x)/5**x", "(2/5)**x + (3/5)**x"),
            ("(2/5)**x", "exp(x*log(2/5))"),
            ("(3/5)**x", "exp(x*log(3/5))"),
        ),
        rays=(
            ("exp(x*log(2/5))/log(2/5)", "exp(x*log(2/5))", "0", "oo", "-1/log(2/5)"),
            ("exp(x*log(3/5))/log(3/5)", "exp(x*log(3/5))", "0", "oo", "-1/log(3/5)"),
        ),
        final="1/(-log(2) + log(5)) + 1/(-log(3) + log(5))",
    ),
    "YANG-1.4-P04": _steps(
        [
            "Split the fraction. 1/(exp(x) + 1) = 1 - exp(x)/(exp(x) + 1).",
            "The first term integrates to x. The second is a logarithm, with antiderivative log(exp(x) + 1), so the signed term is -log(exp(x) + 1).",
        ],
        [
            r"Split \(1/(e^{x}+1)=1-e^{x}/(e^{x}+1)\).",
            r"Integrate term by term.",
        ],
        kind="indefinite",
        equations=(("1/(exp(x) + 1)", "1 - exp(x)/(exp(x) + 1)"),),
        parts=(
            ("x", "1"),
            ("-log(exp(x) + 1)", "-exp(x)/(exp(x) + 1)"),
        ),
        final="x - log(exp(x) + 1)",
    ),
    "YANG-1.4-P05": _indefinite(
        "log(x + exp(x) + 1)",
        "(exp(x) + 1)/(x + exp(x) + 1)",
        [
            "The numerator of (exp(x) + 1)/(x + exp(x) + 1) is the derivative of the denominator.",
            "The integral is the logarithm of the denominator.",
        ],
        [
            r"The numerator of \((e^{x}+1)/(x+e^{x}+1)\) is the derivative of the denominator.",
            r"The integral is the logarithm of the denominator.",
        ],
    ),
    "YANG-1.4-P06": _steps(
        [
            "Expand the power. (exp(x) + exp(-x))**4 = exp(4*x) + 4*exp(2*x) + 6 + 4*exp(-2*x) + exp(-4*x).",
            "Integrate term by term.",
        ],
        [
            r"Expand \((e^{x}+e^{-x})^{4}\).",
            r"Integrate each exponential.",
        ],
        kind="indefinite",
        equations=(
            (
                "(exp(x) + exp(-x))**4",
                "exp(4*x) + 4*exp(2*x) + 6 + 4*exp(-2*x) + exp(-4*x)",
            ),
        ),
        parts=(
            (
                "6*x + exp(4*x)/4 + 2*exp(2*x) - 2*exp(-2*x) - exp(-4*x)/4",
                "exp(4*x) + 4*exp(2*x) + 6 + 4*exp(-2*x) + exp(-4*x)",
            ),
        ),
        final="6*x + exp(4*x)/4 + 2*exp(2*x) - 2*exp(-2*x) - exp(-4*x)/4",
    ),
    "YANG-1.4-P07": _steps(
        [
            "Combine the bases. 2**(x - 1)*exp(x + 1) = (E/2)*exp(x*(1 + log(2))).",
            "Divide by the constant in the exponent. The antiderivative is (E/2)*exp(x*(1 + log(2)))/(1 + log(2)).",
        ],
        [
            r"Combine the bases into one exponential, \((e/2)\exp(x(1+\log 2))\).",
            r"Divide by the constant in the exponent.",
        ],
        kind="indefinite",
        equations=(("2**(x - 1)*exp(x + 1)", "(E/2)*exp(x*(1 + log(2)))"),),
        parts=(
            (
                "(E/2)*exp(x*(1 + log(2)))/(1 + log(2))",
                "(E/2)*exp(x*(1 + log(2)))",
            ),
        ),
        final="2**x*E*exp(x)/(2*log(2) + 2)",
    ),
    "YANG-1.4-P08": _indefinite(
        "-cos(exp(x))",
        "exp(x)*sin(exp(x))",
        [
            "Substitution u = exp(x). Then du = exp(x) dx, and exp(x)*sin(exp(x)) becomes sin(u).",
            "The antiderivative is -cos(u).",
        ],
        [
            r"Substitution \(u=e^{x}\). Then \(du=e^{x}\,dx\).",
            r"The antiderivative is \(-\cos u\).",
        ],
    ),
    "YANG-1.4-P09": _steps(
        [
            "Cancel the common factor exp(3*x) + 1. (exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x)) = exp(2*x).",
            "Integrate the remaining exponential.",
        ],
        [
            r"Cancel \(e^{3x}+1\). The quotient is \(e^{2x}\).",
            r"Integrate that exponential.",
        ],
        kind="indefinite",
        equations=(("(exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x))", "exp(2*x)"),),
        parts=(("exp(2*x)/2", "exp(2*x)"),),
        final="exp(2*x)/2",
    ),
    "YANG-1.4-P10": _indefinite(
        "asin(exp(x))",
        "exp(x)/sqrt(1 - exp(2*x))",
        [
            "Substitution u = exp(x). Then exp(x)/sqrt(1 - exp(2*x)) becomes 1/sqrt(1 - u**2).",
            "The antiderivative is asin(u).",
        ],
        [
            r"Substitution \(u=e^{x}\). The integrand becomes \(1/\sqrt{1-u^{2}}\).",
            r"The antiderivative is \(\operatorname{asin}(u)\).",
        ],
    ),
    "YANG-1.4-P11": _steps(
        [
            "Split the integrand. (exp(2*x) + exp(x))/(exp(2*x) + 1) = exp(2*x)/(exp(2*x) + 1) + exp(x)/(exp(2*x) + 1).",
            "The first term has antiderivative log(exp(2*x) + 1)/2.",
            "Substitution u = exp(x) turns the second term into 1/(u**2 + 1), with antiderivative atan(exp(x)).",
        ],
        [
            r"Split the integrand into \(e^{2x}/(e^{2x}+1)\) and \(e^{x}/(e^{2x}+1)\).",
            r"The first antiderivative is \(\log(e^{2x}+1)/2\).",
            r"Substitution \(u=e^{x}\) integrates the second term to \(\operatorname{atan}(e^{x})\).",
        ],
        kind="indefinite",
        equations=(
            (
                "(exp(2*x) + exp(x))/(exp(2*x) + 1)",
                "exp(2*x)/(exp(2*x) + 1) + exp(x)/(exp(2*x) + 1)",
            ),
        ),
        parts=(
            ("log(exp(2*x) + 1)/2", "exp(2*x)/(exp(2*x) + 1)"),
            ("atan(exp(x))", "exp(x)/(exp(2*x) + 1)"),
        ),
        final="log(exp(2*x) + 1)/2 + atan(exp(x))",
    ),
    "YANG-1.4-P12": _steps(
        [
            "Expand the product. (1 + exp(-x))*(exp(x) + 1) = exp(x) + 2 + exp(-x).",
            "Integrate term by term.",
        ],
        [
            r"Expand \((1+e^{-x})(e^{x}+1)\).",
            r"Integrate term by term.",
        ],
        kind="indefinite",
        equations=(("(1 + exp(-x))*(exp(x) + 1)", "exp(x) + 2 + exp(-x)"),),
        parts=(("2*x + exp(x) - exp(-x)", "exp(x) + 2 + exp(-x)"),),
        final="2*x + exp(x) - exp(-x)",
    ),
    "YANG-1.4-P13": _steps(
        [
            "Clear the negative power. 1/(exp(x) + exp(-x)) = exp(x)/(exp(2*x) + 1).",
            "Substitution u = exp(x) produces 1/(u**2 + 1), with antiderivative atan(exp(x)).",
        ],
        [
            r"Multiply numerator and denominator by \(e^{x}\).",
            r"Substitution \(u=e^{x}\) produces \(\operatorname{atan}(u)\).",
        ],
        kind="indefinite",
        equations=(("1/(exp(x) + exp(-x))", "exp(x)/(exp(2*x) + 1)"),),
        parts=(("atan(exp(x))", "exp(x)/(exp(2*x) + 1)"),),
        final="atan(exp(x))",
    ),
    "YANG-1.4-P14": _indefinite(
        "log(log(exp(x) - 1))",
        "exp(x)/((exp(x) - 1)*log(exp(x) - 1))",
        [
            "Substitution u = log(exp(x) - 1). Then du = exp(x)/((exp(x) - 1)) dx, and exp(x)/((exp(x) - 1)*log(exp(x) - 1)) becomes 1/u.",
            "The antiderivative is log(u).",
        ],
        [
            r"Substitution \(u=\log(e^{x}-1)\).",
            r"The integrand becomes \(1/u\).",
        ],
    ),
    "YANG-1.4-P15": _indefinite(
        "tan(exp(2*x))/2",
        "exp(2*x)/cos(exp(2*x))**2",
        [
            "Substitution u = exp(2*x). Then du = 2*exp(2*x) dx, and exp(2*x)/cos(exp(2*x))**2 becomes sec(u)**2 / 2.",
            "The antiderivative is tan(u)/2.",
        ],
        [
            r"Substitution \(u=e^{2x}\). Then \(du=2e^{2x}\,dx\).",
            r"The integrand becomes \(\sec^{2}(u)/2\).",
        ],
    ),
    "YANG-1.4-P16": _indefinite(
        "exp(x)*exp(exp(x))",
        "(exp(2*x) + exp(x))*exp(exp(x))",
        [
            "The integrand (exp(2*x) + exp(x))*exp(exp(x)) is the derivative of exp(x)*exp(exp(x)).",
            "The product rule on exp(x)*exp(exp(x)) produces the front factor's derivative exp(2*x) and the chain-rule factor exp(x).",
        ],
        [
            r"The integrand is the derivative of \(e^{x}e^{e^{x}}\).",
            r"The product rule supplies both \(e^{x}\) and \(e^{2x}\).",
        ],
    ),
    "YANG-1.4-P17": _steps(
        [
            "Simplify the printed root. sqrt(exp(x)*sqrt(exp(x))) = exp(3*x/4).",
            "The catalog integrand is that power. Divide by the exponent 3/4.",
        ],
        [
            r"The printed root is \(e^{3x/4}\).",
            r"Divide by the exponent.",
        ],
        kind="indefinite",
        equations=(("sqrt(exp(x)*sqrt(exp(x)))", "exp(3*x/4)"),),
        parts=(("4*exp(3*x/4)/3", "exp(3*x/4)"),),
        final="4*exp(3*x/4)/3",
    ),
    "YANG-1.4-P18": _steps(
        [
            "Substitution t = exp(-x). The derivative of exp(-x) is -exp(-x). At 0 the value is 1, and the limit at oo is 0.",
            "Substitute into the integrand. (sqrt(1 - exp(-x)) + 1)*exp(-x) = -(1 + sqrt(1 - exp(-x)))*(-exp(-x)).",
            "The integral is therefore the integral of -(1 + sqrt(1 - t)) from 1 to 0. An antiderivative is -t + (2/3)*(1 - t)**(3/2), and the evaluated difference is 5/3.",
        ],
        [
            r"Substitution \(t=e^{-x}\). Then \(dt=-e^{-x}\,dx\), with \(t(0)=1\) and \(t(\infty)=0\).",
            r"The integrand becomes \(-(1+\sqrt{1-t})\,dt\).",
            r"Evaluate \(-t+(2/3)(1-t)^{3/2}\) from 1 to 0.",
        ],
        kind="definite",
        equations=(
            (
                "(sqrt(1 - exp(-x)) + 1)*exp(-x)",
                "-(1 + sqrt(1 - exp(-x)))*(-exp(-x))",
            ),
        ),
        derivatives=(("exp(-x)", "-exp(-x)"),),
        ends=(("exp(-x)", "0", "1"), ("exp(-x)", "oo", "0")),
        rays=(("-t + (2/3)*(1 - t)**(3/2)", "-(1 + sqrt(1 - t))", "1", "0", "5/3"),),
        final="5/3",
    ),
    "YANG-1.5-P01": _steps(
        [
            "Split the quotient. (sin(x) + cos(x))/cos(x) = tan(x) + 1.",
            "The antiderivative of tan(x) is -log(cos(x)), and the constant 1 contributes x.",
        ],
        [
            r"Split the quotient into \(\tan x+1\).",
            r"Integrate each term.",
        ],
        kind="indefinite",
        equations=(("(sin(x) + cos(x))/cos(x)", "tan(x) + 1"),),
        parts=(("x - log(cos(x))", "tan(x) + 1"),),
        final="x - log(cos(x))",
    ),
    "YANG-1.5-P02": _indefinite(
        "sin(x)**3/3",
        "sin(x)**2*cos(x)",
        [
            "Substitution u = sin(x). Then du = cos(x) dx, and sin(x)**2*cos(x) becomes u**2.",
            "The antiderivative is u**3/3.",
        ],
        [
            r"Substitution \(u=\sin x\).",
            r"The antiderivative is \(u^{3}/3\).",
        ],
    ),
    "YANG-1.5-P03": _steps(
        [
            "Save one cosine and write the rest in sin. sin(x)**2*cos(x)**3 = sin(x)**2*(1 - sin(x)**2)*cos(x).",
            "Substitution u = sin(x) integrates u**2 - u**4.",
        ],
        [
            r"Write \(\cos^{2}x=1-\sin^{2}x\) and keep one factor of \(\cos x\).",
            r"Substitution \(u=\sin x\).",
        ],
        kind="indefinite",
        equations=(("sin(x)**2*cos(x)**3", "sin(x)**2*(1 - sin(x)**2)*cos(x)"),),
        parts=(("-sin(x)**5/5 + sin(x)**3/3", "sin(x)**2*(1 - sin(x)**2)*cos(x)"),),
        final="-sin(x)**5/5 + sin(x)**3/3",
    ),
    "YANG-1.5-P04": _indefinite(
        "tan(x)**3/3",
        "tan(x)**2*sec(x)**2",
        [
            "Substitution u = tan(x). Then du = sec(x)**2 dx, and tan(x)**2*sec(x)**2 becomes u**2.",
            "The antiderivative is u**3/3.",
        ],
        [
            r"Substitution \(u=\tan x\).",
            r"The antiderivative is \(u^{3}/3\).",
        ],
    ),
    "YANG-1.5-P05": _indefinite(
        "sec(x)**3/3",
        "tan(x)*sec(x)**3",
        [
            "Substitution u = sec(x). Then du = sec(x)*tan(x) dx, and tan(x)*sec(x)**3 becomes u**2.",
            "The antiderivative is u**3/3.",
        ],
        [
            r"Substitution \(u=\sec x\).",
            r"The antiderivative is \(u^{3}/3\).",
        ],
    ),
    "YANG-1.5-P06": _steps(
        [
            "Pythagorean rewrite. tan(x)**2 = sec(x)**2 - 1.",
            "Integrate. sec(x)**2 gives tan(x), and -1 gives -x.",
        ],
        [
            r"Write \(\tan^{2}x=\sec^{2}x-1\).",
            r"Integrate each term.",
        ],
        kind="indefinite",
        equations=(("tan(x)**2", "sec(x)**2 - 1"),),
        parts=(("-x + tan(x)", "sec(x)**2 - 1"),),
        final="-x + tan(x)",
    ),
    "YANG-1.5-P07": _indefinite(
        "atan(sin(x))",
        "cos(x)/(sin(x)**2 + 1)",
        [
            "Substitution u = sin(x). Then cos(x)/(sin(x)**2 + 1) becomes 1/(u**2 + 1).",
            "The antiderivative is atan(u).",
        ],
        [
            r"Substitution \(u=\sin x\).",
            r"The antiderivative is \(\operatorname{atan}(u)\).",
        ],
    ),
    "YANG-1.5-P08": _indefinite(
        "-log(csc(x) + 1)",
        "cot(x)*csc(x)/(csc(x) + 1)",
        [
            "Substitution u = csc(x). Then du = -cot(x)*csc(x) dx, and cot(x)*csc(x)/(csc(x) + 1) becomes -1/(u + 1) after the sign.",
            "The antiderivative is -log(u + 1).",
        ],
        [
            r"Substitution \(u=\csc x\). Then \(du=-\csc x\cot x\,dx\).",
            r"The antiderivative is \(-\log(u+1)\).",
        ],
    ),
    "YANG-1.5-P09": _indefinite(
        "-log(sin(x) + cos(x))",
        "(sin(x) - cos(x))/(sin(x) + cos(x))",
        [
            "The numerator of (sin(x) - cos(x))/(sin(x) + cos(x)) is the negative of the derivative of the denominator.",
            "The integral is the negative logarithm of the denominator.",
        ],
        [
            r"The numerator is the negative derivative of \(\sin x+\cos x\).",
            r"The integral is the negative logarithm.",
        ],
    ),
    "YANG-1.5-P10": _steps(
        [
            "Save one sine. sin(x)**3 = sin(x)*(1 - cos(x)**2).",
            "Substitution u = cos(x) integrates -(1 - u**2).",
        ],
        [
            r"Write \(\sin^{2}x=1-\cos^{2}x\) and keep one factor of \(\sin x\).",
            r"Substitution \(u=\cos x\).",
        ],
        kind="indefinite",
        equations=(("sin(x)**3", "sin(x)*(1 - cos(x)**2)"),),
        parts=(("cos(x)**3/3 - cos(x)", "sin(x)*(1 - cos(x)**2)"),),
        final="cos(x)**3/3 - cos(x)",
    ),
    "YANG-1.5-P11": _steps(
        [
            "Simplify the quotient. (tan(x) + cot(x))/(sin(x)*cos(x)) = sec(x)**2 + csc(x)**2.",
            "Those two terms are the derivatives of tan(x) and -cot(x).",
        ],
        [
            r"The quotient equals \(\sec^{2}x+\csc^{2}x\).",
            r"Integrate each square.",
        ],
        kind="indefinite",
        equations=(("(tan(x) + cot(x))/(sin(x)*cos(x))", "sec(x)**2 + csc(x)**2"),),
        parts=(("tan(x) - cot(x)", "sec(x)**2 + csc(x)**2"),),
        final="tan(x) - cot(x)",
    ),
    "YANG-1.5-P12": _steps(
        [
            "Expand and use the double angle. (sin(x) + cos(x))**2 = 1 + sin(2*x).",
            "Integrate. The sine term contributes -cos(2*x)/2.",
        ],
        [
            r"Expand and use \(\sin(2x)=2\sin x\cos x\).",
            r"Integrate \(1+\sin(2x)\).",
        ],
        kind="indefinite",
        equations=(("(sin(x) + cos(x))**2", "1 + sin(2*x)"),),
        parts=(("x - cos(2*x)/2", "1 + sin(2*x)"),),
        final="x - cos(2*x)/2",
    ),
    "YANG-1.5-P13": _steps(
        [
            "Expand and replace tan(x)**2. (tan(x) + sec(x))**2 = 2*sec(x)**2 + 2*sec(x)*tan(x) - 1.",
            "Integrate. The new terms are derivatives of tan(x) and sec(x).",
        ],
        [
            r"Expand and replace \(\tan^{2}x\) by \(\sec^{2}x-1\).",
            r"Integrate term by term.",
        ],
        kind="indefinite",
        equations=(("(tan(x) + sec(x))**2", "2*sec(x)**2 + 2*sec(x)*tan(x) - 1"),),
        parts=(("-x + 2*tan(x) + 2*sec(x)", "2*sec(x)**2 + 2*sec(x)*tan(x) - 1"),),
        final="-x + 2*tan(x) + 2*sec(x)",
    ),
    "YANG-1.5-P14": _steps(
        [
            "Expand the product. (sin(x) + 1)*(cos(x) + 1) = sin(x)*cos(x) + sin(x) + cos(x) + 1.",
            "Integrate. sin(x)*cos(x) gives sin(x)**2/2.",
        ],
        [
            r"Expand the product.",
            r"Integrate \(\sin x\cos x\) by substituting \(u=\sin x\).",
        ],
        kind="indefinite",
        equations=(("(sin(x) + 1)*(cos(x) + 1)", "sin(x)*cos(x) + sin(x) + cos(x) + 1"),),
        parts=(("x + sin(x)**2/2 + sin(x) - cos(x)", "sin(x)*cos(x) + sin(x) + cos(x) + 1"),),
        final="x + sin(x)**2/2 + sin(x) - cos(x)",
    ),
    "YANG-1.5-P15": _indefinite(
        "tan(tan(x))",
        "sec(x)**2*sec(tan(x))**2",
        [
            "Substitution u = tan(x). Then du = sec(x)**2 dx, and sec(x)**2*sec(tan(x))**2 becomes sec(u)**2.",
            "The antiderivative is tan(u).",
        ],
        [
            r"Substitution \(u=\tan x\).",
            r"The antiderivative is \(\tan u\).",
        ],
    ),
    "YANG-1.5-P16": _steps(
        [
            "Rationalize by the conjugate. 1/(tan(x) + sec(x)) = sec(x) - tan(x), because sec(x)**2 - tan(x)**2 = 1.",
            "The antiderivative of sec(x) - tan(x) is log(sin(x) + 1).",
        ],
        [
            r"Multiply by \(\sec x-\tan x\). The denominator becomes 1.",
            r"Integrate \(\sec x-\tan x\).",
        ],
        kind="indefinite",
        equations=(("1/(tan(x) + sec(x))", "sec(x) - tan(x)"),),
        parts=(("log(sin(x) + 1)", "sec(x) - tan(x)"),),
        final="log(sin(x) + 1)",
    ),
    "YANG-1.5-P17": _steps(
        [
            "Cancel the secant. (tan(x) + 1)/sec(x) = sin(x) + cos(x).",
            "Integrate the sum.",
        ],
        [
            r"Multiply through by \(\cos x\).",
            r"Integrate \(\sin x+\cos x\).",
        ],
        kind="indefinite",
        equations=(("(tan(x) + 1)/sec(x)", "sin(x) + cos(x)"),),
        parts=(("sin(x) - cos(x)", "sin(x) + cos(x)"),),
        final="sin(x) - cos(x)",
    ),
    "YANG-1.5-P18": _steps(
        [
            "Expand the product. (sin(x) + 1)*(sec(x)**2 + 1) = 1 + sin(x) + sec(x)**2 + sec(x)*tan(x).",
            "Each term is a derivative. sin(x)*sec(x)**2 equals sec(x)*tan(x).",
        ],
        [
            r"Expand, then replace \(\sin x\sec^{2}x\) by \(\sec x\tan x\).",
            r"Integrate term by term.",
        ],
        kind="indefinite",
        equations=(
            (
                "(sin(x) + 1)*(sec(x)**2 + 1)",
                "1 + sin(x) + sec(x)**2 + sec(x)*tan(x)",
            ),
        ),
        parts=(("x - cos(x) + tan(x) + sec(x)", "1 + sin(x) + sec(x)**2 + sec(x)*tan(x)"),),
        final="x - cos(x) + tan(x) + sec(x)",
    ),
    "YANG-1.5-P19": _steps(
        [
            "The numerator is a difference of squares. (-csc(x) + sec(x))*(csc(x) + sec(x))/(tan(x) + cot(x)) = -2*cot(2*x).",
            "The antiderivative of -2*cot(2*x) is -log(sin(2*x)).",
        ],
        [
            r"The numerator is \(\sec^{2}x-\csc^{2}x\), and the quotient simplifies to \(-2\cot(2x)\).",
            r"Integrate \(-2\cot(2x)\).",
        ],
        kind="indefinite",
        equations=(
            (
                "(-csc(x) + sec(x))*(csc(x) + sec(x))/(tan(x) + cot(x))",
                "-2*cot(2*x)",
            ),
        ),
        parts=(("-log(sin(2*x))", "-2*cot(2*x)"),),
        final="-log(sin(2*x))",
    ),
    "YANG-1.5-P20": _steps(
        [
            "Cancel sin(x) + cos(x). (sin(x) + cos(x))/(csc(x) + sec(x)) = sin(x)*cos(x).",
            "Substitution u = sin(x) integrates that product to sin(x)**2/2.",
        ],
        [
            r"Write \(\sec x+\csc x=(\sin x+\cos x)/(\sin x\cos x)\) and cancel.",
            r"Substitution \(u=\sin x\).",
        ],
        kind="indefinite",
        equations=(("(sin(x) + cos(x))/(csc(x) + sec(x))", "sin(x)*cos(x)"),),
        parts=(("sin(x)**2/2", "sin(x)*cos(x)"),),
        final="sin(x)**2/2",
    ),
}


def _parse(text: str):
    names = {"x", "t"}
    local = {name: sp.symbols(name, real=True) for name in names}
    return sp.sympify(text, locals=local)


def _zero(expr) -> bool:
    if expr == 0:
        return True
    attempts = (
        lambda item: sp.simplify(item),
        lambda item: sp.simplify(sp.trigsimp(item)),
        lambda item: sp.simplify(sp.expand(item)),
        lambda item: sp.simplify(sp.expand_trig(item)),
        lambda item: sp.cancel(sp.together(item)),
        lambda item: sp.simplify(sp.cancel(sp.together(sp.expand_trig(item)))),
        lambda item: sp.simplify(sp.powsimp(sp.expand(item), force=True)),
        lambda item: sp.simplify(item.rewrite(sp.sin)),
        lambda item: sp.fu(item),
    )
    for attempt in attempts:
        try:
            if attempt(expr) == 0:
                return True
        except Exception:
            continue
    return False


def _same(left, right) -> bool:
    return _zero(left - right)


def _symbol(expr):
    names = [symbol for symbol in expr.free_symbols if symbol.name in {"x", "t"}]
    if len(names) != 1:
        return None
    return names[0]


def _endpoint(expr, symbol, point: str):
    if point == "oo":
        value = sp.limit(expr, symbol, sp.oo)
    elif point == "-oo":
        value = sp.limit(expr, symbol, -sp.oo)
    else:
        value = expr.subs(symbol, _parse(point))
    if value.has(sp.Limit) or (getattr(value, "free_symbols", set()) & {symbol}):
        return None
    return value


def _render(spec: dict, row: dict) -> tuple[str, str]:
    plain = spec["plain"].replace(ANSWER, row["answer_sympy"])
    latex = spec["latex"].replace(ANSWER, row["answer_latex"])
    return plain, latex


def _mentioned(spec: dict) -> list[str]:
    texts = [spec["final"]]
    for left, right in spec["equations"]:
        texts.extend((left, right))
    for anti, piece in spec["parts"]:
        texts.extend((anti, piece))
    for primitive, piece, _lo, _hi, value in spec["rays"]:
        texts.extend((primitive, piece, value))
    for left, right in spec["derivatives"]:
        texts.extend((left, right))
    for expr, _point, value in spec["ends"]:
        texts.extend((expr, value))
    return texts


def _target(row: dict) -> bool:
    return (
        row.get("source") == "yang_book"
        and row.get("kind") != "reference"
        and row.get("section") in SECTIONS
    )


def check_rows(rows: list[dict], solutions: dict | None = None) -> list[str]:
    book = SOLUTIONS if solutions is None else solutions
    errors = []
    seen = set()
    for row in rows:
        if not _target(row):
            continue
        ident = row.get("id")
        spec = book.get(ident)
        if spec is None:
            errors.append(f"{ident} missing worked steps")
            continue
        seen.add(ident)
        try:
            errors.extend(_check_one(row, spec))
        except Exception as exc:
            errors.append(f"{ident} {exc}")
    extra = sorted(set(book) - seen)
    if extra:
        errors.append("steps for rows outside 1.4 and 1.5: " + ", ".join(extra))
    return errors


def _check_one(row: dict, spec: dict) -> list[str]:
    ident = row["id"]
    if row.get("kind") != spec["kind"]:
        return [f"{ident} kind"]
    if row.get("worked_solution_origin") != "missing":
        return [f"{ident} origin"]
    plain, latex = _render(spec, row)
    if row.get("worked_solution_plain") != plain or row.get("worked_solution_latex") != latex:
        return [f"{ident} worked text drift"]
    folded = plain.replace(" ", "")
    for text in _mentioned(spec):
        compact = text.replace(" ", "")
        if len(compact) >= 3 and compact not in folded:
            return [f"{ident} step missing from the writeup: {text}"]
    integrand = _parse(row["sympy_expr"])
    answer = _parse(row["answer_sympy"])
    final = _parse(spec["final"])
    if not _same(final, answer):
        return [f"{ident} final disagrees with answer_sympy"]
    for left, right in spec["equations"]:
        if not _same(_parse(left), _parse(right)):
            return [f"{ident} equation {left} != {right}"]
    if spec["kind"] == "indefinite":
        return _check_indefinite(ident, spec, integrand, final)
    if spec["kind"] == "definite":
        return _check_definite(ident, spec, integrand, final)
    return [f"{ident} unsupported kind"]


def _check_indefinite(ident, spec, integrand, final) -> list[str]:
    pieces = []
    antis = []
    for anti_text, piece_text in spec["parts"]:
        anti = _parse(anti_text)
        piece = _parse(piece_text)
        symbol = _symbol(anti)
        if symbol is None or not _same(sp.diff(anti, symbol), piece):
            return [f"{ident} derivative {anti_text}"]
        pieces.append(piece)
        antis.append(anti)
    if not pieces:
        return [f"{ident} no antiderivative"]
    if not _covers(integrand, pieces, spec["equations"]):
        return [f"{ident} pieces do not rebuild the integrand"]
    if not _same(sum(antis), final):
        return [f"{ident} antiderivatives do not add to the answer"]
    return []


def _covers(integrand, pieces, equations) -> bool:
    total = sum(pieces)
    if _same(total, integrand):
        return True
    for left, right in equations:
        left_expr = _parse(left)
        right_expr = _parse(right)
        if (_same(left_expr, integrand) and _same(right_expr, total)) or (
            _same(right_expr, integrand) and _same(left_expr, total)
        ):
            return True
    return False


def _check_definite(ident, spec, integrand, final) -> list[str]:
    linked = False
    for left, right in spec["equations"]:
        if _same(_parse(left), integrand) or _same(_parse(right), integrand):
            linked = True
    values = []
    pieces = []
    for primitive_text, piece_text, lo, hi, value_text in spec["rays"]:
        primitive = _parse(primitive_text)
        piece = _parse(piece_text)
        symbol = _symbol(primitive)
        if symbol is None or not _same(sp.diff(primitive, symbol), piece):
            return [f"{ident} derivative {primitive_text}"]
        upper = _endpoint(primitive, symbol, hi)
        lower = _endpoint(primitive, symbol, lo)
        if upper is None or lower is None:
            return [f"{ident} endpoint {primitive_text}"]
        if not _same(upper - lower, _parse(value_text)):
            return [f"{ident} ray {value_text}"]
        values.append(_parse(value_text))
        pieces.append(piece)
    for left_text, right_text in spec["derivatives"]:
        left = _parse(left_text)
        symbol = _symbol(left)
        if symbol is None or not _same(sp.diff(left, symbol), _parse(right_text)):
            return [f"{ident} derivative {left_text}"]
    for expr_text, point, value_text in spec["ends"]:
        expr = _parse(expr_text)
        symbol = _symbol(expr)
        if symbol is None:
            return [f"{ident} endpoint {expr_text}"]
        got = _endpoint(expr, symbol, point)
        if got is None or not _same(got, _parse(value_text)):
            return [f"{ident} endpoint {expr_text} at {point}"]
    if not values:
        return [f"{ident} no ray"]
    if not _same(sum(values), final):
        return [f"{ident} rays do not add to the answer"]
    if pieces and _same(sum(pieces), integrand):
        linked = True
    if not linked:
        return [f"{ident} definite steps do not meet the integrand"]
    return []


def _load() -> tuple[list[dict], list[str]]:
    text = RECORDS.read_text(encoding="utf-8")
    rows = []
    raw = []
    for line in text.splitlines():
        raw.append(line)
        rows.append(json.loads(line))
    return rows, raw


def _dumps(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, separators=(", ", ": "))


def write_rows() -> list[str]:
    rows, raw = _load()
    for row, line in zip(rows, raw):
        if _dumps(row) != line:
            return ["json round trip changed a row before the edit"]
    preview = [dict(row) for row in rows]
    for row in preview:
        spec = SOLUTIONS.get(row.get("id"))
        if spec is None:
            continue
        if not _target(row):
            return [f"{row.get('id')} is outside 1.4 and 1.5"]
        plain, latex = _render(spec, row)
        row["worked_solution_plain"] = plain
        row["worked_solution_latex"] = latex
    errors = check_rows(preview)
    if errors:
        return errors
    lines = [_dumps(row) for row in preview]
    RECORDS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return []


def main() -> int:
    args = sys.argv[1:]
    if args == ["--write"]:
        errors = write_rows()
        if errors:
            print("FAIL yang worked steps")
            for item in errors:
                print(item)
            return 1
        print(f"WROTE yang worked steps ({len(SOLUTIONS)} rows)")
        return 0
    if args == ["--expect-fail"]:
        rows, _raw = _load()
        bad = copy.deepcopy(SOLUTIONS)
        anti, _piece = bad["YANG-1.4-P01"]["parts"][0]
        bad["YANG-1.4-P01"]["parts"] = ((anti, "exp(x)"),)
        errors = check_rows(rows, bad)
        if not any("YANG-1.4-P01" in item and "derivative" in item for item in errors):
            print("FAIL mutation yang-worked-step")
            return 1
        print("PASS mutation yang-worked-step")
        return 0
    if args:
        print(f"unknown args {args}", file=sys.stderr)
        return 2
    rows, _raw = _load()
    errors = check_rows(rows)
    if errors:
        print("FAIL yang worked steps")
        for item in errors:
            print(item)
        return 1
    print(f"PASS yang worked steps ({len(SOLUTIONS)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
