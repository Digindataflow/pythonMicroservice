from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set
from . import commands, events

class Book:
    def __init__(self, isbn: str, name: str, price: float, pub_date: Optional[date], version_number: int = 0):
        self.isbn = isbn
        self.name = name
        self.price = price
        self.pub_date = pub_date
        self.version_number = version_number
        self.events = [] # type: List[events.Event]

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return other.isbn == self.isbn

    def __hash__(self):
        return hash(self.isbn)

    def create(self):
        self.version_number += 1
        self.events.append(
            events.BookAdded(
                isbn=self.isbn,
                name=self.name,
                price=self.price,
                pub_date=self.pub_date,
            )
        )
