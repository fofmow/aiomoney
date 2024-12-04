from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InvoiceSource:
    BANK_CARD = "AC"
    YOOMONEY_WALLET = "PC"


@dataclass(frozen=True, slots=True)
class InvoiceForm:
    url: str
    label: str | None = None
