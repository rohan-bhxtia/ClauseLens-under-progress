# grouping the blocks made in parser

import re
from clauselens.ingest.parser import parse_pdf
from clauselens.schemas.clause import Block_format, Clause_format


def is_heading(block: Block_format) -> bool:
    return block.label.lower() in {"section_header", "title"}


def groupBlocks_toClauses(blocks: list[Block_format]) -> list[Clause_format]:
    clauses = []

    current_title = None
    current_number = None
    current_page = None
    current_text = []

    def save_clause():
        if not current_text:
            return

        clauses.append(
            Clause_format(
                number=current_number,
                title=current_title or "Preamble",
                text="\n\n".join(current_text),
                page=current_page or 1,
            )
        )

    for block in blocks:
        if is_heading(block):
            save_clause()

            match = re.match(
                r"^\s*(\d+(?:\.\d+)*)[.)]?\s*(.*)$",
                block.text,
            )

            if match:
                current_number = int(match.group(1).split(".")[0])
                current_title = match.group(2).strip() or block.text.strip()
            else:
                current_number = None
                current_title = block.text.strip()

            current_page = block.page
            current_text = [block.text]

        elif current_text:
            current_text.append(block.text)

        else:
            current_title = "Preamble"
            current_number = None
            current_page = block.page
            current_text.append(block.text)

    save_clause()

    return clauses


if __name__ == "__main__":
    blocks = parse_pdf("data/lease_01.pdf")
    clauses = groupBlocks_toClauses(blocks)

    for clause in clauses:
        print(f"\nClause: {clause.title}")
        print(f"Number: {clause.number}")
        print(f"Page: {clause.page}")
        print(clause.text)
