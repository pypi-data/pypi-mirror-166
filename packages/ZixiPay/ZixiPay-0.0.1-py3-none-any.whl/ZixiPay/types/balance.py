from dataclasses import dataclass


@dataclass(frozen=True)
class Balance:
    name: str  # Currency name
    code: str  # Currency symbol
    balance: float  # Available balance
