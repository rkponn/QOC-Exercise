# controllers/customer_controller.py
import logging
from odoo_client import OdooClient
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from utils.customer_helpers import create_customer, update_customer

customer_bp = Blueprint("customer", __name__)
client = OdooClient()

# Set up logging - for this I set as DEBUG to capture all logs. Format is set to include timestamp, log level, and message
logging.basicConfig(
    filename="record.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@customer_bp.route("/", methods=["GET"])
@swag_from("../swagger/all_customers.yml")
def index():
    """
    Fetch all customer data.
    Empty list given since no filter conditions are needed.
    Returns:
        A tuple containing a object and a status code.
    """
    try:
        customers = client.execute(
            "res.partner",
            "search_read",
            [],
            [
                "name",
                "phone",
                "email",
                "street",
                "street2",
                "city",
                "zip",
                "state_id",
                "country_id",
            ],
        )
        logging.info(f"All customers fetched successfully \n")
        return jsonify(customers), 200
    except Exception as e:
        logging.error(f"Error fetching all customers: {e}\n")
        return jsonify({"status": "error", "message": str(e)}), 500


@customer_bp.route("/search", methods=["GET"])
@swag_from("../swagger/search_customer.yml")
def show():
    """
    Fetch customer data by name.

    This function takes a query parameter 'name' from the request
    and uses it to filter the customers by name.
    Returns:
        A tuple containing a object and a status code.
    """
    name_filter = request.args.get("name")
    if not name_filter:
        logging.error(f"Missing 'name' query parameter \n")
        return (
            jsonify({"status": "error", "message": "Missing 'name' query parameter"}),
            400,
        )

    try:
        filter_conditions = [["name", "ilike", name_filter]]
        customers = client.execute(
            "res.partner",
            "search_read",
            filter_conditions,
            [
                "name",
                "phone",
                "email",
                "street",
                "street2",
                "city",
                "zip",
                "state_id",
                "country_id",
            ],
        )
        logging.info(f"Customer with name {name_filter} fetched successfully \n")
        return jsonify(customers), 200
    except Exception as e:
        logging.error(f"Error fetching customer with name {name_filter}: {e}\n")
        return jsonify({"status": "error", "message": str(e)}), 500


@customer_bp.route("/", methods=["POST"])
@swag_from("../swagger/create_customer.yml")
def create():
    """
    Create a new customer .

    This function takes a JSON object from the request, containing the customer's name, phone number, and/or email.
    It then creates a new customer with the provided data.

    Returns:
        A tuple containing a JSON object and a status code.
    """

    # Get the JSON data from the request
    data = request.json
    logging.info(f"Request to create customer received: {data} \n")

    # Validate that either phone or email is provided - both being provided is also valid
    if not data.get("phone") and not data.get("email"):
        logging.error(f"Either phone or email must be provided \n")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Either phone or email must be provided.",
                }
            ),
            400,
        )

    try:
        # Handles only if phone or email or both are provided
        filter_conditions = []
        if data.get("email"):
            filter_conditions.append(("email", "=", data["email"]))
        if data.get("phone"):
            filter_conditions.append(("phone", "=", data["phone"]))

        # If both phone and email are provided
        if len(filter_conditions) == 2:
            filter_conditions = ["|"] + filter_conditions

        if filter_conditions:
            existing_customer = client.execute(
                "res.partner", "search", filter_conditions
            )
            if existing_customer:
                logging.error(
                    f"A customer with this email or phone number already exists \n"
                )
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "A customer with this email or phone number already exists",
                        }
                    ),
                    400,
                )

        customer_id = create_customer(data)
        logging.info(f"Customer with name {data['name']} created successfully \n")
        return (
            jsonify({"status": "successfully created", "customer_id": customer_id}),
            200,
        )

    except Exception as e:
        logging.error(f"Error creating customer with name {data['name']}: {e}\n")
        # If an error occurred, return the error message in JSON format with a 500 Internal Server Error status code
        return jsonify({"status": "error", "message": str(e)}), 500


@customer_bp.route("/", methods=["PATCH"])
@swag_from("../swagger/update_customer.yml")
def update():
    """
    Update an existing customer.

    This function takes a JSON object from the request, containing the customer's ID and the data to update.
    It then updates the customer with the provided data.

    Only update the fields that you want to change. For example, to update the phone number of a customer,
    you can send a JSON object with the customer's ID and the new phone number. Remove the fields that you don't want to change.

    Returns:
        A tuple containing a JSON object and a status code.
    """

    # Get the JSON data from the request
    data = request.json
    logging.info(f"Request to update customer received: {data} \n")

    # Validate the input
    if not data or "id" not in data or "values" not in data:
        logging.error(f"Invalid input for updating customer \n")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": 'Invalid input. The request must include a JSON object with "id" and "values" keys.',
                }
            ),
            400,
        )

    try:
        # Check if the customer exists
        customer_exists = client.execute(
            "res.partner", "search", [("id", "=", data["id"])]
        )
        if not customer_exists:
            logging.error(f"Customer with ID {data['id']} not found \n")
            return jsonify({"status": "error", "message": "Customer not found."}), 404

        # Call the helper function to handle the update
        update_customer(data["id"], data["values"])

        # Return a success message in JSON format with a 200 OK status code
        logging.info(f"Customer with ID {data['id']} updated successfully \n")
        return jsonify({"status": "successfully updated"}), 200

    except ValueError as ve:
        logging.error(f"Validation error: {ve}\n")
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        logging.error(f"Error updating customer with ID {data['id']}: {e}\n")
        return jsonify({"status": "error", "message": str(e)}), 500


@customer_bp.route("/bulk_create", methods=["POST"])
@swag_from("../swagger/bulk_create_customers.yml")
def bulk_create_customers():
    """
    Bulk create new customers.

    This function takes a JSON array from the request, where each object contains a customer's details.
    It then creates each customer with the provided data.
    list of dictionaries containing customer data.

    Returns:
        A tuple containing a JSON object and a status code.
    """

    # Get the JSON data from the request
    data = request.json
    logging.info(f"Request to bulk create customers received: {data} \n")

    # Validate the input - check that the data is a list of customer data
    if not isinstance(data, list):
        logging.error(f"Input must be a list of customer data \n")
        return (
            jsonify(
                {"status": "error", "message": "Input must be a list of customer data."}
            ),
            400,
        )

    for customer in data:
        if not customer.get("name") or (
            not customer.get("phone") and not customer.get("email")
        ):
            logging.error(
                f"Each customer must include 'name' and either 'phone' or 'email' \n"
            )
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Each customer must include 'name' and either 'phone' or 'email'.",
                    }
                ),
                400,
            )

    try:
        created_customers = []

        for customer in data:
            customer_id = create_customer(customer)
            created_customers.append(customer_id)

        # Return the IDs of the newly created customers in JSON format with a 200 OK status code
        logging.info(f"Bulk created customers successfully: {created_customers} \n")
        return (
            jsonify(
                {"status": "successfully created", "customer_ids": created_customers}
            ),
            200,
        )

    except Exception as e:
        logging.error(f"Error bulk creating customers: {e}\n")
        # If an error occurred, return the error message in JSON format with a 500 Internal Server Error status code
        return jsonify({"status": "error", "message": str(e)}), 500
