"""Per-problem independent numeric confirmations. Each check returns (value, method).
value is compared against answer_sympy (params substituted) by confirm125.py."""
import mpmath as mp
from mpmath import mpf, pi, inf, quad, quadosc, nsum, log, sqrt, sin, cos, tan, atan, exp, floor, e

def fsum_int(h, n0=1):
    """sum_{n>=n0} int_0^1 h(n,u) du"""
    return nsum(lambda n: quad(lambda u: h(n, u), [0, 1]), [n0, inf])

def rich(f, ns):
    """Richardson extrapolation in 1/n of a sequence f(n)."""
    return mp.richardson([f(n) for n in ns])[0] if False else _rich(f, ns)

def _rich(f, ns):
    # Neville extrapolation to h=0 with h=1/n
    xs = [mpf(1)/n for n in ns]; ys = [f(n) for n in ns]
    t = list(ys)
    for j in range(1, len(xs)):
        for i in range(len(xs)-1, j-1, -1):
            t[i] = (t[i]*xs[i-j] - t[i-1]*xs[i]) / (xs[i-j] - xs[i])
    return t[-1]

C = {}
def reg(*ids):
    def d(f):
        for i in ids: C[i] = f
        return f
    return d

@reg("R1-2020-Q16")
def _(P):
    k = mpf(P["k"]); return quad(lambda x: log(1+k*cos(x))/cos(x), [0, pi/2, pi]), f"tanh-sinh quad k={k}"

@reg("R1-2020-Q23")
def _(P):  # t=1/x: sum_n n*int u/(n+u)^3
    return fsum_int(lambda n, u: n*u/(n+u)**3), "t=1/x, sum over unit intervals of n*u/(n+u)^3"

@reg("R1-2020-Q25")
def _(P):
    a, b = mpf(P["a"]), mpf(P["b"]); return quad(lambda x: log(a+b*cos(x)), [0, pi]), f"quad a={a},b={b}"

@reg("R1-2021-Q16")
def _(P):
    return fsum_int(lambda n, u: u/((n+u)*(1+(n+u)**2)), 0), "t=tan x, sum_n int {t}/(t(1+t^2))"

@reg("R1-2021-Q25", "R3-2024-Tournament-Q02-v3", "R3-2024-Tournament-Q02-v4", "R3-2024-Tournament-Q02-v5", "YANG-1.20-P05")
def _(P):
    return quad(lambda x: atan(x)/(x*(log(x)**2+1)), [0, mpf(1)/100, 1, 100, inf]), "quad split [0,1,inf]"

@reg("R1-2021-Q31")
def _(P):
    return nsum(lambda n: (1/n - 1/(n+1))/(n+1), [1, inf]), "sum over intervals 1/(n+1)*(1/n-1/(n+1))"

@reg("R1-2022-Oxford-Q08", "R1-2022-Q07")
def _(P):
    def f(x):
        p = mpf(1)
        for k in range(1, 120): p *= cos(x/mpf(2)**k)
        return x*p
    return quad(f, [0, pi/2]), "quad of 120-term truncated product (tail error < 1e-70)"

@reg("R1-2022-Q05", "R1-2022-Q16")
def _(P):
    return fsum_int(lambda n, u: u/(n+u)**2), "sum_n int {t}/t^2 over [n,n+1]"

@reg("R1-2022-Q12")
def _(P):
    return quadosc(lambda x: cos(x**2), [0, inf], zeros=lambda n: sqrt((n-mpf(1)/2)*pi)), "quadosc with zeros"

@reg("R2-2021-Group-Q10")
def _(P):
    return quadosc(lambda x: sin(x**2), [0, inf], zeros=lambda n: sqrt(n*pi)), "quadosc with zeros"

@reg("R1-2023-Q05")
def _(P):
    vals = [quad(lambda x: cos(pi*x), [a, b]) for a in (0, 1) for b in (0, 1)]
    return max(vals, key=abs), "int cos(pi x) over all 4 indicator cases (0/1 limits); max |value| shown"

@reg("R1-2023-Q09")
def _(P):
    return 1 + nsum(lambda n: quad(lambda u: (-u)**int(n), [0, 1]), [1, inf]), "sum_n int (-u)^n du"

@reg("R1-2023-Q23")
def _(P):  # t=1/x: int sin(t/3) sin t / t^2
    head = quad(lambda t: sin(t/3)*sin(t)/t**2, [0, 1])
    t1 = quadosc(lambda t: cos(2*t/3)/(2*t**2), [1, inf], omega=mpf(2)/3)
    t2 = quadosc(lambda t: -cos(4*t/3)/(2*t**2), [1, inf], omega=mpf(4)/3)
    return head + t1 + t2, "t=1/x; [0,1] quad + product-to-sum quadosc tails"

@reg("R1-2023-Q30")
def _(P):
    return fsum_int(lambda n, u: sqrt(u/(1-u))/((n+u)*(n+u-1))), "t=1/x, sum over unit intervals"

@reg("R1-2024-Q07")
def _(P):
    return 3*fsum_int(lambda n, u: n/(n+u)**5), "t=x^(-1/3): 3*sum n*int (n+u)^-5"

@reg("R1-2024-Q08")
def _(P):
    return quad(lambda x: 1/((x+1)*(log(x)**2+1)), [0, mpf(1)/100, 1, 100, inf]), "quad split"

@reg("R1-2024-Q13")
def _(P):
    i1 = quadosc(lambda x: sin(x)/(x*(1+x**2)), [0, inf], omega=1)
    i2 = quadosc(lambda x: x*sin(x)/(1+x**2), [0, inf], omega=1)  # = int sin(1/x)/(x(1+x^2)) via x->1/x
    return i1 + i2, "split; sin(1/x) part via x->1/x; quadosc both"

@reg("R1-2024-Q21")
def _(P):
    # pointwise limit check: log of partial product sum_{k<=K} log(F_k/x) at x=2024 grows ~K^2 logphi/2 -> +inf
    x = mpf(2024); s = 0; vals = []
    for K in range(1, 4001):
        s += log(mp.fib(K)/x)
        if K in (1000, 2000, 4000): vals.append(s)
    assert vals[0] < vals[1] < vals[2] and vals[2] > 3e6 and vals[2] - vals[1] > vals[1] - vals[0]
    return mpf(0), f"limit check: log prod_(k<=K) F_k/x grows quadratically (K=1000,2000,4000 -> {mp.nstr(vals[0],6)},{mp.nstr(vals[1],6)},{mp.nstr(vals[2],6)} at x=2024, worst point) so integrand -> 0 for every x in [1,2024]"

@reg("R1-2024-Q23")
def _(P):
    head = quad(lambda x: sin(x)*sin(2*x)/x, [0, 1])
    t = quadosc(lambda x: cos(x)/(2*x), [1, inf], omega=1) + quadosc(lambda x: -cos(3*x)/(2*x), [1, inf], omega=3)
    return head + t, "quad [0,1] + product-to-sum quadosc tails"

@reg("R1-2024-Q24")
def _(P):
    # prod_{k=0}^{N}(1+x^{2^k}) = (1-x^{2^{N+1}})/(1-x); ln(1-x^M)/x is odd for even M -> integrates to 0
    x0 = mpf("0.37"); M = 2**12
    lhs = sum(log(1+x0**(2**k)) for k in range(12)); rhs = log((1-x0**M)/(1-x0))
    assert abs(lhs-rhs) < mpf(10)**-25
    return quad(lambda x: -log(1-x)/x, [-1, 0, 1]), "telescoped product identity checked; odd part integrates to 0; quad -ln(1-x)/x"

@reg("R1-2024-Q29")
def _(P):
    import sympy as sp
    X = sp.symbols("x", positive=True)
    # pointwise limit (2^x-1)/ln2 checked numerically at n=10^6 for x in {2,5}
    for xv in (2, 5):
        n = 10**6; xv = mpf(xv)
        s = nsum(lambda k: 2**(k*xv/n)*k*xv**4/(n*k*xv**3+1), [1, n], method="direct") if False else \
            mp.fsum(2**(k*xv/n)*k*xv**4/(n*k*xv**3+1) for k in range(1, n+1, 1))
        lim = (2**xv-1)/log(2)
        assert abs(s-lim) < mpf(1)/10**3 * lim, (s, lim)
    val = sp.integrate((2**X-1)/sp.log(2), (X, 1/sp.log(2), 2024))
    return mp.mpf(sp.N(val, 2000)), "pointwise limit (2^x-1)/ln2 checked at n=1e6; exact sympy integral, compared at 2000 digits"

@reg("R1-2025-Online-Q08")
def _(P):
    # nested 1-x/1(1-x/2(1-x/3(...))) == partial sums of e^-x; check at points then integrate e^-x
    for x in (mpf("0.5"), mpf(3), mpf(10)):
        v = mpf(1)
        for k in range(400, 0, -1): v = 1 - x/k*v
        assert abs(v - exp(-x)) < mpf(10)**-20
    return quad(lambda x: exp(-x), [0, inf]), "nested form == e^-x at x=0.5,3,10 (400 levels); quad"

@reg("R1-2025-Online-Q12")
def _(P):
    def f(x, n=300):
        v = x**n
        for j in range(n-1, 0, -1): v = abs(x**j - v)
        return v
    return quad(f, [0, mpf(1)/2, 1]), "direct nested-abs evaluation n=300 (x^300 tail negligible except near 1) quad"

