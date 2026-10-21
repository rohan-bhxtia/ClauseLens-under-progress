from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

# ---------- Answer shapes ----------
# Some answers have two parts, like "60 days" or "5% on renewal".

class Duration(BaseModel):
    amount: int
    unit: Literal["days", "months", "years"]   # only these 3 words allowed

class RentIncrease(BaseModel):
    percent: float
    when: Literal["every_year", "on_renewal", "conditional"]

class Maintenance(BaseModel):
    amount: int
    payer: Literal["tenant", "landlord", "shared"]


# ---------- One fact ----------
# T is a placeholder. Fact[int] means "a fact whose answer is a number",
# Fact[Duration] means "a fact whose answer is like 60 days".
T = TypeVar("T")

class Fact(BaseModel, Generic[T]):
    status: Literal["found", "not_stated", "unclear"]
    answer: T | None = None
    line: str | None = None
    page: int | None = None

    @model_validator(mode="after")      # runs after the fields are filled
    def check_rules(self):
        if self.status == "found":
            if self.answer is None or self.line is None or self.page is None:
                raise ValueError("found needs answer, line and page")
        if self.status == "not_stated":
            # TODO 2: if answer or line is NOT None → raise ValueError("not_stated must be empty")
            pass
        if self.status == "unclear":
            # TODO 3: answer must be None, and line must NOT be None
            pass
        return self


# ---------- The full answer sheet for one lease ----------
class LeaseFacts(BaseModel):
    model_config = ConfigDict(extra="forbid")   # a typo like "tennant_notice" → error

    doc_id: str
    agreement_type: Fact[Literal["rent", "leave_and_licence"]]
    monthly_rent: Fact[int]
    security_deposit: Fact[int]
    # TODO 4: add the other 12 facts. Use the names from your JSON files.
    # Pick the type for each: int, bool, Duration, RentIncrease, Maintenance,
    # or Literal["tenant", "landlord", "both"] for lock_in_applies_to. 
