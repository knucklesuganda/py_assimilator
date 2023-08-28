from assimilator.rabbit.events.events_bus import RabbitEventConsumer, RabbitEventProducer
from assimilator.core.usability.registry import register_provider, PatternList

register_provider(provider='rabbit', pattern_list=PatternList(
    event_consumer=RabbitEventConsumer,
    event_producer=RabbitEventProducer,
))
