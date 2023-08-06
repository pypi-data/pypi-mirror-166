from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Invoice:
    invoice_id: str
    amount: float
    currency: str
    ref: str
    accept_multi: bool
    validity: int
    date: Optional[datetime] = None
    status: Optional[str] = None
    url: Optional[str] = None
    qr_url: Optional[str] = None
