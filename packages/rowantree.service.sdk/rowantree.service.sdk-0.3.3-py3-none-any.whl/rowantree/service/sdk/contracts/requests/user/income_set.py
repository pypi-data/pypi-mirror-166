from pydantic import BaseModel


class UserIncomeSetRequest(BaseModel):
    income_source_name: str
    amount: int
