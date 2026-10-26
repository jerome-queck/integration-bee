"""Exact clue checks for the two 2024 Round 2 crossnumber sheets.

See solutions/pack/R2-2024-{Across-Across,Down-Down}-1.md for source
readings and the analytic reductions supporting the finite certificates.
"""

from itertools import permutations

import sympy as s


GRID = (
    "####2###563", "###15###148", "###8####729", "12#3###1###",
    "2##89##7##9", "84#114#2##9", "#9##4#58720", "#5832#3#9##",
    "####390625#", "######3#1##",
)
ACROSS = {1: 12, 2: 84, 4: 5832, 6: 15, 7: 89, 8: 114, 11: 390625,
          12: 58720, 15: 563, 18: 148, 19: 729}
DOWN = {1: 128, 3: 495, 5: 25, 6: 18381, 9: 91423, 10: 1728,
        12: 5303, 13: 7921, 14: 990, 15: 517, 16: 642, 17: 389}
STARTS = {
    "A1": (3, 0), "A2": (5, 0), "A4": (7, 1), "A6": (1, 3),
    "A7": (4, 3), "A8": (5, 3), "A11": (8, 4), "A12": (6, 6),
    "A15": (0, 8), "A18": (1, 8), "A19": (2, 8),
    "D1": (3, 0), "D3": (5, 1), "D5": (0, 4), "D6": (1, 3),
    "D9": (4, 4), "D10": (3, 7), "D12": (6, 6), "D13": (6, 8),
    "D14": (4, 10), "D15": (0, 8), "D16": (0, 9), "D17": (0, 10),
}
CLUES = {
    "A1": "f(0), given f(x)+Integral(f(t),(t,-1,1))=24*x**2-25*x+52.",
    "A2": "a*b for coprime integers 1<=a,b<20 with Integral(1/((abs(x)+a**(1/b))*log(abs(x)+a**(1/b))**2),(x,-oo,oo))=14/(log(3)+2*log(2)).",
    "A4": "A perfect cube.",
    "A6": "Shares a factor greater than 1 with the smallest positive integer n such that Integral(cos(x)*Product(sin(x/(2*k-1))/(x/(2*k-1)),(k,1,n)),(x,0,oo)) != pi/4.",
    "A7": "sqrt(13 DOWN).",
    "A8": "(7 ACROSS)**a+(5 DOWN)**b, where Integral(Integral((x*y)**(x*y),(x,0,1)),(y,0,1))=(a/b)*Integral(x**x,(x,0,1)) and a/b is in simplest form.",
    "A11": "(b**a)**2 for the greatest positive a/b in simplest terms such that floor((2 ACROSS)/10)/20*Integral(f(x),(x,0,1))+(2/3)*Integral(f(x),(x,0,3/5))>=Integral(f(x),(x,0,a/b)) for every continuous convex f:[0,1]->R.",
    "A12": "Five-digit abcde with the two-digit integer de=a+b+c.",
    "A15": "A sexy prime: a prime differing from another prime by exactly 6. Across 15,18,19 together contain exactly one of each digit 1 through 9.",
    "A18": "An even number. Across 15,18,19 together contain exactly one of each digit 1 through 9.",
    "A19": "A perfect square greater than 20*25. Across 15,18,19 together contain exactly one of each digit 1 through 9.",
    "D1": "Three distinct digits a,b,c in some order, where b,c are both digits of a**3 and abs(a-b)**3.",
    "D3": "abs(20*Integral(f(x),(x,1,3))-25*Integral(f(x),(x,0,1))), given 20*Integral(f(x),(x,0,1))+25*Integral(f(x),(x,0,2))=2025 and 25*Integral(f(x),(x,1,2))+20*Integral(f(x),(x,0,3))=2520.",
    "D5": "a such that Integral((a*x+5)/(x**2-6*x+10),(x,2,3))=20*pi-25*log(2)/2.",
    "D6": "A palindromic number divisible by 11.",
    "D9": "The middle digit is floor((largest answer)/(second largest answer)).",
    "D10": "The only integer in {(Integral(Sum(sin(n*x)/n,(n,1,oo))**((2 ACROSS)/(1 ACROSS)-5),(x,0,pi))/pi**k)**(-3):k in Z}.",
    "D12": "Integral(floor(x*floor(x))-floor(sqrt(x*floor(x)))**2,(x,0,(7 ACROSS)+(2 ACROSS)))-2050.",
    "D13": "Four-digit abcd: d is nonzero and half the second-smallest digit; limit(Integral(exp(-x**2+x)**n,(x,-oo,oo))**(1/n),n,oo)=((b-a)/2)*exp(1/sqrt(a+b)).",
    "D14": "Of 3 DOWN and this number, one divides the other; equality is allowed.",
    "D15": "Not a prime. Down 15,16,17 together contain exactly one of each digit 1 through 9.",
    "D16": "Last digit is 3 less than the first digit of 15 DOWN. Down 15,16,17 together contain exactly one of each digit 1 through 9.",
    "D17": "Odd three-digit abc with a<b<c and a+b+c=20. Down 15,16,17 together contain exactly one of each digit 1 through 9.",
}


