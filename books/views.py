from books.service_layer import unit_of_work
from typing import List

def books(isbns: List[str], uow: unit_of_work.MemoryUnitOfWork):
    with uow:
        if isbns is None:
            results = uow.book_collection.books
        else:
            results = uow.book_collection.filter_by_isbn(isbns)
    return [r.as_dict() for r in results]
