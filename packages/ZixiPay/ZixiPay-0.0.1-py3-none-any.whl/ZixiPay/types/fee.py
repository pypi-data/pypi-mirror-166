from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Fee:
    name: str
    symbol: str
    min_amount: float
    max_amount: float
    fee: float


@dataclass(frozen=True)
class FeeGroup:
    eurz: Fee
    ltc: Fee
    btc: Fee
    eth: Fee
    usdt: Fee
    usdz: Optional[Fee] = None


@dataclass(frozen=True)
class Fees:
    deposit: FeeGroup
    withdrawal: FeeGroup
    internal_transfer: FeeGroup
    exchange: FeeGroup
