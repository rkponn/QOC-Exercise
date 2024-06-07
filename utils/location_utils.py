# utils/location_utils.py
from odoo_client import OdooClient

# Initialize the Odoo client
client = OdooClient()


def get_state_id(state_name, country_name=None):
    """
    Get the state ID.

    This function fetches the state ID based on the provided state name.
    If the country name is also provided, it will narrow down the search to that country.

    Args:
        state_name (str): The name of the state to fetch the ID for.
        country_name (str, optional): The name of the country the state belongs to.

    Returns:
        int: The ID of the state.

    Raises:
        ValueError: If the country or state is not found.
    """
    # If country_name is provided, fetch the country ID (This will be more efficient than fetching it for each state)
    country_id = None
    if country_name:
        country = client.execute("res.country", "search", [("name", "=", country_name)])
        if not country:
            raise ValueError(f"Country '{country_name}' not found")
        country_id = country[0]

    # Prepare the search criteria for state
    search_criteria = [("name", "=", state_name)]
    if country_id:
        search_criteria.append(("country_id", "=", country_id))

    # Fetch the state ID based on the state name and optional country ID
    state = client.execute("res.country.state", "search_read", search_criteria, ["id"])

    if not state:
        raise ValueError(
            f"State '{state_name}' not found"
            + (f" in country '{country_name}'" if country_name else "")
        )

    return state[0]["id"]


def get_country_id(country_name):
    """
    Get the country ID.

    This function fetches the country ID based on the provided country name.

    Args:
        country_name (str): The name of the country to fetch the ID for.

    Returns:
        int: The ID of the country.

    Raises:
        ValueError: If the country is not found.
    """
    # Fetch the country ID based on the country name
    country = client.execute(
        "res.country", "search_read", [("name", "=", country_name)], ["id"]
    )
    if not country:
        raise ValueError(f"Country '{country_name}' not found")
    return country[0]["id"]
