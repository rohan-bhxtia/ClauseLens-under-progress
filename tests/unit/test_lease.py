
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from clauselens.schemas.lease import Fact, LeaseFacts


# Find the gold JSON files
GOLD_DIR = Path(__file__).parent.parent.parent / "eval" / "gold"
GOLD_FILES = sorted(GOLD_DIR.glob("*.json"))


# TEST 1: A valid fact should be accepted
def test_found_fact_is_valid():
    fact = Fact[int](
        status="found",
        answer=30000,
        line="Monthly rent is Rs. 30000",
        page=2,
    )

    assert fact.answer == 30000


# TEST 2: A found fact without an answer should be rejected
def test_found_fact_without_answer_is_invalid():
    with pytest.raises(ValidationError):
        Fact[int](
            status="found",
            answer=None,
            line="Monthly rent is Rs. 25,000",
            page=2,
        )


# TEST 3: A not_stated fact cannot have an answer
def test_not_stated_fact_with_answer_is_invalid():
    with pytest.raises(ValidationError):
        Fact[int](
            status="not_stated",
            answer=25000,
        )


# TEST 4: An unclear fact cannot have an answer
def test_unclear_fact_with_answer_is_invalid():
    with pytest.raises(ValidationError):
        Fact[int](
            status="unclear",
            answer=25000,
            line="The lease contains conflicting terms.",
            page=2,
        )


# TEST 5: Make sure we have exactly five gold JSON files
def test_we_have_five_gold_files():
    assert len(GOLD_FILES) == 5


# TEST 6: Every gold JSON file must match our schema
@pytest.mark.parametrize("path", GOLD_FILES, ids=lambda p: p.stem)
def test_gold_file_is_valid(path):
    LeaseFacts.model_validate_json(path.read_text())


# TEST 7: A misspelled field name must be rejected
def test_typo_in_fact_name_is_rejected():
    data = json.loads((GOLD_DIR / "lease_01.json").read_text())
    data["tennant_notice"] = {"status": "not_stated"}

    with pytest.raises(ValidationError):
        LeaseFacts.model_validate(data)
