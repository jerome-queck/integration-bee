# Answers are parsed by a whitelisted grammar, not sympify

Audit F1 (receipt ibe-audit-remediation-2026-10-31) showed that a learner answer
reached `sympy.sympify`, which evaluates Python. A typed answer such as
`__import__('os').system(...)` ran on the machine.

Every learner- or row-supplied expression now goes through
`verify/safe_expr.py:safe_sympify`. It parses the text with `ast` and accepts
only numbers, `+ - * / **` (`^` is read as `**`), unary signs, `& |`, `< <= > >=`,
tuples (for `Piecewise`), short variable names, names in the caller's namespace,
and calls to SymPy expression classes or `sqrt`-style helpers. String arguments
are allowed only as the name of `Symbol`/`Dummy`/`Wild`/`Function` or the
decimal of `Float`/`Integer`/`Rational`, and keywords only as boolean
assumptions on those name constructors, so stored `srepr` rows still parse. Attribute access, subscripts, lambdas, strings, underscore
names, exponents above 1000, stacked numeric powers, and text over 8000
characters are rejected with `UnsafeExpression`. The checked tree is then built
by SymPy from the whitelisted namespace only.

`verify/turn_contract.py`, `verify/pack_answer_contracts.py`, and
`verify/pack_gate.py` use it. `verify/safe_expr_check.py` runs each payload
against every entry point and requires that no marker file appears.
