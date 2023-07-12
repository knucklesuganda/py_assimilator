from assimilator.core.services.crud import CRUDService
from assimilator.core.database import UnitOfWork
from assimilator.core.events.events_bus import EventProducer

from examples.fastapi_event_microservices.common.events import UserCreated


class UsersCRUD(CRUDService):
    """ We create our custom CRUD class that will send out events """

    def __init__(self, uow: UnitOfWork, event_producer: EventProducer):
        super(UsersCRUD, self).__init__(uow=uow)
        self.event_producer = event_producer

    def create(self, obj_data):
        result = super(UsersCRUD, self).create(obj_data)
        self.event_producer.produce(
            UserCreated(
                user_id=result.id,
                username=result.username,
                email=result.email,
                balance=result.balance,
            )
        )
        return result
