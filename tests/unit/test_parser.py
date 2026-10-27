
# For parser.py

from clauselens.ingest.parser import clean_text, parse_pdf, normalize
from clauselens.schemas.clause import Block_format
import pytest

# checking clean text function 
def test_clean_text_fixes_rupee_symbol():
    assert clean_text("rent of n25,000") == "rent of ₹25,000"
def test_clean_text_preserves_words_starting_with_n():
    assert clean_text("Tenant") == "Tenant"

# checking parse_pdf fucntion 
def test_parse_pdf_returns_blocks():
    blocks = parse_pdf("data/lease_01.pdf")

    assert len(blocks) > 0
    assert all(isinstance(block, Block_format) for block in blocks)


def test_parse_pdf_preserves_text_and_page_numbers():
    blocks = parse_pdf("data/lease_01.pdf")

    assert all(block.text.strip() for block in blocks)
    assert all(block.page >= 1 for block in blocks)


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ("Hello   world", "Hello world"),
        ("Hello\tworld", "Hello world"),
        ("Hello\nworld", "Hello world"),
        ("  Hello world  ", "Hello world"),
        ("30 days’ notice", "30 days' notice"),
        ("‘tenant’", "'tenant'"),
        ("“rent”", '"rent"'),
        ("Normal text", "Normal text"),
        ("", ""),
    ],
)
def test_normalize(input_text: str, expected: str) -> None:
    assert normalize(input_text) == expected