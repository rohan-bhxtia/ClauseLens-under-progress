from typing import Literal, Generic, TypeVar
from pydantic import BaseModel, model_validator

class Duration(BaseModel):
    amount: int
    unit: Literal["days", "months", "years"]

class RentIncrease(BaseModel):
    percent: float
    when: Literal["every_year", "on_renewal", "conditional"]

class Maintenance(BaseModel):
    amount: int
    payer: Literal["tenant", "landlord", "shared"]

T = TypeVar("T")

class Fact(BaseModel, Generic[T]):
    status: Literal["found","not_stated","unclear"]
    answer: T | None = None
    line: str | None = None # the actual text itself 
    page: int | None = None

    @model_validator(mode="after")
    def check_rules(self):
        if self.status == "found":
            if self.answer is None or self.line is None or self.page is None:
                raise ValueError("Found facts need answer, line, and page")

        if self.status == "not_stated":
            if self.answer is not None or self.line is not None:
                raise ValueError(" Non - stated facts must have no answer or line")

        if self.status == "unclear":
            if self.answer is not None or self.line is None or self.page is None:
                raise ValueError(" Unclear facts need no answer but must have page and line as evidence for unclearness")    

        return self

class LeaseFacts(BaseModel):
    doc_id: str

    agreement_type: Fact[Literal["rent", "leave_and_license"]]
    monthly_rent: Fact[int]
    security_deposit: Fact[int]
    total_length: Fact[Duration]
    lock_in: Fact[Duration]
    lock_in_applies_to: Fact[Literal["tenant", "landlord", "both"]]
    tenant_notice: Fact[Duration]
    landlord_notice: Fact[Duration]
    tenant_can_leave_early: Fact[bool]
    landlord_can_end_early: Fact[bool]
    rent_increase: Fact[RentIncrease]
    maintenance: Fact[Maintenance]
    deposit_refund_time: Fact[Duration]
    auto_renewal: Fact[bool]
    late_fee: Fact[int] 