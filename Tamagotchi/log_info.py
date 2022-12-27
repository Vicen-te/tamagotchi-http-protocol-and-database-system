# Import standard modules (libraries of python)
from time import asctime
import sys
import json
import requests
from socket import gethostbyname, gethostname

# Others
# import time
# from datetime import date, datetime, timedelta: other form

# Log File
LOG = "log.txt"


# Save info to the log file
def save_info_log(data, reply, code):
    # Create a new tuple
    new_tuple = (data, reply)

    # IP Geolocation API
    # You can create one on app.abstractapi.com
    # Or comment this part and remove the ip_address from text
    GEOLOCATION_KEY = ''

    try:
        # URL to send the request to
        request_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + GEOLOCATION_KEY
        response = requests.get(request_url)
        result = json.loads(response.content)
        ip_address = result['ip_address']
        # Api requests are limited to 1 per second
        # time.sleep(1)

        # Date, hour, ip_address, html code and message
        text = f"Time: {asctime()}\nIp_address:{ip_address}\nHTMLCode:{code}\nMessage: \n{getjson(new_tuple)}\n\n"

    except Exception:
        print(f"Exception: {str(sys.exc_info())}")
        print("GEOLOCATION_KEY not added")

        # Date, hour, hostname, html code and message
        text = f"Time: {asctime()}\nHost_ip:{gethostbyname(gethostname())}\nHTMLCode:{code}\nMessage: \n{getjson(new_tuple)}\n\n"

    save_log(text)


# Save data in a txt file name log
def save_log(jsonformat):
    file = open(LOG, "a")
    file.write(jsonformat)
    file.write("\n")
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
