"""Source-bound checks for the 2023 Round 2 crossnumber.

Down 7 is certified under the explicit grading clarification below; the
printed integral alone does not determine an isolated point value.  The
literal clue remains unchanged, and the counterexample and conditional proof
are recorded in solutions/pack/R2-2023-Crossnumber-Down-1.md.
"""

import sympy as s


GRID = (
    "#10##16#", "#1###4##", "#532416#", "##7##8##",
    "#36#4320", "###53#5#", "####2201", "##610###",
    "##9#####", "271##738", "7#3##295", "#343#146",
)
ACROSS = {1: 10, 2: 16, 3: 532416, 5: 36, 6: 4320, 8: 53,
          9: 2201, 10: 610, 11: 271, 12: 343, 13: 738, 16: 295, 17: 146}
DOWN = {1: 115, 2: 14183, 4: 376, 6: 4320, 7: 250, 10: 69134,
        11: 27, 13: 721, 14: 394, 15: 856}
STARTS = {
    "A1": (0, 1), "A2": (0, 5), "A3": (2, 1), "A5": (4, 1),
    "A6": (4, 4), "A8": (5, 3), "A9": (6, 4), "A10": (7, 2),
    "A11": (9, 0), "A12": (11, 1), "A13": (9, 5),
    "A16": (10, 5), "A17": (11, 5),
    "D1": (0, 1), "D2": (0, 5), "D4": (2, 2), "D6": (4, 4),
    "D7": (4, 6), "D10": (7, 2), "D11": (9, 0),
    "D13": (9, 5), "D14": (9, 6), "D15": (9, 7),
}
CLUES = {
    "A1": "abs(Integral(f(t),(t,0,1))*Integral(f(t),(t,1,2))), where 3*Integral(f(t),(t,0,2))+2*Integral(f(t),(t,1,2))=5 and 2*Integral(f(t),(t,0,1))+3*Integral(f(t),(t,1,2))=4.",
    "A2": "Integral((1-sqrt(log(x)))**a+(1+sqrt(log(x)))**a,(x,0,1)), where a is the final digit of 11 DOWN.",
    "A3": "The six-digit ABCDEF: A*B*C+D*E-F=28, digits 1 through 6 without repetition, A>B>C and D>E.",
    "A5": "limit(floor(Integral(atan(x**n),(x,0,24))),n,oo).",
    "A6": "floor((second largest clue on this crossnumber)/(second smallest clue on this crossnumber)).",
    "A8": "Sum of the three smallest clues.",
    "A9": "a+b+c+d for positive integers a,b,c,d with gcd(a,b)=gcd(c,d)=1 and Integral(log((20*exp(1337*x)+24*exp(420*x))/(20*exp(1337*x)+24*exp(69*x)))/x,(x,0,oo))=log(a/b)*log(c/d).",
    "A10": "A Fibonacci number.",
    "A11": "a+b-1 if Integral(log(x**2)*log(1-x**2),(x,-1,1))=a-pi**2-log(b).",
    "A12": "A power of 7.",
    "A13": "One less than a prime. Across 13,16,17 together contain exactly one of each digit 1 through 9.",
    "A16": "The product of two primes. Across 13,16,17 together contain exactly one of each digit 1 through 9.",
    "A17": "Digit product 24 and digit sum 11. Across 13,16,17 together contain exactly one of each digit 1 through 9.",
    "D1": "Integral(f(t),(t,0,2)), where 3*Integral(f(t),(t,0,2))-7*Integral(f(t),(t,0,1))=23 and 3*Integral(f(t),(t,0,1))-2*Integral(f(t),(t,1,2))=0.",
    "D2": "a+b, gcd(a,b)=1, Integral(x*log(x)**c,(x,0,1))=a/b, c=1 ACROSS.",
    "D4": "f(11), where f(x)+Integral(f(t),(t,-1,1))=3*x**2+x+8.",
    "D6": "Product of the three smallest clues.",
    "D7": "f(0), if limit(Integral(n*f(x)/(25*n**2+x**2),(x,-1,1)),n,0,'+')=50*pi. The printed clue gives no continuity assumption.",
    "D10": "f(0), if f(pi)=866 and Integral((f(x)+f''(x))*sin(x),(x,0,pi))=70000.",
    "D11": "A, if Integral(Integral(...Integral(Integral(z,(z,0,y)),(y,0,x))...,(b,0,a)),(a,0,1))=1/A!: all 26 letters a through z occur in order.",
    "D13": "One more than a factorial. Down 13,14,15 together contain exactly one of each digit 1 through 9.",
    "D14": "Digit product 108 and digit sum 16. Down 13,14,15 together contain exactly one of each digit 1 through 9.",
    "D15": "Digits alternate between even and odd. Down 13,14,15 together contain exactly one of each digit 1 through 9.",
}
CLARIFICATIONS = {
    "D7": "For grading Down 7, f is absolutely integrable on [-1,1] and continuous at 0.",
}


