"""Source-faithful 2025 crossnumber clues and their exact certificates.

The SG and UK clue sheets are identical.  SG catalog rows select A3 and D1;
UK rows select a whole direction.  GRID is transcribed from both answer grids.
The certificates verify the printed clue conditions, including deliberately
underdetermined digit clues; the shared contract checks the chosen mark grid
and every crossing.  See the four solutions/pack/R2-2025-* transcripts.
"""

from __future__ import annotations

from math import gcd, isqrt

import sympy as sp


GRID = (
    "#####4######",
    "#####2######",
    "9##2026#####",
    "4915##351###",
    "5#357#3#189#",
    "###18181####",
    "#####9##8###",
    "#####1681###",
    "##248#7#0#4#",
    "##609###639#",
    "##751#####55",
)
ACROSS = {3: 2026, 5: 4915, 7: 351, 9: 357, 11: 189, 12: 18181,
          15: 1681, 17: 248, 21: 609, 22: 639, 23: 751, 24: 55}
DOWN = {1: 422, 2: 945, 3: 2551, 4: 6338, 6: 13, 8: 11, 10: 78,
        13: 191, 14: 8106, 16: 67, 17: 267, 18: 405, 19: 891, 20: 495}
STARTS = {
    "A3": (2, 3), "A5": (3, 0), "A7": (3, 6), "A9": (4, 2),
    "A11": (4, 8), "A12": (5, 3), "A15": (7, 5), "A17": (8, 2),
    "A21": (9, 2), "A22": (9, 8), "A23": (10, 2), "A24": (10, 10),
    "D1": (0, 5), "D2": (2, 0), "D3": (2, 3), "D4": (2, 6),
    "D6": (3, 2), "D8": (3, 8), "D10": (4, 4), "D13": (5, 5),
    "D14": (6, 8), "D16": (7, 6), "D17": (8, 2), "D18": (8, 3),
    "D19": (8, 4), "D20": (8, 10),
}

