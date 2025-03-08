from mysql.connector import pooling
import os
import signal
import sys
import atexit

class Database:


    def __init__(self):
        self.connect()
        self.register_cleanup()



    def connect(self):
        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USERNAME')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        dbconfig = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "database": db_name
        }

        # Create a pool
        try:
            pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=1, pool_reset_session=True, **dbconfig)
            # Get a connection from the pool
            self.connection = pool.get_connection()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)



    def fetch(self, query, params=None, dictionary=False, fetch_one=False):

        cursor = self.connection.cursor(dictionary=dictionary)
        cursor.execute(query, params)
        if fetch_one is False:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()

        return result
    

    def commit(self, query, params=None):
        
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()



    def _cleanup(self, signal_received=None, frame=None):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed due to signal or exit.")

        sys.exit(0)


    def register_cleanup(self):
        signal.signal(signal.SIGINT, self._cleanup)
        signal.signal(signal.SIGTERM, self._cleanup)
        atexit.register(self._cleanup)

