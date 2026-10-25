# for parser.py 

from clauselens.ingest.parser import clean_text


def test_clean_text_fixes_rupee_symbol():
    assert clean_text("rent of n25,000") == "rent of ₹25,000"


def test_clean_text_preserves_words_starting_with_n():
    assert clean_text("Tenant") == "Tenant"