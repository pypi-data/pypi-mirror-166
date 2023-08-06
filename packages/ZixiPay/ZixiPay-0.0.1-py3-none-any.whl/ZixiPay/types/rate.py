from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    code: str  # Currency code
    decimal: int  # Number of decimal digits
    rate: float  # Exchange rate


@dataclass(frozen=True)
class Rates:
    usdz: Rate
    eurz: Rate
    ltc: Rate
    btc: Rate
    eth: Rate
    usdt: Rate
    trx: Rate  # Useless yet