# Mathematical transcriptions, with overlined concatenated digits written
# as digit strings.  Every ceiling/floor and the divisor in D1 is retained.
CLUES = {
    "A3": "Four-digit abcd: ab=ceiling(Integral(f(x),(x,2,5))), "
          "cd=ceiling(Integral(f(x),(x,2,6))); f>=0 on [2,6]; "
          "Integral(f(x),(x,5,6)) is a positive perfect number; "
          "Integral(f(x),(x,2,5))**2+Integral(f(x),(x,2,6))**2=1076.",
    "A5": "Four-digit abcd: Integral((1+2*exp(a)*x+exp(2*a))*log(x)/"
          "(x+exp(a)+exp(2*a)*x+exp(a)*x**2),(x,0,1))="
          "(4004-2*A3-pi**2)/(b-3); the two-digit cd divides at least one grid answer.",
    "A7": "A7=1 modulo 10; ceiling(A7/10)*Abs(Integral(sin(pi*x)/floor(x)**2,"
          "(x,1,oo)))=2*floor(sqrt(D8))*pi.",
    "A9": "The middle digit is the arithmetic mean of the digits of D4.",
    "A11": "D16*Integral(Abs(sin(x))/(1+(2+5*x**2)**x),(x,-pi,pi))+"
           "A24*Integral(log(sqrt((1-cos(x))**cos(x)/(1-sin(x))**sin(x))),"
           "(x,0,pi)).",
    "A12": "A palindromic number.",
    "A15": "A square number whose first and last digits are the same.",
    "A17": "Each digit is a power of 2. Across A17,A21,A23 contain nine distinct "
           "digits from 0..9, excluding exactly the first digit of A9.",
    "A21": "Three-digit abc: each digit divisible by 3, 9 divides b+c, c>0. "
           "Across A17,A21,A23 contain nine distinct digits from 0..9, "
           "excluding exactly the first digit of A9.",
    "A22": "D20 is the arithmetic mean of A7 and this number.",
    "A23": "First and last digits happy; middle digit unhappy and a prime not "
           "dividing A21; last digit makes gcd(D19,floor(A12/10))>3. "
           "Across A17,A21,A23 contain nine distinct digits from 0..9, "
           "excluding exactly the first digit of A9.",
    "A24": "f(exp(56)), where f(z)=Limit(Integral(Integral(y*t**(x-2)*"
           "exp(t**x-y**x),(t,0,y)),(x,E,z)),y,oo).",
    "D1": "A divisor of 5*Integral(sqrt(sqrt(2*x-2*sqrt(x**2-1))+sqrt(x-1)),"
          "(x,15,80)).",
    "D2": "Second-largest three-digit integer k*a, k integer, a integer such "
          "that exactly one real x has a*x-2026<x**2-a*x and, for every "
          "integrable f, its average on [a*x-2026,x**2-a*x] equals its integral.",
    "D3": "Three consecutive nonnegative integer terms of a geometric sequence "
          "concatenated as a single number.",
    "D4": "Four-digit abcd: Integral(atanh(sqrt(1-x**(a/b)))/(1-x),(x,0,1))="
          "c*pi**k/d for some rational k.",
    "D6": "A prime factor of D10 whose digit reversal is also prime.",
    "D8": "An unhappy prime.",
    "D10": "Greater than Johannes Kepler's age when he died.",
    "D13": "floor(D13/10)=Integral(f(x),(x,-6,6)); f is integrable and "
           "4-periodic; 2*Integral(f(x),(x,2,6))+6*Integral(f(x),(x,5,6))=26; "
           "5*Integral(f(x),(x,2,5))+2*Integral(f(x),(x,5,6))=25.",
    "D14": "Largest positive integer n for which ceiling(Integral(r_n(x),"
           "(x,0,2**n*pi))/pi) has A3+1 hexadecimal digits; "
           "r_1(x)=sqrt(2+2*cos(x)), r_(j+1)(x)=sqrt(2+r_j(x)).",
    "D16": "Two-digit ab: Integral((x+2)*log(x)/(x**k+x**3+x),(x,1,oo))="
           "(pi**a)**(1/3)/(b+k), where k is the smallest prime factor of A3.",
    "D17": "Product of any two digits exceeds the remaining digit. "
           "D17,D18,D19 contain nine distinct digits from 0..9.",
    "D18": "Five more than a square. D17,D18,D19 contain nine distinct "
           "digits from 0..9.",
    "D19": "First digit times second digit is a two-digit ab with a-b equal "
           "to the last digit of D18. D17,D18,D19 contain nine distinct "
           "digits from 0..9.",
    "D20": "Three-digit abc: Abs(Integral(log(x**8-x**7+x**5-x**4+x**3-x+1)"
           "/x,(x,0,1)))=a*pi**2/(b*c).",
}


def _require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def _same(left, right):
    return sp.simplify(sp.trigsimp(left - right)) == 0


def _digits(value):
    return tuple(int(c) for c in str(value))


def _happy(value):
    seen = set()
    while value != 1 and value not in seen:
        seen.add(value)
        value = sum(d*d for d in _digits(value))
    return value == 1


def _across_digits(across):
    digits = ''.join(str(across[k]) for k in (17, 21, 23))
    return len(digits) == 9 and len(set(digits)) == 9 and (
        set(digits) == set('0123456789') - {str(across[9])[0]}
    )


def _down_digits(down):
    digits = ''.join(str(down[k]) for k in (17, 18, 19))
    return len(digits) == 9 and len(set(digits)) == 9


def _across3(across):
    # If p=B-A is perfect, 0<=A<B and A²+B²=1076 imply p²<=1076.
    bound = isqrt(1076)
    perfect = [p for p in range(1, bound+1)
               if sum(sp.divisors(p)) - p == p]
    candidates = []
    for p in perfect:
        first = (sp.sqrt(2*1076-p*p)-p)/2
        second = first+p
        if first >= 0:
            _require(_same(first**2+second**2, 1076), "A3 square identity")
            a, b = int(sp.ceiling(first)), int(sp.ceiling(second))
            if 10 <= a <= 99 and 0 <= b <= 99:
                candidates.append(100*a+b)
    return candidates == [across[3]]


