# utils/customer_helpers.py
from odoo_client import OdooClient
from utils.location_utils import get_state_id, get_country_id

client = OdooClient()


def get_id(values, key, get_id_func):
    """
    Helper function to get the ID of a record by name.
    Takes the name state or country and returns the id of the state or country and adds it to the values dictionary.
    Example:
        state -> state_id: 1
        country -> country_id: 1
    """
    if key in values:
        name = values.pop(key)
        try:
            id = get_id_func(name)
            values[f"{key}_id"] = id
        except Exception as e:
            raise ValueError(f"Invalid {key} '{name}': {e}")


def create_customer(data):
    """
    Helper function to create a customer.
    Args:
        data (dict): Dictionary containing customer details.
            Expected keys: 'name', 'phone', 'email', 'street', 'city', 'state', 'country', 'zip'.
    Returns:
        int: ID of the newly created customer.
    """
    # get the id of the state and country from the string given if nothing is given then it will return None (ternary)
    state_id = (
        get_state_id(data.get("state", ""), data.get("country", ""))
        if data.get("state") and data.get("country")
        else None
    )
    country_id = (
        get_country_id(data.get("country", "")) if data.get("country") else None
    )

    customer_data = {
        "name": data["name"],
        "phone": data.get("phone", ""),
        "email": data.get("email", ""),
        "street": data.get("street", ""),
        "city": data.get("city", ""),
        "state_id": state_id or "",
        "country_id": country_id or "",
        "zip": data.get("zip", ""),
    }

    customer_data = {k: v for k, v in customer_data.items() if v}
    customer_id = client.execute("res.partner", "create", customer_data)
    return customer_id


def update_customer(customer_id, values):
    """
    Helper function to update a customer.
    Args:
        customer_id (int): ID of the customer to be updated.
        values (dict): Dictionary containing fields to be updated.
            Expected keys may include 'phone', 'email', 'street', 'city', 'state', 'country', 'zip'.
    """
    # using a lambda function to get the id of the state and country since the get_id function requires a function as an argument
    get_id(values, "state", lambda state_name: get_state_id(state_name))
    get_id(values, "country", get_country_id)

    client.execute("res.partner", "write", [customer_id], values)
