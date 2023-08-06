from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Wallet:
    address: str  # Wallet address
    name: str  # Wallet name
    code: str  # Currency symbol
    confirm: int  # Number of confirmations required
    qr_code: Optional[str] = None  # QR-code of the address


@dataclass(frozen=True)
class USDTWallet:
    erc20: Wallet  # ERC20 (Ethereum) wallet
    trc20: Wallet  # TRC20 (Tron) wallet
    omni: Wallet  # OMNI (Bitcoin) wallet