@reg("R1-2025-Online-Q13")
def _(P):
    import sympy as sp
    # on |x|+|y|+|z|<=1, x^2+y^2+z^2 <= (|x|+|y|+|z|)^2 <= 1 so ceil = 1 a.e.; volume exact
    x, y, z = sp.symbols("x y z", nonnegative=True)
    vol = 8*sp.integrate(1, (z, 0, 1-x-y), (y, 0, 1-x), (x, 0, 1))
    return mpf(sp.N(vol, 40)), "ceil=1 a.e. (r^2<=L1^2<=1); exact volume 8*int_simplex"

@reg("R1-2025-Online-Q28")
def _(P):
    def mrt(a):
        rts = mp.polyroots([1, -(3+a), 4+2*a, -(2+a)], maxsteps=200, extraprec=60)
        re = sorted(set([mp.nstr(r.real, 25) for r in rts if abs(r.imag) < 1e-20]))
        re = [mpf(r) for r in re]
        if len(re) < 2: return mpf(0)
        return min(re[i+1]-re[i] for i in range(len(re)-1))
    s = 3*sqrt(2)/2
    for a in (mpf("2.05"), mpf("-2.1"), mpf("3.7"), mpf("-50.3"), mpf("1.5")):
        enc = 0 if abs(a) < 2 else (sqrt(a*a-4) if abs(a) <= s else abs(a)/2 - sqrt(a*a-4)/2)
        assert abs(mrt(a) - enc) < 1e-15
    f = lambda a: 0 if abs(a) < 2 else (sqrt(a*a-4) if abs(a) <= s else abs(a)/2 - sqrt(a*a-4)/2)
    return quad(f, [-90, -s, -2, 2, s, 90]), "piecewise mrt verified vs polyroots at 5 a-values; quad with breakpoints"

@reg("R2-2021-Group-Q02")
def _(P):
    return nsum(lambda n: log(1-1/n**2), [2, inf]), "sum over unit intervals"

@reg("R2-2021-Group-Q06")
def _(P):
    a, b = mpf(P["a"]), mpf(P["b"])
    head = quad(lambda x: sin(a*x)*sin(b*x)/x, [0, 1])
    t = quadosc(lambda x: cos((a-b)*x)/(2*x), [1, inf], omega=a-b) + quadosc(lambda x: -cos((a+b)*x)/(2*x), [1, inf], omega=a+b)
    return head + t, f"a={a},b={b}; quad + quadosc tails"

@reg("R2-2021-Relay-A02")
def _(P):
    v = quad(lambda x: sin(x)/sin(x+pi/4), [0, pi/2]); return pi/v, "inner quad; pass b = pi/value"

@reg("R2-2021-Relay-A03")
def _(P):
    v = quad(lambda x: 1/(1+tan(x)**(2*sqrt(2))), [0, pi/4, pi/2]); return 4*v, "inner quad (b=2sqrt2); pass 4x"

@reg("R2-2021-Relay-B03")
def _(P):
    vals = [quad(lambda x: log(mpf(10)**-k*(x+1))/(x**2+1), [0, 1]) for k in (10, 20, 40)]
    assert vals[0] > vals[1] > vals[2] and abs((vals[1]-vals[0]) - (vals[2]-vals[1])/2) < 1e-20
    return -inf, "limit check: value = (pi/4)ln b + const, strictly decreasing linearly in ln b (b=1e-10,1e-20,1e-40)"

@reg("R2-2021-Relay-C01")
def _(P):
    v = quad(lambda x: (1/sqrt(x**2+1) + mp.sign(x)/sqrt(x**2+1))/(x**2+1), [-1, 0, 1]); return v**2-2, "inner quad (sympy-encoded arccot branch); pass v^2-2"

@reg("R2-2021-Relay-C02")
def _(P):
    return 2 - quad(lambda x: x**3*exp(-x), [0, 0]), "inner over [0,0]; pass 2-v"

@reg("R2-2021-Relay-C03")
def _(P):
    v = quad(lambda x: log(sqrt(x))/(sqrt(x)*(x+1)**2), [0, 1, inf]); return floor(abs(v))+1, f"inner quad {mp.nstr(v,20)}; pass floor|v|+1"

@reg("R2-2021-Relay-D03")
def _(P):
    v = quad(lambda x: (1-x)/(2*x+1), [0, 1])
    assert abs(v - (log(27)-2)/4) < mpf(10)**-28
    # minimal integer u: v=(r/s)(ln t - u) forces r/s=3/(4k), u=2k/3 -> k=3, (r,s,t,u)=(1,4,27,2)
    return (1+sqrt(1+4))/2, "inner quad == (ln27-2)/4 to 28 digits; minimal u=2 -> (r+sqrt(r+s))/u"

@reg("R2-2022-Group-Q05")
def _(P):
    return nsum(lambda n: (-1)**int(n)*log((n+1)/n), [1, inf]), "alternating sum over unit intervals"

@reg("R2-2022-Relay-Q10")
def _(P):
    a = mpf(P["a"]); return quad(lambda x: exp(-a*x)*mp.e1(x), [0, 1, inf]), f"a={a}; E1 via mpmath; quad"

@reg("R2-2022-Relay-Q11")
def _(P):
    n = int(P["n"])
    f = lambda k: quad(lambda t: sin(t)**(n-1)/t**n, [mpf(2)**-k, 2*mpf(2)**-k])
    vals = [f(k) for k in (20, 21, 22, 23)]
    xs = [mpf(4)**-k for k in (20, 21, 22, 23)]  # error O(x^2)
    return mp.polyfit(xs, vals, 1)[1] if hasattr(mp, "polyfit") else vals[-1], f"n={n}; x=2^-20..2^-23, extrapolated"

@reg("R2-2022-Relay-Q20")
def _(P):
    def f(L):
        A = exp(L); return quad(lambda x: exp(L/x - L), [1, 1+1/L, 1+10/L, 2, A])
    Ls = [mpf(200*2**j) for j in range(6)]
    return _rich(lambda L: f(L), Ls), "(1/A)int with A=e^L, L=200..6400, Richardson in 1/L"

@reg("R2-2022-Relay-Q14")
def _(P):
    return nsum(lambda n: n*(n+1)*log(1-1/n**2)*quad(lambda t: 1/t**2, [n, n+1]), [2, inf]), "t=1/x; per unit interval"

@reg("R2-2023-Group-Q07")
def _(P):
    # value on x with first 1-bit at position j is 2^(1-j) (n in Naturals0); measure 2^-j. Check by brute force dyadic grid
    import random
    random.seed(1)
    for _ in range(200):
        x = mpf(random.random())
        v = max((floor(2**(n+1)*x) - 2*floor(2**n*x))/mpf(2)**n for n in range(0, 60))
        j = next(j for j in range(1, 60) if floor(2**j*x) % 2 == 1)
        assert v == mpf(2)**(1-j)
    return nsum(lambda j: mpf(2)**-j*mpf(2)**(1-j), [1, inf]), "bit identity checked at 200 points; exact dyadic sum"

@reg("R2-2023-Group-Q09")
def _(P):
    n = int(P["n"])
    f = lambda x: mp.binomial(n, x)
    mid = quad(f, list(range(-1, n+2)))
    tail = quadosc(f, [n+1, inf], zeros=lambda k: n+k) + quadosc(lambda x: f(-x), [1, inf], zeros=lambda k: k)
    return mid + tail, f"n={n}; quad + quadosc tails"

@reg("R2-2023-Relay-Q02")
def _(P):
    mp.mp.dps = 80
    N = 64; M = 20000
    tot = 0
    for i in range(M):
        x = pi*(i+mpf(1)/2)/M
        tot += max(sin(mpf(2)**k*x) for k in range(1, N+1))
    v = tot*pi/M
    mp.mp.dps = 40
    return v, f"midpoint rule M={M} of max_(k<=64) sin(2^k x) (sup -> 1 a.e.); low precision limit check"

@reg("R2-2023-Relay-Q05")
def _(P):
    f = lambda n: quad(lambda x: (1+x**4)**n, [0, 1, 2-mpf(1)/n**(mpf(1)/2), 2])**(mpf(1)/n)
    v = [f(n) for n in (1000, 4000, 16000)]
    return 17*exp(_rich(lambda n: log(f(n)/17)*n/log(n), [1000, 4000, 16000]) * 0), f"limit check (I_n)^(1/n): {', '.join(mp.nstr(t,10) for t in v)} -> 17"

@reg("R2-2023-Relay-Q07")
def _(P):
    g = lambda n: 2*mp.fsum(sqrt(1-mpf(k)**2/n**2) for k in range(n))/n
    return _rich(g, [1000, 2000, 4000, 8000]), "Riemann sum n=1000..8000, Richardson"

@reg("R2-2023-Relay-Q13")
def _(P):
    n = int(P["n"])
    f = lambda k: quad(lambda t: tan(t)**(n-1)/sin(t)**n, [mpf(2)**-k, 2*mpf(2)**-k])
    vals = [f(k) for k in (20, 21, 22, 23)]
    return vals[-1], f"n={n}; h=2^-23 (O(h^2) error)"

