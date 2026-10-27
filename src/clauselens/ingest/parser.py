# to correct things in our lease texts .. found by peek_raw.py script

import re 
from docling.document_converter import DocumentConverter
from clauselens.schemas.clause import Block_format

def clean_text(text: str) -> str:
    # fixing the corrupted rupee symbol
    text = re.sub(r"(?<![A-Za-z])n(?=\d)", "₹", text)


    # Remove Markdown escaping from underscores ( landlord __________________)
    text = text.replace(r"\_", "_")

    return text

def parse_pdf(path:str) -> list[Block_format]:

    doc = DocumentConverter().convert(path).document
    blocks: list[Block_format] = []

    for item, level in doc.iterate_items():
        text = getattr(item, "text", "")

        if not text:
            continue

        # skip elements without page info 
        if not item.prov:
            continue

        page = item.prov[0].page_no

        block_mapping = Block_format(
            label = str(item.label),
            text = clean_text(text),
            page = page,
        )


        blocks.append(block_mapping)

    return blocks    


