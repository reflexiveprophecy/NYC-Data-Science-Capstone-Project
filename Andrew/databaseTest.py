# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Install mysql:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Pretty easy, follow the steps here:
# https://dev.mysql.com/doc/refman/5.6/en/osx-installation-pkg.html
# When install finishes, make sure to note what the password is.

# Restart computer.

# Log into mysql and set password when prompted.
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Install mysql connector: 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download file:
# https://pypi.python.org/pypi/mysql-connector-python/8.0.6

# Run this command in Downloads folder:
# $ tar xzf mysql-connector-python-8.0.6.tar.gz 

# cd mysql-connector-python-8.0.6

# sudo python3 setup.py install

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Verification: 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Run this script to verify install.

import mysql.connector

cnx = mysql.connector.connect(user='root', password='cookies',
                              host='127.0.0.1',
                              database='mynewdb')
cnx.close()

print("yay")