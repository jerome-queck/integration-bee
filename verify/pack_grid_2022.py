"""Exact clue certificates for the 2022/23 Round 2 crossnumber.

The printed clue numbers are not in row-major order: 2 precedes 1 visually.
STARTS therefore records the printed labels explicitly.  Source pages and
the mathematical reductions are transcribed in the matching pack notes.
"""

import sympy as s


PROBLEM_PDFS = ("sources/past/r2/2022/Crossnumber_R2_2022_UK_University_Integration_Bee.pdf",)
MARK_PDF = "sources/past/r2/2022/Mark_Scheme_R2_2022_UK_University_Integration_Bee_(2).pdf"
GRID = (
    "############1#",
    "#########1729#",
    "#########3##13",
    "17062###25####",
    "###5#####7####",
    "#106#3#6996###",
    "###13824######",
    "####4#########",
    "###639600#####",
    "###2#5########",
    "#505#449######",
)
ACROSS = {1: 1729, 3: 17062, 5: 13, 6: 25, 7: 106, 9: 6996,
          10: 13824, 12: 639600, 14: 505, 15: 449}
DOWN = {1: 13579, 2: 191, 4: 6561, 8: 38, 9: 64, 11: 343, 12: 625, 13: 954}
STARTS = {
    "A1": (1, 9), "A3": (3, 0), "A5": (2, 12), "A6": (3, 8),
    "A7": (5, 1), "A9": (5, 7), "A10": (6, 3), "A12": (8, 3),
    "A14": (10, 1), "A15": (10, 5),
    "D1": (1, 9), "D2": (0, 12), "D4": (3, 3), "D8": (5, 5),
    "D9": (5, 7), "D11": (6, 4), "D12": (8, 3), "D13": (8, 5),
}
CLUES = {
    "A1": "x^3+y^3=z^3+w^3 for integers x<z<w<y; x is the final digit of D4 and w is the product of the last two digits of D12.",
    "A3": "A15*D8.",
    "A5": "Difference between the other two smallest numbers.",
    "A6": "f(x)=2*x*(1-x); f_n is the n-fold composition. Integral(f_cuberoot(D9)(x),(x,0,1))=a/b; find a+b.",
    "A7": "Integral(f(x),(x,0,2)), where 5*Integral(f(x),(x,0,1))-2*Integral(f(x),(x,0,2))=23 and 3*Integral(f(x),(x,0,2))-4*Integral(f(x),(x,1,2))=82.",
    "A9": "Palindrome.",
    "A10": "(factorial((1/pi)*Integral(sin(5*x)^2*sin(4*x)^2/sin(x)^2,(x,0,2*pi))))^3.",
    "A12": "Let x=10*cuberoot(D9). Find Integral(ceiling(t)*t*floor(t),(t,0,x)).",
    "A14": "D13-A15.",
    "A15": "f(21), where f(x)+Integral(f(x),(x,1,2))=floor(x)^2+17.",
    "D1": "Digits are in arithmetic progression.",
    "D2": "f(218), where f(x)-Integral(f(t),(t,3,5))=x+D8/2.",
    "D4": "A power of 9.",
    "D8": "4*Integral(f_D13(x),(x,y,y+1)), where f(x)=1-1/x, f_n is the n-fold composition, and y is the second digit of A9.",
    "D9": "n^3 where Integral(1/x-sin(2*x)/(1-cos(2*x)),(x,0,pi/4))=log(pi*sqrt(2)/n).",
    "D11": "A palindrome cube.",
    "D12": "A square number.",
    "D13": "A multiple of A7 whose digits are in decreasing order.",
}


def _power(n, base):
    if n < 1:
        return False
    while n % base == 0:
        n //= base
    return n == 1


