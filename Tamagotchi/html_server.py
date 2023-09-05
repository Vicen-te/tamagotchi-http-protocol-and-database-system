# Import standard modules (libraries of python)
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
# Docu: https://docs.python.org/3/library/urllib.parse.html

# Import modules (other files)
from log_info import get_log, getjson, write_log  # , show_log
from pdu import *

# 500 – Internal Server Error
HTMLcode = 500


# Create a correct code
def correct_info():
    print(f"{200} – OK")
    create_info(200, "OK")


# Create an error code
def wrong_info(error_code, message):
    print(f"{error_code} – {message}")
    create_info(error_code, "NOK")


# Create a response saying nok (not ok) or ok
def create_info(html_code, message):
    global HTMLcode
    HTMLcode = html_code
    create_res(message)


# Server management.
# We create a class that inherits from BaseHTTPRequestHandler, (which handles HTTP requests)
class Server(BaseHTTPRequestHandler):
    # The method for requests that arrive via HTTP is defined
    # Receives self as a parameter: the reference to the current object

    def do_GET(self):
        global HTMLcode
        favicon_or_api = False
        try:
            # Extract the parameters
            parameters = parse_qs(urlparse(self.path).query)

            # Check if there are no parameters
            if (parameters is None) or (len(parameters) == 0):
                favicon_or_api = True
                raise KeyError("No parameters defined")

            # Generate responses
            pdu_type = parameters["type"]
            print("Type: " + pdu_type[0])

            # Print parameters by console treating it as a JSON
            print(f"Received parameters: {getjson(parameters)}")

            # The type will be parsed to generate the corresponding response
            match pdu_type[0]:
                # Pdu to compare an id with the values in the database
                case "ID_REQ":
                    if id_req(parameters['id'][0], parameters['pass'][0]):
                        correct_info()
                    else:
                        raise TypeError("Values not found")

                # Pdu to compare an id with the ids in the database and set hungry, sleep and cleaning in the
                # database with the current id
                case "PROCESS_LOG_REQ":
                    if process_log_req(parameters['id'][0], parameters['feed'][0], parameters['light'][0],
                                       parameters['duck'][0]):
                        correct_info()
                    else:
                        raise TypeError("Values not found")
                    pass

                # Pdu to compare an id with the id in the database and create a new row in the database with the
                # purchased item and the id.
                case "PURCHASE_REQ":
                    if purchase_req(parameters['id'][0], parameters['item'][0]):
                        correct_info()
                    else:
                        raise TypeError("Values not found")

                # Pdu to register an id
                case "ID_REC":
                    if not rec_id(parameters['id'][0], parameters['pass'][0]):
                        correct_info()
                    else:
                        raise TypeError("Id register previously")

                # Pdu to register an element
                case "ITEM_REC":
                    if not rec_item(parameters['item'][0]):
                        correct_info()
                    else:
                        raise TypeError("Value register previously")

                case _:
                    raise TypeError("PDU not defined")

        # Exception that has unauthorized values
        except KeyError as error:
            print(f"KeyError: {str(sys.exc_info())}")
            wrong_info(401, f"Unauthorized - {error}")

        # Exception that did not have the correct values, or they have already been set before
        except TypeError as error:
            print(f"TypeError: {str(sys.exc_info())}")
            wrong_info(404, f"Not found - {error}")

        # After try and exceptions, run this block of code
        finally:
            # We add the code to the response
            self.send_response(HTMLcode)

            # We add the code to the header
            self.send_header("Content-type", "text/plain; utf-8")
            self.end_headers()

            # Transform the dict to a JSON with getjson
            # Including the UTF-8 codification
            str_reply = getjson(get_reply())
            self.wfile.write(bytes(str_reply, "utf-8"))

            if not favicon_or_api:
                # Save the information in the log
                text = get_log(get_data(), get_reply(), HTMLcode)
                write_log(text)

            # We print the result of the operation
            # show_log()
