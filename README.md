# Welcome to the QOC Application

This README will guide you through setting up and running the QOC application.

## Prerequisites

1. **Python 3.6+** - Ensure you have Python installed.
2. **Virtual Environment** - Use `venv` for virtual environment management.
3. **Flask** - Python web framework.
4. **Odoo** - Odoo client and dependencies.

## Setup Instructions

### 1. Create and Configure Environment Variables

1. Create a `.env` file in the root directory.
2. Copy the contents of `.env.example` into `.env`.

### 2. Create a Virtual Environment

To isolate project dependencies, create a virtual environment:

```bash
python -m venv venv
```
### 3. Activate the virtual environment:
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

# Running the Application

## Web Scraper Note
A web scraper is used to fetch the frequently changing Odoo database name. Sometimes, it may fail, and you may need to try a few times.

### 1. Start the Flask Application
Run the Flask app:
```bash
python app.py
```
This should start the server. If it doesn't, follow the steps below.

### 2. Run the Database Name Scraper
If the server doesn't start, manually run the database name scraper:

1) Open db_name_scraper.py.
2) Uncomment the last line to update the .env file with the correct database name.

3) Run the scraper:
```bash
python db_name_scraper.py
```
4) Comment out the last line again after running the scraper.
5) Try starting the server again
```bash
python app.py
```
# Manual Database Name Update (if needed)
If the above steps fail:

1) Go to Odoo Demo.
2) Navigate to Settings > Activate Developer Mode.
3) Return to the landing page and refresh.
4) Look for the database name in the tan bar at the top right under the profile.
5) Inspect the element to get the full database name.
6) Update the .env file with this database name.
7) Start the server again:
```bash
python app.py
```
# Accessing Swagger API Documentation
Once the server is running, access the Swagger API documentation to create, update, or modify a customer:
```arduino
http://<your-server-address>/apidocs
```
Replace <your-server-address> with the appropriate address (e.g., localhost:5000 if running locally).
