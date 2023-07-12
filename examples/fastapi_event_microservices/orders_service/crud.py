from assimilator.core.database import UnitOfWork
from assimilator.core.services.crud import CRUDService
from assimilator.core.events.events_bus import EventProducer

from examples.fastapi_event_microservices.common.events import OrderCreated


class OrdersCRUD(CRUDService):
    """ We create our custom CRUD class that will send out events """

    def __init__(self, uow: UnitOfWork, event_producer: EventProducer):
        super(OrdersCRUD, self).__init__(uow=uow)
        self.event_producer = event_producer

    def create(self, obj_data):
        result = super(OrdersCRUD, self).create(obj_data)
        self.event_producer.produce(
            OrderCreated(
                order_id=result.id,
                user_id=result.user_id,
                status=result.order_status.status,
                price=result.price,
            )
        )
        return result
