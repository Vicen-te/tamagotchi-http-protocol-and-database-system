# Import standard modules (libraries of python)
# We must have added the mysql package for the project to work
import mysql.connector
from mysql.connector import errorcode
# Docu: https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html


class Database:
    # Connexion, and cursor (to execute statements to communicate with MYSQL database)
    def __init__(self, database_name):
        self.cnx = None
        self.cursor = None
        self.database_name = database_name
        self.tables_struct = {
            'users': ("CREATE TABLE `users` ("
                      "  `id` VARCHAR(100) NOT NULL,"
                      "  `pass` VARCHAR(100) NOT NULL DEFAULT 'NOK',"
                      "  PRIMARY KEY (`id`)"
                      ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"),
            'process': ("CREATE TABLE `process` ("
                        "  `id` VARCHAR(100) NOT NULL,"
                        "  `feed` TINYINT UNSIGNED NOT NULL DEFAULT 0,"
                        "  `light` TINYINT UNSIGNED NOT NULL DEFAULT 0,"
                        "  `duck` TINYINT UNSIGNED NOT NULL DEFAULT 0,"
                        "  PRIMARY KEY (`id`)"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"),
            'purchases': ("CREATE TABLE `purchases` ("
                          "  `id` VARCHAR(100) NOT NULL,"
                          "  `item` VARCHAR(25) NOT NULL,"
                          "  `item_number` TINYINT UNSIGNED NOT NULL DEFAULT 1"
                          ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"),
            'items': ("CREATE TABLE `items` ("
                      "  `item` VARCHAR(25) NOT NULL,"
                      "  PRIMARY KEY (`item`)"
                      ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
        }

    def get_cnx(self):
        return self.cnx

    def get_cursor(self):
        return self.cursor

    # Connect to the server with a host, port, user and password
    def connect_server(self, has_database_name=False):
        connected = False
        try:
            if has_database_name:
                # And database name
                self.cnx = mysql.connector.connect(user='root', password='root', database=self.database_name,
                                                   host='localhost', port='3307')
            else:
                self.cnx = mysql.connector.connect(user='root', password='root', host='localhost', port='3307')

            self.cursor = self.cnx.cursor()
            # Check if you haven't had any problems up to this line and set connected to true
            connected = True

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print("Failed accessing to database: {}".format(err))
        return connected

    # Close connexion
    def close_server(self):
        # Make sure data is committed to the database
        self.cnx.commit()

        # The close cursor and connexion
        self.cursor.close()
        self.cnx.close()

    # Create a new database with the project name (DB_NAME)
    def create_database(self):
        try:
            self.cursor.execute("CREATE DATABASE `{}` DEFAULT CHARACTER SET 'utf8'".format(self.database_name))
            print("Database created")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print("Failed creating database: {}".format(err))

    # Delete the current database if exist
    def delete_database(self):
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS `{}`".format(self.database_name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print("Failed deleting database: `{}`".format(err))

    # Use the currently created database
    def use_database(self):
        try:
            self.cursor.execute("USE `{}`".format(self.database_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.database_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print("Database {} created successfully.".format(self.database_name))
                self.cnx.database = self.database_name
            else:
                print(err)

    # Create tables in the database
    def create_tables(self):
        for table in self.tables_struct:
            table_description = self.tables_struct[table]
            try:
                print("Creating table {}: ".format(table), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                # if everything is correct then print ok
                print("OK")

        self.close_server()
