from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    pass


@dataclass
class AddBook(Command):
    isbn: str
    name: str
    price: float
    pub_date: Optional[date] = None