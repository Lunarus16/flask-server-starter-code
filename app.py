# import the Flask class from the flask module, as well as various modules we will be using
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
import sqlite3

# create the application object
app = Flask(__name__, static_url_path='/')
CORS(app)

# set up the sqlite database
app.database = "messages.db"


# a convenience function we will use to connect to the database
def connect_db():
    return sqlite3.connect(app.database)


# we use the @app.route decorators to link the functions to a url
# so when you go to http://localhost:33507/rest this function will be called
# and it allows only GET and POST http requests
# @cross_origin is used to allow CORS requests

@app.route('/rest', methods=['GET', 'POST'])
@cross_origin()
def rest():
    if request.method == 'GET':                             # handle a GET request
        connection = connect_db()                           # get the db connection
        cur = connection.execute('SELECT * FROM messages')  # get all the messages
        message_list = []                                   #initialize an empty list for collecting the json results
        for row in cur.fetchall():                          # use a for loop to build a json string from the results
            json = '{"name":' + '"' + row[0] + '",'
            json += '"email":' + '"' + row[1] + '",'
            json += '"message":' + '"' + row[2] + '"}'
            message_list.append(json)
        result = '['                                        # create a json array with another loop
        for i in range(len(message_list)):
            result += message_list[i]
            if i != len(message_list) - 1:
                result += ','
        result += ']'
        connection.close()                                  # close the db connection
        return result                                       # return the json result


    elif request.method == 'POST':                          # handle a POST request
        name = request.form['name']                         # get the form data to create a new message
        email = request.form['email']
        message = request.form['message']
        connection = connect_db()                           # get the db connection
        cursor = connection.cursor()                         
        cursor.execute("INSERT INTO messages VALUES(?, ?, ?)", (name, email, message))  # insert a new record in the db
        connection.commit()
        connection.close()                                  # close the db connection
        return 'Message Sent!'                              # return a success message


# handle a case where a user browses to http://localhost:33507

@app.route('/')
def index():
    if request.method == 'GET':
        return "Nothing to see here"
    else:
        return 'Error 404'

# this if statement handle executing of this python script from the command line
# where the __name__ environment variable is set to the value '__main__' and
# the below will evaluate to True, the port will be set and the server started

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=False, host='0.0.0.0', port=port)