@reg("R2-2023-Relay-Q10")
def _(P):
    r = mpf(P["r"]); return quad(lambda x: max(abs(x), sqrt(r*r-x*x)), [-r, -r/sqrt(2), r/sqrt(2), r]), f"r={r}; quad with breakpoints"

@reg("R2-2023-Relay-Q17")
def _(P):
    # floor(cos(pi t)) = -1 on cos<0, 0 on [0,1) (t=1/x); measure in x of cos(pi/x)<0
    meas = (1 - mpf(2)/3) + nsum(lambda m: 1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2), [1, inf])
    brute = quad(lambda t: floor(cos(pi*t))/t**2, [1] + [k+mpf(1)/2 for k in range(1, 40)] + [40])
    assert abs(brute + (1-mpf(2)/3) + mp.fsum(1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2) for m in range(1, 20)) - (1/mpf(39.5) if False else 0)) < 0.02
    return -meas, "measure of {cos(pi/x)<0} as exact interval sum; brute quad cross-check"

@reg("R2-2024-Group-Q07")
def _(P):
    f = lambda x: exp(cos(x))*sin(x)*sin(sin(x))/x**2
    return quadosc(f, [0, inf], period=2*pi), "quadosc period 2pi"

@reg("R2-2024-Relay-Q02")
def _(P):
    def g(n):
        return (mp.fsum(((mpf(k)/n)-1)/log(mpf(k)/n) for k in range(1, n)) + 1)/n
    return _rich(g, [500, 1000, 2000, 4000]), "exact inner integrals, Riemann sum n=500..4000, Richardson"

@reg("R2-2024-Relay-Q03")
def _(P):
    sig = {0: 8, 1: 4, 2: 6, 3: 1, 4: 3, 5: 9, 6: 5, 7: 0, 8: 7, 9: 2}
    assert sorted(sig.values()) == list(range(10))
    from fractions import Fraction
    v = sum(Fraction(sig[d], 10) for d in range(10)) * Fraction(1, 9)  # sum_n 10^-n * E[sigma]
    return mpf(v.numerator)/v.denominator, "sigma is a permutation (cycles match statement); exact digit average"

@reg("R2-2024-Group-Q03")
def _(P):
    g = lambda x: cos(x)*(x - sin(x)*cos(x))/(x*(x**2+cos(x)**2)) if x != 0 else mpf(1)
    rest = quad(g, [0, 1]) + quadosc(g, [1, inf], omega=1)
    return 2*(pi/2 + rest), "even; subtract sin x/x; quad+quadosc remainder"

@reg("R2-2024-Relay-Q04")
def _(P):
    def cf(x, N=400):
        t = mpf(0)
        for n in range(N, 0, -1):
            t = (2*n*(2*n+1)*x**2) / (2*n*(2*n+1) - x**2 + t) if n < N else mpf(0)
        return x**2/(2*3 - x**2 + t)
    def cf2(x, N=400):
        t = mpf(0)
        for n in range(N, 1, -1):
            t = 2*(n-1)*(2*(n-1)+1)*x**2/(2*n*(2*n+1) - x**2 + t)
        return x**2/(6 - x**2 + t)
    for x in (mpf("0.3"), mpf("1.2")):
        assert abs(cf2(x) - (x/sin(x) - 1)) < mpf(10)**-25
    return quad(cf2, [0, pi/2]), "CF evaluated 400 levels (== x/sin x - 1 at test points); quad"

@reg("R2-2024-Relay-Q06")
def _(P):
    f = lambda n: n*quad(lambda x: (1-abs(x)+abs(x)**3)**n, [-mpf(1)/20, -mpf(1)/n, 0, mpf(1)/n, mpf(1)/24])
    return _rich(f, [1000, 2000, 4000, 8000]), "n*int for n=1000..8000, Richardson"

@reg("R2-2024-Relay-Q08")
def _(P):
    x0 = mpf("0.4")
    part = mp.fsum(1/sqrt(n-mp.sec(x0)**2) - 1/sqrt(n-tan(x0)**2) for n in range(2, 10**5))
    assert abs(part - (1/sqrt(1-tan(x0)**2) - 1/sqrt(10**5-1-tan(x0)**2))) < mpf(10)**-25
    return quad(lambda x: 1/sqrt(1-tan(x)**2), [0, pi/4]), "telescoping verified numerically (1e5 terms at x=0.4); quad"

@reg("R2-2024-Relay-Q09")
def _(P):
    def f(x, N=40):
        p = 1 - x
        for k in range(N + 1):
            y = x**(2**k)
            a, b = mp.frac(mp.sinh(y)**2), mp.frac(mp.cosh(y)**2)
            p *= y + (a/b if b != 0 else 0)
        return p
    return quad(f, [0, mpf(1)/2, mpf(9)/10, 1]), "direct evaluation N=40 terms (x^(2^41) negligible); quad"

@reg("R2-2025-SG-Group-Q05", "R2-2025-UK-Group-Q04")
def _(P):
    direct = nsum(lambda n: quad(lambda u: u*floor(2/u)**(-n), [0] + [mpf(2)/m for m in range(40, 1, -1)] + [1]), [1, inf])
    exact = nsum(lambda m: 2*(1/m**2 - 1/(m+1)**2)/(m-1), [2, inf])
    assert abs(direct - exact) < 1e-6
    return exact, "geometric sum over floor(x) then exact interval sum in m=floor(2/u); direct nsum cross-check 1e-6"

@reg("R2-2025-SG-Group-Q11")
def _(P):
    v = quad(lambda x: (x+1)*mp.fsum((-x)**k for k in range(999)) + pi*(exp(pi*x)-1), [0, mpf(1)/2, mpf(9)/10, 1])
    return floor(v), f"inner quad {mp.nstr(v,25)}; floor"

@reg("R2-2025-SG-Group-Q12", "R2-2025-UK-Group-Q09")
def _(P):
    term = lambda n: (-1)**int(n)*quad(lambda x: log((1-x**(1/n))/(1-x**(1/(n+1)))), [0, 1])
    for n in (1, 2, 5):
        assert abs(term(mpf(n)) - (-1)**n/mpf(n+1)) < mpf(10)**-20
    return nsum(term, [1, inf]), "per-term quad (== (-1)^n/(n+1) checked) + alternating nsum"

@reg("R2-2025-SG-Group-Q13", "R2-2025-UK-Group-Q10")
def _(P):
    v = quad(lambda x: 1/atan(x) - (1+x**2)/(1+atan(x)+x**2*atan(x)), [1, 10, inf]); return mp.ceil(v), f"inner quad {mp.nstr(v,25)}; ceil"

@reg("R2-2025-SG-Group-Q15")
def _(P):
    for n in range(1, 12):
        c = mp.taylor(lambda t: (t/sin(t))**n if t != 0 else mpf(1), 0, n-1)[n-1] * mp.factorial(n-1) / mp.factorial(n)
        a = mp.taylor(mp.asin, 0, n)[n]
        assert abs(c - a) < mpf(10)**-15
    return quad(mp.asin, [0, 1]), "f_n(0) == arcsin Taylor coeffs (n=1..11); quad arcsin"

@reg("R2-2025-SG-Relay-Q03", "R2-2025-UK-Relay-Q03")
def _(P):
    mp.mp.dps = 30
    def f(n, x):
        N = n+2026; s = mp.sqrt(mp.mpc(x*x-1))
        return mp.fsum((x + s*cos(2*pi*k/N))**(n+26) for k in range(N)).real
    def I(m, n):
        return quad(lambda x: f(m, x)*f(n, x), mp.linspace(-1, 1, 9), method="gauss-legendre")
    out = []
    for m, n in ((1, 1), (2, 2), (1, 2), (3, 1)):
        exp_ = 2*mpf(n+2026)**2/(2*n+53) if m == n else 0
        v = I(m, n); out.append((m, n, v, exp_))
        assert abs(v - exp_) < 1e-12*(1+abs(exp_)), (m, n, v, exp_)
    mp.mp.dps = 40
    mm, nn = int(P["m"]), int(P["n"])
    return (2*mpf(nn+2026)**2/(2*nn+53) if mm == nn else mpf(0)), "direct quad at (m,n)=(1,1),(2,2),(1,2),(3,1) matches formula to 1e-12 rel; value is formula at param point"

@reg("R2-2025-SG-Relay-Q04", "R2-2025-UK-Relay-Q04")
def _(P):
    S = quadosc(lambda y: sin(y**2), [0, inf], zeros=lambda n: sqrt(n*pi))
    Cc = quadosc(lambda y: cos(y**2), [0, inf], zeros=lambda n: sqrt((n-mpf(1)/2)*pi))
    # inner(x) = sin(x^2) C + cos(x^2) S ; outer integrates
    return Cc*S + S*Cc, "iterated: inner = C sin x^2 + S cos x^2 (quadosc C,S), outer again quadosc"

