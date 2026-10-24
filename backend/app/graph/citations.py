"""Citation post-processing utilities.

``finalize`` cleans LLM output by:
- Splitting comma-separated markers like [1, 2] → [1][2]
- Normalising markdown-style [N](url) → [N]
- Removing out-of-range / invented citation numbers
- Renumbering markers by first appearance so the final list is compact
"""

import re
from typing import Any


# Matches [1, 2] or [1,2]
_COMMA_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)+)\]")

# Matches [N](anything) – markdown link style citations
_MD_LINK_RE = re.compile(r"\[(\d+)\]\([^)]*\)")

# Matches bare [N]
_NUM_RE = re.compile(r"\[(\d+)\]")


def _split_comma_citations(text: str) -> str:
    """Turn [1, 2] into [1][2]."""
    def _expand(m: re.Match) -> str:
        numbers = re.findall(r"\d+", m.group(1))
        return "".join(f"[{n}]" for n in numbers)

    return _COMMA_RE.sub(_expand, text)


def _normalise_md_links(text: str) -> str:
    """Turn [N](url) into [N]."""
    return _MD_LINK_RE.sub(lambda m: f"[{m.group(1)}]", text)


def finalize(
    text: str,
    sources: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    """Clean citation markers in *text* against the provided *sources* list.

    Parameters
    ----------
    text:
        The raw LLM output containing citation markers such as ``[1]``,
        ``[1](https://...)`` or ``[1, 2]``.
    sources:
        The ordered list of source dicts that were provided to the LLM.
        Each dict must have at least a ``"url"`` key.

    Returns
    -------
    (cleaned_text, used_sources):
        *cleaned_text* has markers renumbered by first appearance and
        out-of-range markers removed.
        *used_sources* is the subset of *sources* actually cited, in
        first-appearance order.
    """
    # Step 1: normalise syntax
    text = _split_comma_citations(text)
    text = _normalise_md_links(text)

    n_sources = len(sources)

    # Step 2: first pass – collect first-appearance order of valid indices
    seen: dict[int, int] = {}  # original 1-based index → new 1-based index
    for m in _NUM_RE.finditer(text):
        original = int(m.group(1))
        if 1 <= original <= n_sources and original not in seen:
            seen[original] = len(seen) + 1

    # Step 3: second pass – rewrite markers
    def _replace(m: re.Match) -> str:
        original = int(m.group(1))
        if original in seen:
            return f"[{seen[original]}]"
        # Out-of-range or invented – remove the marker entirely
        return ""

    text = _NUM_RE.sub(_replace, text)

    # Step 4: build the ordered list of used sources (1-based original indices
    # sorted by their assigned new index)
    used = [sources[orig - 1] for orig, _ in sorted(seen.items(), key=lambda kv: kv[1])]

    return text, used
