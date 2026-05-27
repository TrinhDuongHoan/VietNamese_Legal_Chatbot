from typing import List


class TextNode:
    def __init__(self, text: str):
        self.text = text



def split_document(text: str, chunk_size: int = 600, overlap: int = 80) -> List[TextNode]:
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [TextNode(text)]

    nodes: List[TextNode] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        nodes.append(TextNode(text[start:end]))
        if end == len(text):
            break
        start = max(end - overlap, 0)
    return nodes
