from flask_bcrypt import Bcrypt
from dotenv import dotenv_values
from end_point import urls
from flask import request

# Load existing environment variables
env_values = dotenv_values('.env')

bcrypt = Bcrypt()

# Get user inputs from the registration route
username = request.form.get('username')
password = request.form.get('password')


# Hash the password
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

# Update the .env file with the username and hashed password
env_values['USERNAME'] = username
env_values['HASHED_PASSWORD'] = hashed_password

# Write the updated values back to the .env file
with open('.env', 'w') as f:
    for key, value in env_values.items():
        f.write(f"{key}={value}\n")

print("Username and hashed password have been updated in the .env file.")
