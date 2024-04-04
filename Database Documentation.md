# Two Tier Web Application

## The Database

Our task was to create a two-tier web application that interacts with a MySQL database. The database schema was provided in the form of a SQL script. The schema is based on the Northwind database, a sample database used by Microsoft for tutorials and demonstrations.

We are using an AWS EC2 instance running Ubuntu 20.04 to host the MySQL database. The database is accessible by the application, which is running on a second AWS EC2 instance.

Things to consider when setting up the database:

- The database should be configured to allow remote connections.
- The database should be populated with the schema provided.
- A new user should be created with the necessary privileges to interact with the database.

## Set-up script

This can run on a fresh Ubuntu 20.04 server to install MySQL Server, configure it for remote connections, clone the repository containing the application, import the database schema, and create a new MySQL user 'group_2' with the necessary privileges.

```bash
#!/bin/bash

# Update and upgrade packages
sudo apt update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install MySQL Server
sudo apt-get install -y mysql-server

# Configure MySQL Server for non-interactive secure installation
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';"
sudo mysql -e "FLUSH PRIVILEGES"

# Enable and restart MySQL service
sudo systemctl enable mysql
sudo systemctl restart mysql

# Configure MySQL to allow remote connections
MYSQL_CONF="/etc/mysql/mysql.conf.d/mysqld.cnf"
sudo sed -i 's/^bind-address\s*=.*/bind-address = 0.0.0.0/' $MYSQL_CONF
sudo systemctl restart mysql

# Clone the repository containing the application
mkdir -p ~/repo && cd $_
git clone https://github.com/followcrom/northwind_python_app.git

# Import the database schema
sudo mysql -u root -proot < ~/repo/northwind_python_app/northwind_sql.sql

# Create a new MySQL user 'group_2' and grant privileges
sudo mysql -u root -proot -e "CREATE USER IF NOT EXISTS 'group_2'@'%' IDENTIFIED BY 'password';"
sudo mysql -u root -proot -e "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'group_2'@'%'"
sudo mysql -u root -proot -e "FLUSH PRIVILEGES;"
```

## Automating the Set-up

We wanted to automate the set-up process as much as possible. This would make it easier to deploy the application in different environments and reduce the chances of human error. To do this, we utilized Terraform to provision the EC2 instances, and included the above bash script as user data, which would run on the creation of the EC2 instance.