# api examples

import requests

# Replace with the actual IMS API endpoint and your credentials
url = 'https://ims.example.com/api/data'
headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}

# Make a GET request to the IMS API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON data
    data = response.json()
    print(data)
else:
    print(f'Error: {response.status_code}')

# To get started, you'll need to use the appropriate APIs provided by IMS. IMS offers several APIs for accessing its database and transaction management features1. Here are a few steps to help you get started:

# Identify the API: Determine which API you need to use based on your requirements. IMS provides APIs for database access, transaction management, and more.

# Set Up Your Environment: Ensure you have the necessary tools and libraries installed. For example, you might need a library like requests for making HTTP requests in Python.

# Authenticate: Make sure you have the necessary credentials and permissions to access the IMS API.

# Make API Calls: Use the API to pull data from IMS. Here's a basic example using Python and the requests library:

#example pushing into IMS
import requests
import json

# Replace with the actual IMS API endpoint and your credentials
url = 'https://ims.example.com/api/data'
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

# Data to be pushed to the IMS
data = {
    'field1': 'value1',
    'field2': 'value2',
    # Add more fields as needed
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Make a POST request to the IMS API to create a new record
response = requests.post(url, headers=headers, data=json_data)

# Check if the request was successful
if response.status_code == 201:
    print('Data pushed successfully!')
else:
    print(f'Error: {response.status_code} - {response.text}')



# Hybrid Approach
# In some cases, a hybrid approach can be beneficial. You can use Python for certain tasks and have a backend to handle others. For example, you could use Flask or Django to build a lightweight backend that handles API calls, user authentication, and data management, while still leveraging Python for data analysis and processing.

# Here’s a simple example of how you might set up a backend using Flask:
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # Example IMS API call
    url = 'https://ims.example.com/api/data'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

@app.route('/push-data', methods=['POST'])
def push_data():
    data = request.json
    url = 'https://ims.example.com/api/data'
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return jsonify({'message': 'Data pushed successfully!'})
    else:
        return jsonify({'error': 'Failed to push data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)


# # create persistent api for run counter
# Step 1: Create the Flask API
# First, you'll set up a Flask application to handle GET and POST requests for the run count.
app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///run_count.db'
db = SQLAlchemy(app)

class RunCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

db.create_all()

@app.route('/get-count', methods=['GET'])
def get_count():
    run_count = RunCount.query.get(1)
    if not run_count:
        run_count = RunCount(id=1, count=0)
        db.session.add(run_count)
        db.session.commit()
    
    return jsonify({'count': run_count.count})

@app.route('/increment-count', methods=['POST'])
def increment_count():
    run_count = RunCount.query.get(1)
    if not run_count:
        run_count = RunCount(id=1, count=0)
        db.session.add(run_count)
    
    run_count.count += 1
    db.session.commit()
    
    return jsonify({'count': run_count.count})

if __name__ == '__main__':
    app.run(debug=True)

# run python app.py to start the server

# Step 3: Interacting with the API from a Python Script
# You can now create a Python script to interact with this API. Here's an example of how to fetch and increment the run count:

import requests

# Define the API endpoints
get_count_url = 'http://127.0.0.1:5000/get-count'
increment_count_url = 'http://127.0.0.1:5000/increment-count'

# Fetch the current run count
response = requests.get(get_count_url)
if response.status_code == 200:
    count = response.json().get('count', 0)
    print(f'Current run count: {count}')
else:
    print(f'Error fetching count: {response.status_code}')

# Increment the run count
response = requests.post(increment_count_url)
if response.status_code == 200:
    new_count = response.json().get('count', 0)
    print(f'New run count: {new_count}')
else:
    print(f'Error incrementing count: {response.status_code}')
