# SymPy-gated pack rows

Resource-pack rows in Rounds 1–3 can be `verify: sympy` when a layout reading of the committed problem PDF and the cited mark scheme is proved by SymPy. The proof is a derivative for an indefinite integral, or a closed evaluation for a definite integral. A closed evaluation may use a floor sum from 0 to infinity when the integrand is constant on each integer interval, the even part on symmetric limits, King's reflection, a constant sum `f(x)+f(b-x)` on `[0, b]`, the reciprocal substitution on `(0, ∞)`, positive assumptions on parameters other than `x`, or `x = exp(-u)` on `[0, 1]` when the integrand contains a logarithm. Numeric agreement is not a proof.

`scripts/recover_pack_math.py` is the only writer of those fields. It rereads the committed Round 1, Round 2, and Round 3 PDFs and leaves every unproved row `manual` or `unchecked`. Yang practice is not gated. `R1-2024-Q01` stays manual, with the mark scheme that contains `sin(1)`.

`make check` re-proves the stored expressions and does not open the PDFs. A mark of a `sympy` row sends `extract.final_answer` and does not send `verdict`. A manual row still needs a verdict. An unchecked row still has no answer.
