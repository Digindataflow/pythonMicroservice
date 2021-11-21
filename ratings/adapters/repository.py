import abc
from typing import Set, List
# from books.adapters import orm
from ratings.domain import model
import datetime

RATINGS = {
    1: model.Rating(**{'account_id': 1, 'rating': 3, 'book_isbn': '1', "comment": "good"}),
    2: model.Rating(**{'account_id': 3, 'rating': 2, 'book_isbn': '2', "comment": "good 1"}),
    3: model.Rating(**{'account_id': 2, 'rating': 5, 'book_isbn': '2', "comment": "good 1"}),
    4: model.Rating(**{'account_id': 1, 'rating': 2, 'book_isbn': '3', 'comment': ""})
}


PERSONALRATINGS = {
    1: model.PersonalRating(1, [RATINGS[1], RATINGS[4]]),
    2: model.PersonalRating(2, [RATINGS[3]]),
    3: model.PersonalRating(3, [RATINGS[2]])
}

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Rating]

    def add(self, rating: model.PersonalRating):
        self._add(rating)
        self.seen.add(rating)

    def get(self, account_id: int) -> model.PersonalRating:
        rating = self._get(account_id)
        if rating:
            self.seen.add(rating)
        return rating

    @abc.abstractmethod
    def _add(self, rating: model.PersonalRating):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, isbn) -> model.PersonalRating:
        raise NotImplementedError

class MemoryRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.ratings = PERSONALRATINGS

    def _add(self, rating: model.PersonalRating):
        self.ratings.update({rating.account_id: rating})
        new_id = max(RATINGS.keys()) + 1
        for item in rating.ratings:
            if item not in RATINGS.values():
                RATINGS.update({new_id: item})
                break

    def _get(self, account_id: int) -> model.PersonalRating:
        return self.ratings.get(account_id)

