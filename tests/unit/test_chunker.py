
# Import the function we want to test and the schema for creating test blocks
from clauselens.ingest.chunker import groupBlocks_toClauses
from clauselens.schemas.clause import Block_format


# TEST 1: Check whether numbered headings are split correctly
def test_numbered_heading():
    # Create fake blocks instead of reading a real PDF
    blocks = [
        Block_format(label="section_header", text="1. PREMISES", page=1),
        Block_format(label="text", text="The property is in Delhi.", page=1),
        Block_format(label="section_header", text="2. RENT", page=1),
        Block_format(label="text", text="Monthly rent is 25000.", page=1),
    ]

    # Pass the blocks to our chunker
    clauses = groupBlocks_toClauses(blocks)

    # Check that two clauses were created with the right numbers and titles
    assert len(clauses) == 2
    assert clauses[0].number == 1
    assert clauses[0].title == "PREMISES"
    assert "The property is in Delhi." in clauses[0].text
    assert clauses[1].number == 2
    assert clauses[1].title == "RENT"


# TEST 2: Check whether a heading without a number is handled correctly
def test_unnumbered_heading():
    blocks = [
        Block_format(label="title", text="PARTIES AND DATE", page=1),
        Block_format(label="text", text="Agreement between two parties.", page=1),
    ]

    clauses = groupBlocks_toClauses(blocks)

    # The heading should be preserved, with no clause number
    assert len(clauses) == 1
    assert clauses[0].number is None
    assert clauses[0].title == "PARTIES AND DATE"
    assert "Agreement between two parties." in clauses[0].text


# TEST 3: Check whether a clause can continue onto another page
def test_clause_spanning_multiple_pages():
    blocks = [
        Block_format(label="section_header", text="1. PREMISES", page=1),
        Block_format(label="text", text="The property is in Delhi.", page=1),
        Block_format(label="text", text="The property has two bedrooms.", page=2),
        Block_format(label="section_header", text="2. RENT", page=2),
        Block_format(label="text", text="Monthly rent is 25000.", page=2),
    ]

    clauses = groupBlocks_toClauses(blocks)

    # Both paragraphs should remain in the first clause
    assert len(clauses) == 2
    assert "The property has two bedrooms." in clauses[0].text

    # The clause's page should be its starting page
    assert clauses[0].page == 1
    assert clauses[1].page == 2
