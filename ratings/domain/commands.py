from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    pass


@dataclass
class AddRating(Command):
    account_id: int
    rating: int
    book_isbn: str
    comment: str