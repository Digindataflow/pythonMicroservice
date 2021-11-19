from books.domain import commands, events, model
from . import unit_of_work

class InvalidIsbn(Exception):
    pass


def add_book(
    cmd: commands.AddBook,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        book = uow.book_collection.get(isbn=cmd.isbn)
        if book is not None:
            raise InvalidIsbn(f"Invalid ISBN {cmd.isbn}")
        book = model.Book(cmd.isbn, cmd.name, cmd.price, cmd.pub_date)
        book.create()
        uow.book_collection.add(book)
        uow.commit()
