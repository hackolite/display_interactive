dtype_dict_customer = {
    'customer_id': int,
    'title': int,
    'lastname': str,
    'firstname': str,
    'postal_code': str,
    'city': str,
    'email': str
}




schema_validation = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "salutation": {"type": "string"},
      "last_name": {"type": "string"},
      "first_name": {"type": "string"},
      "email": {"type": "string"},
      "purchases": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "product_id": {"type": "integer"},
            "price": {"type": "number"},
            "currency": {"type": "string"},
            "quantity": {"type": "integer"},
            "purchased_at": {"type": "string", "format": "date"}
          },
          "required": ["product_id", "price", "currency", "quantity", "purchased_at"]
        }
      }
    },
    "required": ["last_name", "first_name", "purchases"]
  }
}
