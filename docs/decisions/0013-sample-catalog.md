# Sample problems in the catalog

The UK site sample sheet is twenty integrals, linked from the home page apart from the resource pack. They live in `problems/records.jsonl` with `round` `sample` and `source` `uk_sample`, ids `SAMPLE-Q01` through `SAMPLE-Q20`. `problems list`, `problems select`, and `problems show` read those rows. A mark goes through `turn apply` on the same path as a pack row.

A `verify: sympy` sample is one the pack gate proves. The companion sends `extract.final_answer` and does not send `verdict`. A `verify: manual` sample has a cited answer the gate does not prove. The companion sends `verdict`. Worked notes are `solutions/sample/`. `past/samples/answers_feed.json` stays the citation cross-check.

SAMPLE-Q17 is \(\int x^{1/\ln x}\,dx\). The solutions PDF shows that the integrand equals \(e\), so the antiderivative is \(ex+C\). The answers sheet prints `ex + c` on one baseline, the product. An earlier feed read the integrand as \(1/(x\ln x)\) and treated that print as \(e^x\). That reading is withdrawn. `ln|ln x|+C` does not match.

SAMPLE-Q15's answers PDF and the last line of the solutions PDF put a minus sign on the arctan term. That expression is not an antiderivative of \(1/(x^3+1)\). The graded answer finishes the previous line of the solutions PDF, which has the positive arctan integral. The note is marked authored and verified.

SAMPLE-Q10 multiplies \(\bigl(x^3\cos(x/2)+1/2\bigr)\) by \(\sqrt{4-x^2}\). The value is still \(\pi\).
