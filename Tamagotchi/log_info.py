# Import standard modules (libraries of python)
from time import asctime
import sys
import json
# Docu: https://docs.python.org/3/library/json.html
import requests
from socket import gethostbyname, gethostname

# Others
# import time
# from datetime import date, datetime, timedelta: other form

# Log File
LOG = "log.txt"

# IP Geolocation API
# You can create one on app.abstractapi.com
# Or comment this part and remove the ip_address from text
GEOLOCATION_KEY = ''


def ip_geolocation():
    # URL to send the request to
    request_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + GEOLOCATION_KEY
    response = requests.get(request_url)
    result = json.loads(response.content)
    ip_address = result['ip_address']
    # Api requests are limited to 1 per second
    # time.sleep(1)
    return ip_address


# Get the log info
def get_log(data, reply, code):
    # Create a new tuple
    new_tuple = (data, reply)

    # Date, hour, html code, message
    try:
        ip_address = ip_geolocation()
        # And ip_address
        text = f"Time: {asctime()}\nIp_address:{ip_address}\nHTMLCode:{code}\nMessage: \n{getjson(new_tuple)}\n\n"

    except Exception:
        print(f"Exception: {str(sys.exc_info())}")
        print("GEOLOCATION_KEY not added")

        # And hostname
        text = f"Time: {asctime()}\nHost_ip:{gethostbyname(gethostname())}\nHTMLCode:{code}\nMessage: \n{getjson(new_tuple)}\n\n"
    return text


# Write the log in a txt file name log.txt
def write_log(text):
    file = open(LOG, "a")
    file.write(f"{text}\n")
    file.close()


# Gets the JSON format of the dictionary
def getjson(jsonformat):
    return json.dumps(jsonformat, indent=2)


# Show file log
def show_log():
    try:
        file = open(LOG, "r")
        content = file.readlines()
        file.close()
        for linea in content:
            print(linea.replace('\n', ''))
    except FileNotFoundError:
        print("The log file doesn't exist")


# Empty all file info
def empty_log():
    try:
        open(LOG, 'w').close()
    except FileNotFoundError:
        print("The log file doesn't exist")
