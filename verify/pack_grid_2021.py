"""Contest-convention certificates for the 2021/22 crossnumber.

CLUES preserves the printed statements; CLARIFICATIONS declares the grading
readings for A8's publication date, D3's missing parentheses, and D4's
congruence.  The notes cite the source conflicts and derive the marked values
under those readings.  Neither the source text nor the mark lattice is edited.
"""

import math

import sympy as s


PROBLEM_PDFS = ("sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf",)
MARK_PDF = "sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf"
GRID = (
    "#77177#########",
    "27###7#########",
    "8####2#####7###",
    "#####82##53131#",
    "####1868###3#20",
    "####4#55###46##",
    "######6####3###",
    "######4181#1#3#",
    "#########95791#",
    "#######230###5#",
    "########343####",
)
ACROSS = {1: 77177, 3: 27, 6: 53131, 8: 1868, 10: 20, 11: 46,
          12: 4181, 15: 95791, 16: 230, 17: 343}
DOWN = {1: 77, 2: 77288, 3: 28, 4: 7134317, 5: 26564, 7: 12,
        8: 14, 9: 85, 13: 1904, 14: 315}
STARTS = {
    "A1": (0, 1), "A3": (1, 0), "A6": (3, 9), "A8": (4, 4),
    "A10": (4, 13), "A11": (5, 11), "A12": (7, 6), "A15": (8, 9),
    "A16": (9, 7), "A17": (10, 8),
    "D1": (0, 1), "D2": (0, 5), "D3": (1, 0), "D4": (2, 11),
    "D5": (3, 6), "D7": (3, 13), "D8": (4, 4), "D9": (4, 7),
    "D13": (7, 9), "D14": (7, 13),
}
CLUES = {
    "A1": "Smallest palindrome bigger than A17*(D8+1)^2.",
    "A3": "Integral(f(x),(x,0,2)), where 3*Integral(f(x),(x,1,2))-5*Integral(f(x),(x,0,1))=17 and 21*Integral(f(x),(x,0,1))-7*Integral(f(x),(x,1,2))=35.",
    "A6": "(1+A16^4+(A16+1)^4)/(1+A16^2+(A16+1)^2).",
    "A8": "The year the Riemann Integral was first published.",
    "A10": "Limit(Integral(atan(x^n),(x,0,14)),n,oo), to 2 significant figures.",
    "A11": "Sum of the three smallest clues.",
    "A12": "A Fibonacci number.",
    "A15": "(1+310^2+310^4)/(1+310+310^2).",
    "A16": "D7*A10-10.",
    "A17": "A power of 7.",
    "D1": "(A16+1)/3.",
    "D2": "Nearest integer to (279^4+4)/(279^2+2*279+2)+Integral(log(sqrt(1+x))/(x*sqrt(x)),(x,0,oo)).",
    "D3": "The x-th triangular number where x is 7^(D9) mod D7 + 1 (as printed, without parentheses).",
    "D4": "Palindromic number whose product of digits is 1764 and whose digit sum is x mod 9 where x solves x^2-D7*x+32=0.",
    "D5": "Largest n such that I_n=Integral(x^n/(1+x),(x,0,1))>1/(A6-1).",
    "D7": "Integral(f(x),(x,0,1)), where 5*Integral(f(x),(x,0,2))+4*Integral(f(x),(x,0,1))=143 and 7*Integral(f(x),(x,0,2))+11*Integral(f(x),(x,1,2))=210.",
    "D8": "Expected number of fair-coin flips to get three heads in a row.",
    "D9": "D14-A16.",
    "D13": "The year the Lebesgue Integral was published.",
    "D14": "f(6), where f(x)+Integral(f(t),(t,2,5))=12*x^2.",
}
CLARIFICATIONS = {
    "A8": "Contest convention: use the publication year of Abhandlungen der Koniglichen Gesellschaft der Wissenschaften in Gottingen, volume 13. The solution note separately records the earlier standalone offprint.",
    "D3": "Contest grouping: x = 7**D9 mod (D7+1). The source omits these parentheses.",
    "D4": "Contest reading: the digit sum is congruent modulo 9 to a root of x**2-D7*x+32=0.",
}


def _power(n, base):
    if n < 1:
        return False
    while n % base == 0:
        n //= base
    return n == 1


def _fibonacci(n):
    first, second = 0, 1
    while first < n:
        first, second = second, first+second
    return first == n


