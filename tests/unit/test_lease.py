import pytest
from clauselens.schemas.lease import Fact

def test_found_fact_is_valid():
    fact = Fact[int](
    status="found",
    answer=30000,
    line= " Monthly rent is Rs.30000",
    page = 2
    )

    assert fact.answer ==30000


def test_found_fact_without_answer_is_invalid():
    with pytest.raises(ValueError):
        Fact[int](
            status="found",
            answer=None,
            line="Monthly rent is Rs. 25,000",
            page=2
        )