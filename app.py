from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# DHIS2 configuration
DHIS2_URL = 'https://your-dhis2-instance/api/'
USERNAME = 'your-username'
PASSWORD = 'your-password'

LOG_FILE = 'upload_history.log'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def upload_form():
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Replace with real validation
            user = User(username)
            login_user(user)
            return redirect(url_for('upload_form'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    dataset = request.form['dataset']
    
    if 'file' not in request.files:
        flash('No file part', 'danger')
        log_upload('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        log_upload('No selected file', 'danger')
        return redirect(request.url)
    
    if file:
        try:
            df = pd.read_excel(file)
            payload = format_data_for_dhis2(df, dataset)
            response = upload_data_to_dhis2(payload)
            flash(response, 'success')
            log_upload(response, 'success')
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            flash(error_message, 'danger')
            log_upload(error_message, 'danger')
    
    return redirect(url_for('upload_form'))

@app.route('/download-template')
def download_template():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_template.xlsx')
    return send_file(file_path, as_attachment=True)

def format_data_for_dhis2(df, dataset):
    data_values = []
    for index, row in df.iterrows():
        data_value = {
            "dataElement": row['dataElement'],
            "period": row['period'],
            "orgUnit": row['orgUnit'],
            "value": row['value']
        }
        data_values.append(data_value)
    
    payload = {
        "dataSet": dataset,
        "dataValues": data_values
    }
    
    return payload

def upload_data_to_dhis2(payload):
    response = requests.post(
        DHIS2_URL + 'dataValueSets',
        json=payload,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    if response.status_code == 200:
        return "Data uploaded successfully!"
    else:
        return f"Failed to upload data. Status code: {response.status_code}, Response: {response.text}"

def log_upload(message, status):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'[{timestamp}] {status.upper()}: {message}\n')

if __name__ == "__main__":
    app.run(debug=True)
