import requests
from bs4 import BeautifulSoup
import json
import logging
import re


def get_current_database_name(url):
    try:
        # Step 1: Get the demo page
        response = requests.get(url)
        response.raise_for_status()

        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Step 3: Look for the script tag containing session info
        script_tag = soup.find(
            "script", string=lambda string: string and "odoo.__session_info__" in string
        )

        # turn script_tag into a string that lives in a list
        script_lines = str(script_tag).split("\n")
        # Find the line that contains the JSON data
        json_line = next(
            line for line in script_lines if "odoo.__session_info__ =" in line
        )

        # Extract the JSON string from the line
        json_str = json_line.split("odoo.__session_info__ =")[1].split(";")[0].strip()

        # Parse the JSON string into a Python dictionary
        session_info = json.loads(json_str)

        # Return the database name
        return session_info["db"]

    except Exception as e:
        logging.error(f"Failed to get current database name: {e}")
        return None


def update_env_file(db_name):
    # Read in the file
    with open(".env", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = re.sub(
        r"^ODOO_DB=demo_saas-.*$", f"ODOO_DB={db_name}", filedata, flags=re.MULTILINE
    )

    # Write the file out again
    with open(".env", "w") as file:
        file.write(filedata)


# uncomment the line below to run this alone
# update_env_file(get_current_database_name("https://demo.odoo.com"))
