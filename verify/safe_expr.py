"""Restricted expression grammar for text that reaches SymPy (audit F1).

sympify() runs Python eval on its input, so a learner answer such as
``__import__('os').system('...')`` used to execute code. Every
learner-facing parse goes through safe_sympify(), which accepts only:
numbers, + - * / ** ^ and unary signs, parentheses, names from the
caller's namespace (or short symbol names), and calls to functions in
that namespace. Anything else raises UnsafeExpression before eval.
"""
from __future__ import annotations

import ast
import re

import sympy as sp

MAX_LEN = 400
MAX_NUMBER = 10**9
MAX_LITERAL_EXPONENT = 1000
_SYMBOL = re.compile(r"[A-Za-z][A-Za-z0-9]{0,2}\Z")
_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
_UNARY = (ast.UAdd, ast.USub)


class UnsafeExpression(ValueError):
    pass


def _check(node, names: dict) -> None:
    if isinstance(node, ast.Expression):
        return _check(node.body, names)
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise UnsafeExpression(f"literal not allowed: {value!r}")
        if abs(value) > MAX_NUMBER:
            raise UnsafeExpression("number too large")
        return None
    if isinstance(node, ast.Name):
        if node.id.startswith("_"):
            raise UnsafeExpression(f"name not allowed: {node.id}")
        if node.id in names or _SYMBOL.match(node.id):
            return None
        raise UnsafeExpression(f"unknown name: {node.id}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, _UNARY):
        return _check(node.operand, names)
    if isinstance(node, ast.BinOp) and isinstance(node.op, _BINOPS):
        if isinstance(node.op, ast.Pow):
            right = node.right
            if isinstance(right, ast.UnaryOp):
                right = right.operand
            if isinstance(right, ast.Constant) and abs(right.value) > MAX_LITERAL_EXPONENT:
                raise UnsafeExpression("exponent too large")
            if isinstance(node.left, ast.Constant) and isinstance(right, ast.BinOp) \
                    and isinstance(right.op, ast.Pow):
                raise UnsafeExpression("stacked numeric power")
        _check(node.left, names)
        return _check(node.right, names)
    if isinstance(node, ast.Call):
        func = node.func
        if not isinstance(func, ast.Name) or func.id.startswith("_") \
                or not callable(names.get(func.id)):
            raise UnsafeExpression("only namespace functions may be called")
        if node.keywords:
            raise UnsafeExpression("keyword arguments not allowed")
        for arg in node.args:
            _check(arg, names)
        return None
    raise UnsafeExpression(f"syntax not allowed: {type(node).__name__}")


def validate(text: str, names: dict) -> str:
    """Return normalised text (``^`` -> ``**``) or raise UnsafeExpression."""
    if not isinstance(text, str):
        raise UnsafeExpression("expression must be text")
    if len(text) > MAX_LEN:
        raise UnsafeExpression("expression too long")
    normalised = text.replace("^", "**").replace("\N{MINUS SIGN}", "-")
    try:
        tree = ast.parse(normalised.strip(), mode="eval")
    except SyntaxError as exc:
        raise sp.SympifyError(text, exc) from None
    _check(tree, names)
    return normalised


def safe_sympify(text: str, locals: dict):
    """sympify() restricted to the grammar above."""
    return sp.sympify(validate(text, locals), locals=locals)
