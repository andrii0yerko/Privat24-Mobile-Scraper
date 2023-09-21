from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Record:
    uid: str
    date: datetime
    amount: float
    currency: str
    description: str
    category: str
