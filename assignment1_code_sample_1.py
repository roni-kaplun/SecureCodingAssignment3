import os
import pymysql
from urllib.request import urlopen


# Category: Cryptographic Failures, Broken Access Control, Security Misconfiguration, Identification and Authentication Failures
# (does not attempt to prove the identity of the user)

# Password stored in-code, 
# if this were a real password and in a github repository (which it is), 
# it would be visible to everyone who can view the repository.
# Better to store it in secrets or environment variables or something.
db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
}


# Category: Injection

# User input is not validated at all
# There could at LEAST be a check to make sure it isn't empty
# The user should not be allowed to type whatever they want
# Since this is supposed to be a name presumably,
# there could be a check to ensure the input only contains
# letters of the alphabet
# Possibly also a maximum length
def get_user_input():
    user_input = input('Enter your name: ')
    return user_input


# Category: Injection, Insecure Design

# Any of these parameters could probably be used for malicious purposes
# in the case that the user can imput anything (which is true as seen above),
# the user could inject code into the system command 
# (because it is done with string building/formatting)
def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')

# Category: Broken Access Control and Software and Data Integrity Failures

# Explanation
# Data must only be pulled from trusted sources/links 
# as unauthorized access and malicious code can be introduced within the software
# The developer must review code for potential problems such as this.
# Another problem is that the url is not validated and if it does not return
# any data, the code will break.

# Recommendations
# An array should be created of trusted websites, and the url should be compared
# To this array to see if the url the data is pulled from is trusted
def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

# Category: Injection

# Explanation
# The query does not validate itself and/or check for potentially malicious code
# Meaning that data can potentially alter or destroy the database.
# Another issue is that there is no error handling, meaning that if
# something does not work for any reason, the program will break.

# Recommendations
# Validate and sanitize the query and make sure that it cannot possibly harm 
# or alter the database 
# Add error handling

def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

# Category: Injection, Insecure Design, Software and Data Integrity Failures

# Explanation
# This code executes the program which contains the insecure functions
# I talked about earlier
# For example, the get_user_input function is not validated
# and can be used to run malicious code within the program
# The get_data() and save_to_db() commands are insecure and can use
# SQL injection to modify and/or destroy the used database
# Finally, the send_email function does not validate the user_input
# and can also be used to run malicious code using the program

# Recommendations
# Do all previous recommendations and add error handling
# within this function so that the program does not destruct upon an error
# Validate the send_email function and add error handling for it as well

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
