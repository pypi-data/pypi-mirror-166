import re
import textwrap
from typing import List


def extract_indent(x: str) -> str:
    m = re.match("([\\s\t]*).+", x.lstrip("\n"))
    if not m:
        return ""
    return m.group(1)


def left_align(*texts: str, prefix: str = ""):
    blocks: List[str] = []
    for t in texts:
        blocks.append(textwrap.indent(textwrap.dedent(t), prefix=prefix))
    return "\n".join(blocks)
