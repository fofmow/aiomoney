from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OperationDetails(BaseModel):
    """
    Детальная информация об операции из истории
    https://yoomoney.ru/docs/wallet/user-account/operation-details
    """
    error: str | None = None
    operation_id: str | None = None
    status: str | None = None
    pattern_id: str | None = None
    direction: Literal["in", "out"] | None = None
    amount: float | None = None
    amount_due: float | None = None
    fee: float | None = None
    operation_datetime: datetime | None = Field(None, alias="datetime")
    title: str | None = None
    sender: int | None = None
    recipient: str | None = None
    recipient_type: str | None = None
    message: str | None = None
    comment: str | None = None
    label: str | None = None
    details: str | None = None
    operation_type: str | None = Field(None, alias="type")
