#!/usr/bin/python3

import mysql.connector
from DBConnection import create_db_connection, ConnectionTypes
import pandas as pd

def real_count():
    conn = create_db_connection(ConnectionTypes.READ)
    query = 'SELECT * FROM PeopleCounter'
    df = pd.read_sql(query, con=conn) 
    return df

def type4():
    conn = create_db_connection(ConnectionTypes.READ)
    query = 'SELECT timestamp,count AS "NumPeople" FROM `PeopleCounter` WHERE measurement_type = 4 order by timestamp desc'
    df = pd.read_sql(query, con=conn) 
    return df

def type0():
    conn = create_db_connection(ConnectionTypes.READ)
    query = 'SELECT timestamp,count AS "NumPeople" FROM `PeopleCounter` WHERE measurement_type = 0 order by timestamp desc'
    df = pd.read_sql(query, con=conn) 
    return df

    # display real_count, count where meastype == 4 and count where meastype == 0