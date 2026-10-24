import re

_LINKED = re.compile(r"(\[\d+\])\(https?://[^)\s]+\)")          # [1](https://...) -> [1]
_MULTI = re.compile(r"\[(\d+(?:\s*,\s*\d+)+)\]")                  # [1, 3] -> [1][3]
_CITE = re.compile(r"\[(\d+)\]")


def finalize(markdown: str, sources: list[dict]) -> tuple[str, list[dict]]:
    """Guarantees every [n] in the report points at a real source.
    Drops invented numbers, renumbers by first appearance and keeps only the sources actually cited."""
    text = _LINKED.sub(r"\1", markdown)
    text = _MULTI.sub(lambda m: "".join(f"[{n.strip()}]" for n in m.group(1).split(",")), text)
    order: dict[int, int] = {}

    def remap(m: re.Match) -> str:
        n = int(m.group(1))
        if not 1 <= n <= len(sources):
            return ""
        order.setdefault(n, len(order) + 1)
        return f"[{order[n]}]"

    text = _CITE.sub(remap, text)
    text = re.sub(r"[ \t]+([.,;:])", r"\1", text)
    text = re.sub(r"(?<=\S)[ \t]{2,}", " ", text)
    return text, [sources[n - 1] for n in sorted(order, key=order.get)]
