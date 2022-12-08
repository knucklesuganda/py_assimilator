from abc import ABC


class EventModel(ABC):
    acknowledged_field = "acknowledged"

    def __init__(self, model):
        raise NotImplementedError("implement init in your EventModel")
