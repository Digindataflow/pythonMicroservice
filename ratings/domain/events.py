# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from datetime import date
from typing import Optional

class Event:
    pass

@dataclass
class RatingAdded(Event):
    account_id: int
    rating: int
    book_isbn: str
    comment: str