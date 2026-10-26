# to check how docling is handling page numbers...

from docling.document_converter import DocumentConverter

doc = DocumentConverter().convert("data/lease_01.pdf").document

for i, (item, level) in enumerate(doc.iterate_items()):
    print(
        item.label,
        item.prov,
        getattr(item, "text", "")[:40]
    )

    if i >= 14:
        break