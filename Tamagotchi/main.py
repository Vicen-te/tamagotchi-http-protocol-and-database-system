"""
Web server that listens for HTTP requests and uses a
MySQL database to handle requests and responses

Author: Vicen-te
date: MM-DD-YYYY
Creation date: 12-27-2022
Modification date: 09-05-2022

Web-Service: http://localhost:8000/
Database service HostName&Port: localhost:3307
"""

# Import modules (other files) and standard modules (libraries of python)
from http.server import HTTPServer
from html_server import Server, database

# Define constants: hostName and port
DB_SERVER_ADDRESS = "localhost"
DB_PORT = 8000


# Start the database
def start_database():
    if database.connect_server():
        database.delete_database()
        database.create_database()
        database.use_database()
        database.create_tables()


# Main program
def main():
    server = HTTPServer((DB_SERVER_ADDRESS, DB_PORT), Server)
    try:
        print("Open server on " + DB_SERVER_ADDRESS + " on " + str(DB_PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping server')
        server.socket.close()


# Start the program
if __name__ == '__main__':
    print('Start server')
    start_database()
    main()
