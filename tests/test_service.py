import json
import pytest
from send_display.app import app
from send_display.utils import schema_validation
from jsonschema import validate

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_update_customer_success(client):
    url = '/v1/customers'
    headers = {"Content-Type": "application/json"}
    data = [{
        "salutation": "Male.",
        "last_name": "Doe",
        "first_name": "John",
        "email": "john.doe@example.com",
        "purchases": [
            {
                "product_id": 1234,
                "price": 10.00,
                "currency": "dollars",
                "quantity": 1,
                "purchased_at": "2024-01-01"
            },
            {
                "product_id": 5678,
                "price": 20.00,
                "currency": "euros",
                "quantity": 2,
                "purchased_at": "2024-01-15"
            }
        ]
    }]


    validate(instance=data, schema=schema_validation)
    response = client.put(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_update_customer_failure(client):
    url = '/v1/customers'
    headers = {"Content-Type": "application/json"}
    data = [{
        "salutation": "Female",
        "last_name": "Doe",
        "first_name": "John",
        "email": "invalid.email@example.com",
        "purchases": [
            {
                "product_id": 1234,
                "price": 10.00,
                "currency": "dollars",
                "quantity": 1,
                "purchased_at": "2024-01-01"
            },
            {
                "product_id": 5678,
                "price": 20.00,
                "currency": "dollars",
                "quantity": 2,
                "purchased_at": "2024-01-15"
            }
        ]
    }]

    validate(instance=data, schema=schema_validation)
    response = client.put(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response_json = response.get_json()
 