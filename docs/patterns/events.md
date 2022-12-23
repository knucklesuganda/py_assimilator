# Events patterns

## Events and how they work
Event shows changes in your system and listeners(consumers) respond to them. Events contain all the possible things that
other parts of the system may need once they respond to them. That is useful in lots of systems, and this page will describe
the basics of assimilator events. Events use [Pydantic](https://docs.pydantic.dev/) module to ease the process of creation, integration
and parsing.


## Event based systems with Assimilator

1. `Event` - representation of a change in your system that carries all the useful data
2. `EventProducer` - something that produces events(executes the changes in the system and shows it with events)
3. `EventConsumer` - something that waits for the producer to emit various events for it to consume them and execute various operations based on the other changes
4. `EventBus` - combines both producers and consumers in one Entity that can produce and consume simultaneously


## Event example with user registration:
1. User sends his registration data to our website
2. We create a new user in the database and emit an `UserCreated` event using an `EventProducer`
3. `EventConsumers` listen to our `UserCreated` event and executes all the operations that must be done once the user is registered


## Event
###### `id: int`
Unique identification for the event.
###### `event_name: str`
Name of the event. We can have different events in our system. For example, if we
have an event for User creation and an event for User deletion, then we can name them:

- User creation: event_name = user_created
- User deletion: event_name = user_deleted

Those names can help us sort and only listen to specific kind of events. All the names
must be in the past, since an event is the change in the past.
###### `event_date: datetime`
Date of the event. You don't need to change this field since it is assigned by default when an event
is created.

###### `from_json()`
`from_json()` is a function that is used to convert json data to an event.
That method is in the `JSONParsedMixin` class, and it allows us to quickly convert json
to a Python object.

- `cls: Type['BaseModel']` - Any [Pydantic](https://docs.pydantic.dev/) class, but typically an `Event`
- `data: str` - json data for our event

## Create a custom event

`events.py`: 
```python
from assimilator.core.events import Event

class UserCreated(Event):
    user_id: int
    username: str
    email: str  # all the data that could be useful is in the event.
    # Since Event is a Pydantic model, we can just create new fields like this

```

`logic.py`:
```python
from assimilator.core.database import UnitOfWork

from events import UserCreated
from models import User


def create_user(username: str, email: str, uow: UnitOfWork):
    with uow:
        user = User(username=username, email=email)
        uow.repository.save(user)
        uow.commit()
    
        # Refresh the object and get the user id from the database
        uow.repository.refresh(user)

        event = UserCreated(    # we create an event
            user_id=user.id,
            username=user.username,
            email=user.email,
        )
```

In that example, we only create an event without publishing it anywhere. Find out how to emit your events below.

## EventConsumer
`EventConsumer` reads all the incoming events and yields them to the functions that use it.

###### `start()`
Starts the event consumer by connecting to all the required systems

###### `close()`
Closes the consumer and finishes the work

###### `consume()`
Yields incoming events

> `EventConsumer` uses `StartCloseContextMixin` class that allows us to use context managers(with)
> without calling `start()` or `close()` ourselves

Here is an example of how you would create and use your `EventConsumer`:

`events_bus.py`:
```python
from assimilator.core.events import EventConsumer, ExternalEvent


class MyEventConsumer(EventConsumer):
    def __init__(self, api):
        # some object that connects to an external system
        self.api = api

    def start(self) -> None:
        self.api.connect()

    def close(self) -> None:
        self.api.disconnect()
    
    def consume(self):
        while True:
            message = self.api.listen()     # we receive a message from the API
            yield ExternalEvent(**message.convert_to_json())    # parse it
```

`logic.py`:

```python
from events_bus import MyEventConsumer


def consume_events(consumer: MyEventConsumer):
    with consumer:
        for event in events_bus.consume():
            if event.event_name == "user_created":
                user_created_handler(UserCreated(**event.data))
            elif event.event_name == "user_deleted":
                user_deleted_handler(UserDeleted(**event.data))
```

We create a new `EventConsumer` called `MyEventConsumer`. Then, we use an `api` object
to implement all the functions. After that, we use it in `logic.py` file where we consume
all the events and handle them depending on the `event_name`.

As you have already noticed, we use something called an `ExternalEvent`. We do that
because all the events that are coming from external sources are unidentified and can only
use specific later. `ExternalEvent` contains all the event data in the `data: dict` field which
can be used later.

## ExternalEvent
When we listen to external systems, it is sometimes hard to make an event class
that represents a specific class. That is why we use an `ExternalEvent`. It contains all the data
in the `data: dict` field, which can be accessed later in order to use an event class that represents
that specific event.

- `data: dict` - all the data for the event

## AckEvent
`AckEvent` is an event that has acknowledgement in it. If you want to show that your event
was processed(acknowledged), then use `AckEvent`.

- `ack: bool` - whether an event was processed. `False` by default

## EventProducer
`EventProducer` is the class that produces all the events and sends them.

###### `start()`
Starts the event producer by connecting to all the required systems.

###### `close()`
Closes the producer and finishes the work.

###### `produce()`
Sends an event to an external system for it to be consumed.

- `event: Event` - the event that must be sent.

> `EventProducer` uses `StartCloseContextMixin` class that allows us to use context managers(with)
> without calling `start()` or `close()` ourselves

Here is an example of how you would create and use your `EventProducer`:

`events_bus.py`:
```python
from assimilator.core.events import EventProducer


class MyEventProducer(EventProducer):
    def __init__(self, api):
        # some object that connects to an external system
        self.api = api

    def start(self) -> None:
        self.api.connect()

    def close(self) -> None:
        self.api.disconnect()
    
    def produce(self, event: Event) -> None:
        self.api.send_event(event.json())   # parse event to json and send it

```

`logic.py`:

```python
from events_bus import MyEventProducer
from events import UserCreated
from models import User


def create_user(
    username: str,
    email: str,
    uow: UnitOfWork,
    producer: MyEventProducer,
):
    with uow:
        user = User(username=username, email=email)
        uow.repository.save(user)
        uow.commit()

        # Refresh the object and get the user id from the database
        uow.repository.refresh(user)

        with producer:
            producer.produce(
                UserCreated(  # we create an event
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                )
            )     # send an event to an external system

```

> `ExternalEvent` must not be used in the producer, since when we emit the events we are the ones
> creating them, so we have a separate class for them with all the data inside.


## EventBus
`EventBus` combines both `EventProducer` and `EventConsumer` together. You can use those
classes separately, but sometimes you need one object that combines them.

###### `__init__()`

- `consumer: EventConsumer` - the consumer that we want to use 
- `producer: EventProducer` - the producer that we want to use


###### `produce()`
produces the event using `producer`

- `event: Event` - an event that has to be emitted

###### `consume()`
consumes the events using `consumer`. Returns an `Iterator[Event]`


## Event fails and transaction management
Sometimes we want to be sure that our events are emitted. But, if we use normal
event producers and Unit Of Work separately, we may run into a problem:

1) User is created(added in the database and unit of work committed it)
2) Event producer encounters an error(the event is not published)
3) Inconsistency: User exists, but consumers do not know about that

Because of that, we may employ Outbox Relay. It is a pattern that allows us
to save all the events in the database in the same transaction as the main entity. Then,
another program(thread, task, function) gets all the events from the database and ensures that
they are published. We basically save the events to the database in one transaction, emit them in a separate
thing and delete them afterwards.

## OutboxRelay
This class gets all the events using `UnitOfWork` provided, emits all events, and acknowledges them.

###### `__init__()`
- `uow: UnitOfWork` - unit of work that is used in order to get the events, acknowledge them
- `producer: EventProducer` - event producer that we use to publish the events

###### `start()`
Start the relay. This function must run forever, must get the events from the repository from unit of work,
and produce the events. After that, it must call `acknowledge()` to show that these events are produced.

###### acknowledge()
Acknowledges the events in the database. It might change a boolean column for these events,
might delete them, but the idea is that those events will not be produced twice.

- `events: Iterable[Event]` - events that must be acknowledged