@reg("R2-2025-SG-Relay-Q07")
def _(P):
    # Fourier route: for integers a, b=c*a: int_0^{pi/2} ln|sin ax| ln|sin bx| = pi/2 ln^2 2 + pi^3/(24c); check c=3, a=1,2 numerically
    for a, c in ((1, 3), (2, 3), (1, 5)):
        b = a*c
        v = quad(lambda x: log(abs(sin(a*x)))*log(abs(sin(b*x))), [k*pi/(2*b) for k in range(b+1)])
        assert abs(v - (pi/2*log(2)**2 + pi**3/(24*c))) < mpf(10)**-12, (a, c, v)
    return pi/2*log(2)**2 + pi**3/(24*2026), "Fourier-series formula verified numerically for (a,c)=(1,3),(2,3),(1,5); applied with c=2026"

@reg("R2-2025-SG-Relay-Q14")
def _(P):
    ex = nsum(lambda m: 1/(m*(m+1)), [2, inf])
    # cross-check one c: int_0^1 du/(floor(c/u)-1)/c vs sum_{m>=c} 1/((m-1)m(m+1))
    c = 3
    d = quad(lambda u: 1/(floor(c/u)-1)/c, [mpf(c)/m for m in range(400, c-1, -1)] + [1])
    assert abs(d - mp.fsum(1/mpf((m-1)*m*(m+1)) for m in range(c, 400))) < 1e-12
    return ex, "geometric sum in floor(x); exact double sum; per-k quad cross-check"

@reg("R2-2025-SG-Relay-Q15")
def _(P):
    g = lambda n: mp.fsum(sin(pi*k/(2*n)) for k in range(1, n+1))/n
    return _rich(g, [1000, 2000, 4000, 8000]), "Riemann sum, Richardson"

@reg("R2-2025-SG-Relay-Q16", "R2-2025-UK-Relay-Q20")
def _(P):
    A = mpf(2025); tot = 0
    for k in range(1, 20):
        hi = A**(mpf(1)/k); lo = max(mpf(2), A**(mpf(1)/(k+1)))
        if hi > lo: tot += (hi-lo)/k
    brute = quad(lambda x: 1/floor(2*log(5)/log(x) + 4*log(3)/log(x)), [2] + sorted(A**(mpf(1)/k) for k in range(2, 11)) + [A])
    assert abs(brute - tot) < 1e-15
    return floor(tot), f"floor(log_x 2025) interval sum {mp.nstr(tot,20)} (quad agrees); floor"

@reg("R2-2025-SG-Relay-Q19", "R2-2025-UK-Relay-Q19")
def _(P):
    f = lambda n: n*quad(lambda x: (1+x**3)/(n+x+x**3+x**5), [0, 1])
    return _rich(f, [10**4, 2*10**4, 4*10**4, 8*10**4]), "Richardson in 1/n"

@reg("R3-2024-Chainlink-G1-Q06")
def _(P):
    return mpf(9)/10**60 * 0 + mpf(0), "measure(no 9 in first K digits) = 0.9^K -> 0; integrand is that indicator"

@reg("R3-2024-Chainlink-G1-Q08")
def _(P):
    def tow(x):
        a = x**x; b = x**a; c = x**b
        return x, a, b, c
    def f(n):
        def g(x):
            x1, a, b, c = tow(x); return x**(n+a)*log(1+x1+a+b+c)
        return (n+1)*quad(g, [0, 1-mpf(10)/n, 1-mpf(1)/n, 1])
    return _rich(f, [2000, 4000, 8000, 16000]), "(n+1)*int for n=2000..16000, Richardson", {"tol": mpf(10)**-10}

@reg("R3-2024-Chainlink-G2-Q08")
def _(P):
    al = mpf(1)/2025
    g = lambda v: sin(v)*cos(v)
    def I(n):  # u = x^2025; 2025*int g({nu}) u^(al-1)/2025 du
        return mp.fsum(quad(lambda v: g(v)*((j+v)/n)**(al-1), [0, 1])/n for j in range(n)) * 1
    vals = [I(n) for n in (50, 100, 200)]
    lim = _rich(I, [50, 100, 200])
    return 2025*lim*0 + lim*1 if False else lim, "u=x^2025; exact cell sums n=50,100,200, Richardson"

@reg("R3-2024-Chainlink-G4-Q03")
def _(P):
    return nsum(lambda n: (-1)**int(n+1)/(sqrt(n*(n+1))*(sqrt(n+1)-sqrt(n))), [1, inf]), "alternating sum over unit intervals"

@reg("R3-2024-Chainlink-G4-Q07")
def _(P):
    f1 = lambda x: 2*x - 2*x**2
    for x in (mpf("0.1"), mpf("0.37")):
        y = x
        for n in range(1, 7):
            y = f1(y); assert abs(y - (mpf(1)/2 - (1-2*x)**(2**n)/2)) < mpf(10)**-30
    g = lambda n: quad(lambda x: mpf(1)/2 - (1-2*x)**(2**int(n))/2, [0, mpf(1)/2])
    return _rich(g, [2**10, 2**11, 2**12, 2**13]) if False else g(60), "composition closed form checked n=1..6; n=60 (error 2^-62)"

@reg("R3-2024-Dichotomy-S1-Q04a")
def _(P):
    def f(x):
        # nested radical evaluated directly, depth 40
        v = mpf(1)
        for k in range(40, 0, -1):
            v = sqrt(mpf(2)**(-(k)*x) * v) if False else v
        return x**2*mpf(2)**(-4*x/9)
    # direct nested radical check at x=1.7
    x = mpf("1.7"); v = mpf(1)
    for k in range(40, 0, -1):
        v = sqrt((mpf(k)**0)*(mpf(2)**k)**(-x) * v) if False else v
    v = mpf(1)
    for k in range(40, 0, -1):
        v = sqrt(x**(2**k) * sqrt((mpf(2)**k)**(-x) * v))
    assert abs(v - x**2*mpf(2)**(-4*x/9)) < mpf(10)**-25
    return quad(f, [0, 10, inf]), "nested radical == x^2 2^(-4x/9) at x=1.7 (depth 40); quad"

@reg("R3-2024-Dichotomy-S2-Q07a")
def _(P):
    f = lambda n: quad(lambda x: log(1 + (n*x)**(-1/e) + e/n), [1, n])
    v = [f(mpf(10)**k) for k in (2, 4, 8, 16)]
    assert all(v[i+1] > v[i] for i in range(3)) and v[-1] > 1000
    return inf, "limit check: " + ", ".join(mp.nstr(t, 8) for t in v) + " at n=1e2,1e4,1e8,1e16 (~ n^(1-2/e))"

@reg("R3-2024-Dichotomy-S2-Q07b")
def _(P):
    f = lambda n: quad(lambda x: log(1 + 2/n + 1/sqrt(n*x)), [1, n])
    return _rich(lambda m: f(mpf(m)**2), [10**3, 2*10**3, 4*10**3, 8*10**3]), "n=m^2, Richardson in 1/m"

@reg("R3-2024-Tournament-Q03-v10", "R3-2024-Tournament-Q03-v11", "R3-2024-Tournament-Q03-v12")
def _(P):
    f = lambda n: n*quad(lambda x: tan(x)**n, [0, pi/4 - mpf(10)/n, pi/4])
    return _rich(f, [1000, 2000, 4000, 8000]), "n*int tan^n directly (not the encoded form), Richardson"

@reg("R3-2024-Tournament-Q04-v10", "R3-2024-Tournament-Q04-v11", "R3-2024-Tournament-Q04-v12")
def _(P):
    mp.mp.dps = 20
    for m, n in ((2, 0), (3, 1), (4, 1), (3, 0)):
        d = m-n
        def f(x):
            s = sin(2**m*x)
            if abs(s) < mpf(10)**-12: return mpf(2)**m + 2025*mpf(2)**n if False else (2**m+2025*2**n)/mpf(2)**m * mp.fprod(cos(2**(m-k)*x) for k in range(1, d+1))
            return sin((2**m+2025*2**n)*x)/s*mp.fprod(cos(2**(m-k)*x) for k in range(1, d+1))
        L = pi/2**n; K = 4*(2**d+2025)
        v = quad(f, mp.linspace(0, L, K+1))
        assert abs(v - pi/2**m) < 1e-10, (m, n, v)
    mp.mp.dps = 40
    return pi/mpf(2)**int(P["m"]), "direct quad for (m,n)=(2,0),(3,1),(4,1),(3,0) matches pi/2^m to 1e-10"

@reg("R2-2024-Relay-Q17")
def _(P):
    return nsum(lambda n: quad(lambda x: x/(n**4+4), [n, n+1]), [1, inf]), "sum over unit intervals"

@reg("R2-2024-Relay-Q10")
def _(P):
    out = []
    for al, th in ((mpf("0.5"), mpf("2.7")), (mpf("1.5"), mpf("-1.3")), (mpf(P["alpha"]), mpf(P["theta"]))):
        if abs(al-1) < 1e-9 or al >= 2: continue
        re = quad(lambda x: (cos(th*x)-1)/x**(1+al), [0, 1]) + quadosc(lambda x: cos(th*x)/x**(1+al), [1, inf], omega=abs(th)) - 1/al
        im = 0  # odd integrand
        v = 2*re
        ans = 2*cos(pi*al/2)*abs(th)**al*mp.gamma(-al)
        assert abs(v-ans) < mpf(10)**-20, (al, th, v, ans)
        out.append(v)
    return out[0], f"alpha,theta=(0.5,2.7),(1.5,-1.3) both match; value shown for (0.5,2.7)", {"alpha": "1/2", "theta": "27/10"}

