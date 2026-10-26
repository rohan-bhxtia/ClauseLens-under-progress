from pydantic import BaseModel

class Block_format(BaseModel):
    label: str
    text: str
    page: int


class Clause_format(BaseModel):
    number: int| None
    title: str
    text: str
    page: int    