from flask import Blueprint, request, jsonify
from flasgger import swag_from
from odoo_client import OdooClient

state_bp = Blueprint("state", __name__)
client = OdooClient()


@state_bp.route("/", methods=["GET"])
@swag_from("../swagger/states.yml")
def index():
    """
    Get states.

    This function fetches states based on the provided query parameters.
    If no parameters are provided, it fetches all states.

    Returns:
        A tuple containing a JSON object and a status code.
    """
    try:
        # Get query parameters
        state_name = request.args.get("name")
        state_id = request.args.get("id")
        filter_conditions = []

        # If state name is provided, add to the search filter_conditions
        if state_name:
            filter_conditions.append(("name", "ilike", state_name))

        # If state id is provided, add to the search filter_conditions
        if state_id:
            filter_conditions.append(("id", "=", int(state_id)))

        # Fetch states
        states = client.execute(
            "res.country.state",
            "search_read",
            filter_conditions,
            ["id", "name", "country_id"],
        )

        # Return the states in JSON format with a 200 OK status code
        return jsonify(states), 200

    except Exception as e:
        # If an error occurred, return the error message in JSON format with a 500 Internal Server Error status code
        return jsonify({"status": "error", "message": str(e)}), 500