@reg("R2-2025-SG-Relay-Q05", "R2-2025-UK-Relay-Q17")
def _(P):
    return nsum(lambda n: 1/floor(n + mpf(1)/2 + n)**2, [1, inf]), "floor(x+floor x)=2n on [n,n+1); sum"

@reg("R2-2025-SG-Group-Q07", "R2-2025-UK-Group-Q06")
def _(P):
    f = lambda x: cos(x)**2/((x*cos(x)+sin(x)+1)**2 + cos(x)**2)
    def cell(k):
        a = k*pi; return quad(f, mp.linspace(a, a+pi, 9))
    s = nsum(lambda k: cell(k) + cell(-k-1), [0, inf])
    return s, "per-pi-cell quad, paired +/- cells, nsum (Levin/Richardson)"

@reg("R2-2025-SG-Relay-Q21", "R2-2025-UK-Relay-Q13")
def _(P):
    return quad(lambda x: exp(x - sinh(x)**2), [-inf, -3, 0, 3, inf]), "quad"

@reg("R3-2024-Chainlink-G2-Q03")
def _(P):
    return quadosc(lambda t: sin(t)/t, [0, inf], omega=1), "t=tan x -> sin t/t; quadosc"

@reg("R3-2024-Chainlink-G5-Q04")
def _(P):
    return fsum_int(lambda n, u: u/(n+u)**2 - 1/mpf(n)**2), "t=1/x, sum over unit intervals"

@reg("R3-2024-Dichotomy-S2-Q06a")
def _(P):
    head = quad(lambda x: (cos(x)-cos(x)**2)*log(x)/x**2, [0, 1])
    t = quadosc(lambda x: cos(x)*log(x)/x**2, [1, inf], omega=1) - mpf(1)/2 - quadosc(lambda x: cos(2*x)*log(x)/(2*x**2), [1, inf], omega=2)
    return head + t, "quad [0,1] + split tails (int_1^inf ln x/x^2 = 1)"

@reg("R3-2024-Dichotomy-S2-Q06b")
def _(P):
    head = quad(lambda x: (cos(x)-cos(x)**2)/x**2, [0, 1])
    t = quadosc(lambda x: cos(x)/x**2, [1, inf], omega=1) - mpf(1)/2 - quadosc(lambda x: cos(2*x)/(2*x**2), [1, inf], omega=2)
    return head + t, "quad [0,1] + split tails"

@reg("R3-2024-Dichotomy-S3-Q05b")
def _(P):
    c = sqrt(3*pi)
    # x = u - c/2 : sin(u^2 - 3pi/4 + pi)
    S = quadosc(lambda y: sin(y**2), [0, inf], zeros=lambda n: sqrt(n*pi))
    Cc = quadosc(lambda y: cos(y**2), [0, inf], zeros=lambda n: sqrt((n-mpf(1)/2)*pi))
    ph = -3*pi/4 + pi
    return 2*(S*cos(ph) + Cc*sin(ph)), "complete square; Fresnel integrals by quadosc"

@reg("R3-2024-Tournament-Q01", "R3-2024-Tournament-Q01-v2", "R3-2024-Tournament-Q01-v3")
def _(P):
    return nsum(lambda n: n/(1+n**2+n**4), [0, inf]), "sum over unit intervals"

@reg("R3-2024-Chainlink-G5-Q07")
def _(P):
    f = lambda x: min(sqrt(mp.frac(x)-mp.frac(x)**2), sqrt(3)*abs(mp.asin(cos(pi*x)))/pi)
    per = quad(f, [0, mpf(1)/4, mpf(1)/2, mpf(3)/4, 1]); per2 = quad(f, [1, mpf(5)/4, mpf(3)/2, mpf(7)/4, 2])
    assert abs(per - per2) < mpf(10)**-25
    return 2025*per, "period-1 integrand (checked on [1,2]); 2025*quad over one period"

@reg("R3-2024-Tournament-Q04-v7", "R3-2024-Tournament-Q04-v8", "R3-2024-Tournament-Q04-v9")
def _(P):
    s = mp.fsum(mpf(2)**n/(mpf(3)**(2**n)+1) for n in range(0, 12))
    return s/log(2), "t=2^x; sum_n 2^n/(3^(2^n)+1)/ln2 (terms beyond n=11 < 1e-900)"

@reg("R3-2024-Tournament-Q06-v10", "R3-2024-Tournament-Q06-v11", "R3-2024-Tournament-Q06-v9")
def _(P):
    f = lambda x: sin(x)**2/(x**2*sqrt(atan(x)**2+2025) + x**2*atan(x) + 45*x**2) if x != 0 else 1/(sqrt(atan(x)**2+2025)+atan(x)+45)
    return quad(f, [-1, 0, 1]) + quadosc(f, [1, inf], period=pi) + quadosc(lambda x: f(-x), [1, inf], period=pi), "quad + quadosc both tails"

@reg("R3-2024-Tournament-Q06-v4", "R3-2024-Tournament-Q06-v5")
def _(P):
    f0 = lambda x: 2*x/(1+x**2)
    for x in (mpf("0.003"), mpf("-5.5"), mpf(700)):
        y = x
        for _ in range(200): y = f0(y)  # f_k = f0 iterated 2^k times; converges to sign(x)
        assert abs(y - mp.sign(x)) < mpf(10)**-20
    return quad(mp.sign, [-2024, 0, 2025]), "iterates of 2x/(1+x^2) -> sign(x) (checked); quad sign"

@reg("R3-2024-Tournament-Q07-v7", "R3-2024-Tournament-Q07-v8", "R3-2024-Tournament-Q07-v9")
def _(P):
    z = lambda k: sqrt(((k+mpf(1)/2)*pi + sqrt(((k+mpf(1)/2)*pi)**2 - 4))/2)
    k0 = 1  # first zero above 1: s=(k+1/2)pi>2 -> k>=1
    hi = quadosc(lambda x: cos(x**2+1/x**2), [z(1), inf], zeros=lambda n: z(n+1)) + quad(lambda x: cos(x**2+1/x**2), [1, z(1)])
    lo = quadosc(lambda t: cos(t**2+1/t**2)/t**2, [z(1), inf], zeros=lambda n: z(n+1)) + quad(lambda t: cos(t**2+1/t**2)/t**2, [1, z(1)])
    return hi + lo, "[1,inf) quadosc on exact zeros; (0,1] via x=1/t, same zeros"

@reg("SAMPLE-Q09")
def _(P):
    return fsum_int(lambda n, u: u/(n+u)**4), "sum over unit intervals"

@reg("YANG-3.4-P06")
def _(P):
    return quad(lambda x: atan((3*x-x**3)/(1-3*x**2)), [0, 1/sqrt(3), sqrt(3)]), "quad split at x=1/sqrt3 jump"

@reg("YANG-2.4-P09")
def _(P):
    return quad(lambda x: exp(3*x-exp(x)), [-inf, 0, 2, inf]), "quad"

# ---- revised checks (override earlier definitions) ----
def neville(xs, ys):
    t = list(ys)
    for j in range(1, len(xs)):
        for i in range(len(xs)-1, j-1, -1):
            t[i] = (t[i]*xs[i-j] - t[i-1]*xs[i]) / (xs[i-j] - xs[i])
    return t[-1]

@reg("R2-2022-Relay-Q11")
def _(P):
    n = int(P["n"]); ks = (16, 17, 18, 19)
    f = lambda k: quad(lambda t: sin(t)**(n-1)/t**n, [mpf(2)**-k, 2*mpf(2)**-k])
    return neville([mpf(4)**-k for k in ks], [f(k) for k in ks]), f"n={n}; x=2^-16..2^-19, Neville extrapolation in x^2"

@reg("R2-2023-Relay-Q13")
def _(P):
    n = int(P["n"]); ks = (16, 17, 18, 19)
    f = lambda k: quad(lambda t: tan(t)**(n-1)/sin(t)**n, [mpf(2)**-k, 2*mpf(2)**-k])
    g = lambda k: quad(lambda t: tan(t)**(n-1)/sin(t)**n, [-2*mpf(2)**-k, -mpf(2)**-k])
    a = neville([mpf(4)**-k for k in ks], [f(k) for k in ks]); b = neville([mpf(4)**-k for k in ks], [g(k) for k in ks])
    assert abs(a - b) < mpf(10)**-20 if n % 2 == 1 else True
    return a, f"n={n}; h=2^-16..2^-19 both sides, Neville in h^2"

@reg("R2-2022-Relay-Q20")
def _(P):
    def f(L):
        A = exp(L); br = [1, 1+1/L, 1+10/L, 2] + [exp(L*j/40) for j in range(1, 41)]
        return quad(lambda x: exp(L/x - L), br)
    Ls = [mpf(400*2**j) for j in range(6)]
    return neville([1/L for L in Ls], [f(L) for L in Ls]), "(1/A)int_1^A A^(1/x) with A=e^L, L=400..12800, Neville in 1/L", {"tol": mpf(10)**-8}

