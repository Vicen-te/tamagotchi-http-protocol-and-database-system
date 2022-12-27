# Tamagotchi - HTTP Protocol and Database System
This is an assignment made for the University, and it's also my first project with python.

## About this project
I use a local html web service and a local service for the databse.
All PDU requests have a PDU respones that tells you in the python run console whether the information is correct or not, and if it was not correct why. Also, this information will be stored in a txt file call log.txt.
In the HTML file will only be a message saying ok or nok (not ok), it is the json of the PDU response.

# Running App
- Must run all two of below: 
## Running Back-end
- Open Tamagotchi folder as a proyect in PyCharm if possible
- Set interperter.
- Install `mysql`, `mysql-connector-python` and `requests` packages in the interpreter.
- Run the proyect.
## Running Database
- Run remote MySQL Server on workbench or XAMPP.

# Web Photos and PDU responses
![Alt text](/images/web.png?raw=true "Tamagotchi web page")
![Alt text](/images/database.png?raw=true "PhpMyAdmin, MySQL database - Items records")
![Alt text](/images/user.png?raw=true "User ID record")
![Alt text](/images/PDU-response.png?raw=true "Purchase Request PDU")
![Alt text](/images/PDU-response2.png?raw=true "User identification PDU")
![Alt text](/images/log.png?raw=true "PDU records")