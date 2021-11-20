#!/usr/bin/python3

# ==================== IMPORT ====================

from enum import Enum
import mysql.connector


# ======================== CONSTANTS ========================

# The name of the database to access
DATABASE_TO_USE = 'testing'

# Helper class containing types of connections that can be made
class ConnectionTypes(Enum):
    READ = 'READ'
    WRITE = 'WRITE'

# ==================== DATEBASE CONNECTION HELPER FUNCTION ====================

# Create and return a DB connection
def create_db_connection(connectionType):

    try:

        # Determine type of connection to make (which user to use)
        settingsFileName = '/home/wi-wait/database/'+'db-settings-read.txt' if connectionType == ConnectionTypes.READ else 'db-settings-write.txt'

        # Read DB settings from external file
        with open(settingsFileName) as DBSettings:
            host, user, password = map(lambda x: x.replace('\n', '').replace('\r', ''), 
                [DBSettings.readline(), DBSettings.readline(), DBSettings.readline()])

        # Create the connection and return it
        return mysql.connector.connect(database=DATABASE_TO_USE,
                                            host=host,
                                            user=user,
                                            password=password)

    except Exception as error:
        
        # If an error occurred, print it
        print(f"Failed to connect to database: {error}")

        # Return None to indicate a conneciton could not be made
        return None