# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from datetime import date
from typing import Optional

class Event:
    pass

@dataclass
class BookAdded(Event):
    isbn: str
    name: str
    price: float
    pub_date: Optional[date] = None