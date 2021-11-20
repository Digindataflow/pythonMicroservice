from books.domain import commands, events, model
from typing import List, Dict, Callable, Type, TYPE_CHECKING
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

def publish_book_added_event(
    event: events.BookAdded,
    publish: Callable,
):
    publish("book_added", event)

EVENT_HANDLERS = {
    # events.Allocated: [publish_allocated_event, add_allocation_to_read_model],
    # events.Deallocated: [remove_allocation_from_read_model, reallocate],
    events.BookAdded: [publish_book_added_event],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddBook: add_book,
    # commands.CreateBatch: add_batch,
    # commands.ChangeBatchQuantity: change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]