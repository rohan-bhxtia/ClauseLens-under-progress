# for testing the docling on our leases , to see does the extraction looks fine


from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

for number in range(1, 6):
    pdf = f"data/lease_{number:02d}.pdf"
    output = Path(f"scratch/lease_{number:02d}_raw.md")

    result = converter.convert(pdf)
    text = result.document.export_to_markdown()

    output.parent.mkdir(exist_ok=True)
    output.write_text(text, encoding="utf-8")

    print(f"Saved {output}")




# we did found a bug .. rupees symbol is coming as a cube .. which we need to make fine 