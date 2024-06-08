import os
import ssl
import certifi
import xmlrpc.client

from dotenv import load_dotenv

load_dotenv()

url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")


class OdooClient:
    def __init__(self):
        """
        Initializes the OdooClient with necessary configurations.
        Sets up an SSL context that ignores certificate verification errors (not recommended for production).
        Authenticates the user and sets up a common server proxy.
        """
        # Create an SSL context that ignores certificate verification errors - DO NOT USE IN PRODUCTION, keep it simple for this demo
        self.context = ssl._create_unverified_context()

        # Create a common server proxy
        self.common = xmlrpc.client.ServerProxy(
            f"{url}/xmlrpc/2/common", context=self.context
        )

        # Authenticate the user
        self.uid = self.common.authenticate(db, username, password, {})

    def authenticate(self):
        """
        Authenticate the user and return the user ID.
        Returns:
            int: The user ID if authentication is successful.
        """
        return self.uid

    def execute(self, model, method, *args):
        """
        Execute a method on a model with the given arguments.
        Args:
            model (str): The model name.
            method (str): The method name.
            *args: The method arguments.
        Returns:
            The result of the method call.
        """
        models = xmlrpc.client.ServerProxy(
            f"{url}/xmlrpc/2/object", context=self.context
        )
        return models.execute_kw(db, self.uid, password, model, method, args)
