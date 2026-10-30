import sys, time, mpmath as mp
from mpmath import mpf, pi, sin, cos, quad
mp.mp.dps = int(sys.argv[1]) if len(sys.argv) > 1 else 45
h = lambda x: x + (sin(x) + 1)/cos(x)
f = lambda x: cos(x)**2/(cos(x)**2 + (x*cos(x) + sin(x) + 1)**2)
b = lambda k: pi/2 + 2*pi*k
def per(k):
    lo, hi = b(k-1), b(k)
    r = mp.findroot(lambda y: h(y), (lo + mpf(10)**-30, hi - mpf(10)**-30), solver="anderson")
    w = 1/(1 + abs(r))**2
    pts = sorted({lo, hi, r} | {r + s*w*mpf(4)**j for s in (-1, 1) for j in range(14) if lo < r + s*w*mpf(4)**j < hi})
    return quad(f, pts)
if __name__ == "__main__":
    t = time.time(); print(per(0), per(50), time.time() - t, flush=True)
