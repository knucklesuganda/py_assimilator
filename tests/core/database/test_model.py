import pytest

from assimilator.core.database import BaseModel
from assimilator.core.exceptions import ParsingError


class Product(BaseModel):
    title: str
    balance: float
    quantity: float


def test_product_instance():
    product = Product(title="Product A", balance=10.0, quantity=5.0)
    assert isinstance(product, Product)
    assert isinstance(product, BaseModel)


def test_product_attributes():
    product = Product(title="Product A", balance=10.0, quantity=5.0)
    assert product.title == "Product A"
    assert product.balance == 10.0
    assert product.quantity == 5.0


def test_product_generate_id():
    product = Product(title="Product A", balance=10.0, quantity=5.0)
    assert isinstance(product.id, str)
    assert len(product.id) == 36  # UUID format


def test_product_autogenerate_id():
    class CustomProduct(Product):
        pass

    product = CustomProduct(title="Product A", balance=10.0, quantity=5.0)
    assert isinstance(product.id, str)
    assert len(product.id) == 36  # UUID format


def test_product_custom_id():
    class CustomProduct(Product):
        id: str

    product = CustomProduct(id="custom_id", title="Product A", balance=10.0, quantity=5.0)
    assert product.id == "custom_id"


def test_product_loads():
    data = '{"id": "12345", "title": "Product A", "balance": 10.0, "quantity": 5.0}'
    product = Product.loads(data)
    assert product.id == "12345"
    assert product.title == "Product A"
    assert product.balance == 10.0
    assert product.quantity == 5.0


def test_product_loads_invalid_data():
    data = '{"id": 12345", "title": "Product A", "balance": "10.0", "quantity": 5.0}'
    with pytest.raises(ParsingError):
        Product.loads(data)


def test_product_json():
    product = Product(id="12345", title="Product A", balance=10.0, quantity=5.0)
    expected_json = '{"id": "12345", "title": "Product A", "balance": 10.0, "quantity": 5.0}'
    assert product.json() == expected_json


def test_product_dict():
    product = Product(id="12345", title="Product A", balance=10.0, quantity=5.0)
    expected_dict = {"id": "12345", "title": "Product A", "balance": 10.0, "quantity": 5.0}
    assert product.dict() == expected_dict
