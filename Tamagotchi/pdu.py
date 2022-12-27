from database import Database

# Create the database with tables and correspondent columns
database = Database()

# Create two dict types, these can be converted to a JSON
data = {}
response = {}


def get_data():
    return data


def get_reply():
    return response


'''
Create a PDU of type ID_REQ or REC_ID
The structure that the JSON will have will be:
{
    "type": "ID_REQ/ID_REC",
    "id": "arwen",
    "pass": "1234"
}
'''


def create_id(identifier, password, register=False):
    global data
    type = "ID_REQ"
    if register:
        type = "ID_REC"

    data = {
        "type": type,
        "id": identifier,
        "pass": password
    }


# Create an id record and check if the id exist
def rec_id(identifier, password):
    global database, data
    create_id(identifier, password, True)

    check = False
    if database.connect_server(True):
        sql_select_Query = "select * from `users`"
        database.cursor.execute(sql_select_Query)
        records = database.cursor.fetchall()
        for (id, password) in records:
            if id == identifier:
                check = True
                break

        if not check:
            add_id = ("INSERT INTO users(id, pass)"
                      "VALUES (%(id)s, %(pass)s)")
            database.cursor.execute(add_id, data)
        database.close_server()
    return check


# Create an id request and check if the id exists
def id_req(identifier, password):
    global database
    create_id(identifier, password)

    check = False
    if database.connect_server(True):
        query = (f"SELECT * FROM `users`"
                 "WHERE id = %s AND pass = %s")
        database.cursor.execute(query, (identifier, password))
        for (id, passw) in database.cursor:
            if id == identifier and passw == password:
                check = True
                break
        database.close_server()
    return check


''' 
Create a PDU of type PROCESS_LOG_REQ
The structure that the JSON will have will be:
{
    "type": "PROCESS_LOG_REQ",
    "id": "arwen",
    "feed": 100, (hunger percent)
    "light": 50, (sleeping percent)
    "duck": 10 (cleaning percent)
}
'''


def create_process_log(identifier, feed, light, duck):
    global data
    data = {
        "type": "PROCESS_LOG_REQ",
        "id": identifier,
        "feed": feed,
        "light": light,
        "duck": duck
    }


# Check if the id exist in the process table and create or update the values
def rec_process_log(identifier):
    global database, data
    query = (f"SELECT * FROM `process`"
             "WHERE id = %s")
    database.cursor.execute(query, (identifier,))

    check = False
    for (id, feed, light, duck) in database.cursor:
        if id == identifier:
            check = True
            break

    if check:
        add_process_log = ("UPDATE process "
                           "SET feed = %(feed)s, "
                           "light = %(light)s, duck = %(duck)s "
                           "WHERE id = %(id)s")
        print("Values Changed")
    else:
        add_process_log = ("INSERT INTO process(id, feed, light, duck)"
                           "VALUES (%(id)s, %(feed)s, %(light)s, %(duck)s)")
    database.cursor.execute(add_process_log, data)


# Create a process log request and check if the id exist in the users table
def process_log_req(identifier, feed, light, duck):
    global database
    create_process_log(identifier, feed, light, duck)

    check = False
    if database.connect_server(True):
        query = "SELECT * FROM `users` WHERE id = %s"
        database.cursor.execute(query, (identifier,))

        for (id, passw) in database.cursor:
            if id == identifier:
                check = True
                rec_process_log(identifier)
                break
        database.close_server()
    return check


'''
Create a PDU of type SHOP_REQ
The structure that the JSON will have will be:
{
    "type": "PURCHASE_REQ",
    "id": "arwen",
    "item": "sponge",
    "item_number": 1
}
'''


def create_purchase(identifier, item):
    global data
    data = {
        "type": "PURCHASE_REQ",
        "id": identifier,
        "item": item
    }


# Check if the element exist and create a new row with the new item,
# or add a number to the item_number that has the id
def rec_purchase(identifier, item):
    global database, data

    # Check if an item exist in table items
    query = "SELECT * FROM `items`"
    database.cursor.execute(query)
    check_item = False

    for (i,) in database.cursor:
        if i == item:
            check_item = True

    # Check if id has an item and add a number or create a new one
    query = "SELECT * FROM `purchases`"
    database.cursor.execute(query)
    check_has_item = False

    for (id, i, number) in database.cursor:
        if i == item and id == identifier:
            check_has_item = True

    if check_has_item:
        add_purchase = ("UPDATE purchases "
                        "SET item_number = item_number + 1 "
                        "WHERE id = %(id)s AND item = %(item)s")
        print("Values Changed")
        database.cursor.execute(add_purchase, data)
        return True

    elif check_item:
        add_purchase = ("INSERT INTO purchases(id, item, item_number) "
                        "VALUES (%(id)s, %(item)s, DEFAULT)")
        database.cursor.execute(add_purchase, data)
        return True

    else:
        return False


# Create an in-app purchase request and check if the id exist
def purchase_req(identifier, item):
    global database
    create_purchase(identifier, item)

    check = False
    if database.connect_server(True):
        query = "SELECT * FROM `users` WHERE id = %s"
        database.cursor.execute(query, (identifier,))

        for (id, passw) in database.cursor:
            if id == identifier:
                check = rec_purchase(id, item)
                break

        database.close_server()
    return check


'''
Create a PDU of type ELEMENT_REC
The structure that the JSON will have will be:
{
    "type": "ITEM_REC",
    "item": "sponge",
}
'''


def create_item(item):
    global data
    data = {
        "type": "ITEM_REC",
        "item": item
    }


# Create an item record and check if the item exist
def rec_item(item):
    global database, data
    create_item(item)

    check = False
    if database.connect_server(True):
        sql_select_Query = "SELECT * FROM `items`"
        database.cursor.execute(sql_select_Query)
        records = database.cursor.fetchall()
        for (i,) in records:
            if i == item:
                check = True
                break
        if not check:
            add_item = ("INSERT INTO items(item)"
                        "VALUES (%(item)s)")
            database.cursor.execute(add_item, data)
        database.close_server()
    return check


'''
Create a PDU of type RES
The structure that the JSON will have will be:
{
    "type": "RES",
    "code": "OK",
}
'''


def create_res(code):
    global response
    response = {
        "type": "RES",
        "code": code,
    }
