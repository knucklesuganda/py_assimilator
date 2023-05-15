import pytest

from assimilator.core.database.models import BaseModel
from assimilator.core.exceptions import ParsingError


def test_base_model_generate_id():
    model = BaseModel()
    assert isinstance(model.id, str)
    assert len(model.id) == 36  # UUID format


def test_base_model_autogenerate_id():
    class MyModel(BaseModel):
        pass

    model = MyModel()
    assert isinstance(model.id, str)
    assert len(model.id) == 36  # UUID format


def test_base_model_custom_id():
    class MyModel(BaseModel):
        id: str

    model = MyModel(id='custom_id')
    assert model.id == 'custom_id'


def test_base_model_loads():
    data = '{"id": "12345"}'
    model = BaseModel.loads(data)
    assert model.id == '12345'


def test_base_model_loads_invalid_data():
    with pytest.raises(ParsingError):
        BaseModel.loads('{"id: 12345}')


def test_base_model_json():
    class MyModel(BaseModel):
        name: str
        age: int

    model = MyModel(id='12345', name='Alice', age=30)
    expected_json = '{"id": "12345", "name": "Alice", "age": 30}'
    assert model.json() == expected_json


def test_base_model_dict():
    class MyModel(BaseModel):
        name: str
        age: int

    model = MyModel(id='12345', name='Alice', age=30)
    expected_dict = {'id': '12345', 'name': 'Alice', 'age': 30}
    assert model.dict() == expected_dict
