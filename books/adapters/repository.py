import abc
from typing import Set, List
# from books.adapters import orm
from books.domain import model
import datetime

BOOKS = [
    model.Book(**{'isbn': '1', 'name': 'book1', 'price': 14}),
    model.Book(**{'isbn': '2', 'name': 'book2', 'price': 15.2}),
    model.Book(**{'isbn': '3', 'name': 'book3', 'price': 24.99, 'pub_date': datetime.date(2019, 6, 12)})
]

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Book]

    def add(self, book: model.Book):
        self._add(book)
        self.seen.add(book)

    def get(self, isbn: str) -> model.Book:
        book = self._get(isbn)
        if book:
            self.seen.add(book)
        return book

    def filter_by_isbn(self, isbns: List[str]) -> List[model.Book]:
        books = self._filter_by_isbn(isbns)
        for book in books:
            self.seen.add(book)
        return books

    @abc.abstractmethod
    def _filter_by_isbn(self, isbns: List[str]) -> List[model.Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, book: model.Book):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, isbn) -> model.Book:
        raise NotImplementedError

class MemoryRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.books = BOOKS

    def _add(self, book):
        self.books.append(book)

    def _get(self, isbn):
        for item in self.books:
            if item.isbn == isbn:
                return item

    def _filter_by_isbn(self, isbns: List[str]) -> List[model.Book]:
        res = []
        for item in self.books:
            if item.isbn in isbns:
                res.append(item)
        return res
