#!/usr/bin/python3

# ==================== IMPORT ====================

import zmq
import sys
import signal
import mysql.connector
from enum import Enum
from mysql.connector import Error
from DBConnection import create_db_connection, ConnectionTypes

# ======================== CONSTANTS ========================

# Helper class containing valid commands as the first part of each received message
class Commands():
    UPDATE_IP_ADDRESS = 'IP'

# Enable printing of debugging info
# Errors are always printed
printDebugMessages = True

# The port used for ZeroMQ connections
ZMQ_PORT = 5555

# ==================== DEBUG PRINT HELPER FUNCTION ====================

# Print a message only if debug printing is enabled, otherwise don't do anything
def debug_print(*args, **kwargs):
    if(printDebugMessages):
        print(*args, **kwargs)

# ==================== SETUP ZeroMQ CONNECTION ====================

debug_print("Setting up ZMQ connection...")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{ZMQ_PORT}")

# ==================== INSERT/UPDATE DATA IN DB ====================

# Run a SQL query and return number of affected rows
def access_database(query, arguments):

    # The return value is the number of rows affected by the query
    affectedRows = 0 

    try:

        # Create a DB connection
        connection = create_db_connection(ConnectionTypes.WRITE)

        # If a connection could not be made, return number of affected rows as -1 to indicate error
        if(connection == None):
            return -1

        # Execute the query, substituting arguments into it
        cursor = connection.cursor()
        cursor.execute(query, arguments)
        connection.commit()
        affectedRows = cursor.rowcount

    except Exception as error:

        # If an error occurred, print it
        print(f"Failed to run SQL query: {query}")
        print(f"Error: {query}")

        # Set number of affected rows to -1 to indicate error
        affectedRows = -1
        
    finally:

        # Close the cursor and DB connection
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            debug_print('Closed MySQL connection')
    
    # Return the number of affected rows
    return affectedRows

# ==================== IP ADDRESS DATA ====================

def update_ip_address_in_db(deviceId, IPAddress):

    # Construct query to insert new device & IP address or update existing one
    updateOrInsertDeviceQuery = """INSERT INTO online_devices (timestamp, device_id, ip_address)
                                    VALUES (NOW(), %s, %s) ON DUPLICATE KEY UPDATE
                                        timestamp=VALUES(timestamp),
                                        device_id=VALUES(device_id),
                                        ip_address=VALUES(ip_address)"""

    # Run the query whith the device ID and IP address as arguments
    affectedRows = access_database(updateOrInsertDeviceQuery, (deviceId, IPAddress))

    # Return the number of affected rows
    return affectedRows
            
# ==================== PROCESS MESSAGE ====================

# Wait for messages from ZeroMQ connection and do some action based on message
def process_message():

    # Get the reply
    debug_print('Waiting for message...')
    messageBytes = socket.recv()

    # Result that will be sent in the reply (based on number of affected rown in DB)
    result = -1

    # The command (first part) of this message that will be sent back in the reply
    command = 'NULL'

    try:

        # Decode message from bytes to string
        message = messageBytes.decode('utf-8')
        debug_print(f"Received message: '{message}'")

        # Split into parts
        messageParts = message.split('|')
        debug_print(f"Message parts: {messageParts}")

        # If there are zero parts, raise an exception
        if(len(messageParts) == 0):
            raise Exception(f"Message '{message}' contains zero parts!")

        # Get the command (first part) from this message
        command = messageParts[0]

        # If the command is for updating an IP address
        if(messageParts[0] == Commands.UPDATE_IP_ADDRESS):

            print(f"Got update IP address message: {messageParts}")

            # If there are not exactly 3 parts (command, Device ID, IP address), raise an exception
            if(len(messageParts) != 3):
                raise Exception(f"Update IP address message '{message}' does not contain 3 parts!")

            # Get the other parts of this message
            deviceId = messageParts[1]
            IPAddress = messageParts[2].replace('\n', '')
            debug_print(f"Device ID: {deviceId}\nIP address: {IPAddress}")

            # Call the update IP address in DB handler function
            # Passing in the received Device ID and IP address
            debug_print(f"Updating IP address...")
            result = update_ip_address_in_db(deviceId, IPAddress)
            debug_print(f"Update IP address result: {result}")

            # Print the result
            print(f"Affected {result} rows, meaning data was ", end='')
            if(result == 0):
                print('not updated (failed / IP address was unchanged)')
            elif(result == 1):
                print('inserted (new Device ID)')
            elif(result == 2):
                print('updated (existing Device ID)')
    
    except Exception as error:
    
        # If an error occurs, print it
        print(f"Error processing message: {error}")

    finally:

        # Try to send the response
        try:
            debug_print('Sending response...')
            response = f"{command}_result: {result}"
            socket.send(response.encode('utf-8'), zmq.NOBLOCK)
            debug_print(f"Sent response '{response}'\n")
        except Exception as e:
            print('Cannot send response: ' + str(e))
    
# ==================== MAIN ====================

def main():
  
    try:
        
        # Repeat forever
        while(True):

            # Try to get data messages and do something
            process_message()
        
    except Exception as e:
    
        # If an error occurs, print it
        print(f"Error in main: {e}")

# ======================== EXIT HANDLER ========================

# Gracefully exit to prevent the "KeyboardInterrupt" from being printed
def signal_handler(sig, frame):
    sys.exit(0)

# ======================== RUN ========================

if __name__== "__main__":

    # Attach handler to exit when interrupt signal is given
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the main program
    main()