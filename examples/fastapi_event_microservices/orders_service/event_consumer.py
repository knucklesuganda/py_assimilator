from examples.fastapi_event_microservices.common.events import UserBilled
from examples.fastapi_event_microservices.orders_service.dependencies import event_bus, get_orders_crud


@event_bus.consumer.register_callback(UserBilled)
def handle_user_billed(event: UserBilled, **context):
    print(event)
    crud = get_orders_crud()
    order = crud.get(id=event.order_id)
    order.status_id = 3 if event.success else 2
    crud.update(order)
    print("Order status changed!")