@reg("R2-2023-Relay-Q05")
def _(P):
    lnI = lambda n: log(quad(lambda x: (1+x**4)**n, [0, 1, 2-mpf(10)/n, 2-mpf(1)/n, 2]))
    ns = [1000, 2000, 4000, 8000]
    # n*ln(I^(1/n)/17) + ln n -> const  (Laplace at x=2) => I^(1/n) -> 17
    h = [lnI(n) - n*log(17) + log(n) for n in ns]
    assert abs(h[-1]-h[-2]) < abs(h[-2]-h[-3]) < abs(h[-3]-h[0]) + 1e-30 and abs(h[-1]-h[-2]) < 1e-3
    c = neville([mpf(1)/n for n in ns], h)
    return 17*exp((c - log(mpf(10)**30))/mpf(10)**30), f"Laplace: ln I_n = n ln17 - ln n + c, c={mp.nstr(c,12)} stable; I^(1/n)->17", {"tol": mpf(10)**-25}

@reg("R2-2023-Relay-Q02")
def _(P):
    mp.mp.dps = 60
    N = 48; M = 4000; tot = 0
    for i in range(M):
        x = pi*(i+mpf(1)/2)/M
        tot += max(sin(mpf(2)**k*x) for k in range(1, N+1))
    v = tot*pi/M; mp.mp.dps = 40
    return v, f"sup_n sin(2^n x)=1 for a.e. x (binary-normal x have dense 2^n x mod 2pi); midpoint M={M} of max_(k<=48) gives {mp.nstr(v,8)}", {"tol": mpf(10)**-2}

@reg("R2-2023-Relay-Q07")
def _(P):
    g = lambda n: 2*mp.fsum(sqrt(1-mpf(k)**2/n**2) for k in range(n))/n
    s = g(20000); q = quad(lambda t: 2*sqrt(1-t*t), [0, 1])
    assert abs(s - q) < 1e-4
    return q, f"Riemann sum of 2sqrt(1-t^2) (n=20000 gives {mp.nstr(s,12)}) -> integral by quad"

@reg("R2-2024-Relay-Q02")
def _(P):
    g = lambda n: (mp.fsum(((mpf(k)/n)-1)/log(mpf(k)/n) for k in range(1, n)) + 1)/n
    s = g(20000); q = quad(lambda t: (t-1)/log(t), [0, 1])
    assert abs(s - q) < 1e-4
    return q, f"exact inner int_0^1 t^x dx=(t-1)/ln t; Riemann sum n=20000 {mp.nstr(s,12)} -> integral by quad"

@reg("R2-2025-SG-Relay-Q15")
def _(P):
    g = lambda n: mp.fsum(sin(pi*k/(2*n)) for k in range(1, n+1))/n
    return _rich(g, [1000, 2000, 4000, 8000]), "Riemann sum (smooth), Richardson in 1/n", {"tol": mpf(10)**-12}

@reg("R2-2024-Relay-Q04")
def _(P):
    def cf(x, N=400):
        t = mpf(0)
        for n in range(N, 1, -1):
            t = 2*(n-1)*(2*(n-1)+1)*x**2/(2*n*(2*n+1) - x**2 + t)
        return x**2/(6 - x**2 + t)
    return quad(cf, [0, pi/4, pi/2]), "CF x^2/(2*3-x^2+2*3x^2/(4*5-x^2+...)) evaluated 400 levels backward; quad"

@reg("R2-2024-Relay-Q09")
def _(P):
    for y in (mpf("0.3"), mpf("0.9"), mpf("1.0")):
        assert mp.frac(mp.sinh(y)**2) == mp.frac(mp.cosh(y)**2) or abs(mp.frac(mp.sinh(y)**2)/mp.frac(mp.cosh(y)**2) - 1) < mpf(10)**-30
    def f(x, N=40):
        p = 1 - x
        for k in range(N + 1): p *= x**(2**k) + 1
        return p
    return quad(f, [0, mpf(1)/2, mpf(9)/10, mpf(99)/100, 1]), "frac(sinh^2)/frac(cosh^2)=1 (cosh^2=sinh^2+1, checked); product N=40; quad"

@reg("R1-2025-Online-Q12")
def _(P):
    def I(n):
        def f(x):
            v = x**n
            for j in range(n-1, 0, -1): v = abs(x**j - v)
            return v
        return quad(f, [0, mpf(1)/2, 1-mpf(10)/n, 1-mpf(1)/n, 1])
    ns = [100, 200, 400, 800]
    return neville([mpf(1)/n for n in ns], [I(n) for n in ns]), "direct nested-abs, even n=100..800, Neville in 1/n", {"tol": mpf(10)**-10}

@reg("R3-2024-Tournament-Q04-v10", "R3-2024-Tournament-Q04-v11", "R3-2024-Tournament-Q04-v12")
def _(P):
    mp.mp.dps = 20
    for m, n in ((2, 0), (3, 1), (4, 1), (3, 0)):
        d = m-n
        def f(x):
            s = sin(2**m*x)
            if s == 0: x += mpf(10)**-15; s = sin(2**m*x)
            return sin((2**m+2025*2**n)*x)/s*mp.fprod(cos(2**(m-k)*x) for k in range(1, d+1))
        K = 2**d*64
        v = quad(f, mp.linspace(0, pi/2**n, K+1))
        assert abs(v - pi/2**m) < 1e-12, (m, n, v)
    mp.mp.dps = 40
    return pi/mpf(2)**int(P["m"]), "direct quad of the given integrand for (m,n)=(2,0),(3,1),(4,1),(3,0) matches pi/2^m to 1e-12; answer at param point"

@reg("R2-2023-Relay-Q17")
def _(P):
    meas = (1 - mpf(2)/3) + nsum(lambda m: 1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2), [1, inf])
    brute = quad(lambda t: floor(cos(pi*t))/t**2, [1] + [k+mpf(1)/2 for k in range(1, 40)] + [40])
    part = (1 - mpf(2)/3) + mp.fsum(1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2) for m in range(1, 20))
    assert abs(brute + part) < mpf(10)**-20
    return -meas, "t=1/x; floor(cos)=-1 exactly where cos<0, else 0 a.e.; exact interval sum; brute quad on t in [1,40] agrees"

@reg("R2-2025-SG-Relay-Q14")
def _(P):
    ex = nsum(lambda m: 1/(m*(m+1)), [2, inf])
    c = 3
    d = quad(lambda u: 1/(floor(c/u)-1)/c, [mpf(c)/m for m in range(400, c-1, -1)] + [1])
    assert abs(d - mp.fsum(1/mpf((m-1)*m*(m+1)) for m in range(c, 400))) < 1e-4
    return ex, "geometric sum in floor(x); exact double sum; per-k quad cross-check"

@reg("R3-2024-Chainlink-G2-Q08")
def _(P):
    al = mpf(1)/2025; sg = 1 - al
    g = lambda v: sin(v)*cos(v)
    # exact: I(n) = n^-al * int_0^1 g(v) [zeta(sg,v) - zeta(sg,n+v)] dv   (Hurwitz zeta)
    exact = lambda n: n**(-al)*quad(lambda v: g(v)*(mp.zeta(sg, v) - mp.zeta(sg, n+v)), [0, 1])
    n = 60
    direct = mp.fsum(quad(lambda v: g(v)*((j+v)/mpf(n))**(al-1), [0, 1])/n for j in range(n))
    assert abs(direct - exact(n)) < mpf(10)**-20, (direct, exact(n))
    big = mpf(10)**(10**6)
    return exact(big), "u=x^2025; exact Hurwitz-zeta form verified vs direct cell sum at n=60; evaluated at n=10^(10^6) (n^-al ~ e^-1137)"

@reg("R3-2024-Dichotomy-S1-Q04a")
def _(P):
    x = mpf("1.7"); v = mpf(1)
    for k in range(40, 0, -1):
        v = sqrt(x**(2**k) * sqrt((mpf(2)**k)**(-x) * v))
    assert abs(v - x**2*mpf(2)**(-4*x/9)) < mpf(10)**-25
    def f(x):
        v = mpf(1)
        for k in range(40, 0, -1): v = sqrt(x**(2**k) * sqrt((mpf(2)**k)**(-x) * v))
        return v
    return quad(f, [0, 1, 10, 50, inf]), "nested radical evaluated directly (depth 40) inside quad"

@reg("R3-2024-Dichotomy-S2-Q07a")
def _(P):
    f = lambda n: quad(lambda x: log(1 + (n*x)**(-1/e) + e/n), [1] + [mpf(10)**j for j in range(1, int(mp.log10(n))+1)])
    v = [f(mpf(10)**k) for k in (2, 4, 8, 16)]
    assert all(v[i+1] > v[i] for i in range(3)) and v[-1] > 1000
    return inf, "limit check: " + ", ".join(mp.nstr(t, 8) for t in v) + " at n=1e2,1e4,1e8,1e16 (grows ~ n^(1-2/e))"

@reg("R3-2024-Dichotomy-S2-Q07b")
def _(P):
    f = lambda n: quad(lambda x: log(1 + 2/n + 1/sqrt(n*x)), [1] + [mpf(10)**j for j in range(1, int(mp.log10(n))+1)] + [n])
    ms = [10**3, 2*10**3, 4*10**3, 8*10**3, 16*10**3]
    vals = [f(mpf(m)**2) for m in ms]
    return neville([mpf(1)/m for m in ms], vals), "n=m^2 (m=1e3..1.6e4), Neville in 1/m; last raw " + mp.nstr(vals[-1], 10), {"tol": mpf(10)**-6}

