from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import ssl
import certifi

class Connection:

    @classmethod
    def connection(cls):
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        return (conn, conn.cursor())