from mysql.connector import pooling, errors
import os
import signal
import sys
import atexit
import time

class Database:
    def __init__(self):
        self._create_pool()
        self.register_cleanup()

    def _create_pool(self):
        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USERNAME')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        dbconfig = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "database": db_name,
            # Add timeout parameters
            "connection_timeout": 30,
            "pool_reset_session": True,
            "charset": "utf8mb4"
        }

        # Create a pool
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mypool", 
                pool_size=5,  # Increased pool size
                **dbconfig
            )
            print("Database pool created successfully")
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            sys.exit(1)



    def _get_connection(self):
        """Get a connection from the pool with retry logic"""
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                connection = self.pool.get_connection()
                # Verify connection is working with a simple query
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                return connection
            except (errors.PoolError, errors.InterfaceError, errors.OperationalError) as e:
                print(f"Connection attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("All connection attempts failed")
                    return None  # Explicitly return None after all retries



    def fetch(self, query, params=None, dictionary=False, fetch_one=False):
        
        connection = None

        try:
            connection = self._get_connection()
            if connection is None:
                raise errors.OperationalError("Could not establish database connection after multiple attempts")
                
            cursor = connection.cursor(dictionary=dictionary)
            cursor.execute(query, params)
            
            
            if fetch_one is False:
                result = cursor.fetchall()

            else:

                fetched_result = cursor.fetchone()

                if fetched_result is None:
                    result = None

                elif dictionary:
                    result = fetched_result  # Return the entire dictionary

                else:
                    result = fetched_result[0]  # Access first element only if not None

            cursor.close()
            return result
        
        except Exception as e:
            print(f"Database fetch error: {e}")
            raise

        finally:
            if connection:
                connection.close()  # Return connection to pool



    def commit(self, query, params=None):
        connection = None
        try:
            connection = self._get_connection()
            if connection is None:
                raise errors.OperationalError("Could not establish database connection after multiple attempts")
                
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Database commit error: {e}")
            raise
        finally:
            if connection:
                connection.close()  # Return connection to pool



    def _cleanup(self, signal_received=None, frame=None):
        print("Cleaning up database resources...")
        # No need to close individual connections as they're managed by the pool
        sys.exit(0)



    def register_cleanup(self):
        signal.signal(signal.SIGINT, self._cleanup)
        signal.signal(signal.SIGTERM, self._cleanup)
        atexit.register(self._cleanup)