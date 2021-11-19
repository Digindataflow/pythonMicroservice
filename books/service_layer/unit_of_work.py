import abc

from books import config
from books.adapters import repository


class AbstractUnitOfWork(abc.ABC):
    book_collection: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for book in self.book_collection.seen:
            while book.events:
                yield book.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class MemoryUnitOfWork(AbstractUnitOfWork):

    def __enter__(self):
        self.book_collection = repository.MemoryRepository()
        return super().__enter__()

    def _commit(self):
        pass

    def rollback(self):
        pass
