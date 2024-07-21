# DHIS2 Uploader

## Overview
This is a Flask application that allows users to upload data from an Excel sheet into a specific dataset in DHIS2.

## Project Structure

dhis2_uploader/
├── templates/
│   ├── upload.html
│   ├── login.html
├── static/
│   └── (any static files like CSS, JS, images if needed)
├── sample_template.xlsx
├── upload_history.log
├── app.py
└── README.md (optional, for documentation)


## Setup Instructions

1. **Install Python**:
   Make sure you have Python installed on your system.

2. **Install Required Libraries**:
   Open a terminal and run the following command:
   ```sh
   pip install flask flask-login pandas requests openpyxl

Update DHIS2 Configuration:
Edit the app.py file and update the DHIS2 configuration with your instance's URL, username, and password.

Access the Application:
Open your web browser and go to http://127.0.0.1:5000/.


