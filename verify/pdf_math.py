"""Read integral sheets and mark schemes from the committed PDFs.

The text layer is positioned TeX, not a sentence. This module rebuilds fractions,
radicals, scripts, and integrals from glyph boxes and fraction bars. A row is
usable only when the caller can prove the reading. A failed reading returns None.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import pymupdf

INTEGRAL_TEXT = {"ˆ", "∫", "Z"}
RADICAL_TEXT = set("pqrstuvw")
OPENERS = {"(", "[", "{", "⌊"}
CLOSERS = {")", "]", "}", "⌋"}
STOP_WORDS = {"where", "for", "if"}
FUNCS = {
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "sec": "sec",
    "csc": "csc",
    "cot": "cot",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "sech": "sech",
    "ln": "log",
    "log": "log",
    "exp": "exp",
    "arcsin": "asin",
    "arccos": "acos",
    "arctan": "atan",
    "asin": "asin",
    "acos": "acos",
    "atan": "atan",
    "gamma": "gamma",
    "Gamma": "gamma",
    "Γ": "gamma",
    "zeta": "zeta",
    "ζ": "zeta",
    "W": "LambertW",
    "arccot": "acot",
    "arcsec": "asec",
    "arccsc": "acsc",
    "arcsinh": "asinh",
    "arccosh": "acosh",
    "arctanh": "atanh",
    "arccsch": "acsch",
    "arcsech": "asech",
    "arccoth": "acoth",
}
INVERSES = {
    "sin": "asin",
    "cos": "acos",
    "tan": "atan",
    "sinh": "asinh",
    "cosh": "acosh",
    "tanh": "atanh",
    "sec": "asec",
    "csc": "acsc",
    "cot": "acot",
}
NUMBER = re.compile(r"\d+(?:\.\d+)?")
PROBLEM_NO = re.compile(r"^(\d+)[.:]$")
FUNC_NAMES = (
    "arcsinh",
    "arccosh",
    "arctanh",
    "arccsch",
    "arcsech",
    "arccoth",
    "arcsin",
    "arccos",
    "arctan",
    "arccsc",
    "arcsec",
    "arccot",
    "sinh",
    "cosh",
    "tanh",
    "sech",
    "sin",
    "cos",
    "tan",
    "sec",
    "csc",
    "cot",
    "log",
    "ln",
    "exp",
)
FUNC_PREFIXES = {name[:i] for name in FUNC_NAMES for i in range(1, len(name) + 1)}
STANDALONE = set("+-−=()[]{}·×,ˆ∫√⌊⌋π∞θΓζ") | {"·"}
DIFF = re.compile(r"^d([a-zA-Z]|theta)$")
LETTER = re.compile(r"^[a-zA-Z]$")


@dataclass
class Node:
    kind: str
    x0: float
    y0: float
    x1: float
    y1: float
    size: float
    text: str = ""
    font: str = ""
    sup: "Node | None" = None
    sub: "Node | None" = None
    kids: list["Node"] = field(default_factory=list)

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2


@dataclass
class Bar:
    x0: float
    x1: float
    y: float

    @property
    def w(self) -> float:
        return self.x1 - self.x0


def _clean(text: str) -> str:
    return (
        text.replace("\u2212", "-")
        .replace("\u00b7", "·")
        .replace("\u221e", "∞")
        .replace("\u00a0", " ")
        .strip()
    )


def _is_integral_node(node: Node) -> bool:
    if node.kind != "text":
        return False
    if node.text in {"ˆ", "∫"}:
        return True
    return node.text == "Z" and node.font.startswith("CMEX")


def _is_radical_glyph(node: Node) -> bool:
    if node.kind != "text":
        return False
    if node.text in {"√", "√"}:
        return True
    return node.font.startswith("CMEX") and node.text in RADICAL_TEXT


def _can_extend(text: str, font: str, nxt: str, gap: float, size: float) -> bool:
    if gap > max(1.6, 0.22 * size):
        return False
    if text in STANDALONE or nxt in STANDALONE or font.startswith("CMEX"):
        return False
    if nxt == "." and NUMBER.fullmatch(text):
        return True
    if "." in text or nxt == ".":
        return False
    if text.isdigit() and nxt.isdigit():
        return True
    if text.isdigit() or nxt.isdigit():
        return False
    # Function names arrive as one roman span ("sin", "exp"). Joining italic
    # letters here turns the constant e followed by x into the non-name "ex".
    return False


def _keep_span(text: str) -> bool:
    if text in FUNC_NAMES or text in {"ˆ", "∫", "√", "π", "∞", "θ", "Γ", "ζ"}:
        return True
    if NUMBER.fullmatch(text) or PROBLEM_NO.match(text):
        return True
    if len(text) == 1:
        return True
    return False


def _nodes_from_span(span) -> list[Node]:
    font = span.get("font") or ""
    size = float(span["size"])
    raw = "".join(glyph["c"] for glyph in span.get("chars") or [])
    if font.startswith("CMEX"):
        raw = raw.replace("\x0c", "|")
    text = _clean(raw)
    if font.startswith("CMEX"):
        # Computer Modern extension slots used as ordinary fences in these sheets.
        for src, dst in (
            ("\x00", "("),
            ("\x01", ")"),
            ("\x10", "("),
            ("\x11", ")"),
            ("\x12", "("),
            ("\x13", ")"),
            ("!", ")"),
            ("\x0c", "|"),
        ):
            text = text.replace(src, dst)
    if not text or text.startswith("Page"):
        return []
    x0, y0, x1, y1 = span["bbox"]
    if y0 < 55 or y0 > 800:
        return []
    if _keep_span(text):
        return [Node("text", x0, y0, x1, y1, size, text, font)]
    glyphs = []
    for glyph in span.get("chars") or []:
        raw_piece = glyph["c"]
        piece = "|" if font.startswith("CMEX") and raw_piece == "\x0c" else _clean(raw_piece)
        if not piece or piece == " ":
            continue
        if font.startswith("CMEX"):
            piece = {
                "\x00": "(",
                "\x01": ")",
                "\x10": "(",
                "\x11": ")",
                "\x12": "(",
                "\x13": ")",
                "!": ")",
                "\x0c": "|",
            }.get(piece, piece)
        gx0, gy0, gx1, gy1 = glyph["bbox"]
        glyphs.append((gx0, gy0, gx1, gy1, size, piece, font))
    nodes: list[Node] = []
    prev: Node | None = None
    for gx0, gy0, gx1, gy1, gsize, piece, gfont in glyphs:
        if prev is not None and _can_extend(prev.text, prev.font, piece, gx0 - prev.x1, gsize):
            prev.text += piece
            prev.x1 = max(prev.x1, gx1)
            prev.y0 = min(prev.y0, gy0)
            prev.y1 = max(prev.y1, gy1)
            continue
        if piece == ".":
            continue
        prev = Node("text", gx0, gy0, gx1, gy1, gsize, piece, gfont)
        nodes.append(prev)
    return _merge_vertical_bars(_merge_function_names(nodes))


def _take_function_name(nodes: list[Node], index: int, name: str) -> list[Node] | None:
    """Match ``name`` against glyphs that may already be a whole syllable.

    ``cot`` is often one span, so ``arccot`` is the three letters ``arc`` plus
    that span, not six single letters. A gap or a superscript breaks the name.
    """
    chosen: list[Node] = []
    pos = 0
    cursor = index
    while pos < len(name):
        if cursor >= len(nodes):
            return None
        node = nodes[cursor]
        text = node.text.strip()
        if not text or name[pos : pos + len(text)] != text:
            return None
        if chosen:
            gap = node.x0 - chosen[-1].x1
            if gap > max(1.6, 0.22 * node.size):
                return None
            if abs(node.size - chosen[0].size) > 0.8:
                return None
            if abs(node.cy - chosen[0].cy) > max(2.0, 0.35 * chosen[0].size):
                return None
        chosen.append(node)
        pos += len(text)
        cursor += 1
    return chosen


def _merge_function_names(nodes: list[Node]) -> list[Node]:
    """Join glyphs that spell a whole function name, and nothing shorter.

    ``cos(`` is one span, so the letters are split before this pass. ``ex`` is
    the constant e times x and must stay two glyphs.
    """
    if len(nodes) < 2:
        return nodes
    names = sorted(FUNC_NAMES, key=len, reverse=True)
    out: list[Node] = []
    index = 0
    while index < len(nodes):
        matched = None
        for name in names:
            matched = _take_function_name(nodes, index, name)
            if matched is not None:
                break
        if matched is None:
            out.append(nodes[index])
            index += 1
            continue
        host = matched[0]
        host.text = name
        host.x0 = min(node.x0 for node in matched)
        host.x1 = max(node.x1 for node in matched)
        host.y0 = min(node.y0 for node in matched)
        host.y1 = max(node.y1 for node in matched)
        out.append(host)
        index += len(matched)
    return out


def _merge_vertical_bars(nodes: list[Node]) -> list[Node]:
    """Stack CMEX extension pieces of one absolute-value bar into a single glyph."""
    bars = [node for node in nodes if node.text == "|"]
    if len(bars) < 2:
        return nodes
    others = [node for node in nodes if node.text != "|"]
    bars.sort(key=lambda node: (node.x0, node.y0))
    merged: list[Node] = []
    for bar in bars:
        if merged and abs(bar.cx - merged[-1].cx) < 2.5 and bar.y0 <= merged[-1].y1 + 2.5:
            host = merged[-1]
            host.x0 = min(host.x0, bar.x0)
            host.x1 = max(host.x1, bar.x1)
            host.y0 = min(host.y0, bar.y0)
            host.y1 = max(host.y1, bar.y1)
            host.size = max(host.size, bar.y1 - bar.y0, host.size)
            continue
        merged.append(bar)
    return sorted(others + merged, key=lambda node: (node.x0, node.y0))


def page_primitives(page) -> tuple[list[Node], list[Bar]]:
    nodes: list[Node] = []
    for block in page.get_text("rawdict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                nodes.extend(_nodes_from_span(span))
    bars: list[Bar] = []
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        if rect.height > 1.4 or rect.width < 2.2 or rect.width > 200:
            continue
        if rect.y0 < 55:
            continue
        bars.append(Bar(rect.x0, rect.x1, (rect.y0 + rect.y1) / 2))
    return nodes, bars


def _overlaps_bar(node: Node, bar: Bar, pad: float = 1.6) -> bool:
    return node.cx >= bar.x0 - pad and node.cx <= bar.x1 + pad


def _above(node: Node, bar: Bar) -> bool:
    return node.y1 <= bar.y + 1.8 and bar.y - node.y1 < 16 and node.y0 > bar.y - 28


def _below(node: Node, bar: Bar) -> bool:
    if node.y1 >= bar.y + 28:
        return False
    if node.y0 >= bar.y - 1.8 and node.y0 - bar.y < 16:
        return True
    # A denominator's font box can start above the fraction bar. Keep it when
    # the center is still below the bar and the overhang is only a few points.
    overhang = bar.y - node.y0
    if node.cy <= bar.y or overhang <= 1.8:
        return False
    return overhang <= max(6.0, 0.55 * node.size)


def _union_box(nodes: list[Node], fallback: Node) -> tuple[float, float, float, float]:
    if not nodes:
        return fallback.x0, fallback.y0, fallback.x1, fallback.y1
    return (
        min(n.x0 for n in nodes),
        min(n.y0 for n in nodes),
        max(n.x1 for n in nodes),
        max(n.y1 for n in nodes),
    )


def _script_band(host: Node, script: Node) -> str | None:
    # x + 1/x is a sum. The inner fraction sits below the plus and is not its subscript.
    if host.kind == "text" and host.text.strip() in {"+", "-", "="} and script.kind in {"frac", "sqrt", "paren"}:
        return None
    if script.kind == "text":
        token = script.text.strip()
        if token in {"=", ",", "·", "×", ":"} or token in OPENERS or token in CLOSERS:
            return None
        if token in STOP_WORDS or "where" in token:
            return None
    if _is_integral_node(script) or _is_radical_glyph(script):
        return None
    smaller = script.size <= host.size * 0.92
    if not smaller:
        return None
    mid = (host.y0 + host.y1) / 2
    above = script.y0 < host.y0 - 0.35 and script.cy < mid
    below = script.y1 > host.y1 + 0.35 and script.cy > mid
    if above and not below:
        return "sup"
    if below and not above:
        return "sub"
    return None


def _attach_script(host: Node, script: Node, band: str) -> None:
    current = host.sup if band == "sup" else host.sub
    if current is None:
        attached = script
    else:
        kids = []
        if current.kind == "row":
            kids.extend(current.kids)
        else:
            kids.append(current)
        kids.append(script)
        kids.sort(key=lambda n: n.x0)
        attached = Node(
            "row",
            min(n.x0 for n in kids),
            min(n.y0 for n in kids),
            max(n.x1 for n in kids),
            max(n.y1 for n in kids),
            max(n.size for n in kids),
            kids=kids,
        )
    if band == "sup":
        host.sup = attached
    else:
        host.sub = attached


def merge_scripts(nodes: list[Node]) -> list[Node]:
    nodes = sorted(nodes, key=lambda n: (n.x0, n.y0))
    while len(nodes) > 1:
        best = None
        for s_index, script in enumerate(nodes):
            for h_index, host in enumerate(nodes):
                if h_index == s_index:
                    continue
                if host.x1 > script.cx + 0.8:
                    continue
                gap = script.x0 - host.x1
                if gap > 9:
                    continue
                band = _script_band(host, script)
                if band is None:
                    continue
                score = (-gap, host.x1)
                if best is None or score > best[0]:
                    best = (score, h_index, s_index, band)
        if best is None:
            break
        _, h_index, s_index, band = best
        host = nodes[h_index]
        script = nodes[s_index]
        _attach_script(host, script, band)
        del nodes[s_index]
    return sorted(nodes, key=lambda n: n.x0)


def _near_below(nodes: list[Node]) -> list[Node]:
    if len(nodes) < 2:
        return nodes
    anchor = min(node.y0 for node in nodes)
    return [node for node in nodes if node.y0 <= anchor + 8.0]


def _near_above(nodes: list[Node]) -> list[Node]:
    if len(nodes) < 2:
        return nodes
    anchor = max(node.y1 for node in nodes)
    return [node for node in nodes if node.y1 >= anchor - 8.0]


def _bar_candidates(bar: Bar, nodes: list[Node]) -> tuple[list[Node], list[Node]]:
    above = [n for n in nodes if _overlaps_bar(n, bar) and _above(n, bar)]
    below = [n for n in nodes if _overlaps_bar(n, bar) and _below(n, bar)]
    # A short bar is a limit or a one-digit fraction. The next limit is about
    # 15 points away and shares that narrow x-range. Tall display fractions
    # keep the wider window.
    if bar.w < 12:
        above = _near_above(above)
        below = _near_below(below)
    return above, below


def _peel_fence_power(nodes: list[Node]) -> tuple[list[Node], Node | None]:
    """A small digit just right of a closing fence is the power of that group, not another term."""
    if len(nodes) < 2:
        return nodes, None
    ordered = sorted(nodes, key=lambda n: n.x0)
    power = ordered[-1]
    fence = ordered[-2]
    if power.kind != "text" or not _is_close(fence):
        return nodes, None
    if power.size > fence.size * 0.92:
        return nodes, None
    if power.x0 - fence.x1 > 2.5:
        return nodes, None
    if power.cy >= (fence.y0 + fence.y1) / 2:
        return nodes, None
    return ordered[:-1], power


def _root_index(radical: Node, nodes: list[Node]) -> Node | None:
    """A small digit in the crook of a CMEX radical is the root index, not a factor."""
    if not (radical.font.startswith("CMEX") and radical.text in RADICAL_TEXT):
        return None
    found = None
    for node in nodes:
        if node is radical or node.kind != "text":
            continue
        token = node.text.strip()
        if not NUMBER.fullmatch(token):
            continue
        if node.size > radical.size * 0.7:
            continue
        if node.x0 > radical.cx or node.x1 < radical.x0 - 1:
            continue
        if node.cy < radical.y0 - 2 or node.cy > radical.y1 + 2:
            continue
        found = node
    return found


def _radical_for(bar: Bar, nodes: list[Node]) -> Node | None:
    found = None
    for node in nodes:
        if not _is_radical_glyph(node):
            continue
        if bar.x0 - node.x1 > 6 or node.x1 - bar.x0 > 8:
            continue
        # The radical hook sits a few points above its vinculum. A fraction
        # bar inside the root is much lower and must not claim this glyph.
        if abs(node.y0 - bar.y) > 10:
            continue
        if found is None or node.x1 > found.x1:
            found = node
    return found


def structure(nodes: list[Node], bars: list[Bar]) -> list[Node]:
    nodes = list(nodes)
    bars = list(bars)
    while bars:
        bars.sort(key=lambda b: (b.w, b.x0))
        built = False
        for bar in list(bars):
            above, below = _bar_candidates(bar, nodes)
            radical = _radical_for(bar, nodes)
            # A radical vinculum can sit just under a fraction bar, so the
            # fraction's numerator is also "above" this bar. The root does not
            # consume that numerator.
            if radical is not None and below:
                index = _root_index(radical, nodes)
                captured = [radical, *below]
                if index is not None:
                    captured.append(index)
                    below = [n for n in below if n is not index]
                rest = [n for n in nodes if n not in captured]
                inner_bars = [b for b in bars if b is not bar]
                body = structure(below, inner_bars)
                box = _union_box(captured, radical)
                kids = [_as_row(body)]
                if index is not None:
                    kids.append(index)
                sqrt = Node(
                    "sqrt",
                    box[0],
                    box[1],
                    max(bar.x1, box[2]),
                    box[3],
                    radical.size,
                    kids=kids,
                )
                nodes = rest + [sqrt]
                bars = [b for b in bars if b is not bar]
                built = True
                break
            below, fence_power = _peel_fence_power(below)
            if above and below:
                captured = above + below
                rest = [n for n in nodes if n not in captured and n is not fence_power]
                inner_bars = [b for b in bars if b is not bar]
                num = structure(above, inner_bars)
                den = structure(below, inner_bars)
                box = _union_box(captured, captured[0])
                right = box[2] if fence_power is not None else max(bar.x1, box[2])
                frac = Node(
                    "frac",
                    min(bar.x0, box[0]),
                    box[1],
                    right,
                    box[3],
                    max(n.size for n in captured),
                    kids=[_as_row(num), _as_row(den)],
                )
                if fence_power is not None:
                    frac.sup = fence_power
                nodes = rest + [frac]
                bars = [b for b in bars if b is not bar]
                built = True
                break
        if not built:
            break
    return group_fences(extend_superscripts(merge_scripts(nodes)))


def extend_superscripts(nodes: list[Node]) -> list[Node]:
    """A superscript sum is several script-sized glyphs, not one attached atom.

    e^{-x^2+4x+1} attaches -x^2 first. The rest of the exponent stays beside it
    at the same size and height. Fold those glyphs into the superscript.
    """
    nodes = sorted(nodes, key=lambda n: (n.x0, n.y0))
    consumed: set[int] = set()
    for host in nodes:
        sup = host.sup
        if sup is None:
            continue
        while True:
            nxt = None
            for node in nodes:
                if node is host or id(node) in consumed or node.sup or node.sub:
                    continue
                if abs(node.size - sup.size) > max(1.6, 0.25 * sup.size):
                    continue
                if abs(node.cy - sup.cy) > max(3.5, 0.55 * sup.size):
                    continue
                gap = node.x0 - sup.x1
                if gap < -0.8 or gap > 4.5:
                    continue
                nxt = node
                break
            if nxt is None:
                break
            kids = list(sup.kids) if sup.kind == "row" else [sup]
            kids.append(nxt)
            sup = _as_row(kids)
            host.sup = sup
            consumed.add(id(nxt))
    if not consumed:
        return nodes
    return [node for node in nodes if id(node) not in consumed]


def _as_row(nodes: list[Node]) -> Node:
    if len(nodes) == 1:
        return nodes[0]
    if not nodes:
        return Node("text", 0, 0, 0, 0, 1, "")
    return Node(
        "row",
        min(n.x0 for n in nodes),
        min(n.y0 for n in nodes),
        max(n.x1 for n in nodes),
        max(n.y1 for n in nodes),
        max(n.size for n in nodes),
        kids=sorted(nodes, key=lambda n: n.x0),
    )


def _op(node: Node) -> str | None:
    if node.kind != "text":
        return None
    token = node.text.strip()
    if token in {"+", "-", "=", "·", "×", ","}:
        return token
    return None


def _is_open(node: Node) -> bool:
    return node.kind == "text" and node.text.strip() in OPENERS


def _is_close(node: Node) -> bool:
    return node.kind == "text" and node.text.strip() in CLOSERS


def _stop(node: Node) -> bool:
    if node.kind != "text":
        return False
    token = node.text.strip().rstrip(",.")
    if token in STOP_WORDS or token.startswith("where"):
        return True
    return "where" in node.text


def group_fences(nodes: list[Node]) -> list[Node]:
    out: list[Node] = []
    index = 0
    while index < len(nodes):
        node = nodes[index]
        if node.kind == "text" and node.text.strip() == "|":
            close = None
            for cursor in range(index + 1, len(nodes)):
                if nodes[cursor].kind == "text" and nodes[cursor].text.strip() == "|":
                    close = cursor
                    break
            if close is None:
                out.append(node)
                index += 1
                continue
            inner = group_fences(nodes[index + 1 : close])
            closer = nodes[close]
            grouped = Node(
                "abs",
                node.x0,
                min(n.y0 for n in [node, closer, *inner]) if inner else min(node.y0, closer.y0),
                closer.x1,
                max(n.y1 for n in [node, closer, *inner]) if inner else max(node.y1, closer.y1),
                node.size,
                kids=[_as_row(inner)],
            )
            out.append(grouped)
            index = close + 1
            continue
        if not _is_open(node):
            out.append(node)
            index += 1
            continue
        depth = 1
        cursor = index + 1
        while cursor < len(nodes) and depth:
            if _is_open(nodes[cursor]):
                depth += 1
            elif _is_close(nodes[cursor]):
                depth -= 1
            cursor += 1
        if depth:
            return nodes
        inner = group_fences(nodes[index + 1 : cursor - 1])
        opener = node.text.strip()
        kind = "floor" if opener == "⌊" else "paren"
        closer = nodes[cursor - 1]
        grouped = Node(
            kind,
            node.x0,
            min(n.y0 for n in [node, *inner]) if inner else node.y0,
            closer.x1,
            max(n.y1 for n in [node, *inner]) if inner else node.y1,
            node.size,
            kids=[_as_row(inner)],
        )
        grouped.sup = closer.sup
        grouped.sub = closer.sub
        out.append(grouped)
        index = cursor
    return out


def _func_name(node: Node) -> str | None:
    if node.kind != "text" or node.sup or node.sub:
        return None
    return FUNCS.get(node.text.strip())


def _inverse_name(node: Node) -> str | None:
    if node.kind != "text" or node.sup is None:
        return None
    base = FUNCS.get(node.text.strip())
    if base is None:
        return None
    exp = emit(node.sup)
    if exp is None:
        return None
    if exp.replace(" ", "") not in {"-1", "(-1)", "(-(1))", "((-1))"}:
        return None
    return INVERSES.get(node.text.strip())


def _powered(base: str, node: Node) -> str | None:
    if node.sup is not None:
        exp = emit(node.sup)
        if exp is None:
            return None
        base = f"(({base})**({exp}))"
    if node.sub is not None:
        sub = emit(node.sub)
        if sub is None:
            return None
        scripted = _apply_subscript(base, sub)
        if scripted is None:
            return None
        base = scripted
    return base


def _apply_subscript(base: str, sub: str) -> str | None:
    """ζ_3 is the value zeta(3). Other numeric subscripts stay indexed symbols."""
    if base == "zeta" and NUMBER.fullmatch(sub):
        return f"zeta({sub})"
    if NUMBER.fullmatch(sub) or LETTER.fullmatch(sub):
        return f"{base}_{sub}"
    return None


def _dx_numerator(node: Node) -> str | None:
    """A fraction whose numerator is exactly d<var> is dx over the denominator."""
    if node.kind != "frac" or len(node.kids) < 2:
        return None
    num = node.kids[0]
    kids = num.kids if num.kind == "row" else [num]
    if len(kids) != 2:
        return None
    left, right = kids
    if left.kind != "text" or left.text.strip() != "d" or left.sup or left.sub:
        return None
    if right.kind != "text" or right.sup or right.sub:
        return None
    letter = right.text.strip()
    if letter == "θ":
        return "theta"
    if LETTER.fullmatch(letter):
        return letter
    return None


def _dx_variables(nodes: list[Node]) -> list[str]:
    found: list[str] = []

    def walk(node: Node | None) -> None:
        if node is None:
            return
        var = _dx_numerator(node)
        if var:
            found.append(var)
        for kid in node.kids:
            walk(kid)
        walk(node.sup)
        walk(node.sub)

    for node in nodes:
        walk(node)
    return found


def emit(node: Node | None) -> str | None:
    if node is None:
        return None
    if node.kind == "frac":
        if _dx_numerator(node):
            den = emit(node.kids[1])
            if den is None:
                return None
            return _powered("((1)/(" + den + "))", node)
        num = emit(node.kids[0])
        den = emit(node.kids[1])
        if num is None or den is None:
            return None
        return _powered(f"(({num})/({den}))", node)
    if node.kind == "sqrt":
        body = emit(node.kids[0])
        if body is None:
            return None
        if len(node.kids) > 1:
            index = emit(node.kids[1])
            if index is None:
                return None
            rendered = f"(({body})**(1/({index})))"
        else:
            rendered = f"sqrt({body})"
        return _powered(rendered, node)
    if node.kind == "abs":
        body = emit(node.kids[0])
        if body is None:
            return None
        return _powered(f"Abs({body})", node)
    if node.kind in {"paren", "floor"}:
        body = emit(node.kids[0])
        if body is None:
            return None
        if node.kind == "floor":
            rendered = f"floor({body})"
        else:
            rendered = f"({body})"
        return _powered(rendered, node)
    if node.kind == "row":
        # Scripts are attached before fences are grouped, so ⌊x⌋ inside an
        # exponent is still three glyphs. Group them at emit time.
        return _emit_sum(group_fences(node.kids))
    if node.kind == "integral":
        return None
    if node.kind != "text":
        return None
    inv = _inverse_name(node)
    if inv is not None:
        return inv
    token = node.text.strip()
    base = _emit_base(token)
    if base is None:
        return None
    if node.sup is not None:
        exp = emit(node.sup)
        if exp is None:
            return None
        if token == "e":
            base = f"exp({exp})"
        else:
            base = f"(({base})**({exp}))"
    if node.sub is not None:
        sub = emit(node.sub)
        if sub is None:
            return None
        scripted = _apply_subscript(base, sub)
        if scripted is None:
            return None
        base = scripted
    return base


def _emit_base(token: str) -> str | None:
    mapping = {
        "π": "pi",
        "∞": "oo",
        "θ": "theta",
        "Γ": "gamma",
        "ζ": "zeta",
        "·": None,
        "×": None,
        "ˆ": None,
        "∫": None,
        "√": None,
    }
    if token in mapping:
        return mapping[token]
    if token in {"+", "-", "=", ",", "(", ")", "[", "]", "{", "}"}:
        return None
    if token == "e":
        return "E"
    if token in FUNCS:
        return FUNCS[token]
    if NUMBER.fullmatch(token):
        return token
    if re.fullmatch(r"[a-zA-Z](?:_[a-zA-Z0-9]+)?", token):
        return token
    return None


def _emit_sum(nodes: list[Node]) -> str | None:
    nodes = [n for n in nodes if not (_op(n) == "·" or _op(n) == "×")]
    if not nodes:
        return None
    return _parse_sum(nodes, 0)[0]


def _parse_sum(nodes: list[Node], index: int) -> tuple[str | None, int]:
    if index < len(nodes) and _op(nodes[index]) == "-":
        rhs, index = _parse_prod(nodes, index + 1)
        if rhs is None:
            return None, index
        left = f"(-({rhs}))"
    else:
        left, index = _parse_prod(nodes, index)
        if left is None:
            return None, index
    while index < len(nodes) and _op(nodes[index]) in {"+", "-", "="}:
        op = _op(nodes[index])
        rhs, index = _parse_prod(nodes, index + 1)
        if rhs is None:
            return None, index
        if op == "=":
            left = f"Eq({left}, {rhs})"
        elif op == "+":
            left = f"(({left})+({rhs}))"
        else:
            left = f"(({left})-({rhs}))"
    return left, index


def _parse_prod(nodes: list[Node], index: int) -> tuple[str | None, int]:
    factors: list[str] = []
    if index >= len(nodes) or _op(nodes[index]) in {"+", "-", "=", ","}:
        return None, index
    while index < len(nodes) and _op(nodes[index]) not in {"+", "-", "=", ","} and not _stop(nodes[index]):
        if _op(nodes[index]) in {"·", "×"}:
            index += 1
            continue
        piece, index = _parse_factor(nodes, index)
        if piece is None:
            return None, index
        factors.append(piece)
        if index < len(nodes) and (_stop(nodes[index]) or _op(nodes[index]) in {"+", "-", "=", ","}):
            break
    if not factors:
        return None, index
    if len(factors) == 1:
        return factors[0], index
    return "(" + "*".join(f"({part})" for part in factors) + ")", index


def _callable(node: Node) -> tuple[str, str | None] | None:
    """A TeX function, optionally raised to a power. Inverse trig is a name with no power."""
    inv = _inverse_name(node)
    if inv:
        return inv, None
    if node.kind != "text" or node.sub is not None:
        return None
    base = node.text.strip()
    if base not in FUNCS:
        return None
    if node.sup is None:
        return FUNCS[base], None
    exp = emit(node.sup)
    if exp is None:
        return None
    return FUNCS[base], exp


def _argument_follows(nodes: list[Node], index: int) -> bool:
    if index >= len(nodes):
        return False
    nxt = nodes[index]
    if _op(nxt) or _stop(nxt) or _is_integral_node(nxt) or _diff_at(nodes, index):
        return False
    return True


def _starts_call(nodes: list[Node], index: int) -> bool:
    return index < len(nodes) and _callable(nodes[index]) is not None and _argument_follows(nodes, index + 1)


def _parse_factor(nodes: list[Node], index: int) -> tuple[str | None, int]:
    node = nodes[index]
    if _is_integral_node(node):
        return None, index
    called = _callable(node)
    if called and _argument_follows(nodes, index + 1):
        name, power = called
        nxt = nodes[index + 1]
        if nxt.kind in {"paren", "floor"}:
            # ln(x)^2 puts the 2 on the closing fence, outside the argument.
            # That is a power of the call. A power of x sits on x, inside the fence.
            lifted = nxt.sup if power is None else None
            if lifted is not None:
                nxt.sup = None
            arg = emit(nxt)
            if lifted is not None:
                nxt.sup = lifted
                exp = emit(lifted)
                if exp is None or arg is None:
                    return None, index
                arg_call = f"(({name}({arg}))**({exp}))"
            else:
                arg_call = None
            cursor = index + 2
        else:
            # sin 2x is one argument. The next function starts a new factor: sin x cos x.
            arg, cursor = _parse_factor(nodes, index + 1)
            if arg is None:
                return None, index
            parts = [arg]
            while cursor < len(nodes) and _argument_follows(nodes, cursor) and not _starts_call(nodes, cursor):
                piece, nxt_cursor = _parse_factor(nodes, cursor)
                if piece is None or nxt_cursor == cursor:
                    break
                parts.append(piece)
                cursor = nxt_cursor
            if len(parts) > 1:
                arg = "(" + "*".join(f"({part})" for part in parts) + ")"
        if arg is None:
            return None, index
        if nxt.kind in {"paren", "floor"} and power is None and nxt.sup is not None:
            call = arg_call
        else:
            call = f"{name}({arg})"
            if power is not None:
                call = f"(({call})**({power}))"
        return call, cursor
    text = emit(node)
    if text is None:
        return None, index
    return text, index + 1


def _diff_at(nodes: list[Node], index: int) -> tuple[str, int] | None:
    node = nodes[index]
    if node.kind != "text":
        return None
    token = node.text.strip()
    match = DIFF.fullmatch(token)
    if match:
        var = "theta" if match.group(1) == "theta" else match.group(1)
        return var, index + 1
    if token == "d" and index + 1 < len(nodes) and nodes[index + 1].kind == "text":
        nxt = nodes[index + 1].text.strip()
        if nxt == "θ":
            return "theta", index + 2
        if LETTER.fullmatch(nxt):
            return nxt, index + 2
    return None


@dataclass
class IntegralReading:
    number: int
    integrand: str
    variable: str
    limits: tuple[str, str] | None
    latex_hint: str


@dataclass
class AnswerReading:
    number: int
    expr: str
    latex_hint: str


def _first_integral(nodes: list[Node]) -> tuple[Node, int] | None:
    for index, node in enumerate(nodes):
        if _is_integral_node(node):
            return node, index
    return None


def _split_stacked_limits(integral: Node) -> None:
    """Upper and lower limits sometimes land in one script row."""
    node = integral.sub if integral.sup is None else integral.sup
    other = "sup" if integral.sup is None else "sub"
    if node is None or integral.sup is not None and integral.sub is not None:
        return
    if node.kind != "row" or len(node.kids) < 2:
        return
    centers = [kid.cy for kid in node.kids]
    if max(centers) - min(centers) < 5:
        return
    mid = (max(centers) + min(centers)) / 2
    upper = [kid for kid in node.kids if kid.cy <= mid]
    lower = [kid for kid in node.kids if kid.cy > mid]
    if not upper or not lower:
        return
    integral.sup = _as_row(upper)
    integral.sub = _as_row(lower)


def read_integral_row(nodes: list[Node]) -> tuple[str, str, tuple[str, str] | None] | None:
    found = _first_integral(nodes)
    if found is None:
        return None
    integral, index = found
    _split_stacked_limits(integral)
    lo = emit(integral.sub) if integral.sub is not None else None
    hi = emit(integral.sup) if integral.sup is not None else None
    body: list[Node] = []
    cursor = index + 1
    variable = None
    while cursor < len(nodes):
        if _stop(nodes[cursor]) or _op(nodes[cursor]) == ",":
            break
        diff = _diff_at(nodes, cursor)
        if diff is not None:
            variable, cursor = diff
            break
        body.append(nodes[cursor])
        cursor += 1
    if not body:
        return None
    script_vars = _dx_variables(body)
    if variable is None:
        if len(set(script_vars)) != 1:
            return None
        variable = script_vars[0]
    elif any(item != variable for item in script_vars):
        return None
    expr = _emit_sum(body)
    if expr is None:
        return None
    limits = None
    if lo is not None or hi is not None:
        if lo is None or hi is None:
            return None
        limits = (lo, hi)
    return expr, variable, limits


def read_answer_row(nodes: list[Node]) -> str | None:
    if _first_integral(nodes) is not None:
        return None
    expr = _emit_sum(nodes)
    return expr


def _region_nodes(nodes: list[Node], bars: list[Bar], top: float, bottom: float, label: Node):
    chosen = [n for n in nodes if n is not label and top <= n.cy <= bottom]
    region_bars = [b for b in bars if top - 4 <= b.y <= bottom + 4]
    return chosen, region_bars


def readings_from_pdf(path: str) -> dict[int, list[Node]]:
    doc = pymupdf.open(path)
    grouped: dict[int, list[Node]] = {}
    for page in doc:
        nodes, bars = page_primitives(page)
        numbers = []
        for node in nodes:
            match = PROBLEM_NO.match(node.text.strip())
            if match and node.x0 < 200 and int(match.group(1)) <= 80:
                numbers.append((int(match.group(1)), node))
        numbers.sort(key=lambda item: item[1].y0)
        for index, (number, node) in enumerate(numbers):
            if index == 0:
                top = node.y0 - 22
            else:
                top = (numbers[index - 1][1].y0 + node.y0) / 2
            if index + 1 < len(numbers):
                bottom = (node.y0 + numbers[index + 1][1].y0) / 2
            else:
                bottom = 790
            chosen, region_bars = _region_nodes(nodes, bars, top, bottom, node)
            extra = []
            for bar in region_bars:
                band = [glyph for glyph in chosen if _overlaps_bar(glyph, bar) and _below(glyph, bar)]
                anchor = min((glyph.y0 for glyph in band), default=bar.y)
                for glyph in nodes:
                    if glyph is node or glyph in chosen or glyph in extra:
                        continue
                    if glyph.cy <= bottom:
                        continue
                    if not (_overlaps_bar(glyph, bar) and _below(glyph, bar)):
                        continue
                    if bar.w < 12 and glyph.y0 > anchor + 8.0:
                        continue
                    extra.append(glyph)
            chosen = chosen + extra
            if not chosen:
                continue
            grouped[number] = structure(chosen, region_bars)
    return grouped


def integral_readings(path: str) -> dict[int, IntegralReading]:
    found = {}
    for number, nodes in readings_from_pdf(path).items():
        parsed = read_integral_row(nodes)
        if parsed is None:
            continue
        expr, variable, limits = parsed
        found[number] = IntegralReading(number, expr, variable, limits, expr)
    return found


def answer_readings(path: str) -> dict[int, AnswerReading]:
    found = {}
    for number, nodes in readings_from_pdf(path).items():
        expr = read_answer_row(nodes)
        if expr is None:
            continue
        found[number] = AnswerReading(number, expr, expr)
    return found