def _eq(left, right):
    return bool(s.simplify(left - right) == 0)


def _digits(value):
    return tuple(map(int, str(value)))


def _nine_digits(values, keys):
    return sorted("".join(str(values[k]) for k in keys)) == list("123456789")


def _fredholm(answer):
    x = s.Symbol("x")
    polynomial = 24 * x**2 - 25 * x + 52
    total = s.integrate(polynomial, (x, -1, 1)) / 3
    return _eq(polynomial.subs(x, 0) - total, answer)


def _log_integral(answer):
    x, c = s.symbols("x c", positive=True)
    primitive = -1 / s.log(x + c)
    if not (_eq(s.diff(primitive, x), 1 / ((x + c) * s.log(x + c)**2))
            and _eq(s.limit(primitive, x, s.oo), 0)):
        return False
    # The even integral is 2*b/log(a); logarithmic equality is equivalent
    # to a**7=12**b.  a=1 is excluded because its improper integral diverges.
    pairs = [(a, b) for a in range(2, 20) for b in range(1, 20)
             if s.gcd(a, b) == 1 and a**7 == 12**b]
    return len(pairs) == 1 and pairs[0][0] * pairs[0][1] == answer


def _borwein_factor(answer):
    # The convolution argument in the transcript says pi/4 persists iff
    # sum_{k=2}^n 1/(2*k-1)<=2.  Positivity of the convolution on its open
    # support makes the first strict excess a strict change in the integral.
    total = s.Rational(0)
    for n in range(2, 100):
        previous = total
        total += s.Rational(1, 2 * n - 1)
        if total > 2:
            return bool(previous <= 2 and s.gcd(answer, n) > 1)
    return False


def _sophomore_pair(answer, across7, down5):
    x = s.Symbol("x", positive=True)
    h = x**x
    # Product substitution turns the double integral into integral -log(x)h.
    # h'=h*(1+log x), and both endpoint values of h are 1.
    if not (_eq(s.diff(h, x), h * (1 + s.log(x)))
            and _eq(s.limit(h, x, 0, dir="+"), h.subs(x, 1))):
        return False
    return across7 + down5 == answer  # The reduced positive ratio is 1/1.