def _eq(left, right):
    return bool(s.simplify(left - right) == 0)


def _digits(value):
    return tuple(map(int, str(value)))


def _nine_digits(values, keys):
    return sorted("".join(str(values[k]) for k in keys)) == list("123456789")


def _linear_across(answer):
    u, v = s.symbols("u v")
    result = s.solve((3 * u + 5 * v - 5, 2 * u + 3 * v - 4), (u, v))
    return _eq(abs(result[u] * result[v]), answer)


def _binomial_log(answer, last_digit):
    # Odd powers of the same principal square root cancel.  The remaining
    # moments follow from t=-log(x): integral log(x)^k=(-1)^k*k!.
    z = s.Symbol("z")
    polynomial = s.expand((1 - z)**last_digit + (1 + z)**last_digit)
    if any(power[0] % 2 for power, coefficient in s.Poly(polynomial, z).terms()):
        return False
    value = sum(coefficient * (-1)**(power[0] // 2) * s.factorial(power[0] // 2)
                for power, coefficient in s.Poly(polynomial, z).terms())
    return _eq(value, answer)


def _digit_equation(answer):
    digits = _digits(answer)
    if sorted(digits) != list(range(1, 7)):
        return False
    a, b, c, d, e, f = digits
    return a > b > c and d > e and a * b * c + d * e - f == 28


def _atan_limit(answer):
    n, u = s.symbols("n u", positive=True)
    if not (_eq(s.limit(s.atan(s.exp(n * u)), n, s.oo), s.pi / 2)
            and _eq(s.limit(s.atan(s.exp(-n * u)), n, s.oo), 0)):
        return False
    # Domination by pi/2 on [0,24] permits the limit exchange.  The limit
    # 23*pi/2 is strictly between adjacent integers, so floor is continuous
    # at the limit (the floor is INSIDE the printed limit).
    value = 23 * s.pi / 2
    return bool(s.floor(value) == answer and value.is_integer is False)


def _frullani(answer):
    # Factor exp(1337*x) from numerator and denominator.  Frullani applies
    # to h(t)=log(1+(6/5)*exp(-t)), whose derivative is integrable.
    x = s.Symbol("x", positive=True)
    h = s.log(1 + s.Rational(6, 5) * s.exp(-x))
    if not _eq(s.diff(h, x), -6 / (5 * s.exp(x) + 6)):
        return False
    if not _eq(s.limit(h, x, s.oo), 0):
        return False
    if not _eq(h.subs(x, 0), s.log(s.Rational(11, 5))):
        return False
    a, b, c, d = 1337 - 69, 1337 - 420, 11, 5
    return s.gcd(a, b) == 1 and s.gcd(c, d) == 1 and a + b + c + d == answer


def _beta_logs(answer):
    p, q = s.symbols("p q", positive=True)
    beta = s.gamma(p) * s.gamma(q) / s.gamma(p + q)
    value = s.simplify(s.diff(beta, p, q).subs({p: s.Rational(1, 2), q: 1}))
    # Shift the trigamma argument using psi_1(z+1)=psi_1(z)-1/z**2.
    value = value.subs(s.polygamma(1, s.Rational(3, 2)),
                       s.polygamma(1, s.Rational(1, 2)) - 4)
    # t=x^2 on the two halves gives this mixed derivative of B(p,q).
    if not _eq(value, 16 - s.pi**2 - 8 * s.log(2)):
        return False
    return 16 + 2**8 - 1 == answer


def _linear_down(answer):
    u, v = s.symbols("u v")
    result = s.solve((-4 * u + 3 * v - 23, 3 * u - 2 * v), (u, v))
    return _eq(result[u] + result[v], answer)


def _log_moment(answer, exponent):
    # The exact gamma moment after x=exp(-t).
    value = s.Rational((-1)**exponent * s.factorial(exponent), 2**(exponent + 1))
    return int(value.p + value.q) == answer


def _fredholm(answer):
    x = s.Symbol("x")
    polynomial = 3 * x**2 + x + 8
    total = s.integrate(polynomial, (x, -1, 1)) / 3
    return _eq(polynomial.subs(x, 11) - total, answer)


def _cauchy_point_value(answer):
    """Certify D7 under CLARIFICATIONS, including the vanishing remainder."""
    n, delta, epsilon, norm = s.symbols("n delta epsilon norm", positive=True)
    x = s.Symbol("x", real=True)
    excess = s.Symbol("excess", nonnegative=True)
    kernel = n / (25 * n**2 + x**2)
    primitive = s.atan(x / (5 * n)) / 5
    if kernel.is_positive is not True or not _eq(s.diff(primitive, x), kernel):
        return False
    mass = primitive.subs(x, 1) - primitive.subs(x, -1)
    full_mass = s.limit(primitive, x, s.oo) - s.limit(primitive, x, -s.oo)
    if not (_eq(full_mass, s.pi / 5)
            and _eq(s.limit(mass, n, 0, dir="+"), full_mass)):
        return False

    # Continuity at zero gives |f(x)-f(0)| < epsilon for |x| < delta <= 1.
    # Positivity bounds its weighted integral there by epsilon*full_mass.
    # On |x| >= delta, write x**2 = delta**2 + excess.  Check the exact
    # inequality kernel <= n/delta**2, not just its limit at one point.
    tail_gap = s.factor(n / delta**2 - kernel.subs(x**2, delta**2 + excess))
    if tail_gap.is_nonnegative is not True:
        return False
    # Absolute integrability gives a finite positive bound norm on
    # integral_-1^1 |f(x)-f(0)| dx.  Thus the entire error is at most
    # epsilon*pi/5 + n*norm/delta**2; first n -> 0+, then epsilon -> 0+.
    error_bound = epsilon * full_mass + n * norm / delta**2
    error_limit = s.limit(s.limit(error_bound, n, 0, dir="+"),
                          epsilon, 0, dir="+")
    return _eq(error_limit, 0) and _eq(full_mass * answer, 50 * s.pi)


def _sine_by_parts(answer):
    x = s.Symbol("x", real=True)
    f = s.Function("f")(x)
    primitive = s.diff(f, x) * s.sin(x) - f * s.cos(x)
    return (_eq(s.diff(primitive, x), (f + s.diff(f, x, 2)) * s.sin(x))
            and answer + 866 == 70000)


def _alphabet_integral(answer):
    x = s.Symbol("x")
    value = x
    for _ in range(26):
        value = s.integrate(value, (x, 0, x))
    return _eq(value.subs(x, 1), 1 / s.factorial(answer))


def checks(across, down):
    """One bounded proof/check per printed clue; no work is done eagerly."""
    a, d = across, down
    smallest = lambda: sorted(list(a.values()) + list(d.values()))[:3]
    return {
        "A1": lambda: _linear_across(a[1]),
        "A2": lambda: _binomial_log(a[2], d[11] % 10),
        "A3": lambda: _digit_equation(a[3]),
        "A5": lambda: _atan_limit(a[5]),
        "A6": lambda: a[6] == sorted(list(a.values()) + list(d.values()))[-2] // smallest()[1],
        "A8": lambda: a[8] == sum(smallest()),
        "A9": lambda: bool(_frullani(a[9])),
        "A10": lambda: a[10] in {int(s.fibonacci(k)) for k in range(2, 30)},
        "A11": lambda: _beta_logs(a[11]),
        "A12": lambda: bool(s.integer_log(a[12], 7)[1]),
        "A13": lambda: _nine_digits(a, (13, 16, 17)) and bool(s.isprime(a[13] + 1)),
        "A16": lambda: _nine_digits(a, (13, 16, 17)) and sum(s.factorint(a[16]).values()) == 2,
        "A17": lambda: _nine_digits(a, (13, 16, 17)) and s.prod(_digits(a[17])) == 24 and sum(_digits(a[17])) == 11,
        "D1": lambda: _linear_down(d[1]),
        "D2": lambda: _log_moment(d[2], a[1]),
        "D4": lambda: _fredholm(d[4]),
        "D6": lambda: d[6] == s.prod(smallest()),
        "D7": lambda: _cauchy_point_value(d[7]),
        "D10": lambda: _sine_by_parts(d[10]),
        "D11": lambda: _alphabet_integral(d[11]),
        "D13": lambda: _nine_digits(d, (13, 14, 15)) and d[13] - 1 in {int(s.factorial(k)) for k in range(1, 10)},
        "D14": lambda: _nine_digits(d, (13, 14, 15)) and s.prod(_digits(d[14])) == 108 and sum(_digits(d[14])) == 16,
        "D15": lambda: _nine_digits(d, (13, 14, 15)) and all((x - y) % 2 for x, y in zip(_digits(d[15]), _digits(d[15])[1:])),
    }
