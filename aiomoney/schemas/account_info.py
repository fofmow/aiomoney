from pydantic import BaseModel, Field


class BalanceDetails(BaseModel):
    total: float
    available: float
    deposition_pending: float | None = None
    blocked: float | None = None
    debt: float | None = None
    hold: float | None = None


class LinkedCard(BaseModel):
    pan_fragment: str
    card_type: str = Field(None, alias="type")


class AccountInfo(BaseModel):
    """
    Получение информации о состоянии счета пользователя
    https://yoomoney.ru/docs/wallet/user-account/account-info
    """
    account: str  # номер счета
    balance: float  # баланс счета
    currency: str  # код валюты счета
    account_status: str
    account_type: str
    identified: bool
    balance_details: BalanceDetails | None
    cards_linked: list[LinkedCard] | None = None