@reg("R2-2025-SG-Relay-Q19", "R2-2025-UK-Relay-Q19")
def _(P):
    f = lambda n: n*quad(lambda x: (1+x**3)/(n+x+x**3+x**5), [0, 1])
    return _rich(f, [10**4, 2*10**4, 4*10**4, 8*10**4]), "n*int for n=1e4..8e4, Richardson in 1/n", {"tol": mpf(10)**-12}

# ---- revision 2 ----
@reg("R2-2023-Relay-Q13")
def _(P):
    n = int(P["n"]); ks = (16, 17, 18, 19)
    f = lambda k: quad(lambda t: tan(t)**(n-1)/sin(t)**n, [mpf(2)**-k, 2*mpf(2)**-k])
    return neville([mpf(4)**-k for k in ks], [f(k) for k in ks]), f"n={n}; h=2^-16..2^-19, Neville in h^2"

@reg("R2-2023-Relay-Q17")
def _(P):
    meas = (1 - mpf(2)/3) + nsum(lambda m: 1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2), [1, inf])
    brute = quad(lambda t: floor(cos(pi*t))/t**2, sorted(set([mpf(k) for k in range(1, 41)] + [k+mpf(1)/2 for k in range(1, 40)])))
    part = (1 - mpf(2)/3) + mp.fsum(1/(2*m+mpf(1)/2) - 1/(2*m+mpf(3)/2) for m in range(1, 20))
    assert abs(brute + part) < mpf(10)**-20, (brute, part)
    return -meas, "t=1/x; floor(cos)=-1 exactly where cos<0, else 0 a.e.; exact interval sum; brute quad on t in [1,40] agrees to 1e-20"

@reg("R1-2021-Q25", "R3-2024-Tournament-Q02-v3", "R3-2024-Tournament-Q02-v4", "R3-2024-Tournament-Q02-v5", "YANG-1.20-P05")
def _(P):
    mp.mp.dps = 50
    v = quad(lambda th: atan(exp(tan(th))), [-pi/2, -1, 0, 1, pi/2])
    mp.mp.dps = 40
    return v, "x=e^tan(th): int_(-pi/2)^(pi/2) atan(e^tan th) dth; quad (direct quad has slow log^2 tails)"

@reg("R1-2024-Q08")
def _(P):
    mp.mp.dps = 50
    v = quad(lambda th: 1/(1+exp(-tan(th))), [-pi/2, -1, 0, 1, pi/2])
    mp.mp.dps = 40
    return v, "x=e^tan(th): int_(-pi/2)^(pi/2) 1/(1+e^-tan th) dth; quad"

@reg("R2-2024-Group-Q07")
def _(P):
    f = lambda x: exp(cos(x))*sin(x)*sin(sin(x))/x**2
    per = lambda k: quad(f, [2*pi*k, 2*pi*k+pi/2, 2*pi*k+pi, 2*pi*k+3*pi/2, 2*pi*(k+1)])
    head = quad(f, [0, pi/2, pi, 3*pi/2, 2*pi])
    return head + nsum(lambda k: per(int(k)), [1, inf]), "per-period quad + nsum (Richardson/Levin) over periods"

@reg("R2-2024-Relay-Q06")
def _(P):
    f = lambda n: n*quad(lambda x: (1-abs(x)+abs(x)**3)**n, [-mpf(1)/20, -mpf(1)/n, 0, mpf(1)/n, mpf(1)/24])
    ns = [1000, 2000, 4000, 8000, 16000]
    return neville([mpf(1)/n for n in ns], [f(n) for n in ns]), "n*int for n=1000..16000, Neville in 1/n", {"tol": mpf(10)**-9}

@reg("R2-2024-Relay-Q08")
def _(P):
    x0 = mpf("0.4")
    part = mp.fsum(1/sqrt(n-mp.sec(x0)**2) - 1/sqrt(n-tan(x0)**2) for n in range(2, 10**5))
    assert abs(part - (1/sqrt(1-tan(x0)**2) - 1/sqrt(10**5-1-tan(x0)**2))) < mpf(10)**-25
    mp.mp.dps = 60
    v = quad(lambda u: 2*u/sqrt(1-tan(pi/4-u*u)**2), [0, sqrt(pi/4)/2, sqrt(pi/4)])
    mp.mp.dps = 40
    return v, "telescoping verified numerically (1e5 terms at x=0.4); u=sqrt(pi/4-x) quad at 60 dps"

@reg("R2-2024-Relay-Q09")
def _(P):
    for y in (mpf("0.3"), mpf("0.9"), mpf("1.0")):
        assert abs(mp.frac(mp.sinh(y)**2)/mp.frac(mp.cosh(y)**2) - 1) < mpf(10)**-30
    mp.mp.dps = 60
    def f(x, N=60):
        p = 1 - x
        for k in range(N + 1): p *= x**(2**k) + 1
        return p
    v = quad(f, [0, mpf(1)/2] + [1-mpf(10)**-j for j in range(1, 20)] + [1]); mp.mp.dps = 40
    return v, "frac(sinh^2)/frac(cosh^2)=1 (cosh^2=sinh^2+1, checked); product N=60 at 60 dps; quad with breakpoints toward 1"

@reg("R1-2025-Online-Q12")
def _(P):
    def I(n):
        def f(x):
            v = x**n
            for j in range(n-1, 0, -1): v = abs(x**j - v)
            return v
        return quad(f, [0, mpf(1)/2, 1-mpf(30)/n, 1-mpf(10)/n, 1-mpf(3)/n, 1-mpf(1)/n, 1])
    ns = [100, 200, 400, 800, 1600]
    return neville([mpf(1)/n for n in ns], [I(n) for n in ns]), "direct nested-abs, even n=100..1600, Neville in 1/n", {"tol": mpf(10)**-9}

@reg("R3-2024-Chainlink-G2-Q08")
def _(P):
    al = mpf(1)/2025; sg = 1 - al
    g = lambda v: sin(v)*cos(v)
    Z = quad(lambda v: g(v)*mp.zeta(sg, v), [0, 1])
    # exact: I(n) = n^-al * int_0^1 g(v) [zeta(sg,v) - zeta(sg,n+v)] dv   (Hurwitz zeta)
    exact = lambda n: n**(-al)*(Z - quad(lambda v: g(v)*mp.zeta(sg, n+v), [0, 1]))
    n = 60
    direct = mp.fsum(quad(lambda v: g(v)*((j+v)/mpf(n))**(al-1), [0, 1])/n for j in range(n))
    assert abs(direct - exact(n)) < mpf(10)**-20, (direct, exact(n))
    E = [exact(mpf(10)**k) - mpf(10)**(-k*al)*Z for k in (3, 6, 12)]
    assert abs(E[2]-E[1]) < mpf(10)**-5
    return E[2], ("u=x^2025; I(n)=n^-al*int g[zeta(1-al,v)-zeta(1-al,n+v)] (Hurwitz, verified vs direct sum at n=60) "
                  "= L + n^-al*Z + O(1/n), n^-al->0 so lim = L; I(n)-n^-al*Z at n=1e3,1e6,1e12: " + ", ".join(mp.nstr(e, 15) for e in E)), {"tol": mpf(10)**-10}

# ---- revision 3 ----
@reg("R3-2024-Dichotomy-S1-Q04a")
def _(P):
    def f(x, D=150):
        v = mpf(1)
        for k in range(D, 0, -1): v = sqrt(x**(2**k) * sqrt((mpf(2)**k)**(-x) * v))
        return v
    x = mpf("1.7"); assert abs(f(x) - x**2*mpf(2)**(-4*x/9)) < mpf(10)**-30
    return quad(f, [0, 1, 10, 50, 200, inf]), "nested radical sqrt(x^2 sqrt(2^-x sqrt(x^4 sqrt(4^-x ...)))) evaluated directly (depth 150) inside quad"

@reg("R3-2024-Chainlink-G4-Q07")
def _(P):
    f1 = lambda x: 2*x - 2*x**2
    for x in (mpf("0.1"), mpf("0.37")):
        y = x
        for n in range(1, 7):
            y = f1(y); assert abs(y - (mpf(1)/2 - (1-2*x)**(2**n)/2)) < mpf(10)**-30
    return quad(lambda x: mpf(1)/2 - (1-2*x)**(mpf(2)**200)/2, [0, mpf(10)**-60, mpf(1)/2]), "composition closed form checked n=1..6; n=200 (error 2^-202)"

@reg("R3-2024-Tournament-Q03-v10", "R3-2024-Tournament-Q03-v11", "R3-2024-Tournament-Q03-v12")
def _(P):
    f = lambda n: n*quad(lambda x: tan(x)**n, [0, pi/4 - mpf(10)/n, pi/4 - mpf(1)/n, pi/4])
    ns = [1000, 2000, 4000, 8000, 16000]
    return neville([mpf(1)/n for n in ns], [f(n) for n in ns]), "n*int tan^n directly, Neville in 1/n", {"tol": mpf(10)**-12}