def _across5(across, down):
    a, b, c, d = _digits(across[5])
    x, q = sp.symbols('x q', positive=True)
    kernel = (1+2*q*x+q*q)/(x+q+q*q*x+q*x*x)
    _require(_same(kernel, 1/(x+q)+q/(1+q*x)), "A5 kernel split")
    # Primitive of log(x)/(x+q): log(x)log(1+x/q)+Li_2(-x/q).
    # d Li_2(z)/dx = -log(1-z) z'/z cancels its extra log term.
    _require(_same(sp.diff(sp.log(1+x/q), x), 1/(x+q)), "A5 primitive")
    # J(a)=Li_2(-e^-a)+Li_2(-e^a), J'(a)=-a by
    # (1+e^a)/(1+e^-a)=e^a; J(0)=-pi²/6.
    s = sp.Symbol('s', real=True)
    _require(_same((1+sp.exp(s))/(1+sp.exp(-s)), sp.exp(s)), "A5 reflection")
    _require(2*sp.polylog(2, -1) == -sp.pi**2/6, "A5 base value")
    integral = -sp.Rational(a*a, 2)-sp.pi**2/6
    suffix = 10*c+d
    return (b != 3 and suffix > 0
            and _same(integral, (4004-2*across[3]-sp.pi**2)/(b-3))
            and any(v % suffix == 0 for v in (*across.values(), *down.values())))


