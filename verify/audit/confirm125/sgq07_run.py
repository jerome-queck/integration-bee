import sys, mpmath as mp
import sgq07 as S
from mpmath import mpf
dps = int(sys.argv[1]); mp.mp.dps = dps
Ns = [20, 40, 80, 160, 320, 640, 1280]
acc = mpf(0); k_done = 0; partial = []
for N in Ns:
    for k in range(k_done + 1, N + 1):
        acc += S.per(k) + S.per(1 - k)
    k_done = N; partial.append(acc)
    print("N", N, mp.nstr(acc, 40), flush=True)
for m in range(3, len(Ns) + 1):
    xs = [mpf(1)/n for n in Ns[-m:]]; ys = partial[-m:]
    v = mp.polyfit if False else None
    # Neville to 1/N -> 0
    P = list(ys)
    for j in range(1, m):
        P = [(xs[i+j]*P[i] - xs[i]*P[i+1])/(xs[i+j] - xs[i]) for i in range(m - j)]
    print("neville last", m, "pts:", mp.nstr(P[0], 40), " err vs pi:", mp.nstr(abs(P[0] - mp.pi), 5), flush=True)
