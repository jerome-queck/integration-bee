# SymPy-gated pack rows

Round 1 resource-pack rows can be `verify: sympy` when a layout reading of the committed problem PDF and the cited mark scheme is proved by SymPy. The proof is a derivative for an indefinite integral, or a closed evaluation for a definite integral, including a floor sum from 0 to infinity when the integrand is constant on each integer interval. Numeric agreement is not a proof.

`scripts/recover_pack_math.py` is the only writer of those fields. It leaves every unproved row `manual` or `unchecked`. Yang practice is not gated. `R1-2024-Q01` stays manual, with the mark scheme that contains `sin(1)`.

`make check` re-proves the stored expressions and does not open the PDFs. A mark of a `sympy` row sends `extract.final_answer` and does not send `verdict`. A manual row still needs a verdict. An unchecked row still has no answer.
