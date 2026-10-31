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

MAX_LEN = 8000  # stored srepr rows reach ~3900 characters
MAX_LITERAL_EXPONENT = 1000
_SYMBOL = re.compile(r"[A-Za-z][A-Za-z0-9]{0,2}\Z")
_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.BitAnd, ast.BitOr)
_COMPARE = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
_UNARY = (ast.UAdd, ast.USub)
_IDENT = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,30}\Z")
_NUMERIC = re.compile(r"[-+]?[0-9]+(\.[0-9]*)?([eE][-+]?[0-9]+)?\Z")
# Constructors that take a name or a decimal as their first string argument.
_NAMED = {"Symbol", "Dummy", "Wild", "Function"}
_DECIMAL = {"Float", "Integer", "Rational"}
from sympy.core.assumptions import _assume_defined
_ASSUMPTIONS = set(_assume_defined) | {"commutative"}
_HELPERS = {"sqrt", "root", "cbrt", "exp", "log", "ln", "Abs", "re", "im", "conjugate"}


def _builtin_callables() -> dict:
    """SymPy expression classes and plain math helpers, nothing that parses or does I/O."""
    out = {}
    for name in dir(sp):
        if name.startswith("_"):
            continue
        obj = getattr(sp, name)
        if name in _HELPERS or (isinstance(obj, type) and issubclass(obj, sp.Basic)) \
                or isinstance(obj, sp.FunctionClass):
            out[name] = obj
    return out


SYMPY_CALLABLES = _builtin_callables()


class UnsafeExpression(ValueError):
    pass


def _check(node, names: dict) -> None:
    if isinstance(node, ast.Expression):
        return _check(node.body, names)
    if isinstance(node, ast.Constant):
        value = node.value
        if not isinstance(value, (bool, int, float)):
            raise UnsafeExpression(f"literal not allowed: {value!r}")
        # Exact rationals in stored rows have 100+ digit literals; size only matters as an
        # exponent, which the Pow rule below bounds.
        return None
    if isinstance(node, ast.Tuple):
        for item in node.elts:
            _check(item, names)
        return None
    if isinstance(node, ast.Compare) and all(isinstance(op, _COMPARE) for op in node.ops):
        _check(node.left, names)
        for item in node.comparators:
            _check(item, names)
        return None
    if isinstance(node, ast.Name):
        if node.id.startswith("_"):
            raise UnsafeExpression(f"name not allowed: {node.id}")
        if node.id in names or node.id in SYMPY_CALLABLES or _SYMBOL.match(node.id):
            return None
        raise UnsafeExpression(f"unknown name: {node.id}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, _UNARY):
        return _check(node.operand, names)
    if isinstance(node, ast.BinOp) and isinstance(node.op, _BINOPS):
        if isinstance(node.op, ast.Pow):
            right = node.right
            if isinstance(right, ast.UnaryOp):
                right = right.operand
            if isinstance(right, ast.Constant) and not isinstance(right.value, (int, float)):
                raise UnsafeExpression("exponent must be a number")
            if isinstance(right, ast.Constant) and abs(right.value) > MAX_LITERAL_EXPONENT:
                raise UnsafeExpression("exponent too large")
            if isinstance(node.left, ast.Constant) and isinstance(right, ast.BinOp) \
                    and isinstance(right.op, ast.Pow):
                raise UnsafeExpression("stacked numeric power")
        _check(node.left, names)
        return _check(node.right, names)
    if isinstance(node, ast.Call):
        func = node.func
        if not isinstance(func, ast.Name) or func.id.startswith("_"):
            raise UnsafeExpression("only namespace functions may be called")
        target = names.get(func.id, SYMPY_CALLABLES.get(func.id))
        if not callable(target) or (func.id not in names and func.id not in SYMPY_CALLABLES):
            raise UnsafeExpression("only namespace functions may be called")
        for keyword in node.keywords:
            if func.id not in _NAMED or keyword.arg not in _ASSUMPTIONS \
                    or not isinstance(keyword.value, ast.Constant) \
                    or not isinstance(keyword.value.value, bool):
                raise UnsafeExpression("keyword arguments not allowed")
        for index, arg in enumerate(node.args):
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if index == 0 and func.id in _NAMED and _IDENT.match(arg.value):
                    continue
                if func.id in _DECIMAL and _NUMERIC.match(arg.value):
                    continue
                raise UnsafeExpression(f"string not allowed: {arg.value!r}")
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
