from typing import Literal, Generic, TypeVar
from pydantic import BaseModel, model_validator

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
    monthly_rent: int
    security_deposit: int
    agreement_type: Literal["rent","leave_and_license"]