from ratings.service_layer import unit_of_work
from typing import List

def ratings(isbns: List[str], uow: unit_of_work.MemoryUnitOfWork):
    with uow:
        # read from transactional db
        if isbns is None:
            results = uow.book_collection.books
        else:
            results = uow.book_collection.filter_by_isbn(isbns)
        # TODO read from replicated read only db
    return [r.as_dict() for r in results]