def _convex(answer, across2):
    t = s.Symbol("t", real=True)
    c = s.Rational(across2 // 10, 20)
    end = c + s.Rational(2, 3) * s.Rational(3, 5)
    # Constants +1 and -1 force this end; affine functions force the moment.
    first = c / 2 + s.Rational(2, 3) * s.Rational(3, 5)**2 / 2
    if not _eq(first, end**2 / 2):
        return False
    h0 = c * (1 - t)**2 / 2 + (s.Rational(3, 5) - t)**2 / 3 - (end - t)**2 / 2
    h1 = c * (1 - t)**2 / 2 - (end - t)**2 / 2
    h2 = c * (1 - t)**2 / 2
    if not (_eq(h0, t**2 / 30) and _eq(end, s.Rational(4, 5))):
        return False
    # Middle interval: a concave quadratic attains its minimum at an end.
    if not (s.Poly(s.expand(h1), t).coeff_monomial(t**2) < 0
            and h1.subs(t, s.Rational(3, 5)) >= 0
            and h1.subs(t, end) >= 0 and c >= 0):
        return False
    if not _eq(h2, (1 - t)**2 / 5):
        return False
    return int((end.q**end.p)**2) == answer


def _digit_cubes(answer):
    digits = _digits(answer)
    if len(digits) != 3 or len(set(digits)) != 3:
        return False
    return any(str(b) in str(a**3) and str(c) in str(a**3)
               and str(b) in str(abs(a-b)**3) and str(c) in str(abs(a-b)**3)
               for a, b, c in permutations(digits))


def _linear_down(answer):
    u, v, w = s.symbols("u v w")
    first = 20 * u + 25 * (u + v)
    second = 25 * v + 20 * (u + v + w)
    target = 20 * (v + w) - 25 * u
    return _eq(second - first, target) and abs(2520 - 2025) == answer


def _rational_integral(answer):
    x = s.Symbol("x", real=True)
    a = s.Integer(answer)
    primitive = a * s.log((x - 3)**2 + 1) / 2 + (3 * a + 5) * s.atan(x - 3)
    original = (a * x + 5) / (x**2 - 6 * x + 10)
    value = primitive.subs(x, 3) - primitive.subs(x, 2)
    return _eq(s.diff(primitive, x), original) and _eq(value, 20 * s.pi - 25 * s.log(2) / 2)


def _fourier_integer(answer, across1, across2):
    x = s.Symbol("x", real=True)
    power = s.Rational(across2, across1) - 5
    if power != 2:
        return False
    # Abel's logarithmic sum and Dirichlet convergence give (pi-x)/2.
    # This factorization fixes the principal argument for 0<x<pi.
    factor = -2 * s.I * s.exp(s.I * x / 2) * s.sin(x / 2)
    if not _eq(s.expand_complex(1 - s.exp(s.I * x) - factor), 0):
        return False
    value = s.integrate(((s.pi - x) / 2)**power, (x, 0, s.pi))
    # The set is 1728*pi**(3*k-9).  Transcendence of pi excludes nonzero
    # integer exponents; k=3 is the sole rational, hence sole integer, case.
    if not (_eq(value, s.pi**3 / 12) and s.pi.is_transcendental):
        return False
    return _eq((value / s.pi**3)**(-3), answer)


def _floor_integral(answer, upper):
    if upper < 1 or type(upper) is not int:
        return False
    # On n<=x<n+1, sqrt(n*x) lies in [n,n+1), and floor(n*x)-n^2
    # takes values 0,...,n-1 on n equal subintervals.
    value = s.Integer(0)
    for n in range(1, upper):
        if not n * (n + 1) < (n + 1)**2:
            return False
        value += s.Rational(n - 1, 2)
    return _eq(value - 2050, answer)


def _gaussian_digits(answer):
    a, b, c, d = _digits(answer)
    if d == 0 or 2 * d != sorted((a, b, c, d))[1]:
        return False
    x = s.Symbol("x", real=True)
    n = s.Symbol("n", positive=True)
    if not _eq(-x**2 + x, -(x - s.Rational(1, 2))**2 + s.Rational(1, 4)):
        return False
    # Shift by 1/2; SymPy verifies the remaining full Gaussian integral.
    if not _eq(s.integrate(s.exp(-n * x**2), (x, -s.oo, s.oo)), s.sqrt(s.pi / n)):
        return False
    if not _eq(s.limit(s.log(s.sqrt(s.pi / n)) / n, n, s.oo), 0):
        return False
    return _eq(s.Rational(b - a, 2) * s.exp(1 / s.sqrt(a + b)), s.exp(s.Rational(1, 4)))


def checks(across, down):
    """One thunk per printed clue, with cross references to supplied maps."""
    a, d = across, down
    across_digits = lambda: _nine_digits(a, (15, 18, 19))
    down_digits = lambda: _nine_digits(d, (15, 16, 17))
    return {
        "A1": lambda: _fredholm(a[1]),
        "A2": lambda: _log_integral(a[2]),
        "A4": lambda: bool(s.integer_nthroot(a[4], 3)[1]),
        "A6": lambda: _borwein_factor(a[6]),
        "A7": lambda: a[7]**2 == d[13],
        "A8": lambda: _sophomore_pair(a[8], a[7], d[5]),
        "A11": lambda: _convex(a[11], a[2]),
        "A12": lambda: len(str(a[12])) == 5 and a[12] % 100 == sum(_digits(a[12])[:3]),
        "A15": lambda: across_digits() and bool(s.isprime(a[15])) and bool(s.isprime(a[15] - 6) or s.isprime(a[15] + 6)),
        "A18": lambda: across_digits() and a[18] % 2 == 0,
        "A19": lambda: across_digits() and bool(s.integer_nthroot(a[19], 2)[1]) and a[19] > 20 * 25,
        "D1": lambda: _digit_cubes(d[1]),
        "D3": lambda: _linear_down(d[3]),
        "D5": lambda: _rational_integral(d[5]),
        "D6": lambda: str(d[6]) == str(d[6])[::-1] and d[6] % 11 == 0,
        "D9": lambda: _digits(d[9])[len(str(d[9])) // 2] == sorted(list(a.values()) + list(d.values()))[-1] // sorted(list(a.values()) + list(d.values()))[-2],
        "D10": lambda: _fourier_integer(d[10], a[1], a[2]),
        "D12": lambda: _floor_integral(d[12], a[7] + a[2]),
        "D13": lambda: _gaussian_digits(d[13]),
        "D14": lambda: d[14] % d[3] == 0 or d[3] % d[14] == 0,
        "D15": lambda: down_digits() and not s.isprime(d[15]),
        "D16": lambda: down_digits() and d[16] % 10 == _digits(d[15])[0] - 3,
        "D17": lambda: down_digits() and d[17] % 2 == 1 and len(str(d[17])) == 3 and list(_digits(d[17])) == sorted(set(_digits(d[17]))) and sum(_digits(d[17])) == 20,
    }
