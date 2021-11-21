import abc

from ratings import config
from ratings.adapters import repository


class AbstractUnitOfWork(abc.ABC):
    personal_ratings: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for rating in self.personal_ratings.seen:
            while rating.events:
                yield rating.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class MemoryUnitOfWork(AbstractUnitOfWork):

    def __enter__(self):
        self.personal_ratings = repository.MemoryRepository()
        return super().__enter__()

    def _commit(self):
        pass

    def rollback(self):
        pass
