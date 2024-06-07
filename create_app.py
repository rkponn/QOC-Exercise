from flask import Flask
from flasgger import Swagger
from odoo_client import OdooClient
from db_name_scraper import get_current_database_name, update_env_file
from controllers.state_controller import state_bp
from controllers.customer_controller import customer_bp


def create_app():
    app = Flask(__name__)
    Swagger(app)

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(state_bp, url_prefix="/states")

    # Initialize OdooClient and update env file with the current database name
    current_odoo_db = get_current_database_name("https://demo.odoo.com")
    update_env_file(current_odoo_db)
    print("OdooClient initialized")
    OdooClient()

    return app
