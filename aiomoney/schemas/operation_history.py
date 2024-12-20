from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Operation(BaseModel):
    """
    Описание платежной операции
    https://yoomoney.ru/docs/wallet/user-account/operation-history#response-operation
    """
    operation_id: str
    status: str
    execution_datetime: datetime = Field(alias="datetime")
    title: str
    pattern_id: str | None = None
    direction: Literal["in", "out"]
    amount: float
    label: str | None = None
    operation_type: str = Field(alias="type")
