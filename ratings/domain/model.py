from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set
from . import commands, events

class Rating:
    def __init__(self, account_id: int, rating: int, book_isbn: str, comment: str):
        self.account_id = account_id
        self.rating = rating
        self.book_isbn = book_isbn
        self.comment = comment

class PersonalRating:
    def __init__(self, account_id: int, ratings: List[Rating], version_number: int = 0):
        self.account_id = account_id
        self.ratings = ratings
        self.version_number = version_number
        self.events = [] # type: List[events.Event]

    def can_add_rating(self, rating: Rating):
        for item in self.ratings:
            if item.book_isbn == rating.book_isbn and item.account_id == rating.account_id:
                return False
        return True


    def add_rating(self, rating: Rating):
        self.ratings.append(rating)
        self.version_number += 1
        self.events.append(
            events.RatingAdded(
                account_id=rating.account_id,
                rating=rating.rating,
                book_isbn=rating.book_isbn,
                comment=rating.comment,
            )
        )
