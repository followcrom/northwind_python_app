#!/bin/bash

LOG_FILE="/var/log/user-data.log"

echo "Starting user data script execution" >> $LOG_FILE

# Update and upgrade packages
echo "Updating and upgrading packages..." >> $LOG_FILE
sudo apt update -y >> $LOG_FILE 2>&1
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y >> $LOG_FILE 2>&1

# Install MySQL Server
echo "Installing MySQL Server..." >> $LOG_FILE
sudo apt-get install -y mysql-server >> $LOG_FILE 2>&1

# Configure MySQL Server for non-interactive secure installation
echo "Configuring MySQL Server..." >> $LOG_FILE
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';" >> $LOG_FILE 2>&1
sudo mysql -e "FLUSH PRIVILEGES" >> $LOG_FILE 2>&1

# Enable and restart MySQL service
echo "Enabling and restarting MySQL service..." >> $LOG_FILE
sudo systemctl enable mysql >> $LOG_FILE 2>&1
sudo systemctl restart mysql >> $LOG_FILE 2>&1

# Configure MySQL to allow remote connections
echo "Configuring MySQL to allow remote connections..." >> $LOG_FILE
MYSQL_CONF="/etc/mysql/mysql.conf.d/mysqld.cnf"
sudo sed -i 's/^bind-address\s*=.*/bind-address = 0.0.0.0/' $MYSQL_CONF >> $LOG_FILE 2>&1
sudo systemctl restart mysql >> $LOG_FILE 2>&1

# Clone the repository containing the application
echo "Cloning the repository..." >> $LOG_FILE
mkdir -p ~/repo && cd ~/repo >> $LOG_FILE 2>&1
git clone https://github.com/followcrom/northwind_python_app.git >> $LOG_FILE 2>&1

# Import the database schema
echo "Importing the database schema..." >> $LOG_FILE
sudo mysql -u root -proot < ~/repo/northwind_python_app/northwind_sql.sql >> $LOG_FILE 2>&1

# Create a new MySQL user 'group_2' and grant limited privileges
echo "Creating a new MySQL user and granting privileges..." >> $LOG_FILE
sudo mysql -u root -proot -e "CREATE USER IF NOT EXISTS 'group_2'@'%' IDENTIFIED BY 'password';" >> $LOG_FILE 2>&1
sudo mysql -u root -proot -e "GRANT SELECT, CREATE ON *.* TO 'group_2'@'%'" >> $LOG_FILE 2>&1
sudo mysql -u root -proot -e "FLUSH PRIVILEGES;" >> $LOG_FILE 2>&1

echo "User data script execution completed" >> $LOG_FILE
