# Sample Python Web Application Deployment Guide

## Dependencies

Change 1

- Python 3.9
- MySQL 8.0
- northwind database schema created and populated (I used this script https://en.wikiversity.org/wiki/Database_Examples/Northwind/MySQL, if something else is used, the program may need to be updated for different column names)
- The following Python packages in addition to the regular ones included with Python distributions:
  - waitress 3.0.0
  - flask 3.0.2
  - flask-sqlalchemy 3.1.1
  - SQLAlchemy 2.0.27
  - PyMySQL 1.1.0
  - Jinja 3.1.3
  - Flask-Waitress 0.0.1
- The database URI needs to be configured in the OS as an environment variable called DB_CONNECTION_URI
  - The value should be a complete URI for the database in the form mysql+pymysql://uid:pwd@host:port/northwind (eg mysql+pymysql://root:root@localhost:3306/northwind)
  - The database does not need to be running on localhost
- Unzip the zip file to a convenient location, this will create a directory NorthwindWeb

## Testing after deployment

- In a command prompt, go to the NorthwindWeb directory
- Enter
  - waitress-serve --port=5000 northwind_web:app
- Open a browser
- Go to localhost:5000 (or replace localhost with the IP address of the machine running the server if the browser is on another machine) - you should see a table of customers
- Click the link at the top to "Add a New Customer", fill in the details and click "Submit"
- Scroll to the bottom and you should see the customer you just added
- Click the "Delete" link, scroll back to the bottom and your added customer should have disappeared
- Click the "Delete" link on customer #2 and you should get an error page
- If all the above works, the app is successfully deployed

## Limitations

- The "Edit" feature is not yet implemented
- Only the customers table is accessible through the web application
