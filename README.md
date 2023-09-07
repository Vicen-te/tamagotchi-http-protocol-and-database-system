# Tamagotchi - HTTP Protocol and Database System
This is an assignment done for the University and it is also my first project with Python.

## About this project
I use a local html web service and a local service for the database. 
All PDU requests have PDU responses that tell you in the Python runtime console whether or not the information is correct, and if not, why. Also, this information will be stored in a txt file called log.txt. 
In the HTML file there will only be a message that says ok or nok (not ok), it is the json of the PDU response.

# Running App
### Running Back-end
- Open Tamagotchi folder as project in PyCharm if possible
- Set interperter.
- Install the `mysql`, `mysql-connector-python` and `requests` packages in the interpreter.
- Run the proyect.
### Running Database
- Run the remote MySQL Server on workbench or XAMPP.

# Web Photos and PDU responses
![Alt text](/images/web.png?raw=true "Tamagotchi web page")
![Alt text](/images/database.png?raw=true "PhpMyAdmin, MySQL database - Items records")
![Alt text](/images/user.png?raw=true "User ID record")
![Alt text](/images/PDU-response.png?raw=true "Purchase Request PDU")
![Alt text](/images/PDU-response2.png?raw=true "User identification PDU")
![Alt text](/images/log.png?raw=true "PDU records")
