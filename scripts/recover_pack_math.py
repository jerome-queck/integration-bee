#!/usr/bin/env python3
"""Recover pack integrand and answer readings from the committed PDFs.

The script rewrites problems/records.jsonl only for rows whose layout reading
is proved by SymPy. Every other row stays manual or unchecked. Run it again
after a parser change. It is deterministic.

PyMuPDF is required for this script. The catalog check does not import it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import pack_gate  # noqa: E402
import pack_wave5k  # noqa: E402
import pdf_math  # noqa: E402
import problem_catalog  # noqa: E402


def problem_number(row: dict) -> int | None:
    label = str(row.get("problem_id") or "")
    if len(label) < 2 or not label[1:].isdigit():
        return None
    return int(label[1:])


def load_pair(cache: dict, pdf: str, kind: str):
    key = (kind, pdf)
    if key not in cache:
        path = ROOT / pdf
        if not path.is_file():
            cache[key] = None
        elif kind == "problem":
            cache[key] = pdf_math.integral_readings(str(path))
        else:
            cache[key] = pdf_math.answer_readings(str(path))
    return cache[key]


GATED_ROUNDS = frozenset({"r1", "r2", "r3"})
# R2-2023-Relay-Q19 prints upper bound n. That limit is not the mark-scheme
# value sqrt(pi/2), so recovery must not replace the manual row.
# S2-Q07a has an exact +infinity certificate, but the current marking path
# rejects oo against oo. Keep its transcript for a later grading fix.
# Q02-v9 now has a checked damped-cosine reduction below the proof timeout.
HELD_MANUAL = frozenset({"R2-2023-Relay-Q19", "R3-2024-Dichotomy-S2-Q07a"})

_RELAY_M = "Symbol('m', integer=True, positive=True)"
_RELAY_N = "Symbol('n', integer=True, positive=True)"
_RELAY_K = "Symbol('k', integer=True)"
_RELAY_GRID = "*".join(
    f"Sum((x+sqrt(x**2-1)*cos(2*pi*{_RELAY_K}/({index}+2026)))**({index}+26),"
    f"({_RELAY_K},0,{index}+2025))"
    for index in (_RELAY_M, _RELAY_N)
)
_RELAY_TRANSCRIPT = (
    _RELAY_GRID,
    ("-1", "1"),
    f"Piecewise((2*({_RELAY_N}+2026)**2/(2*{_RELAY_N}+53),"
    f"Eq({_RELAY_M},{_RELAY_N})),(0,True))",
)
# Layout readings that do not prove. Each triple is the printed integrand, its
# limits (None when indefinite), and the printed final, taken from the worked
# note that cites the mark scheme. proven() still has to accept the triple.
# An optional fourth item preserves a printed integration variable when x is
# already a parameter.
TRANSCRIPTS = {
    # R1 2023 problem/mark p.2, worked p.6. The unresolved rationality
    # predicates each give a binary endpoint; no rationality claim is needed.
    "R1-2023-Q05": (
        "cos(pi*x)",
        (
            "Piecewise((1,Contains(E+pi,S.Rationals)),(0,True))",
            "Piecewise((1,Contains(E*pi,S.Rationals)),(0,True))",
        ),
        "0",
    ),
    # R1 2024 problem/mark p.2 and worked p.5 use the five letters s,i,n,c,o.
    # Rename s to x; explicit Symbol('i') preserves the printed constant.
    "R1-2024-Q04": (
        "x*Symbol('i')*n**2+c*o*x**2", None,
        "x**2*Symbol('i')*n**2/2+c*o*x**3/3",
    ),
    # R1 2025 Online problem/mark p.2, worked p.14. Nested bounds retain
    # the original octahedron and ceiling rather than assuming its volume.
    "R1-2025-Online-Q13": (
        "Integral(ceiling(x**2+Symbol('y',real=True)**2+Symbol('z',real=True)**2),"
        "(Symbol('z',real=True),-1+Abs(x)+Abs(Symbol('y',real=True)),"
        "1-Abs(x)-Abs(Symbol('y',real=True))),"
        "(Symbol('y',real=True),-1+Abs(x),1-Abs(x)))",
        ("-1", "1"), "4/3",
    ),
    # 2020 problem/answer p.2 and worked p.21; 2021 problem p.2, mark p.1,
    # worked p.18. The 2021 mark agrees with the worked product line, before
    # its last-line omission of log(2)/2.
    "R1-2020-Q19": (
        "x**(-x)", ("0", "1"),
        "Sum(Symbol('k', integer=True, positive=True)**(-Symbol('k', integer=True, positive=True)),"
        "(Symbol('k', integer=True, positive=True),1,oo))",
    ),
    "R1-2021-Q16": (
        "frac(tan(x))/tan(x)", ("0", "pi/2"),
        "(pi-log(sinh(pi)/pi))/2",
    ),
    "R2-2024-Relay-Q17": (
        "x/(floor(x)**4+4)", ("1", "oo"), "(5+pi*coth(pi))/16",
    ),
    "R2-2025-UK-Relay-Q05": (
        f"log(1-x**{_RELAY_N})**{_RELAY_M}/x",
        ("0", "1"),
        f"(-1)**{_RELAY_M}*factorial({_RELAY_M})*zeta({_RELAY_M}+1)/{_RELAY_N}",
    ),
    "R2-2025-SG-Relay-Q23": (
        f"log(1-x**{_RELAY_N})**{_RELAY_M}/x",
        ("0", "1"),
        f"(-1)**{_RELAY_M}*factorial({_RELAY_M})*zeta({_RELAY_M}+1)/{_RELAY_N}",
    ),
    "R2-2025-SG-Relay-Q05": (
        "1/floor(x+floor(x))**2", ("1", "oo"), "pi**2/24",
    ),
    "R2-2025-SG-Group-Q05": (
        "frac(x)*floor(2/frac(x))**(-floor(x))", ("1", "oo"), "2-pi**2/6",
    ),
    "R2-2025-UK-Group-Q04": (
        "frac(x)*floor(2/frac(x))**(-floor(x))", ("1", "oo"), "2-pi**2/6",
    ),
    "R2-2023-Relay-Q04": (
        # The gate checks this unique f against the printed ODE and boundary.
        "exp(-x/2)*(polylog(2,exp(-x/2))-polylog(2,-exp(-x/2)))/2",
        ("0", "oo"), "pi**2/4-2*log(2)",
    ),
    "R2-2024-Group-Q07": (
        "sin(x)*sin(sin(x))*exp(cos(x))/x**2",
        ("0", "oo"),
        "pi*(E-1)/2",
    ),
    "R2-2025-SG-Relay-Q28": (
        "(x**2-1)*sin(x)/(x*(x**2+1))",
        ("0", "oo"),
        "pi/E-pi/2",
    ),
    "R2-2025-UK-Relay-Q18": (
        "(x**2-1)*sin(x)/(x*(x**2+1))",
        ("0", "oo"),
        "pi/E-pi/2",
    ),
    "R2-2022-Group-Q10": (
        "atan(exp(x))*tanh(x/2)/(x*cosh(x))",
        ("-oo", "oo"),
        "pi*log(2)/2",
    ),
    "R1-2021-Q36": (
        "atan(x)**2/x",
        ("0", "1"),
        "pi*G/2-7*zeta(3)/8",
    ),
    "R1-2022-Q28": (
        "log((sqrt(1+x)+1)/(sqrt(1+x)-1))/sqrt(1-x**2)",
        ("0", "1"),
        "4*G",
    ),
    "R3-2024-Dichotomy-S2-Q06a": (
        "(cos(x)-cos(x)**2)*log(x)/x**2",
        ("0", "oo"),
        "-pi*log(2)/2",
    ),
    "R2-2023-Relay-Q15": (
        "4*pi*(1-x**2)**Rational(3,2)/3",
        ("-1", "1"),
        "pi**2/2",
    ),
    "R2-2024-Relay-Q10": (
        "(exp(I*Symbol('theta', real=True)*x)-1-I*Symbol('theta', real=True)*sin(x))/Abs(x)**(1+Symbol('alpha', positive=True))",
        ("-oo", "oo"),
        "2*gamma(-Symbol('alpha', positive=True))*cos(pi*Symbol('alpha', positive=True)/2)*Abs(Symbol('theta', real=True))**Symbol('alpha', positive=True)",
    ),
    "R2-2022-Relay-Q03": (
        "x*log(sin(x))",
        ("0", "pi/2"),
        "7*zeta(3)/16-pi**2*log(2)/8",
    ),
    "R2-2022-Group-Q07": (
        "log(x)*log(1+x**2)",
        ("0", "1"),
        "-log(2)+4-2*G-pi/2",
    ),
    "R2-2025-SG-Relay-Q07": (
        "log(Abs(sin(factorial(2025)*x)))*log(Abs(sin(factorial(2026)*x)))",
        ("0", "pi/2"),
        "pi*log(2)**2/2+pi**3/48624",
    ),
    "R3-2024-Chainlink-G1-Q07": (
        "x/sin(4*x)",
        ("atan(Rational(1,3))", "atan(Rational(1,2))"),
        "pi*log(Rational(4,3))/16",
    ),
    "R3-2024-Chainlink-G2-Q06": (
        "exp(-Symbol('a', positive=True)**2*x**2-Symbol('b', positive=True)**2/x**2)",
        ("0", "oo"),
        "sqrt(pi)*exp(-2*Symbol('a', positive=True)*Symbol('b', positive=True))/(2*Symbol('a', positive=True))",
    ),
    "R3-2024-Chainlink-G3-Q05": (
        "log(sin(x))*tan(x)", ("0", "pi/2"), "-pi**2/24",
    ),
    "R3-2024-Dichotomy-S2-Q05a": (
        "log(1+sqrt(1+((x**4-1)/(2*x**2))**2))", ("0", "1"), "log(2)+pi-2",
    ),
    "R3-2024-Dichotomy-S3-Q02a": (
        "1/sqrt(1+sqrt(exp(x)))", ("0", "oo"),
        "2*(log(sqrt(2)+1)-log(sqrt(2)-1))",
    ),
    # Shuttle D3 passes d=phi; see the source and mark scheme cited in its note.
    "R2-2021-Relay-D04": (
        "x/((1+sqrt(5))/2-cos(x)**2)", ("0", "2*pi"), "2*pi**2",
    ),
    "R2-2024-Relay-Q08": (
        "Sum(1/sqrt(n-sec(x)**2)-1/sqrt(n-tan(x)**2),(n,2,oo))",
        ("0", "pi/4"), "pi/(2*sqrt(2))",
    ),
    "R2-2022-Group-Q05": ("(-1)**floor(x)/x", ("1", "oo"), "log(2/pi)"),
    "R2-2023-Relay-Q17": ("floor(cos(pi/x))", ("0", "1"), "1-pi/2"),
    "R1-2020-Q25": (
        "log(a+b*cos(x))",
        ("0", "pi"),
        "pi*log((a+sqrt(a**2-b**2))/2)",
    ),
    "R1-2022-Q07": ("x*Product(cos(x/2**k), (k, 1, oo))", ("0", "pi/2"), "1"),
    "R1-2022-Q17": ("cos(x)/cosh(x)", ("-oo", "oo"), "pi*sech(pi/2)"),
    "R1-2023-Q04": ("2*x", None, "2*x*X", "X"),
    "R1-2024-Q01": ("exp(i*x)/2", ("-1", "1"), "sin(1)"),
    "R1-2024-Q10": (
        "exp(-t**2)*cos(2*x*t)",
        ("0", "oo"),
        "sqrt(pi)*exp(-x**2)/2",
        "t",
    ),
    "R2-2024-Group-Q01": ("1/(1+Sum(x**k, (k, 1, oo))**2024)", ("0", "1"), "1/2"),
    "R3-2024-Chainlink-G2-Q05": (
        "sin(x)/(cos(x)+tan(x))",
        ("0", "pi/2"),
        "2*atanh(1/sqrt(5))/sqrt(5)",
    ),
    "R1-2020-Q10": ("sqrt(log(9-x))/(sqrt(log(9-x))+sqrt(log(x+3)))", ("2", "4"), "1"),
    "R1-2020-Q11": (
        "(3*x**10+2*x**8-2)*(x**10+x**8+1)**(Rational(1,4))/x**6",
        None,
        "2*(x**6+x**4+x**(-4))**(Rational(5,4))/5",
    ),
    "R1-2020-Q13": (
        "sqrt(1+exp(x))",
        None,
        "log(Abs((sqrt(1+exp(x))-1)/(sqrt(1+exp(x))+1)))+2*sqrt(1+exp(x))",
    ),
    "R1-2020-Q15": (
        "1/sqrt(1+exp(2*x))",
        None,
        "log((sqrt(1+exp(2*x))-1)/(sqrt(1+exp(2*x))+1))/2",
    ),
    "R1-2020-Q18": (
        "1/(2+2*sin(x)+cos(x))",
        None,
        "log(Abs((tan(x/2)+1)/(tan(x/2)+3)))",
    ),
    "R1-2020-Q31": ("sqrt(1+sin(x/2))", None, "4*(sin(x/4)-cos(x/4))"),
    "R1-2021-Q15": ("1/(csc(x)+1)", None, "x - 2*sin(x/2)/(sin(x/2)+cos(x/2))"),
    "R1-2021-Q37": ("sin(x)*cos(x)*(cos(x)-sin(x))", ("0", "pi/2"), "0"),
    "R1-2021-Q39": ("1/(sin(x)**4+cos(x)**4)", None, "atan(tan(2*x)/sqrt(2))/sqrt(2)"),
    "R1-2022-MIT-TB-Q22": ("cos(x)**2022", ("0", "2*pi"), "pi*binomial(2022, 1011)/2**2021"),
    "R1-2022-Q21": ("sqrt(log(x)+1)/x**2", ("exp(-1)", "oo"), "E*sqrt(pi)/2"),
    "R1-2022-Q23": ("(1/x-1)**(Rational(1,4))", ("0", "1"), "pi/(2*sqrt(2))"),
    "R1-2023-Q17": ("exp(asec(sqrt(x)))/(x*sqrt(x))", ("1", "oo"), "exp(pi/2)+1"),
    "R1-2023-Q21": (
        "2023**x/(2023**x+2024**x)",
        None,
        "x - log(1+(2024/2023)**x)/log(2024/2023)",
    ),
    "R1-2024-Q09": ("1/(1+sqrt(1-sin(x)**2))", ("0", "2*pi"), "4"),
    "R1-2025-Online-Q05": ("cos(x)/(1+exp(1/x))", ("-pi/2", "pi/2"), "1"),
    "R1-2025-Online-Q06": ("sqrt(-log(x))", ("0", "1"), "sqrt(pi)/2"),
    "R1-2021-Q03": (
        "sqrt(cos(x))/(sqrt(cos(x))+sqrt(sin(x)))**5",
        ("0", "pi/2"),
        "1/6",
    ),
    "R1-2020-Q05": (
        "sqrt(tan(x))",
        None,
        "sqrt(2)/4*(log(Abs((tan(x)-sqrt(2*tan(x))+1)/(tan(x)+sqrt(2*tan(x))+1)))+2*atan(sqrt(2*tan(x))-1)+2*atan(sqrt(2*tan(x))+1))",
    ),
    "R1-2021-Q02": ("cos(x)**420", ("0", "2*pi"), "pi*binomial(420, 210)/2**419"),
    "R1-2021-Q26": (
        "(x-x*log(x)+1)/(x*(x+1)**2+x*log(x)**2)",
        ("1", "E"),
        "acot(1+E)",
    ),
    "R1-2021-Q31": ("1/(1+floor(1/x))", ("0", "1"), "2-pi**2/6"),
    "R1-2022-Oxford-Q15": (
        "x**(2*n)*exp(-x**2)",
        ("0", "oo"),
        "factorial(2*n)*sqrt(pi)/(4**n*factorial(n)*2)",
    ),
    "R1-2022-Oxford-Q16": ("(sqrt(x)-x)**(Rational(3, 2))", ("0", "1"), "3*pi/128"),
    "R1-2022-Q05": ("1/x-floor(1/x)", ("0", "1"), "1-EulerGamma"),
    "R1-2022-Q15": (
        "cos(x)**2*(1+cos(x))/(1+cos(x)+sin(x))**2",
        ("0", "pi/2"),
        "(pi-2)/4",
    ),
    "R1-2022-Q16": ("(x-floor(x))/x**2", ("1", "oo"), "1-EulerGamma"),
    "R1-2022-TB2022-Q12": (
        "x**(2*n)*exp(-x**2)",
        ("0", "oo"),
        "factorial(2*n)*sqrt(pi)/(4**n*factorial(n)*2)",
    ),
    "R1-2023-Q09": ("(-(x-floor(x)))**floor(x)", ("0", "oo"), "log(2)"),
    "R1-2023-Q20": (
        "4**(4**x/(2+4**x))/(2+4**(4**x/(2+4**x)))",
        ("Rational(1, 4)", "Rational(3, 4)"),
        "Rational(1, 4)",
    ),
    "R1-2024-Q07": (
        "x**(Rational(1, 3))*floor(1/x**(Rational(1, 3)))",
        ("0", "1"),
        "pi**4/120",
    ),
    "R1-2024-Q20": (
        "x**(x-floor(x)-1)*(log(x**x)+(x-floor(x)))",
        ("0", "100"),
        "4950",
    ),
    "R1-2024-Q22": (
        "(atan(x/a)+atan(x/b))/x",
        ("a", "b"),
        "pi*log(b/a)/2",
    ),
    "R1-2024-Q27": ("exp(-x-1/x)/sqrt(x)", ("0", "oo"), "sqrt(pi)/exp(2)"),
    "R1-2024-Q30": ("acosh(sin(x)+cos(x))", ("0", "pi/2"), "pi*log(2)/2"),
    "R1-2025-Online-Q10": ("atan(b*sin(x))/sin(x)", ("0", "pi/2"), "pi*asinh(b)/2"),
    "R1-2025-Online-Q27": (
        "2**x/((1+sqrt(3))**x+(2+sqrt(3))**x)",
        None,
        "((sqrt(3)-1)**x-log(1+(sqrt(3)-1)**x))/log(sqrt(3)-1)",
    ),
    "R2-2021-Group-Q03": ("1/(2+cos(x))**3", ("0", "pi"), "pi/(2*sqrt(3))"),
    "R2-2021-Group-Q10": ("sin(x**2)", ("0", "oo"), "sqrt(pi/2)/2"),
    "R2-2022-Group-Q04": ("1/(sin(x)+cos(x))**2", ("0", "pi/2"), "1"),
    "R2-2022-Group-Q06": ("1/(x+sqrt(1+x**2))**2", ("0", "oo"), "Rational(2, 3)"),
    "R2-2023-Group-Q05": (
        "sin(x)*Integral(exp(sin(x)*(cos(t)-sin(t))), (t, 0, 2*pi))",
        ("0", "pi"),
        "2*sqrt(2)*pi*sinh(sqrt(2))",
    ),
    "R2-2023-Relay-Q14": ("exp(x+exp(x))", ("0", "1"), "exp(E)-E"),
    "R2-2024-Group-Q04": ("atan(sin(x))/sin(x)", ("0", "pi/2"), "pi*log(1+sqrt(2))/2"),
    "R2-2024-Relay-Q01": (
        "x**2*cos(x)/(1+exp(x))",
        ("-pi/2", "pi/2"),
        "(pi**2-8)/4",
    ),
    "R2-2025-SG-Group-Q07": (
        "cos(x)**2/(cos(x)**2+(x*cos(x)+sin(x)+1)**2)", ("-oo", "oo"), "pi",
    ),
    "R2-2025-SG-Relay-Q03": _RELAY_TRANSCRIPT,
    "R2-2025-UK-Group-Q06": (
        "cos(x)**2/(cos(x)**2+(x*cos(x)+sin(x)+1)**2)", ("-oo", "oo"), "pi",
    ),
    "R2-2025-UK-Relay-Q03": _RELAY_TRANSCRIPT,
    "R2-2025-SG-Group-Q14": (
        "((x+1)**2+(3*x+1)*sqrt(x+log(x)))/(x*sqrt(x+log(x))*(x+sqrt(x+log(x))))",
        None,
        "2*sqrt(x+log(x))+2*log(Abs(x+sqrt(x+log(x))))",
    ),
    "R3-2024-Tournament-Q03": (
        "(2-sqrt(tan(x))+tan(x))/(1+tan(x)**(Rational(3, 2)))",
        ("0", "pi/2"),
        "pi/2",
    ),
    "R3-2024-Tournament-Q04": (
        "(x-1)/((x-2)*(x-3))+(x-2)/((x-3)*(x-1))+(x-3)/((x-1)*(x-2))",
        None,
        "Rational(5, 2)*log(Abs(x-3))+Rational(5, 2)*log(Abs(x-1))-2*log(Abs(x-2))",
    ),
    "R3-2024-Tournament-Q05": ("1/(x*(x**log(2048)+1))", ("1", "oo"), "Rational(1, 11)"),
    "R3-2024-Tournament-Q07": (
        "(2025+exp(x)+exp(-x))/(1+2025**x)",
        ("-1", "1"),
        "2025+E-1/E",
    ),
    "R3-2024-Tournament-Q09-v4": (
        "sec(x)*(sec(x)+tan(x))**2025",
        None,
        "(sec(x)+tan(x))**2025/2025",
    ),
    "R3-2024-Tournament-Q09-v7": (
        "1/(sin(x)*(log(sin(x))-log(1+cos(x))))",
        None,
        "log(Abs(log(sin(x))-log(1+cos(x))))",
    ),
    "R3-2024-Tournament-Q09-v10": ("log(x)/(x**2+3)", ("1", "3"), "pi*log(3)/(12*sqrt(3))"),
    # Wave 5i. Each triple is the printed integrand, or the closed form the
    # gate proves equal to the printed nest or series, and the printed final.
    "R1-2020-Q23": ("x*(1/x-floor(1/x))*floor(1/x)", ("0", "1"), "pi**2/12-Rational(1,2)"),
    "R1-2020-Q24": (
        "-Rational(1,2)+sqrt(4*x-3)/2",
        None,
        "(4*x-3)**Rational(3,2)/12-x/2",
    ),
    "R1-2021-Q01": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2021-Q11": ("(log(x)/x)**2011", ("1", "oo"), "factorial(2011)/2010**2012"),
    "R1-2021-Q40": ("cos(log(x))/(1+x)**2", ("0", "oo"), "pi/sinh(pi)"),
    "R1-2022-MIT-TB-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2022-Oxford-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2022-Q04": (
        "Rational(1,2)+sqrt(x+Rational(1,4))",
        ("0", "1"),
        "Rational(5,12)*(1+sqrt(5))",
    ),
    "R1-2022-Q11": ("1/sqrt(1-4*x)", ("0", "Rational(1,4)"), "Rational(1,2)"),
    "R1-2022-Q20": ("log(1+x+x**2)/x", ("0", "1"), "pi**2/9"),
    "R1-2022-TB2022-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2023-Q08": ("4**x", ("0", "1"), "3/(2*log(2))"),
    "R1-2023-Q25": ("LambertW(LambertW(x))/x", ("0", "exp(1+E)"), "E+Rational(1,2)"),
    "R1-2023-Q28": (
        "(sqrt(x**2+1)+x)**Rational(1,3)-(sqrt(x**2+1)-x)**Rational(1,3)",
        ("0", "7"),
        "9",
    ),
    "R1-2024-Q17": ("x*(1+1/(1+x**2))", ("0", "1"), "(1+log(2))/2"),
    "R1-2024-Q28": (
        "(asin(x**2)+asin(sqrt(x)))/sqrt(1-x**2)",
        ("0", "1"),
        "pi**2/4",
    ),
    "R1-2025-Online-Q02": ("sin(pi*floor(x))", ("0", "oo"), "0"),
    "R1-2025-Online-Q23": (
        "sqrt(log(x))+exp(((x-1)/(E-1))**2)/(E-1)",
        ("1", "E"),
        "E",
    ),
    "R1-2025-Online-Q25": ("x+1", ("0", "25"), "Rational(675,2)"),
    "R2-2021-Group-Q04": ("log(sin(x))*cos(x)**3", ("0", "pi"), "0"),
    "R2-2021-Relay-B01": ("sin(sin(x)-x)", ("0", "2*pi"), "0"),
    "R2-2022-Group-Q08": ("sin(24*x)/sin(x)", ("0", "2*pi"), "0"),
    "R3-2024-Chainlink-G1-Q02": (
        "(sinh(x)+cosh(x))/(sinh(exp(x))+cosh(exp(x)))",
        None,
        "-exp(-exp(x))",
    ),
    "R3-2024-Chainlink-G1-Q03": ("(1+log(x))/sqrt(x**(-2*x)-1)", None, "asin(x**x)"),
    "R3-2024-Chainlink-G1-Q04": ("1/(x*sqrt(x)*sqrt(x-1))", ("1", "oo"), "2"),
    "R3-2024-Chainlink-G1-Q05": ("log(1+x+x**2)/x", ("0", "1"), "pi**2/9"),
    "R3-2024-Chainlink-G2-Q01": ("5*(x**6+x)**4", ("-1", "0"), "Rational(1,5)"),
    "R3-2024-Chainlink-G2-Q02": (
        "exp(exp(exp(x)))*exp(exp(x))*exp(exp(x))*exp(x)",
        None,
        "exp(exp(exp(x)))*(exp(exp(x))-1)",
    ),
    "R3-2024-Chainlink-G3-Q04": (
        "sin(2*x)/(sin(x)+cos(x)+1)",
        ("0", "pi/4"),
        "1-pi/4",
    ),
    "R3-2024-Chainlink-G4-Q01": ("sin(x)**2/cos(x)**4", None, "tan(x)**3/3"),
    "R3-2024-Chainlink-G4-Q04": (
        "sqrt(log(x+sqrt(1+x**2))/(1+x**2))",
        None,
        "Rational(2,3)*asinh(x)**Rational(3,2)",
    ),
    "R3-2024-Chainlink-G5-Q01": ("atan(x)/(x**2+1)", ("0", "oo"), "pi**2/8"),
    "R3-2024-Chainlink-G5-Q02": (
        "sec(x)**2*csc(x)**2/(tan(x)**2+cot(x)**2+2)",
        None,
        "x",
    ),
    "R3-2024-Chainlink-G5-Q06": ("1/(x**4+1)**2", ("-oo", "oo"), "3*sqrt(2)*pi/8"),
    "R3-2024-Dichotomy-S1-Q01a": ("sqrt(4-x**2)", ("0", "2"), "pi"),
    "R3-2024-Dichotomy-S1-Q01b": ("sqrt(4-x**2)", ("0", "sqrt(2)"), "pi/2+1"),
    "R3-2024-Dichotomy-S1-Q02b": ("tan(x)/tan(2*x)", None, "x-tan(x)/2"),
    "R3-2024-Dichotomy-S1-Q05b": (
        "log(x**(log(1-log(x))+1-log(x)))",
        ("0", "1"),
        "-4",
    ),
    "R3-2024-Dichotomy-S2-Q02a": ("1/((x+1)*sqrt(x)+2*x)", None, "-2/(sqrt(x)+1)"),
    "R3-2024-Dichotomy-S2-Q03a": (
        "(5*x**2+3*x-2)/(x**3+2*x**2)",
        None,
        "3*log(Abs(x+2))+2*log(Abs(x))+1/x",
    ),
    "R3-2024-Dichotomy-S2-Q03b": (
        "(x+1)**2/((x+2)*(x**2+x+1))",
        None,
        "log(Abs(1+(x+1)**3))/3",
    ),
    "R3-2024-Dichotomy-S3-Q01a": ("(x**4+1)/(x**6+1)", ("0", "1"), "pi/3"),
    "R3-2024-Dichotomy-S3-Q01b": (
        "(x**2+1)/(x**3+1)",
        ("0", "1"),
        "(2*log(2)+sqrt(3)*pi/3)/3",
    ),
    # Wave 5j. Each triple is the printed integrand and the printed final.
    "R1-2024-Q11": ("Si(x)*sin(x)/x", ("0", "oo"), "pi**2/8"),
    "R1-2024-Q13": ("(sin(x)+sin(1/x))/(x*(1+x**2))", ("0", "oo"), "pi/2"),
    "R1-2024-Q15": (
        "sin(sqrt(x))/(sinh(sqrt(x))+sin(sqrt(x)))",
        ("-1", "1"),
        "1",
    ),
    "R1-2025-Online-Q30": ("atan(1+x)/x", ("1", "2"), "3*pi*log(2)/8"),
    "R2-2022-Group-Q01": ("1/x-cot(x)", ("0", "1"), "-log(sin(1))"),
    "R2-2023-Group-Q01": (
        "cos(cos(x)**2)**2+sin(sin(x)**2)**2",
        ("0", "pi"),
        "pi",
    ),
    "R2-2024-Relay-Q05": ("1/(1+(x+1/x)**2)", ("-oo", "oo"), "pi/sqrt(5)"),
    "R2-2024-Relay-Q11": (
        "atan(atan(x/(1-x))/atan((1-x)/x))",
        ("0", "1"),
        "pi/4",
    ),
    "R2-2024-Relay-Q15": ("sin(pi*x/2)**2/sqrt(x-x**2)", ("0", "1"), "pi/2"),
    "R2-2024-Relay-Q16": (
        "Max(Min(x, sin(x)), Min(x, cos(x)))",
        ("pi", "3*pi"),
        "2*sqrt(2)",
    ),
    "R2-2024-Relay-Q19": ("sqrt(log(x)+1)/x**2", ("exp(-1)", "oo"), "E*sqrt(pi)/2"),
    "R2-2025-SG-Group-Q03": (
        "1/(x**Rational(1,3)-x)**Rational(1,3)",
        ("0", "1"),
        "pi/sqrt(3)",
    ),
    "R2-2025-SG-Group-Q04": (
        "(2*x-1)/(sqrt(2*x-x**2)-sqrt(1-x**2))",
        ("0", "1"),
        "pi/2",
    ),
    "R2-2025-SG-Relay-Q06": (
        "x**((sqrt(5)-1)/2)/(1+x**((1+sqrt(5))/2))",
        None,
        "2*log(1+x**((1+sqrt(5))/2))/(1+sqrt(5))",
    ),
    "R2-2025-SG-Relay-Q08": (
        "sin(x)**(tan(x)-2)*(tan(x)**2*log(sin(x))+sin(x)**2)",
        ("pi/4", "pi/2"),
        "1-1/sqrt(2)",
    ),
    "R2-2025-SG-Relay-Q13": (
        "x*sqrt(x**2-1)*exp(-x**2)",
        ("1", "oo"),
        "sqrt(pi)/(4*E)",
    ),
    "R2-2025-SG-Relay-Q25": (
        "(1-x)/((1+x)*sqrt(x+x**2+x**3))",
        ("0", "1"),
        "pi/3",
    ),
    "R2-2025-SG-Relay-Q26": ("1/(1+sin(x)**2*cos(x)**2)", ("0", "pi/2"), "pi/sqrt(5)"),
    "R2-2025-UK-Group-Q03": (
        "(2*x-1)/(sqrt(2*x-x**2)-sqrt(1-x**2))",
        ("0", "1"),
        "pi/2",
    ),
    "R2-2025-UK-Relay-Q06": (
        "x**((sqrt(5)-1)/2)/(1+x**((1+sqrt(5))/2))",
        None,
        "2*log(1+x**((1+sqrt(5))/2))/(1+sqrt(5))",
    ),
    "R2-2025-UK-Relay-Q07": (
        "sin(x)**(tan(x)-2)*(tan(x)**2*log(sin(x))+sin(x)**2)",
        ("pi/4", "pi/2"),
        "1-1/sqrt(2)",
    ),
    "R3-2024-Chainlink-G1-Q01": ("(x-floor(x))**floor(x)", ("1", "4"), "Rational(13,12)"),
    "R3-2024-Chainlink-G3-Q02": (
        "exp(-x**2)*(5*x**4-2*x**6)",
        ("-1", "oo"),
        "exp(-1)",
    ),
    "R3-2024-Chainlink-G4-Q02": (
        "(1+sqrt(1-x**2))/(sqrt(1+x)+sqrt(1-x))",
        ("0", "1"),
        "2*sqrt(2)/3",
    ),
    "R3-2024-Chainlink-G4-Q06": (
        "atan((4*x-4*x**3)/(x**4-6*x**2+1))/(1+x**2)",
        None,
        "atan((4*x-4*x**3)/(x**4-6*x**2+1))**2/8",
    ),
    "R3-2024-Chainlink-G5-Q03": (
        "1/(1+sqrt((1-x+sqrt(x))/(x+sqrt(1-x))))",
        ("0", "1"),
        "Rational(1,2)",
    ),
    "R3-2024-Dichotomy-S1-Q02a": (
        "tan(2*x)/tan(x)",
        None,
        "x+log(Abs(1+tan(x)))/2-log(Abs(1-tan(x)))/2",
    ),
    "R3-2024-Dichotomy-S1-Q06a": (
        "tan(sin(x)**2)/(1-tan(sin(x)**2)*tan(cos(x)**2))",
        ("0", "pi/2"),
        "pi*tan(1)/4",
    ),
    "R3-2024-Dichotomy-S1-Q06b": (
        "log((cos(x)+sin(x))/(sqrt(2)*sin(x)))+log(tan(x))",
        ("0", "pi/4"),
        "0",
    ),
    "R3-2024-Dichotomy-S2-Q01a": ("log(1+x**4)/x**3", ("0", "1"), "pi/4-log(2)/2"),
    "R3-2024-Dichotomy-S2-Q01b": ("log(1+x**4)/x**3", ("-1", "1"), "0"),
    "R3-2024-Dichotomy-S2-Q02b": (
        "1/((sqrt(x)+1)*x+2*sqrt(x))",
        None,
        "4*atan((2*sqrt(x)+1)/sqrt(7))/sqrt(7)",
    ),
    "R3-2024-Dichotomy-S2-Q04a": (
        "1/((x+sqrt(1+x**2))*(1+x**2))",
        ("0", "oo"),
        "log(2)",
    ),
    "R3-2024-Dichotomy-S3-Q04b": ("atan(1/x)/x**2", ("1", "oo"), "pi/4-log(2)/2"),
    "R3-2024-Dichotomy-S3-Q06a": ("cos(x)**8-sin(x)**8", ("0", "pi/4"), "Rational(5,12)"),
    "R3-2024-Dichotomy-S3-Q06b": ("cos(x)**6-sin(x)**6", ("0", "pi/4"), "Rational(11,24)"),
    "R3-2024-Tournament-Q01-v4": (
        "x*log(x)/(1+log(x))**3",
        ("1", "E"),
        "Rational(1,2)*(exp(2)/4-1)",
    ),
    "R3-2024-Tournament-Q03-v7": ("sin(x)*sqrt(sin(2*x))", ("0", "pi/2"), "pi/4"),
    "R3-2024-Tournament-Q05-v6": (
        "sin(x)**tan(x)*(sec(x)**2*log(sin(x))+1)",
        ("pi/4", "pi/2"),
        "1-sqrt(2)/2",
    ),
    "R3-2024-Tournament-Q07-v4": (
        "(x-sqrt(7*x-x**2))/(2*x-7)",
        ("3", "4"),
        "Rational(1,2)",
    ),
    "R3-2024-Tournament-Q08-v6": (
        "x**E*(exp(x)+exp(-x))+x**(E-1)*(exp(x+1)-exp(1-x))",
        ("0", "1"),
        "E-1/E",
    ),
}

# Printed integrals whose SymPy reading is not recovered from the shared
# problem number. R1-2023-Q14's tower parses as log(x), which is the formal
# rewrite in the worked PDF. R1-2025-Online-Q29 is the positive root of
# f**3 + x f = 125, squared.
TRANSCRIPTS.update(
    {
        "R1-2021-Q12": ("sin(x)/x**n", ("0", "oo"), "sin((1-n)*pi/2)*gamma(1-n)"),
        "R1-2021-Q13": (
            "cos(x)/(1+sqrt(sin(2*x)))**2",
            ("0", "pi/2"),
            "Rational(1,3)",
        ),
        "R1-2021-Q30": (
            "atan(x**2)/(1+x**2)",
            ("0", "1"),
            "log(3-2*sqrt(2))**2/16",
        ),
        "R1-2022-MIT-TB-Q17": (
            "x**n/Sum(x**k/factorial(k),(k,0,n))",
            None,
            "factorial(n)*(x-log(Sum(x**k/factorial(k),(k,0,n))))",
        ),
        "R1-2022-Oxford-Q08": ("x*Product(cos(x/2**k),(k,1,oo))", ("0", "pi/2"), "1"),
        "R1-2022-Oxford-Q26": ("cos(x)/cosh(x)", ("-oo", "oo"), "pi*sech(pi/2)"),
        "R1-2022-Q25": ("log(x)*sin(x)/x", ("0", "oo"), "-EulerGamma*pi/2"),
        "R1-2023-Q14": (
            "(log(log(x)))**(log(log(x))/log(log(log(x))))",
            ("0", "1"),
            "-1",
        ),
        "R1-2023-Q30": (
            "sqrt(frac(1/x)/(1-frac(1/x)))/(1-x)",
            ("0", "1"),
            "pi",
        ),
        "R1-2024-Q21": (
            "exp(x**x)/Product(fibonacci(k)/x,(k,1,oo))",
            ("1", "2024"),
            "0",
        ),
        "R1-2024-Q24": (
            "log(Product(1+x**(2**k),(k,0,2024)))/x",
            ("-1", "1"),
            "pi**2/4",
        ),
        "R1-2024-Q29": (
            "Limit(Sum(2**(k*x/n)*k*x**4/(n*k*x**3+1),(k,1,n)), n, oo)",
            ("1/log(2)", "2024"),
            "(1/log(2))*((2**2024 - E + 1)/log(2) - 2024)",
        ),
        "R1-2025-Online-Q07": (
            "Sum(x**k,(k,0,2025))-Sum(x**k,(k,1,2025))",
            ("0", "1"),
            "1",
        ),
        "R1-2025-Online-Q08": (
            "Limit(Sum((-x)**k/factorial(k),(k,0,n)), n, oo)",
            ("0", "oo"),
            "1",
        ),
        "R1-2025-Online-Q12": (
            "Limit(Sum((-1)**(j+1)*x**j,(j,1,n)), n, oo)",
            ("0", "1"),
            "1-log(2)",
        ),
        "R1-2025-Online-Q19": (
            "x/(sqrt(4*x+1)/2+1/2) - sqrt(4*x+1)/2 + 1/2",
            ("0", "2025"),
            "0",
        ),
        "R1-2025-Online-Q20": (
            "Integral(exp(t + t**tan(x)), (t, 0, 1))",
            ("0", "pi/2"),
            "pi/4*(exp(2)-1)",
        ),
        "R1-2025-Online-Q21": ("2025*x**2025", ("0", "1"), "Rational(2025,2026)"),
        "R1-2025-Online-Q22": (
            "x/(2**x-1)**2 - 4*x/(4**x-1)**2",
            ("0", "oo"),
            "1/log(2)",
        ),
        "R1-2025-Online-Q24": (
            "(x**2 + 2**(-x/6)/7 - 2**(-x/7)/6)/((2**(-x/7)+36*x**2)*(2**(-x/6)+49*x**2))",
            ("0", "oo"),
            "0",
        ),
        "R1-2025-Online-Q29": (pack_wave5k.cubic_square_text(), ("0", "124"), "812"),
        "R2-2022-Group-Q02": (
            "x**n/Sum(x**k/factorial(k),(k,0,n))",
            None,
            "factorial(n)*(x-log(Sum(x**k/factorial(k),(k,0,n))))",
        ),
        "R2-2023-Group-Q08": (
            "sqrt((sin(23*x)+10*sin(24*x)+sin(25*x))**2+(cos(23*x)+10*cos(24*x)+cos(25*x))**2)",
            None,
            "10*x+2*sin(x)",
        ),
        "R2-2023-Relay-Q09": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
        "R2-2024-Group-Q02": (
            "(log(exp(x)-1)-x)/(exp(x)-1)",
            None,
            "log(1-exp(-x))**2/2",
        ),
        "R2-2025-SG-Group-Q02": (
            "log(cos(x)+sqrt(1+cos(x)**2))",
            ("0", "pi"),
            "0",
        ),
        "R2-2025-SG-Relay-Q21": ("exp(x-sinh(x)**2)", ("-oo", "oo"), "sqrt(pi)"),
        "R2-2025-SG-Relay-Q30": ("log(x)*sin(x)/x", ("0", "oo"), "-EulerGamma*pi/2"),
        "R2-2025-UK-Group-Q01": (
            "log(cos(x)+sqrt(1+cos(x)**2))",
            ("0", "pi"),
            "0",
        ),
        "R2-2025-UK-Relay-Q11": ("log(x)*sin(x)/x", ("0", "oo"), "-EulerGamma*pi/2"),
        "R2-2025-UK-Relay-Q13": ("exp(x-sinh(x)**2)", ("-oo", "oo"), "sqrt(pi)"),
    }
)

# Wave 5l. Each string is the integral in the pack note, and the note's final
# value agrees with the printed mark. A later recover keeps these rows.
TRANSCRIPTS.update(
    {
        "R3-2024-Tournament-Q01": (
            "floor(x)/(1+floor(x)**2+floor(x)**4)",
            ("0", "oo"),
            "Rational(1,2)",
        ),
        "R3-2024-Tournament-Q02": (
            "(4*cos(x)**2-1)*sqrt(tan(x))",
            ("0", "pi/4"),
            "1",
        ),
        "R3-2024-Tournament-Q02-v3": (
            "atan(x)/(x*(log(x)**2+1))",
            ("0", "oo"),
            "pi**2/4",
        ),
        "R3-2024-Tournament-Q02-v6": (
            "(atan(x/(1+2*x**2))-atan(x/(1+12*x**2)))/x",
            ("0", "oo"),
            "pi/2*(log(3)-log(2))",
        ),
        "R3-2024-Tournament-Q06": (
            "1/((1+2**sin(x))*(1+2**cos(x)))",
            ("0", "2*pi"),
            "pi/2",
        ),
        "R3-2024-Tournament-Q06-v6": (
            "sqrt(x**2+2*sqrt(x**2-1))/x",
            ("1", "sqrt(2)"),
            "log(2)/2+1-pi/4",
        ),
        "R3-2024-Tournament-Q06-v9": (
            "sin(x)**2/(45*x**2+x**2*atan(x)+x**2*sqrt(2025+atan(x)**2))",
            ("-oo", "oo"),
            "pi/90",
        ),
        "R3-2024-Tournament-Q07-v7": (
            "cos(x**2+1/x**2)",
            ("0", "oo"),
            "sqrt(2*pi)/4*(cos(2)-sin(2))",
        ),
        "R3-2024-Tournament-Q07-v10": (
            "1/(2**(Rational(1,4))+sqrt(1+tan(x)))",
            ("0", "pi/4"),
            "pi/(8*2**(Rational(1,4)))",
        ),
        "R3-2024-Tournament-Q08": (
            "1/(sinh(sqrt(x))+csch(sqrt(x)))",
            ("0", "oo"),
            "pi",
        ),
        "R3-2024-Tournament-Q08-v3": (
            "(1+2*x*log(2))/(x*sqrt(x*4**x-1))",
            ("1", "oo"),
            "pi/3",
        ),
        "R3-2024-Tournament-Q08-v9": (
            "factorial(floor(x))*factorial2(2*floor(x))/factorial(2*ceiling(x)-1)",
            ("0", "oo"),
            "pi/2",
        ),
        "R3-2024-Tournament-Q09": (
            "sqrt(x+x**3)+sqrt(x+x**(Rational(1,3)))",
            ("0", "1"),
            "4*sqrt(2)/3",
        ),
        "R3-2024-Tournament-Q01-v10": (
            "3**(-floor(x))*tan(3**(-floor(x)))/(3-tan(3**(-floor(x)))**2)",
            ("0", "oo"),
            "(1-3*cot(3))/8",
        ),
        "R3-2024-Tournament-Q04-v4": (
            "(x**2-1)/(x**3+x)*log(x**3+x**(-3)+3*(x+1/x))",
            None,
            "3*log(x+1/x)**2/2",
        ),
        "R3-2024-Tournament-Q04-v7": (
            "2**(floor(2**x)+x)/(3**(2**floor(2**x))+1)",
            ("-oo", "oo"),
            "1/(2*log(2))",
        ),
        "R3-2024-Tournament-Q05-v4": (
            "log(x)*(2*x-1)/sqrt(x-x**2)",
            ("0", "1"),
            "pi",
        ),
        "R3-2024-Tournament-Q05-v9": (
            "exp(LambertW(x))/x**2",
            None,
            "log(Abs(LambertW(x)))-1/LambertW(x)",
        ),
        "R3-2024-Tournament-Q01-v7": (
            "(log(x)+2)/((x*E)**(-x)+2)",
            None,
            "log(1+2*(x*E)**x)/2",
        ),
        "R3-2024-Dichotomy-S1-Q03a": (
            "1/(1+exp(sqrt(x)))",
            ("0", "oo"),
            "pi**2/6",
        ),
        "R3-2024-Dichotomy-S1-Q03b": (
            "1/(1+x**(E/2))",
            ("0", "oo"),
            "2*pi*exp(-1)*csc(2*pi*exp(-1))",
        ),
        "R3-2024-Dichotomy-S1-Q05a": (
            "log(x**(log(log(x))**2)/log(x))/(log(x)*log(log(x))**3)",
            ("exp(2)", "exp(E)"),
            "exp(E)-exp(2)/log(2)",
        ),
        "R3-2024-Dichotomy-S1-Q07a": (
            "1/((1+x**2)*(1+pi/2+atan(x)*acot(x)))",
            ("0", "1"),
            "log(1+pi/2)/(2+pi/2)",
        ),
        "R3-2024-Dichotomy-S1-Q07b": (
            "1/((1+x**2)*(1+atan(x)*acot(x)))",
            ("0", "1"),
            "4*atanh(pi/sqrt(16+pi**2))/sqrt(16+pi**2)",
        ),
        "R3-2024-Dichotomy-S2-Q06b": (
            "(cos(x)-cos(x)**2)/x**2",
            ("0", "oo"),
            "0",
        ),
        "R3-2024-Dichotomy-S3-Q02b": (
            "exp(-sqrt(sqrt(x)-1))",
            ("1", "oo"),
            "28",
        ),
        "R3-2024-Dichotomy-S3-Q03a": (
            "x**(Rational(1,3))/(x**3+1)",
            ("0", "oo"),
            "pi*csc(4*pi/9)/3",
        ),
        "R3-2024-Dichotomy-S3-Q03b": (
            "x**(Rational(1,3))/(x**4+1)",
            ("0", "oo"),
            "pi/(2*sqrt(3))",
        ),
        "R3-2024-Chainlink-G3-Q07": (
            "(3*x**2-5*x+3)*cos(x**3-3*x**2+4*x-2)",
            ("0", "2"),
            "2*sin(2)",
        ),
        "R3-2024-TB1-Q01": ("sin(4*x)/sin(x)", ("0", "pi/2"), "Rational(4,3)"),
        "R3-2024-TB2-Q01": (
            "(exp(exp(x))+1)/(exp(exp(x)-x)+1)",
            None,
            "log(exp(exp(x))+exp(x))",
        ),
        "R3-2024-TB3-Q01": (
            "1/((x+2)*sqrt((x+1)*(x+3)))",
            None,
            "asec(x+2)",
        ),
        "R3-2024-TB4-Q01": (
            "1/(3**x+sqrt(3))",
            ("-2024", "2025"),
            "4049/(2*sqrt(3))",
        ),
    }
)


TRANSCRIPTS.update({
    # UK 2025 group sheet p.2; the group answers are on mark-scheme p.2.
    "R2-2025-UK-Group-Q02": (
        "1/(x**Rational(1,3)-x)**Rational(1,3)", ("0", "1"), "pi/sqrt(3)",
    ),
    "R2-2025-UK-Group-Q05": (
        "(sin(x)+cos(x))*atan(sin(x))", ("0", "pi/2"),
        "pi/sqrt(2)-pi/4-log(2)/2",
    ),
    "R2-2025-SG-Group-Q06": (
        "(sin(x)+cos(x))*atan(sin(x))", ("0", "pi/2"),
        "pi/sqrt(2)-pi/4-log(2)/2",
    ),
    # SG relay 24 is UK relay 14, printed as pi/e on UK mark-scheme p.3.
    "R2-2025-SG-Relay-Q24": (
        "x**(E/2-1)*(1+log(x))/(x**E+1)", ("0", "oo"), "pi/E",
    ),
    # Shuttle paper pp.2-3 and mark-scheme p.4 give c=pi and c=-oo.
    "R2-2021-Relay-A04": (
        "x*log(sin(x))", ("0", "pi"), "-pi**2*log(2)/2",
    ),
    "R2-2021-Relay-B04": (
        "log(x)/(x**2+pi**2)", ("0", "oo"), "log(pi)/2",
    ),
    "R2-2023-Group-Q10": (
        "atan(1+cos(x))", ("0", "pi"), "pi*acot(sqrt((1+sqrt(5))/2))",
    ),
})

# Wave 5n. Each string is the reduced integral in the pack note, and that
# note's final value agrees with the printed mark. A later recover keeps
# these rows. The integration letter e stays e because x is the parameter.
TRANSCRIPTS.update(
    {
        "R2-2024-Relay-Q12": (
            "((8+(4+(2+1/sqrt(x))/sqrt(x+sqrt(x)))/sqrt(x+sqrt(x+sqrt(x))))/sqrt(x+sqrt(x+sqrt(x+sqrt(x)))))",
            None,
            "16*sqrt(x+sqrt(x+sqrt(x+sqrt(x))))",
        ),
        "R2-2024-Group-Q08": (
            "1/(2*sqrt(1+x**2))-1/(2*sqrt(1-x**2))",
            ("0", "1"),
            "log(1+sqrt(2))/2-pi/4",
        ),
        "R2-2024-Group-Q06": (
            "x*log(x)+x",
            ("1", "E"),
            "3*E**2/4-Rational(1,4)",
        ),
        "R1-2024-Q26": (
            "asin(sqrt(x))+acos(sqrt(x))",
            ("0", "Rational(1,2)"),
            "pi/4",
        ),
        "R2-2021-Relay-C04": (
            "cos(x)/(2-sin(2*x))",
            ("0", "pi/2"),
            "pi/4",
        ),
        "R3-2024-Tournament-Q06-v4": ("sign(x)", ("-2024", "2025"), "1"),
        "R3-2024-Tournament-Q06-v5": ("sign(x)", ("-2024", "2025"), "1"),
        "R2-2023-Group-Q03": ("1-x**2", ("0", "1"), "Rational(2,3)"),
        "R2-2025-SG-Relay-Q10": (
            "sin(x)**67/(2026-cos(x))",
            ("0", "2*pi"),
            "0",
        ),
        "R2-2023-Group-Q06": (
            "exp(-Symbol('c', positive=True)*(y+1/y))/sqrt(y)",
            ("0", "oo"),
            "sqrt(pi/Symbol('c', positive=True))*exp(-2*Symbol('c', positive=True))",
            "y",
        ),
        "R2-2024-Group-Q05": (
            "log(sqrt(1+sqrt(x))+sqrt(1-sqrt(x)))",
            ("0", "1"),
            "log(2)/2+Rational(1,4)",
        ),
        "R2-2024-Group-Q10": (
            "log((1+3*x)/(2-x))/(1+x)",
            ("0", "1"),
            "log(2)**2/2",
        ),
        "R2-2024-Group-Q03": (
            "(cos(x)+x*sin(x))/(x**2+cos(x)**2)",
            ("-oo", "oo"),
            "pi",
        ),
        "R2-2023-Group-Q04": (
            "(x*tan(x)-1)/sqrt(sec(x)**2-x**2)",
            ("0", "pi/2"),
            "0",
        ),
        "R2-2023-Relay-Q10": (
            "Max(sqrt(Symbol('r', positive=True)**2-x**2), Abs(x))",
            ("-Symbol('r', positive=True)", "Symbol('r', positive=True)"),
            "(1+pi/4)*Symbol('r', positive=True)**2",
        ),
        "R2-2022-Group-Q03": (
            "(1-x)*log(1-x)/x",
            ("0", "1"),
            "1-pi**2/6",
        ),
        "R2-2021-Group-Q08": (
            "sqrt(tan(x))*sqrt(1-tan(x))",
            ("0", "pi/4"),
            "pi*(sqrt(2+2*sqrt(2))/2-1)",
        ),
        "R2-2025-SG-Group-Q01": (
            "log(asin(x))/sqrt((1-x**2)*asin(x))",
            ("0", "1"),
            "sqrt(2*pi)*(log(pi/2)-2)",
        ),
        "R2-2025-SG-Group-Q08": (
            "1/((E+exp(x))*(x**4-4*x**3+6*x**2-4*x+2))",
            ("-oo", "oo"),
            "pi/(2*E*sqrt(2))",
        ),
        "R2-2025-UK-Group-Q07": (
            "1/((E+exp(x))*(x**4-4*x**3+6*x**2-4*x+2))",
            ("-oo", "oo"),
            "pi/(2*E*sqrt(2))",
        ),
        "R2-2025-SG-Group-Q09": (
            "sin(x)**6/x**2+sin(x)**5/x+sin(x)**4/x**2+sin(x)**3/x**3",
            ("0", "oo"),
            "pi",
        ),
        "R2-2025-UK-Group-Q08": (
            "sin(x)**6/x**2+sin(x)**5/x+sin(x)**4/x**2+sin(x)**3/x**3",
            ("0", "oo"),
            "pi",
        ),
        "R2-2025-SG-Group-Q10": (
            "x*(2*x+3)*(x+1)**(Rational(1,3))/(x**6+x**2+2*x+1)",
            ("0", "oo"),
            "pi/sqrt(3)",
        ),
        "R2-2025-SG-Relay-Q09": (
            "exp(LambertW(x))/x**2",
            ("E", "2*E**2"),
            "log(2)+Rational(1,2)",
        ),
        "R2-2025-UK-Relay-Q12": (
            "(1+polylog(2,x))/(4+polylog(2,x**2))",
            ("-1", "1"),
            "Rational(1,2)",
        ),
        "R1-2022-Q24": (
            "exp(cos(x))*cos(Symbol('n', integer=True)*x-sin(x))",
            ("0", "2*pi"),
            "Piecewise((2*pi/factorial(Symbol('n', integer=True)), Symbol('n', integer=True)>=0), (0, True))",
        ),
        "R2-2023-Group-Q09": (
            "binomial(Symbol('n', integer=True, nonnegative=True), x)",
            ("-oo", "oo"),
            "2**Symbol('n', integer=True, nonnegative=True)",
        ),
        "R2-2023-Relay-Q08": ("e**x", None, "e**(x+1)/(x+1)", "e"),
        "R2-2024-Relay-Q18": (
            "log((1+x)/(1-x))*log(1+exp(x))",
            ("-1", "1"),
            "1",
        ),
        "R1-2025-Online-Q28": (
            "Piecewise((0, Abs(x)<2), (sqrt(x**2-4), Abs(x)<=3/sqrt(2)), ((Abs(x)-sqrt(x**2-4))/2, True))",
            ("-90", "90"),
            "90*(45-sqrt(2024))-2*log(45-sqrt(2024))-3*log(2)",
        ),
    }
)


# Handoff B. Complete outer limits retain their Integral and multiplier.
# The source notes justify the exact digit, iterate, and radical encodings.
_HANDOFF_B_N = "Symbol('n', integer=True, positive=True)"
_HANDOFF_B_K = "Symbol('k', integer=True, positive=True)"
TRANSCRIPTS.update(
    {
        "R3-2024-Chainlink-G5-Q07": (
            "Min(sqrt(frac(x)-frac(x)**2),Abs(sqrt(3)*asin(cos(pi*x))/pi))",
            ("0", "2025"),
            "2025*pi/12",
        ),
        "R3-2024-Chainlink-G4-Q05": (
            "cos(2*x)/(-log(tan(x))*cos(x)**4)",
            ("0", "pi/4"),
            "log(3)",
        ),
        "R3-2024-Chainlink-G3-Q06": (
            "x**((1+sqrt(5))/2)*atan(x)/(1+x**(2*((1+sqrt(5))/2)**2))",
            ("0", "oo"),
            "pi**2/(8*((1+sqrt(5))/2)**2)",
        ),
        "R3-2024-Chainlink-G2-Q07": (
            "cos(x)**3*sin(x)/log(sin(x))",
            ("0", "pi/2"),
            "-log(2)",
        ),
        "R3-2024-Chainlink-G2-Q03": (
            "sec(x)*csc(x)*sin(tan(x))",
            ("0", "pi/2"),
            "pi/2",
        ),
        "R3-2024-Chainlink-G2-Q04": (
            "log(1+exp(-x))*cos(x)",
            ("0", "oo"),
            "1/2-pi*csch(pi)/2",
        ),
        "R3-2024-Chainlink-G4-Q08": (
            "x*cosh(x)/sinh(pi*x)",
            ("0", "oo"),
            "sec(1/2)**2/4",
        ),
        "R3-2024-Chainlink-G1-Q08": (
            f"Limit(({_HANDOFF_B_N}+1)*Integral(x**(x**x+{_HANDOFF_B_N})*log(1+x+x**x+x**(x**x)+x**(x**(x**x))),(x,0,1)),{_HANDOFF_B_N},oo)",
            ("0", "1"),
            "log(5)",
        ),
        "R3-2024-Chainlink-G1-Q06": (
            f"Product(1-KroneckerDelta(Mod(floor(10**{_HANDOFF_B_K}*x),10),9),({_HANDOFF_B_K},1,oo))",
            ("0", "1"),
            "0",
        ),
        "R3-2024-Chainlink-G5-Q08": (
            "(cos(x)+1-x**2)/((x*sin(x)+1)*sqrt(1-x**2))",
            None,
            "asin((x+sin(x))/(x*sin(x)+1))",
        ),
        "R3-2024-Chainlink-G5-Q05": (
            "sqrt(1+real_root(x-1,3))",
            ("0", "1"),
            "16/35",
        ),
        "R3-2024-Chainlink-G3-Q03": (
            "Sum(k*x**k,(k,1,2025))*Sum(x**k,(k,0,2024))",
            None,
            "Sum(x**k,(k,1,2025))**2/2",
        ),
        "R3-2024-Chainlink-G3-Q01": (
            "exp(-x**Rational(1,2025))",
            ("0", "oo"),
            "factorial(2025)",
        ),
        "R3-2024-Chainlink-G2-Q08": (
            f"Limit(Integral(2025*sin(frac({_HANDOFF_B_N}*x**2025))*cos(frac({_HANDOFF_B_N}*x**2025)),(x,0,1)),{_HANDOFF_B_N},oo)",
            ("0", "1"),
            "2025*sin(1)**2/2",
        ),
        "R3-2024-Chainlink-G4-Q07": (
            f"Limit(Integral((1-(1-2*x)**(2**{_HANDOFF_B_N}))/2,(x,0,Rational(1,2))),{_HANDOFF_B_N},oo)",
            ("0", "1/2"),
            "1/4",
        ),
        "R3-2024-Dichotomy-S1-Q04a": (
            f"Product(x**(2**(1-{_HANDOFF_B_K}))*2**(-{_HANDOFF_B_K}*x/4**{_HANDOFF_B_K}),({_HANDOFF_B_K},1,oo))",
            ("0", "oo"),
            "729/(32*log(2)**3)",
        ),
        "R3-2024-Dichotomy-S1-Q04b": (
            "x**2/2 + x**2/(9*(-x**3/27 + x**2/2 + sqrt(-x**5/27 + x**4/4))**(1/3)) - x/3 + sqrt(x**4 + 4*x**3)/2 + (-x**3/27 + x**2/2 + sqrt(-x**5/27 + x**4/4))**(1/3)",
            ("0", "1/2"),
            "1/4",
        ),
        "R3-2024-Dichotomy-S3-Q05a": (
            "(((1+3/x)**x)**Rational(1,3)-sqrt((1+2/x)**x))/x",
            ("0", "oo"),
            "(E-1)*log(Rational(2,3))",
        ),
        "R3-2024-Dichotomy-S3-Q05b": (
            "sin(x**2+x*sqrt(3*pi)+pi)",
            ("-oo", "oo"),
            "sqrt(pi)",
        ),
        "R3-2024-Dichotomy-S3-Q07a": (
            "sqrt(x/(1-x))*log(x/(1-x))",
            ("0", "1"),
            "pi",
        ),
        "R3-2024-Dichotomy-S3-Q07b": (
            "log(sqrt(x)+sqrt(1-x))/sqrt(x)",
            ("0", "1"),
            "2*sqrt(2)*log(sqrt(2)+1)-2",
        ),
        "R3-2024-Dichotomy-S2-Q05b": (
            "exp(-1-sqrt(1+((x**4-1)/(2*x**2))**2))",
            ("0", "oo"),
            "sqrt(2*pi)/(2*E**2)",
        ),
        "R3-2024-Dichotomy-S2-Q04b": (
            "1/((x+sqrt(x**2+1))*(1+x))",
            ("0", "oo"),
            "-1-log(2)-(sqrt(2)+1)*log(sqrt(2)-1)+(sqrt(2)-1)*log(sqrt(2)+1)",
        ),
        "R3-2024-Dichotomy-S2-Q07a": (
            f"Limit(Integral(log(1+E/{_HANDOFF_B_N}+({_HANDOFF_B_N}*x)**(-1/E)),(x,1,{_HANDOFF_B_N})),{_HANDOFF_B_N},oo)",
            ("1", f"{_HANDOFF_B_N}"),
            "oo",
        ),
        "R3-2024-Dichotomy-S2-Q07b": (
            f"Limit(Integral(log(1+2/{_HANDOFF_B_N}+1/sqrt({_HANDOFF_B_N}*x)),(x,1,{_HANDOFF_B_N})),{_HANDOFF_B_N},oo)",
            ("1", f"{_HANDOFF_B_N}"),
            "4",
        ),
    }
)


# Handoff E: slides 65/67 use the e-th root of x (not exp(sqrt(x))).
# Slides 158/160 give the damped logarithmic trigonometric integral.
# Slides 163/165 give n*integral(tan(t)**n): u=tan(t)**(n+1) changes
# every finite-n integral to the displayed bounded family on [0,1].
TRANSCRIPTS.update(
    {
        "R3-2024-Tournament-Q02-v9": (
            "x**3*sin(log(x))**2*cos(log(x))**2", ("0", "1"), "1/64",
        ),
        "R3-2024-Tournament-Q03-v4": (
            "1/(x*sqrt(x**(1/E)-1))", ("1", "oo"), "E*pi",
        ),
        "R3-2024-Tournament-Q03-v10": (
            "Limit(Symbol('n',integer=True,positive=True)/((Symbol('n',integer=True,positive=True)+1)*(1+x**(2/(Symbol('n',integer=True,positive=True)+1)))),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"), "1/2",
        ),
    }
)

# Answer slides. Each pack note names the source integral and mark.
# The Q04-v10 family remains excluded for a genuine printed discrepancy.
ANSWER_SLIDES = {
    "R3-2024-Tournament-Q02-v10": "R3-2024-Tournament-Q02-v9",
    "R3-2024-Tournament-Q02-v11": "R3-2024-Tournament-Q02-v9",
    "R3-2024-Tournament-Q03-v5": "R3-2024-Tournament-Q03-v4",
    "R3-2024-Tournament-Q03-v6": "R3-2024-Tournament-Q03-v4",
    "R3-2024-Tournament-Q03-v11": "R3-2024-Tournament-Q03-v10",
    "R3-2024-Tournament-Q03-v12": "R3-2024-Tournament-Q03-v10",
    "R3-2024-Tournament-Q01-v11": "R3-2024-Tournament-Q01-v10",
    "R3-2024-Tournament-Q01-v12": "R3-2024-Tournament-Q01-v10",
    "R3-2024-Tournament-Q01-v2": "R3-2024-Tournament-Q01",
    "R3-2024-Tournament-Q01-v3": "R3-2024-Tournament-Q01",
    "R3-2024-Tournament-Q01-v5": "R3-2024-Tournament-Q01-v4",
    "R3-2024-Tournament-Q01-v6": "R3-2024-Tournament-Q01-v4",
    "R3-2024-Tournament-Q01-v8": "R3-2024-Tournament-Q01-v7",
    "R3-2024-Tournament-Q01-v9": "R3-2024-Tournament-Q01-v7",
    "R3-2024-Tournament-Q02-v2": "R3-2024-Tournament-Q02",
    "R3-2024-Tournament-Q02-v4": "R3-2024-Tournament-Q02-v3",
    "R3-2024-Tournament-Q02-v5": "R3-2024-Tournament-Q02-v3",
    "R3-2024-Tournament-Q02-v7": "R3-2024-Tournament-Q02-v6",
    "R3-2024-Tournament-Q02-v8": "R3-2024-Tournament-Q02-v6",
    "R3-2024-Tournament-Q03-v2": "R3-2024-Tournament-Q03",
    "R3-2024-Tournament-Q03-v3": "R3-2024-Tournament-Q03",
    "R3-2024-Tournament-Q03-v8": "R3-2024-Tournament-Q03-v7",
    "R3-2024-Tournament-Q03-v9": "R3-2024-Tournament-Q03-v7",
    "R3-2024-Tournament-Q04-v2": "R3-2024-Tournament-Q04",
    "R3-2024-Tournament-Q04-v3": "R3-2024-Tournament-Q04",
    "R3-2024-Tournament-Q04-v5": "R3-2024-Tournament-Q04-v4",
    "R3-2024-Tournament-Q04-v6": "R3-2024-Tournament-Q04-v4",
    "R3-2024-Tournament-Q04-v8": "R3-2024-Tournament-Q04-v7",
    "R3-2024-Tournament-Q04-v9": "R3-2024-Tournament-Q04-v7",
    "R3-2024-Tournament-Q05-v10": "R3-2024-Tournament-Q05-v9",
    "R3-2024-Tournament-Q05-v11": "R3-2024-Tournament-Q05-v9",
    "R3-2024-Tournament-Q05-v2": "R3-2024-Tournament-Q05",
    "R3-2024-Tournament-Q05-v3": "R3-2024-Tournament-Q05",
    "R3-2024-Tournament-Q05-v5": "R3-2024-Tournament-Q05-v4",
    "R3-2024-Tournament-Q05-v7": "R3-2024-Tournament-Q05-v6",
    "R3-2024-Tournament-Q05-v8": "R3-2024-Tournament-Q05-v6",
    "R3-2024-Tournament-Q06-v10": "R3-2024-Tournament-Q06-v9",
    "R3-2024-Tournament-Q06-v11": "R3-2024-Tournament-Q06-v9",
    "R3-2024-Tournament-Q06-v2": "R3-2024-Tournament-Q06",
    "R3-2024-Tournament-Q06-v3": "R3-2024-Tournament-Q06",
    "R3-2024-Tournament-Q06-v7": "R3-2024-Tournament-Q06-v6",
    "R3-2024-Tournament-Q06-v8": "R3-2024-Tournament-Q06-v6",
    "R3-2024-Tournament-Q07-v11": "R3-2024-Tournament-Q07-v10",
    "R3-2024-Tournament-Q07-v12": "R3-2024-Tournament-Q07-v10",
    "R3-2024-Tournament-Q07-v2": "R3-2024-Tournament-Q07",
    "R3-2024-Tournament-Q07-v3": "R3-2024-Tournament-Q07",
    "R3-2024-Tournament-Q07-v5": "R3-2024-Tournament-Q07-v4",
    "R3-2024-Tournament-Q07-v6": "R3-2024-Tournament-Q07-v4",
    "R3-2024-Tournament-Q07-v8": "R3-2024-Tournament-Q07-v7",
    "R3-2024-Tournament-Q07-v9": "R3-2024-Tournament-Q07-v7",
    "R3-2024-Tournament-Q08-v10": "R3-2024-Tournament-Q08-v9",
    "R3-2024-Tournament-Q08-v11": "R3-2024-Tournament-Q08-v9",
    "R3-2024-Tournament-Q08-v2": "R3-2024-Tournament-Q08",
    "R3-2024-Tournament-Q08-v4": "R3-2024-Tournament-Q08-v3",
    "R3-2024-Tournament-Q08-v5": "R3-2024-Tournament-Q08-v3",
    "R3-2024-Tournament-Q08-v7": "R3-2024-Tournament-Q08-v6",
    "R3-2024-Tournament-Q08-v8": "R3-2024-Tournament-Q08-v6",
    "R3-2024-Tournament-Q09-v11": "R3-2024-Tournament-Q09-v10",
    "R3-2024-Tournament-Q09-v12": "R3-2024-Tournament-Q09-v10",
    "R3-2024-Tournament-Q09-v2": "R3-2024-Tournament-Q09",
    "R3-2024-Tournament-Q09-v3": "R3-2024-Tournament-Q09",
    "R3-2024-Tournament-Q09-v5": "R3-2024-Tournament-Q09-v4",
    "R3-2024-Tournament-Q09-v6": "R3-2024-Tournament-Q09-v4",
    "R3-2024-Tournament-Q09-v8": "R3-2024-Tournament-Q09-v7",
    "R3-2024-Tournament-Q09-v9": "R3-2024-Tournament-Q09-v7",
}

_ANSWER_SLIDE_EXCLUDED = frozenset(
    {
        "R3-2024-Tournament-Q04-v10",
        "R3-2024-Tournament-Q04-v11",
        "R3-2024-Tournament-Q04-v12",
        "R3-2024-Tournament-Q06-v4",
        "R3-2024-Tournament-Q06-v5",
    }
)


def answer_slide_problem() -> str | None:
    """Reject a slide alias that is missing, duplicated, or on the hold list."""
    if set(ANSWER_SLIDES) & _ANSWER_SLIDE_EXCLUDED:
        return "answer slide includes a held row"
    if set(ANSWER_SLIDES.values()) & _ANSWER_SLIDE_EXCLUDED:
        return "answer slide points at a held row"
    missing = sorted(parent for parent in ANSWER_SLIDES.values() if parent not in TRANSCRIPTS)
    if missing:
        return f"answer slide target missing {missing[0]}"
    both = sorted(set(ANSWER_SLIDES) & set(TRANSCRIPTS))
    if both:
        return f"answer slide already transcribed {both[0]}"
    return None


# Handoff C: source-checked readings; outer floors and scalar-only limits stay manual.
TRANSCRIPTS.update(
    {
        "R2-2025-SG-Relay-Q15": (
            "Limit(sin(pi*floor(Symbol('n',integer=True,positive=True)*x+1)/(2*Symbol('n',integer=True,positive=True))),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"),
            "2/pi",
        ),
        "R2-2025-SG-Relay-Q11": (
            "((3*x**2+2*x)/(x**3+x**2-1)+(6*x**2+2*x)/(2*x**3+x**2-2))*sqrt((x**3+x**2-1)*(2*x**3+x**2-2))",
            ("-1", "0"),
            "2*(sqrt(2)-sqrt(3))",
        ),
        "R2-2025-UK-Relay-Q04": (
            "Integral(sin(Symbol('y', real=True)**2+x**2),(Symbol('y', real=True),0,oo))",
            ("0", "oo"),
            "pi/4",
        ),
        "R2-2025-SG-Relay-Q04": (
            "Integral(sin(Symbol('y', real=True)**2+x**2),(Symbol('y', real=True),0,oo))",
            ("0", "oo"),
            "pi/4",
        ),
        "R2-2025-SG-Relay-Q18": (
            "sin(x)/(x*(cosh(x)+cos(x)))",
            ("0", "oo"),
            "pi/4",
        ),
        "R2-2025-UK-Relay-Q09": (
            "sin(x)/(x*(cosh(x)+cos(x)))",
            ("0", "oo"),
            "pi/4",
        ),
        "R2-2022-Relay-Q14": (
            "floor(1/x)*ceiling(1/x)*log(1-1/floor(1/x)**2)",
            ("0", "1/2"),
            "-log(2)",
        ),
        "R2-2022-Relay-Q07": (
            "(sinh(x)-x)/(x**2*sinh(x))",
            ("0", "oo"),
            "log(2)",
        ),
        "R2-2023-Relay-Q07": (
            "Limit(2*sqrt(1-floor(Symbol('n',integer=True,positive=True)*x)**2/Symbol('n',integer=True,positive=True)**2),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"),
            "pi/2",
        ),
        "R2-2024-Relay-Q09": (
            "Limit((1-x)*Product(x**(2**Symbol('k',integer=True,nonnegative=True))+frac(sinh(x**(2**Symbol('k',integer=True,nonnegative=True)))**2)/frac(cosh(x**(2**Symbol('k',integer=True,nonnegative=True)))**2),(Symbol('k',integer=True,nonnegative=True),0,Symbol('n',integer=True,positive=True))),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"),
            "1",
        ),
        "R2-2025-SG-Relay-Q27": (
            "exp(erfinv(x))",
            ("-1", "1"),
            "2*exp(Rational(1,4))",
        ),
        "R2-2025-SG-Relay-Q22": (
            "1/(x*(E+(x**2+1)**(1/log(x))))",
            ("sqrt(2)-1", "sqrt(2)+1"),
            "log(1+sqrt(2))/E",
        ),
        "R2-2025-UK-Relay-Q16": (
            "1/(x*(E+(x**2+1)**(1/log(x))))",
            ("sqrt(2)-1", "sqrt(2)+1"),
            "log(1+sqrt(2))/E",
        ),
        "R2-2025-SG-Relay-Q19": (
            "Limit(Symbol('n',integer=True,positive=True)*(1+x**3)/(Symbol('n',integer=True,positive=True)+x+x**3+x**5),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"),
            "Rational(5,4)",
        ),
        "R2-2025-UK-Relay-Q19": (
            "Limit(Symbol('n',integer=True,positive=True)*(1+x**3)/(Symbol('n',integer=True,positive=True)+x+x**3+x**5),Symbol('n',integer=True,positive=True),oo)",
            ("0", "1"),
            "Rational(5,4)",
        ),
        "R2-2021-Group-Q02": (
            "log((floor(x)**2-1)/floor(x)**2)",
            ("2", "oo"),
            "-log(2)",
        ),
        "R2-2022-Group-Q09": (
            "log(1-x+x**2)/((1+x**2)*log(x))",
            ("0", "oo"),
            "pi/2",
        ),
        "R2-2025-SG-Relay-Q20": (
            "(1+polylog(2,x))/(4+polylog(2,x**2))",
            ("-1", "1"),
            "1/2",
        ),
        "R2-2025-SG-Relay-Q12": (
            "(10-frac(x))/(floor(x)+floor(10-x)+10)",
            ("3", "7"),
            "2",
        ),
    }
)


# Source-checked hard rows. The continued fraction and indexed maximum keep
# their literal operators; the logarithmic Sum has a checked L1 interchange.
TRANSCRIPTS.update(
    {
        "R2-2021-Group-Q01": (
            "atan(x)**2", ("0", "1"), "pi**2/16+pi*log(2)/4-Catalan",
        ),
        "R2-2024-Relay-Q04": (
            "ContinuedFraction(x**2,Lambda(n,2*n*(2*n+1)-x**2),"
            "Lambda(n,2*n*(2*n+1)*x**2),1)",
            ("0", "pi/2"),
            "2*Catalan-pi/2",
        ),
        "R2-2023-Group-Q02": (
            "log((1+sin(x))/(1-sin(x)))", ("0", "pi/2"), "4*Catalan",
        ),
        "R2-2024-Group-Q09": (
            "sin(x)/(exp(x)-1)", ("0", "oo"), "pi*coth(pi)/2-1/2",
        ),
        "R3-2024-Chainlink-G3-Q08": (
            "(1-log(cos(x)))*cos(2*x)/(x**2+(1-log(cos(x)))**2)",
            ("0", "pi/2"),
            "pi/(4*(1+log(2))**2)",
        ),
        "R3-2024-Chainlink-G5-Q04": (
            "1/x-floor(1/x)-1/(x**2*floor(1/x)**2)",
            ("0", "1"),
            "1-EulerGamma-pi**2/6",
        ),
        "R3-2024-Dichotomy-S3-Q04a": (
            "atan(1/x**2)/x", ("1", "oo"), "Catalan/2",
        ),
        "R2-2025-SG-Group-Q12": (
            "Sum((-1)**n*log((1-x**(1/n))/(1-x**(1/(n+1)))),(n,1,oo))",
            ("0", "1"),
            "log(2)-1",
        ),
        "R2-2025-UK-Group-Q09": (
            "Sum((-1)**n*log((1-x**(1/n))/(1-x**(1/(n+1)))),(n,1,oo))",
            ("0", "1"),
            "log(2)-1",
        ),
        "R2-2023-Group-Q07": (
            "IndexedMaximum(Lambda(n,floor(2**(n+1)*x)/2**n-"
            "floor(2**n*x)/2**(n-1)),Naturals0)",
            ("0", "1"),
            "Rational(2,3)",
        ),
        "R2-2025-SG-Relay-Q14": (
            "Sum(floor((k+1)/(x-floor(x)))**(-floor(x))/(k+1),(k,1,oo))",
            ("1", "oo"),
            "Rational(1,2)",
        ),
        "R3-2024-Chainlink-G4-Q03": (
            "(-1)**ceiling(x)/(sqrt(floor(x)*ceiling(x))*"
            "(sqrt(ceiling(x))-sqrt(floor(x))))",
            ("1", "oo"),
            "1",
        ),
    }
)


# Handoff D. Preserve whole integral limits and outer pass-on/rounding
# operations. Subs prevents SymPy from numerically evaluating floor(Integral)
# while parsing. Source pages and any parameter conventions are in the notes.
_HANDOFF_D_N = "Symbol('n', integer=True, positive=True)"
_HANDOFF_D_K = "Symbol('k', integer=True, positive=True)"
_HANDOFF_D_T = "Symbol('t', real=True)"
_HANDOFF_D_H = "Symbol('h', real=True)"
_HANDOFF_D_DIGIT = f"Mod(floor(10**{_HANDOFF_D_N}*x),10)"
_HANDOFF_D_DECIMAL = "+".join(
    f"{value}*KroneckerDelta({_HANDOFF_D_DIGIT},{digit})"
    for digit, value in enumerate((8, 4, 6, 1, 3, 9, 5, 0, 7, 2)) if value
)
TRANSCRIPTS.update(
    {
        "R2-2021-Relay-A01": (
            "Subs(shuttle_value**2,shuttle_value,Integral(log(x)**2,(x,0,1)))",
            ("0", "1"), "4",
        ),
        "R2-2021-Relay-A02": (
            "Subs(pi/shuttle_value,shuttle_value,Integral(sin(x)/sin(x+pi/4),(x,0,pi/2)))",
            ("0", "pi/2"), "2*sqrt(2)",
        ),
        "R2-2021-Relay-A03": (
            "Subs(4*shuttle_value,shuttle_value,Integral(1/(1+tan(x)**(2*sqrt(2))),(x,0,pi/2)))",
            ("0", "pi/2"), "pi",
        ),
        "R2-2021-Relay-B02": (
            "Subs(Mod(floor(shuttle_value),10),shuttle_value,Integral(log(1+169/x**2),(x,0,oo)))",
            ("0", "oo"), "0",
        ),
        "R2-2021-Relay-C01": (
            # The mark 0 selects signed acot; continuous acot would pass 6.
            "Subs(shuttle_value**2-2,shuttle_value,Integral((sin(acot(x))+cos(atan(x)))/(1+x**2),(x,-1,1)))",
            ("-1", "1"), "0",
        ),
        "R2-2021-Relay-C02": (
            "Subs(2-shuttle_value,shuttle_value,Integral(x**3*exp(-x),(x,0,0)))",
            ("0", "0"), "2",
        ),
        "R2-2021-Relay-C03": (
            "Subs(floor(Abs(shuttle_value))+1,shuttle_value,Integral(log(sqrt(x))/(sqrt(x)*(1+x)**2),(x,0,oo)))",
            ("0", "oo"), "2",
        ),
        "R2-2021-Relay-D02": (
            "Subs(floor(shuttle_value)+1,shuttle_value,Integral((x**3-x**2)/log(x),(x,0,1)))",
            ("0", "1"), "1",
        ),
        "R2-2022-Relay-Q10": (
            # Paper's Ei is defined as E1; use that definition and a>0.
            "exp(-Symbol('a',positive=True)*x)*Integral(exp(-t)/t,(t,x,oo))",
            ("0", "oo"), "log(1+a)/a",
        ),
        "R2-2022-Relay-Q11": (
            f"Limit(Integral(sin(t)**({_HANDOFF_D_N}-1)/t**{_HANDOFF_D_N},(t,x,2*x)),x,0,dir='+')",
            ("x", "2*x"), "log(2)", "t",
        ),
        "R2-2022-Relay-Q20": (
            "Limit(Integral(Symbol('A',positive=True)**(1/x),(x,1,Symbol('A',positive=True)))/Symbol('A',positive=True),Symbol('A',positive=True),oo)",
            ("1", "Symbol('A',positive=True)"), "1",
        ),
        "R2-2023-Relay-Q02": (
            # PDF p.2 has 2**n, not OCR's 2*n. The finite log-sum-exp
            # error is at most log(n)/n, giving the exact supremum.
            f"Limit(log(Sum(exp({_HANDOFF_D_N}*sin(2**{_HANDOFF_D_K}*x)),({_HANDOFF_D_K},1,{_HANDOFF_D_N})))/{_HANDOFF_D_N},{_HANDOFF_D_N},oo)",
            ("0", "pi"), "pi",
        ),
        "R2-2023-Relay-Q05": (
            f"Limit(Integral((1+x**4)**{_HANDOFF_D_N},(x,0,2))**(1/{_HANDOFF_D_N}),{_HANDOFF_D_N},oo)",
            ("0", "2"), "17",
        ),
        "R2-2023-Relay-Q13": (
            f"Limit(Integral(tan(x)**({_HANDOFF_D_N}-1)/sin(x)**{_HANDOFF_D_N},(x,{_HANDOFF_D_H},2*{_HANDOFF_D_H})),{_HANDOFF_D_H},0,dir='+-')",
            (_HANDOFF_D_H, f"2*{_HANDOFF_D_H}"), "log(2)",
        ),
        "R2-2024-Relay-Q02": (
            f"Limit(Integral(Sum(({_HANDOFF_D_K}/{_HANDOFF_D_N})**x,({_HANDOFF_D_K},1,{_HANDOFF_D_N})),(x,0,1))/{_HANDOFF_D_N},{_HANDOFF_D_N},oo)",
            ("0", "1"), "log(2)",
        ),
        "R2-2024-Relay-Q03": (
            f"Sum(({_HANDOFF_D_DECIMAL})/10**{_HANDOFF_D_N},({_HANDOFF_D_N},1,oo))",
            ("0", "1"), "1/2",
        ),
        "R2-2024-Relay-Q06": (
            f"Limit({_HANDOFF_D_N}*Integral((1-Abs(x)+Abs(x)**3)**{_HANDOFF_D_N},(x,-1/20,1/24)),{_HANDOFF_D_N},oo)",
            ("-1/20", "1/24"), "2",
        ),
        "R2-2024-Relay-Q07": (
            "exp(Integral(log((x-1)**(1/x**2)),(x,1,2)))",
            ("1", "2"), "1/2",
        ),
        "R2-2024-Relay-Q14": (
            # The certificate proves the original 2025-stage affine-cell
            # recurrence equals this triangle on the ENTIRE interval.
            "Abs(2*frac(x/2)-1)", ("0", "2025"), "2025/2",
        ),
        "R2-2025-SG-Group-Q11": (
            "Subs(floor(rounded_value),rounded_value,Integral(pi*(exp(pi*x)-1)+(1+x)*Sum((-x)**k,(k,0,998)),(x,0,1)))",
            ("0", "1"), "20",
        ),
        "R2-2025-SG-Group-Q13": (
            "Subs(ceiling(rounded_value),rounded_value,Integral(1/atan(x)-(1+x**2)/(1+atan(x)+x**2*atan(x)),(x,1,oo)))",
            ("1", "oo"), "1",
        ),
        "R2-2025-SG-Group-Q15": (
            f"Sum(x**{_HANDOFF_D_N}*Limit(Derivative({_HANDOFF_D_T}**{_HANDOFF_D_N}/(factorial({_HANDOFF_D_N})*sin({_HANDOFF_D_T})**{_HANDOFF_D_N}),({_HANDOFF_D_T},{_HANDOFF_D_N}-1)),{_HANDOFF_D_T},0),({_HANDOFF_D_N},1,oo))",
            ("0", "1"), "pi/2-1",
        ),
        "R2-2025-SG-Relay-Q16": (
            "Subs(floor(rounded_value),rounded_value,Integral(1/floor(2*log(5)/log(x)+4*log(3)/log(x)),(x,2,2025)))",
            ("2", "2025"), "1999",
        ),
        "R2-2025-UK-Relay-Q20": (
            "Subs(floor(rounded_value),rounded_value,Integral(1/floor(2*log(5)/log(x)+4*log(3)/log(x)),(x,2,2025)))",
            ("2", "2025"), "1999",
        ),
    }
)


# Handoff E: problem/mark p.3 and worked p.31, on the positive-a domain.
TRANSCRIPTS["R1-2022-Q30"] = (
    "atan(x)*log(1+x**2)/(x*(Symbol('a',positive=True)**2+x**2))",
    ("0", "oo"),
    "pi*log(1+Symbol('a',positive=True))**2/(2*Symbol('a',positive=True)**2)",
)


def transcribed(row: dict) -> dict | None:
    ident = row.get("id")
    item = TRANSCRIPTS.get(ident)
    if item is None:
        parent = ANSWER_SLIDES.get(ident)
        if parent is not None:
            item = TRANSCRIPTS.get(parent)
    if item is None:
        return None
    integrand, limits, answer, *variable = item
    return pack_gate.fields_from_parts(integrand, limits, answer, variable[0] if variable else "x")


def gate_row(row: dict, cache: dict) -> dict | None:
    if row.get("round") not in GATED_ROUNDS or row.get("source") != "resource_pack":
        return None
    if row.get("id") in HELD_MANUAL:
        return None
    if not str(row.get("answer_plain") or "").strip():
        return None
    # An id-specific transcript wins over the shared problem number. Tournament
    # sheets repeat a number for a different integral, and for an answer slide.
    known = transcribed(row)
    if known is not None:
        return known
    number = problem_number(row)
    problem_pdf = row.get("pdf_path")
    answer_pdf = row.get("answer_source_pdf")
    if number is not None and problem_pdf and answer_pdf:
        integrals = load_pair(cache, problem_pdf, "problem")
        answers = load_pair(cache, answer_pdf, "answer")
        if integrals is not None and answers is not None:
            integral = integrals.get(number)
            answer = answers.get(number)
            if integral is not None and answer is not None:
                fields = pack_gate.fields_for(number, integral, answer)
                if fields is not None:
                    return fields
    return None


def apply_fields(row: dict, fields: dict) -> None:
    row["verify"] = "sympy"
    row["kind"] = fields["kind"]
    row["variable"] = fields["variable"]
    row["limits"] = fields["limits"]
    row["sympy_expr"] = fields["sympy_expr"]
    row["answer_sympy"] = fields["answer_sympy"]
    row["integrand_latex"] = fields["integrand_latex"]
    row["answer_latex"] = fields["answer_latex"]


def recover(rows: list[dict]) -> tuple[list[dict], list[str]]:
    cache: dict = {}
    gated: list[str] = []
    for row in rows:
        if row.get("round") not in GATED_ROUNDS:
            continue
        fields = gate_row(row, cache)
        if fields is not None:
            apply_fields(row, fields)
            gated.append(row["id"])
        elif row.get("verify") == "sympy" and row.get("source") == "resource_pack":
            pack_gate.blank_gate(row)
    return rows, gated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    args = parser.parse_args()
    slide_err = answer_slide_problem()
    if slide_err:
        print(slide_err, file=sys.stderr)
        return 1
    rows = problem_catalog.load_records()
    before = sum(1 for row in rows if row.get("verify") == "sympy")
    rows, gated = recover(rows)
    if args.id:
        wanted = set(args.id)
        gated = [item for item in gated if item in wanted]
        print("\n".join(gated))
    else:
        print(f"sympy {before} -> {len(gated)}")
        for item in gated:
            row = next(row for row in rows if row["id"] == item)
            print(f"{item}\t{row['kind']}\t{row['sympy_expr']}\t{row['limits']}\t{row['answer_sympy']}")
    if args.write:
        if args.id:
            print("refusing a partial write", file=sys.stderr)
            return 2
        err = problem_catalog.catalog_problem(rows)
        if err:
            print(err, file=sys.stderr)
            return 1
        problem_catalog.dump_records(rows)
        print(f"wrote {problem_catalog.RECORDS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
