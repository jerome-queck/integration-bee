"""Answer kinds required by Handoff F, with their source-backed certificates.

Ordinary integrals keep the existing scalar/additive-constant path.  These
contracts preserve a comparison, function, root count, pair, or literal limit
as the problem actually asks it.  A special kind never falls back to an
ordinary antiderivative merely because its bound metadata is empty.
"""

from __future__ import annotations

import ast
import re

import sympy as sp

import pack_handoff_f_domain
import pack_handoff_f_expressions
import pack_handoff_f_integrals
import pack_handoff_m


KINDS = frozenset({
    "comparison", "function", "expression", "root_count", "prime_factors",
    "product_indefinite", "domain",
})
BOUNDED_KINDS = frozenset({"definite", "prime_factors", "domain"})


def infinity_text(text: str) -> str:
    """Normalize only complete signed-infinity answers, not arbitrary text."""
    stripped = text.strip().replace("\N{MINUS SIGN}", "-")
    positive = {"oo", "+oo", "inf", "+inf", "infinity", "+infinity", "∞", "+∞"}
    negative = {"-oo", "-inf", "-infinity", "-∞"}
    if stripped.lower() in positive:
        return "oo"
    if stripped.lower() in negative:
        return "-oo"
    return text


def _prime_pair(text, ns):
    # Parse container elements before SymPy or Python set construction can
    # erase a repeated factor.  In particular {2,2,3} is not the pair {2,3}.
    node = ast.parse(text.strip(), mode="eval").body
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        elements = node.elts
    elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
          and node.func.id in {"Tuple", "FiniteSet"} and not node.keywords):
        elements = node.args
    else:
        return None
    if len(elements) != 2:
        return None
    values = [sp.sympify(ast.unparse(element), locals=ns) for element in elements]
    if any(not isinstance(value, sp.Integer) or not sp.isprime(value) for value in values):
        return None
    return sp.Tuple(*sorted(values))


def parse_answer(kind, text, namespace):
    """Parse a typed answer without stripping an additive constant."""
    ns = dict(namespace)
    if kind == "prime_factors":
        return _prime_pair(text, ns)
    if kind == "comparison":
        compact = re.sub(r"\s+", "", text)
        if compact in {"I=J", "J=I", "I==J", "J==I"}:
            return pack_handoff_f_expressions.EQUAL_VERDICT
        # The stored SymPy spelling is an opaque verdict symbol.  It must
        # never be interpreted as the imaginary unit I or a scalar zero.
        if compact in {"Symbol('I=J')", 'Symbol("I=J")'}:
            return pack_handoff_f_expressions.EQUAL_VERDICT
        if re.fullmatch(r"[IJ](?:[<>=]=?|!=)[IJ]", compact):
            return sp.Symbol(compact)
        # Well-formed numeric proxies are wrong answers. Malformed text is
        # a parse error, which the turn contract must not record as a miss.
        return sp.sympify(text, locals=ns)
    if kind == "function":
        match = re.fullmatch(r"\s*f\s*\(\s*x\s*\)\s*=\s*(.+)", text, re.S)
        if match:
            text = match.group(1)
    if kind == "product_indefinite":
        ns["C"] = sp.Symbol("C", positive=True)
    if kind == "domain":
        ns["n"] = sp.Symbol("n", real=True)
    return sp.sympify(infinity_text(text), locals=ns)


def _closed_scalar(value):
    return (isinstance(value, sp.Expr)
            and not value.has(sp.Integral, sp.Sum, sp.Product, sp.Limit,
                              sp.Derivative, sp.nan, sp.zoo)
            and not value.free_symbols)


def _domain_answer_matches(expected, candidate):
    """Compare every real-parameter branch, including signed infinities.

The expression partition is part of the answer.  Subtracting two Piecewise
expressions would turn matching infinite branches into nan; point sampling
would miss a changed endpoint or a gap.  Intersect exact real sets instead.
    """
    n = sp.Symbol("n", real=True)
    if not isinstance(candidate, sp.Piecewise) or candidate.free_symbols != {n}:
        return False
    try:
        wanted = expected.as_expr_set_pairs(domain=sp.S.Reals)
        supplied = candidate.as_expr_set_pairs(domain=sp.S.Reals)
        if sp.Union(*(region for _, region in supplied)) != sp.S.Reals:
            return False
        for actual, region in supplied:
            if not isinstance(actual, sp.Expr) or actual.has(
                    sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative,
                    sp.nan, sp.zoo):
                return False
            for target, target_region in wanted:
                overlap = sp.Intersection(region, target_region)
                if overlap == sp.S.EmptySet:
                    continue
                if target in (sp.oo, -sp.oo) or actual in (sp.oo, -sp.oo):
                    if target != actual:
                        return False
                elif sp.simplify(target - actual) != 0:
                    return False
        return True
    except (TypeError, ValueError, NotImplementedError):
        return False


def answer_matches(kind, expr, symbol, limits, candidate):
    """Prove an answer to a recognized original problem, without trusting an id."""
    if candidate is None:
        return False
    if kind in {"prime_factors", "product_indefinite"}:
        expected = pack_handoff_f_integrals.answer_value(kind, expr, symbol, limits)
    elif kind == "domain":
        expected = pack_handoff_f_domain.answer_value(kind, expr, symbol, limits)
    else:
        expected = pack_handoff_f_expressions.answer_value(kind, expr, symbol, limits)
        if expected is None:
            expected = pack_handoff_m.answer_value(kind, expr, symbol, limits)
    if expected is None:
        return False
    if kind in {"comparison", "prime_factors"}:
        return candidate == expected
    if kind == "function":
        return pack_handoff_f_expressions.function_answer_ok(candidate, symbol)
    if kind == "product_indefinite":
        return pack_handoff_f_integrals.product_answer_ok(expr, candidate, symbol)
    if kind == "domain":
        return _domain_answer_matches(expected, candidate)
    if kind == "root_count":
        return isinstance(candidate, sp.Integer) and candidate == expected
    return _closed_scalar(candidate) and sp.simplify(expected - candidate) == 0


def open_expression(expr, symbol):
    if pack_handoff_m.open_expression("expression", expr, symbol):
        return True
    if pack_handoff_f_integrals.open_integrand(expr, symbol):
        return True
    if pack_handoff_f_domain.open_expression(expr, symbol):
        return True
    return any(pack_handoff_f_expressions.open_expression(kind, expr, symbol)
               for kind in ("comparison", "function", "expression", "root_count"))


def transcripts():
    """Return typed readings as (kind, text, bounds, answer text, variable)."""
    result = {}
    for module in (pack_handoff_f_integrals, pack_handoff_f_expressions,
                   pack_handoff_f_domain, pack_handoff_m):
        for ident, (kind, expr, limits, answer, variable) in module.transcripts().items():
            text = expr if isinstance(expr, str) else sp.srepr(expr)
            final = answer if isinstance(answer, str) else sp.srepr(answer)
            bounds = tuple(item if isinstance(item, str) else sp.srepr(item)
                           for item in (limits or ()))
            result[ident] = (kind, text, bounds, final, variable)
    return result
