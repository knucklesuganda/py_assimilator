from assimilator.core.database import NotFoundError

from examples.fastapi_event_microservices.common.events import OrderCreated, UserBilled
from examples.fastapi_event_microservices.users_service.dependencies import \
    get_event_bus, get_users_crud

event_bus = get_event_bus()


@event_bus.consumer.register_callback(OrderCreated)
def change_user_balance(event: OrderCreated, **context):
    crud = get_users_crud()

    try:
        user = crud.get(id=event.user_id)
    except NotFoundError:
        print("User not found!")
        return

    if event.price > user.balance:
        print("Price exceeds the balance!")
    else:
        user.balance -= event.price
        crud.update(user)

    event_bus.producer.produce(UserBilled(
        user_id=user.id,
        order_id=event.order_id,
        success=user.balance >= event.price,
    ))
