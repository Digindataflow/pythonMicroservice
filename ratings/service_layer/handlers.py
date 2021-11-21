from ratings.domain import commands, events, model
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from . import unit_of_work

class DuplicateRating(Exception):
    pass


def add_rating(
    cmd: commands.AddRating,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        personal_rating = uow.personal_ratings.get(account_id=cmd.account_id)
        if personal_rating is None:
            personal_rating = model.PersonalRating(cmd.account_id, [])
        new_rating = model.Rating(cmd.account_id, cmd.rating, cmd.book_isbn, cmd.comment)
        if not personal_rating.can_add_rating(new_rating):
            raise DuplicateRating

        personal_rating.add_rating(new_rating)
        uow.personal_ratings.add(personal_rating)
        uow.commit()

def publish_rating_added_event(
    event: events.RatingAdded,
    publish: Callable,
):
    publish("book_rating_added", event)

EVENT_HANDLERS = {
    # events.Allocated: [publish_allocated_event, add_allocation_to_read_model],
    # events.Deallocated: [remove_allocation_from_read_model, reallocate],
    events.RatingAdded: [publish_rating_added_event],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddRating: add_rating,
    # commands.CreateBatch: add_batch,
    # commands.ChangeBatchQuantity: change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]