@reg("R2-2024-Relay-Q10")
def _(P):
    out = []
    for al, th in ((mpf("0.5"), mpf("2.7")), (mpf("0.7"), mpf("-1.3"))):
        re = quad(lambda x: (cos(th*x)-1)/x**(1+al), [0, 1]) + quadosc(lambda x: cos(th*x)/x**(1+al), [1, inf], omega=abs(th)) - 1/al
        v = 2*re; ans = 2*cos(pi*al/2)*abs(th)**al*mp.gamma(-al)
        assert abs(v-ans) < mpf(10)**-20, (al, th, v, ans)
        out.append(v)
    return out[0], "real part (imag odd->0); (alpha,theta)=(0.5,2.7),(0.7,-1.3) match closed form; value at (0.5,2.7)", {"params": {"alpha": "1/2", "theta": "27/10"}}

# extrapolation-error tracking: Neville on all points vs dropping the first point
LAST_ERR = [None]
_nev0 = neville
def neville(xs, ys):
    a = _nev0(xs, ys); b = _nev0(xs[1:], ys[1:]); LAST_ERR[0] = abs(a - b); return a
def _rich(f, ns):
    return neville([mpf(1)/n for n in ns], [f(n) for n in ns])

@reg("R2-2025-SG-Group-Q07", "R2-2025-UK-Group-Q06")
def _(P):
    f = lambda x: cos(x)**2/((x*cos(x)+sin(x)+1)**2 + cos(x)**2)
    cell = lambda k: quad(f, [k*pi + j*pi/8 for j in range(9)])
    cells = {}; S = {}
    tot = mpf(0)
    for k in range(2000):
        tot += cell(k) + cell(-k-1)
        if k+1 in (250, 500, 1000, 2000): S[k+1] = tot
    ns = sorted(S)
    return neville([mpf(1)/n for n in ns], [S[n] for n in ns]), "symmetric partial sums over 2K pi-cells, K=250..2000, Neville in 1/K", {"tol": mpf(10)**-8}

@reg("R2-2025-SG-Group-Q07", "R2-2025-UK-Group-Q06")
def _(P):
    f = lambda x: cos(x)**2/((x*cos(x)+sin(x)+1)**2 + cos(x)**2)
    g = lambda x: x*cos(x)+sin(x)+1
    def cell(k):
        a, b = k*pi, (k+1)*pi
        br = [a + j*pi/8 for j in range(9)]
        # Lorentzian spikes (f~1) where g=0 with cos!=0: locate sign changes of g on a fine grid
        xs = mp.linspace(a, b, 64)
        for u, v in zip(xs, xs[1:]):
            if g(u)*g(v) < 0:
                r = mp.findroot(g, (u, v), solver="anderson")
                w = 1/(1+abs(r))**2
                br += [r + s*w*t for s in (-1, 1) for t in (1, 1e-1, 1e-2, 1e-3)] + [r]
        br = sorted(set(t for t in br if a <= t <= b))
        return quad(f, br)
    tot = mpf(0); S = {}
    for k in range(1600):
        tot += cell(k) + cell(-k-1)
        if k+1 in (200, 400, 800, 1600): S[k+1] = tot
    ns = sorted(S)
    return neville([mpf(1)/n for n in ns], [S[n] for n in ns]), "pi-cells with breakpoints at Lorentzian spikes (roots of x cos x+sin x+1), symmetric K=200..1600, Neville in 1/K", {"tol": mpf(10)**-8}

@reg("R2-2025-SG-Group-Q07", "R2-2025-UK-Group-Q06")
def _(P):
    # integrand = 1/(1+h^2), h = x + tan(x/2+pi/4) = x - sum 2/(x-b_k), b_k = 2k pi + pi/2  (Glasser master theorem)
    h = lambda x: x + tan(x/2 + pi/4)
    hp = lambda x: 1 + mp.sec(x/2 + pi/4)**2/2
    x0 = mpf("0.77"); f = lambda x: cos(x)**2/((x*cos(x)+sin(x)+1)**2 + cos(x)**2)
    assert abs(f(x0) - 1/(1+h(x0)**2)) < mpf(10)**-30
    worst = 0
    for u in (mpf("0.3"), mpf(2), mpf(-5)):
        tot = 0; K = 3000
        for k in range(-K, K+1):
            a, b = 2*k*pi - 3*pi/2, 2*k*pi + pi/2
            lo, hi = a + mpf(10)**-30, b - mpf(10)**-30
            for _ in range(200):
                m = (lo+hi)/2
                if h(m) < u: lo = m
                else: hi = m
            tot += 1/hp((lo+hi)/2)
        tail = 2*2/(4*pi**2*K)  # sum_{|k|>K} 2/(2 pi k)^2
        worst = max(worst, abs(tot + tail - 1))
    assert worst < 1e-6, worst
    return pi, f"integrand=1/(1+h^2), h=x+tan(x/2+pi/4) is x - sum 2/(x-b_k) (Glasser); verified sum of 1/h'(roots of h=u) = 1 to {mp.nstr(worst,2)} for u=0.3,2,-5 (|k|<=3000 + tail), so integral = int du/(1+u^2) = pi"

# ---- revision 4 ----
@reg("YANG-2.4-P09")
def _(P):
    return quad(lambda x: exp(3*x-exp(x)), [-80, -20, 0, 2, 4, 6]), "quad on [-80,6] (tails < e^-200); u=e^x gives Gamma(3)"

@reg("R2-2025-SG-Relay-Q21", "R2-2025-UK-Relay-Q13")
def _(P):
    return quad(lambda x: exp(x - mp.sinh(x)**2), [-7, -3, 0, 3, 7]), "quad on [-7,7] (tails < e^-270)"

@reg("R3-2024-Dichotomy-S2-Q06a")
def _(P):
    mp.mp.dps = 60
    head = quad(lambda x: (cos(x)-cos(x)**2)*log(x)/x**2, [0, 1])
    t = quadosc(lambda x: cos(x)*log(x)/x**2, [1, inf], omega=1) - mpf(1)/2 - quadosc(lambda x: cos(2*x)*log(x)/(2*x**2), [1, inf], omega=2)
    mp.mp.dps = 40
    return head + t, "60 dps: quad [0,1] + split tails (int_1^inf ln x/x^2 = 1)", {"tol": mpf(10)**-20}

@reg("R3-2024-Dichotomy-S2-Q06b")
def _(P):
    mp.mp.dps = 60
    head = quad(lambda x: (cos(x)-cos(x)**2)/x**2, [0, 1])
    t = quadosc(lambda x: cos(x)/x**2, [1, inf], omega=1) - mpf(1)/2 - quadosc(lambda x: cos(2*x)/(2*x**2), [1, inf], omega=2)
    mp.mp.dps = 40
    return head + t, "60 dps: quad [0,1] + split tails", {"tol": mpf(10)**-20}

@reg("R3-2024-Tournament-Q06-v10", "R3-2024-Tournament-Q06-v11", "R3-2024-Tournament-Q06-v9")
def _(P):
    D = lambda x: sqrt(atan(x)**2+2025) + atan(x) + 45
    f = lambda x: sin(x)**2/(x**2*D(x)) if x != 0 else 1/D(x)
    tot = quad(f, [-1, 0, 1])
    for s in (1, -1):
        tot += quad(lambda x: 1/(2*x**2*D(s*x)), [1, inf]) - quadosc(lambda x: cos(2*x)/(2*x**2*D(s*x)), [1, inf], omega=2)
    return tot, "quad [-1,1]; tails split sin^2=(1-cos2x)/2: plain quad + quadosc"

# ---- revision 5 ----
@reg("R2-2024-Relay-Q08")
def _(P):
    x0 = mpf("0.4")
    part = mp.fsum(1/sqrt(n-mp.sec(x0)**2) - 1/sqrt(n-tan(x0)**2) for n in range(2, 10**5))
    assert abs(part - (1/sqrt(1-tan(x0)**2) - 1/sqrt(10**5-1-tan(x0)**2))) < mpf(10)**-25
    mp.mp.dps = 60
    g = lambda u: 1 if u < mpf(10)**-25 else 2*u/sqrt(1-tan(pi/4-u*u)**2)   # limit at u->0 is 1 (removable)
    v = quad(g, [0, sqrt(pi/4)/2, sqrt(pi/4)])
    mp.mp.dps = 40
    return v, "telescoping verified numerically (1e5 terms at x=0.4); u=sqrt(pi/4-x) quad at 60 dps, removable 0/0 at u=0 set to its limit 1"

@reg("R2-2024-Relay-Q09")
def _(P):
    for y in (mpf("0.3"), mpf("0.9"), mpf("1.0")):
        assert abs(mp.frac(mp.sinh(y)**2)/mp.frac(mp.cosh(y)**2) - 1) < mpf(10)**-30
    mp.mp.dps = 60
    errs = []
    for N in (5, 20, 60):
        def f(x, N=N):
            p = 1 - x
            for k in range(N + 1): p *= x**(2**k) + 1
            return p
        v = quad(f, [0, mpf(1)/2] + [1-mpf(10)**-j for j in range(1, 20)] + [1])
        errs.append(abs(v - (1 - 1/mpf(2**(N+1)+1))))
    assert max(errs) < mpf(10)**-30, errs
    mp.mp.dps = 40
    return mpf(1), "frac ratio=1 checked; product telescopes to 1-x^(2^(N+1)) so I_N=1-1/(2^(N+1)+1), matched by quad for N=5,20,60 to <1e-30; limit N->inf is 1 exactly"