def _taxicab(a, d):
    x = d[4] % 10
    w = (d[12] // 10 % 10) * (d[12] % 10)
    if a[1] <= max(x**3, w**3):
        return False
    y, exact_y = s.integer_nthroot(a[1] - x**3, 3)
    z, exact_z = s.integer_nthroot(a[1] - w**3, 3)
    return bool(exact_y and exact_z and x < z < w < y)


def _iterated_quadratic(a, d):
    n, exact = s.integer_nthroot(d[9], 3)
    if not exact or not 1 <= n <= 8:
        return False
    x = s.Symbol("x", real=True)
    f = x
    for _ in range(n):
        f = s.expand(2*f*(1-f))
    integral = s.integrate(f, (x, 0, 1))
    numerator, denominator = integral.as_numer_denom()
    return bool(a[6] == numerator + denominator)


def _linear_integrals(a):
    first, total = s.symbols("first total")
    solution = s.solve([5*first-2*total-23,
                        3*total-4*(total-first)-82], [first, total])
    return bool(a[7] == solution[total])


def _trig_factorial(a):
    # For z=e^(ix), sin(4x)/sin(x)=z^3+z+z^-1+z^-3.
    # Multiplying by sin(5x)^2 gives a finite Laurent polynomial, so
    # integrating over one period extracts exactly its constant coefficient.
    z = s.Symbol("z", nonzero=True)
    quotient = z**3+z+1/z+z**-3
    if s.expand((z-1/z)*quotient-(z**4-z**-4)) != 0:
        return False
    product = s.expand(-((z**5-z**-5)*quotient)**2/4)
    integral_over_pi = 2*product.coeff(z, 0)
    return bool(integral_over_pi.is_Integer and integral_over_pi >= 0
                and a[10] == s.factorial(integral_over_pi)**3)


def _floor_integral(a, d):
    n, exact = s.integer_nthroot(d[9], 3)
    if not exact or n <= 0:
        return False
    k = s.Symbol("k", integer=True, nonnegative=True)
    # On (k,k+1), floor(t)=k and ceiling(t)=k+1; endpoints have zero measure.
    value = s.summation(k*(k+1)*(2*k+1)/2, (k, 0, 10*n-1))
    return bool(a[12] == value)


def _floor_function(a):
    x = s.Symbol("x", real=True)
    # The integral on (1,2) has floor(x)^2=1.  With C=int_1^2 f,
    # integrating f+C=18 gives 2*C=18.
    constant = s.integrate(s.Integer(18), (x, 1, 2))/2
    return bool(a[15] == 21**2+17-constant)


def _affine_function(d):
    x, constant = s.symbols("x constant", real=True)
    expression = x+s.Rational(d[8], 2)+constant
    equation = constant-s.integrate(expression, (x, 3, 5))
    solution = s.solve(equation, constant)[0]
    return bool(d[2] == expression.subs({x: 218, constant: solution}))


def _period_three(a, d):
    x = s.Symbol("x", real=True)
    f = 1-1/x
    f2 = s.cancel(f.subs(x, f))
    f3 = s.cancel(f.subs(x, f2))
    if f3 != x or d[13] <= 0:
        return False
    y = int(str(a[9])[1])
    if y <= 1:  # keeps every intermediate composition away from its poles
        return False
    reduced = (x, f, f2)[d[13] % 3]
    return bool(d[8] == 4*s.integrate(reduced, (x, y, y+1)))


def _logarithmic_limit(d):
    n, exact = s.integer_nthroot(d[9], 3)
    if not exact or n <= 0:
        return False
    x = s.Symbol("x", positive=True)
    primitive = s.log(x)-s.log(s.sin(x))
    derivative = 1/x-s.sin(2*x)/(1-s.cos(2*x))
    if s.trigsimp(s.diff(primitive, x)-derivative) != 0:
        return False
    lower = s.limit(primitive, x, 0, dir="+")
    value = primitive.subs(x, s.pi/4)-lower
    return bool(s.simplify(s.expand_log(value-s.log(s.pi*s.sqrt(2)/n), force=True)) == 0)


def checks(across, down):
    """Return one bounded, independently executable proof per printed clue."""
    a, d = across, down
    return {
        "A1": lambda: _taxicab(a, d),
        "A3": lambda: a[3] == a[15]*d[8],
        "A5": lambda: a[5] == (lambda v: v[1]-v[0])(
            sorted([v for k, v in a.items() if k != 5]+list(d.values()))),
        "A6": lambda: _iterated_quadratic(a, d),
        "A7": lambda: _linear_integrals(a),
        "A9": lambda: str(a[9]) == str(a[9])[::-1],
        "A10": lambda: _trig_factorial(a),
        "A12": lambda: _floor_integral(a, d),
        "A14": lambda: a[14] == d[13]-a[15],
        "A15": lambda: _floor_function(a),
        "D1": lambda: len(set(int(y)-int(x) for x, y in zip(str(d[1]), str(d[1])[1:]))) == 1,
        "D2": lambda: _affine_function(d),
        "D4": lambda: _power(d[4], 9),
        "D8": lambda: _period_three(a, d),
        "D9": lambda: _logarithmic_limit(d),
        "D11": lambda: str(d[11]) == str(d[11])[::-1] and bool(s.integer_nthroot(d[11], 3)[1]),
        "D12": lambda: bool(s.integer_nthroot(d[12], 2)[1]),
        "D13": lambda: d[13] % a[7] == 0 and all(x > y for x, y in zip(str(d[13]), str(d[13])[1:])),
    }
