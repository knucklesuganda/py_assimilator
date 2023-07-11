from assimilator.kafka_.events.events_bus import KafkaEventProducer, KafkaEventConsumer
from assimilator.core.usability.registry import register_provider, PatternList

pattern_list = PatternList(
    event_consumer=KafkaEventConsumer,
    event_producer=KafkaEventProducer,
)

register_provider(provider='kafka', pattern_list=pattern_list)
register_provider(provider='kafka_', pattern_list=pattern_list)