def _next_palindrome(a, d):
    lower = a[17]*(d[8]+1)**2
    if a[1] <= lower or str(a[1]) != str(a[1])[::-1]:
        return False
    # A palindrome above a number differs only at its central-prefix choice.
    # Enumerate those prefixes, not every integer in an unbounded interval.
    length = len(str(lower))
    half = (length+1)//2
    prefix = int(str(lower)[:half])
    for p in (prefix, prefix+1):
        left = str(p)
        candidate = int(left + left[:length//2][::-1])
        if candidate > lower:
            return a[1] == candidate
    return False


def _across_linear(a):
    first, second = s.symbols("first second")
    solution = s.solve([3*second-5*first-17,
                        21*first-7*second-35], [first, second])
    return bool(a[3] == solution[first]+solution[second])


def _arctangent_limit(a):
    # DCT: 0 <= atan(x^n) <= pi/2 on [0,14]; the a.e. limit is
    # 0 on [0,1) and pi/2 on (1,14].  The single point x=1 is null.
    x = s.Symbol("x", real=True)
    value = s.integrate(s.pi/2, (x, 1, 14))
    # The result is between 10 and 100, hence two significant figures means
    # rounding to the nearest unit. These comparisons remain exact.
    return bool(10 <= value < 100
                and s.Rational(2*a[10]-1, 2) <= value
                and value < s.Rational(2*a[10]+1, 2))


def _rounded_logarithm(d):
    x = s.Symbol("x", positive=True)
    integrand = s.log(1+x)/(2*x*s.sqrt(x))
    primitive = -s.log(1+x)/s.sqrt(x)+2*s.atan(s.sqrt(x))
    if s.simplify(s.diff(primitive, x)-integrand) != 0:
        return False
    integral = s.limit(primitive, x, s.oo)-s.limit(primitive, x, 0, dir="+")
    value = s.Rational(279**4+4, 279**2+2*279+2)+integral
    return bool(s.Rational(2*d[2]-1, 2) < value < s.Rational(2*d[2]+1, 2))


def _contest_triangular(d):
    # Declared grouping: the modulus is the complete expression D7+1.
    # At the marked D9=85, D7=12, 7**85 mod 13 = 7, so T_7 = 28.
    # The alternative (7**D9 mod D7)+1 instead gives T_8 = 36.
    x = pow(7, d[9], d[7]+1)
    return d[3] == x*(x+1)//2


def _contest_palindrome(d):
    digits = [int(c) for c in str(d[4])]
    x = s.Symbol("x")
    roots = s.solve(x**2-d[7]*x+32, x)
    # Declared congruence: digit sum 26 is congruent to root 8 modulo 9.
    # Literal equality to x mod 9 would fail and is documented in the note.
    return bool(str(d[4]) == str(d[4])[::-1]
                and math.prod(digits) == 1764
                and any((sum(digits)-root) % 9 == 0 for root in roots))


def _largest_log_moment(a, d):
    n = d[5]
    if n < 0 or a[6] <= 1:
        return False
    # Strict lower bound: 1/(1+x)>1/2 for 0<x<1.
    # Strict upper bound: 1+x>2*sqrt(x) for 0<x<1.
    # Thus 1/(2(n+1)) < I_n < 1/(2n+1), and I_n strictly decreases.
    # At n=26564 the lower bound equals the required threshold;
    # I_(n+1) is already below it. No large alternating sum is needed.
    threshold = s.Rational(1, a[6]-1)
    lower = s.Rational(1, 2*(n+1))
    next_upper = s.Rational(1, 2*n+3)
    return bool(lower >= threshold and next_upper <= threshold)


def _down_linear(d):
    first, total = s.symbols("first total")
    solution = s.solve([5*total+4*first-143,
                        7*total+11*(total-first)-210], [first, total])
    return bool(d[7] == solution[first])


def _coin_wait(d):
    e0, e1, e2 = s.symbols("e0 e1 e2")
    solution = s.solve([e0-1-(e0+e1)/2,
                        e1-1-(e0+e2)/2,
                        e2-1-e0/2], [e0, e1, e2])
    return bool(d[8] == solution[e0])


def _quadratic_function(d):
    x = s.Symbol("x", real=True)
    # With C=int_2^5 f, integrate f+C=12*x^2: C+3*C=int_2^5 12*x^2.
    constant = s.integrate(12*x**2, (x, 2, 5))/4
    return bool(d[14] == 12*6**2-constant)


def checks(across, down):
    a, d = across, down
    return {
        "A1": lambda: _next_palindrome(a, d),
        "A3": lambda: _across_linear(a),
        "A6": lambda: (1+a[16]**4+(a[16]+1)**4) == a[6]*(1+a[16]**2+(a[16]+1)**2),
        # Source-backed volume-year convention, not a symbolic history proof:
        # https://gdz.sub.uni-goettingen.de/id/PPN250442582_0013
        # The note acknowledges the 1867 offprint (PPN309770033).
        "A8": lambda: a[8] == 1868,
        "A10": lambda: _arctangent_limit(a),
        "A11": lambda: a[11] == sum(sorted(list(a.values())+list(d.values()))[:3]),
        "A12": lambda: _fibonacci(a[12]),
        "A15": lambda: 1+310**2+310**4 == a[15]*(1+310+310**2),
        "A16": lambda: a[16] == d[7]*a[10]-10,
        "A17": lambda: _power(a[17], 7),
        "D1": lambda: 3*d[1] == a[16]+1,
        "D2": lambda: _rounded_logarithm(d),
        "D3": lambda: _contest_triangular(d),
        "D4": lambda: _contest_palindrome(d),
        "D5": lambda: _largest_log_moment(a, d),
        "D7": lambda: _down_linear(d),
        "D8": lambda: _coin_wait(d),
        "D9": lambda: d[9] == d[14]-a[16],
        # Source-backed book-publication fact; not a symbolic mathematics claim.
        "D13": lambda: d[13] == 1904,
        "D14": lambda: _quadratic_function(d),
    }
