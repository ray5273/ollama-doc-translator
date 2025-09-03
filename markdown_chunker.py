from typing import List
from markdown_it import MarkdownIt

md = MarkdownIt()

def tokenize_markdown(content: str) -> List[str]:
    """Tokenize markdown content into structural blocks."""
    tokens = md.parse(content)
    lines = content.splitlines()
    blocks: List[str] = []
    for token in tokens:
        if token.map:
            start, end = token.map
            block = "\n".join(lines[start:end])
            if block:
                blocks.append(block)
    return blocks

def chunk_markdown(content: str, max_length: int) -> List[str]:
    """Split markdown content into chunks respecting block boundaries."""
    blocks = tokenize_markdown(content)
    chunks: List[str] = []
    current = ""
    for block in blocks:
        addition = block + "\n\n"
        if len(current) + len(addition) > max_length and current:
            chunks.append(current.rstrip())
            current = ""
        if len(addition) > max_length:
            lines = block.splitlines(True)
            temp = ""
            for line in lines:
                if len(temp) + len(line) > max_length and temp:
                    if current:
                        chunks.append(current.rstrip())
                        current = ""
                    chunks.append(temp.rstrip())
                    temp = ""
                temp += line
            if temp:
                if len(current) + len(temp) > max_length and current:
                    chunks.append(current.rstrip())
                    current = temp
                else:
                    current += temp
            current += "\n"
            continue
        current += addition
    if current.strip():
        chunks.append(current.rstrip())
    return chunks
