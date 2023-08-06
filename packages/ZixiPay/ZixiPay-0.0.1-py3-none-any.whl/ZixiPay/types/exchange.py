from dataclasses import dataclass


@dataclass(frozen=True)
class Exchange:
    from_amount: float
    from_currency: str
    from_txid: str
    to_amount: float
    to_currency: str
    to_txid: str
    rate: float
    fee: float