def _across7(across, down):
    x = sp.Symbol('x', real=True)
    k = sp.Symbol('k', integer=True, positive=True)
    piece = sp.integrate(sp.sin(sp.pi*x), (x, k, k+1))/k**2
    _require(_same(piece, 2*(-1)**k/(sp.pi*k**2)), "A7 unit interval")
    # The absolutely convergent alternating sum is (2/2²-1)*zeta(2).
    integral = 2/sp.pi*(sp.Rational(2, 4)-1)*sp.zeta(2)
    return (across[7] % 10 == 1 and _same(
        ((across[7]+9)//10)*abs(integral), 2*isqrt(down[8])*sp.pi))


def _across11(across, down):
    x = sp.Symbol('x', real=True)
    w = sp.Symbol('w', positive=True)
    _require(_same(1/(1+w)+1/(1+1/w), 1), "A11 reflection")
    # Positive even base 2+5x² makes the reflected exponent reciprocal.
    first = sp.integrate(sp.sin(x), (x, 0, sp.pi))
    _require(_same(sp.sin(x)**2/(1-sp.cos(x)), 1+sp.cos(x)), "A11 cosine parts")
    _require(_same(sp.cos(x)**2/(1-sp.sin(x)), 1+sp.sin(x)), "A11 sine parts")
    cosine_log = -sp.integrate(1+sp.cos(x), (x, 0, sp.pi))
    sine_log = -sp.integrate(1+sp.sin(x), (x, 0, sp.pi))
    t = sp.Symbol('t', positive=True)
    _require(sp.limit(t*sp.log(t), t, 0, dir='+') == 0, "A11 logarithmic boundaries")
    second = (cosine_log-sine_log)/2
    return _same(across[11], down[16]*first+across[24]*second)


def _across24(across):
    # v=y**x-t**x gives (1/x) int_0^Y (1-v/Y)^(-1/x)e^-v dv, Y=y**x.
    t, y, x = sp.symbols('t y x', positive=True)
    _require(_same(y*t**(x-2)/(x*t**(x-1)), y/(x*t)), "A24 substitution")
    v, Y = sp.symbols('v Y', positive=True)
    p = sp.Symbol('p', positive=True)
    primitive = -Y*(1-v/Y)**(1-p)/(1-p)
    _require(_same(sp.diff(primitive, v), (1-v/Y)**(-p)), "A24 tail primitive")
    # x>=e>2 gives p=1/x<1/2.  On v<=Y/2 the weight is <=sqrt(2),
    # and the remaining mass is bounded by 2Y exp(-Y/2), uniformly in x.
    _require(sp.E > 2, "A24 exponent range")
    _require(sp.limit(2*Y*sp.exp(-Y/2), Y, sp.oo) == 0, "A24 vanishing tail")
    _require(sp.integrate(sp.exp(-v), (v, 0, sp.oo)) == 1, "A24 main mass")
    value = sp.log(sp.exp(56))-sp.log(sp.E)
    return across[24] == value


def _down1(down):
    x = sp.Symbol('x', positive=True)
    a, b = sp.sqrt(x+1), sp.sqrt(x-1)
    _require(_same((a-b)**2, 2*x-2*sp.sqrt(x*x-1)), "D1 inner radical")
    # x>=15: a>b>=0, so the positive inner radical is a-b.
    _require(_same((a-b)+b, a), "D1 outer radical")
    primitive = sp.Rational(4, 5)*(x+1)**sp.Rational(5, 4)
    _require(_same(sp.diff(primitive, x), (x+1)**sp.Rational(1, 4)), "D1 primitive")
    total = sp.simplify(5*(primitive.subs(x, 80)-primitive.subs(x, 15)))
    return total.is_Integer is True and down[1] > 0 and int(total) % down[1] == 0


def _down2(down):
    x, a = sp.symbols('x a', real=True)
    # Test an integrable function equal to 1 on this finite interval and 0
    # outside it: this forces length 1, and that length is sufficient.
    quadratic = x*x-2*a*x+2025
    _require(_same(quadratic, (x-a)**2+2025-a*a), "D2 unique root")
    roots = sp.solve(sp.discriminant(quadratic, x), a)
    values = sorted({abs(int(root))*k for root in roots for k in range(1, 1000)
                     if 100 <= abs(int(root))*k <= 999})
    return len(values) > 1 and down[2] == values[-2]


def _down3(down):
    text = str(down[3])
    for i in range(1, len(text)-1):
        for j in range(i+1, len(text)):
            words = (text[:i], text[i:j], text[j:])
            if any(len(w)>1 and w[0]=='0' for w in words):
                continue
            a, b, c = map(int, words)
            if a > 0 and b*b == a*c and (b > 0 or c == 0):
                return True
    return False


def _down4(down):
    a, b, c, d = _digits(down[4])
    if b == 0 or d == 0 or sp.Rational(a, b) != 2:
        return False
    q = sp.Symbol('q', positive=True)
    x = 2*q/(1+q*q)
    _require(_same(1-x*x, ((1-q*q)/(1+q*q))**2), "D4 radical substitution")
    _require(_same(1-x, (1-q)**2/(1+q*q)), "D4 logarithm factorization")
    _require(_same(sp.diff(x, q)/(1-x), -sp.diff(sp.log((1-q)**2/(1+q*q)), q)),
             "D4 integration by parts")
    # For 0<q<1, atanh((1-q²)/(1+q²))=-log(q).
    z = (1-q*q)/(1+q*q)
    _require(_same((1+z)/(1-z), 1/q**2), "D4 atanh branch")
    # -int[2log(1-q)-log(1+q²)]/q = 2zeta(2)+eta(2)/2.
    value = 2*sp.zeta(2)+(1-sp.Rational(1, 2))*sp.zeta(2)/2
    return _same(value, sp.Rational(c, d)*sp.pi**2)


def _down13(down):
    b, c = sp.symbols('b c')
    solution = sp.solve([2*(b+c)+6*c-26, 5*b+2*c-25], [b, c])
    # [-6,6] consists of three periods of length 4.
    value = 3*(solution[b]+solution[c])
    return down[13]//10 == value


def _down14(across, down):
    n = down[14]
    if n < 2:
        return False
    t = sp.Symbol('t', real=True)
    _require(_same(2*sp.cos(t/2)**2-1, sp.cos(t)), "D14 half angle")
    p = sp.Symbol('p', positive=True)
    _require(_same(sp.diff(2*p*sp.sin(t/p), t), 2*sp.cos(t/p)), "D14 period integral")
    # r_n=2cos(arccos(cos x)/2**n).  There are 2**(n-1) periods.
    # I_n/pi = 2**(2n+1) sin(pi/2**n)/pi.
    # 0 < 2**(n+1)-I_n/pi < pi²/(3*2**n) <= pi²/12 < 1.
    _require(_same(2*p*p/sp.pi*(sp.pi/p)**3/6, sp.pi**2/(3*p)), "D14 sine remainder")
    _require(sp.pi**2 < 10 and sp.Rational(10, 12) < 1, "D14 ceiling bound")
    # Thus ceil(I_n/pi)=2**(n+1); base-16 length=floor((n+1)/4)+1.
    digits = across[3]+1
    return (n+1)//4+1 == digits and (n+2)//4+1 > digits


def _down16(across, down):
    a, b = _digits(down[16])
    k = min(sp.factorint(across[3]))
    if k != 2:
        return False
    x = sp.Symbol('x', positive=True)
    t = sp.Symbol('t', positive=True)
    rational = (x+2)/(x**k+x**3+x)
    _require(_same(rational.subs(x, 1/t)/t**2, (1+2*t)/(1+t+t*t)), "D16 reciprocal")
    _require(_same(sp.diff(sp.log(1+t+t*t), t), (1+2*t)/(1+t+t*t)), "D16 parts")
    _require(_same((1-t)*(1+t+t*t), 1-t**3), "D16 cyclotomic factor")
    # int_0^1 log(1-t**m)/t dt=-zeta(2)/m by u=t**m.
    value = (1-sp.Rational(1, 3))*sp.zeta(2)
    return _same(value, sp.pi**sp.Rational(a, 3)/(b+k))


def _down20(down):
    a, b, c = _digits(down[20])
    if b*c == 0:
        return False
    x = sp.Symbol('x', positive=True)
    polynomial = x**8-x**7+x**5-x**4+x**3-x+1
    _require(_same(polynomial*(1-x**3)*(1-x**5), (1-x)*(1-x**15)), "D20 cyclotomic factor")
    # All factors are positive for 0<x<1, so real logarithms split.
    value = (-sp.Rational(1, 15)-1+sp.Rational(1, 3)+sp.Rational(1, 5))*sp.zeta(2)
    return _same(abs(value), sp.Rational(a, b*c)*sp.pi**2)


def checks(across, down):
    """Return lazy independent clue certificates for the shared dispatcher."""
    def a21():
        a, b, c = _digits(across[21])
        return _across_digits(across) and all(v % 3 == 0 for v in (a, b, c)) and (b+c) % 9 == 0 and c > 0

    def a23():
        a, b, c = _digits(across[23])
        return (_across_digits(across) and _happy(a) and _happy(c) and not _happy(b)
                and sp.isprime(b) and across[21] % b != 0 and gcd(down[19], across[12]//10) > 3)

    def d17():
        a, b, c = _digits(down[17])
        return _down_digits(down) and a*b > c and a*c > b and b*c > a

    def d19():
        a, b, _ = _digits(down[19])
        product = a*b
        return _down_digits(down) and 10 <= product <= 99 and product//10-product % 10 == down[18] % 10

    return {
        'A3': lambda: _across3(across),
        'A5': lambda: _across5(across, down),
        'A7': lambda: _across7(across, down),
        'A9': lambda: 4*_digits(across[9])[1] == sum(_digits(down[4])),
        'A11': lambda: _across11(across, down),
        'A12': lambda: str(across[12]) == str(across[12])[::-1],
        'A15': lambda: isqrt(across[15])**2 == across[15] and str(across[15])[0] == str(across[15])[-1],
        'A17': lambda: _across_digits(across) and all(d in (1, 2, 4, 8) for d in _digits(across[17])),
        'A21': a21,
        'A22': lambda: 2*down[20] == across[7]+across[22],
        'A23': a23,
        'A24': lambda: _across24(across),
        'D1': lambda: _down1(down),
        'D2': lambda: _down2(down),
        'D3': lambda: _down3(down),
        'D4': lambda: _down4(down),
        'D6': lambda: sp.isprime(down[6]) and down[10] % down[6] == 0 and sp.isprime(int(str(down[6])[::-1])),
        'D8': lambda: sp.isprime(down[8]) and not _happy(down[8]),
        # NASA gives 1571-12-27 to 1630-11-15, hence 58 completed years.
        'D10': lambda: down[10] > 1630-1571-1,
        'D13': lambda: _down13(down),
        'D14': lambda: _down14(across, down),
        'D16': lambda: _down16(across, down),
        'D17': d17,
        'D18': lambda: _down_digits(down) and down[18] >= 5 and isqrt(down[18]-5)**2 == down[18]-5,
        'D19': d19,
        'D20': lambda: _down20(down),
    }
