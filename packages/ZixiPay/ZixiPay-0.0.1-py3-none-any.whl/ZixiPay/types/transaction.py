from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Transaction:
    txid: str
    status: str
    amount: float
    fee: float
    currency: str
    sender: Optional[str] = None
    recipient: Optional[str] = None
    details: Optional[str] = None
    extras: Optional[str] = None
    merchant_ref: Optional[str] = None
    time: Optional[datetime] = None
    type: Optional[str] = None
    total: Optional[str] = None
    passcode: Optional[int] = None
