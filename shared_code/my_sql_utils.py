import mysql.connector 
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
import logging

def establish_my_sql_connector(u_name:str,pw:str,host_name:str,db_name:str) -> PooledMySQLConnection | MySQLConnectionAbstract:
    '''Establosha connection to the MySQL environment'''
    try:
        con = mysql.connector.connect(host = host_name, user = u_name, password = pw,database = db_name, buffered = True)
        if con.is_connected():
            logging.info(f'Connected to {db_name} MySQL database')
    except Exception as e:
        logging.error(msg=f'Error {e} was observed')
        raise e
    return con
def query_my_sql(u_name:str, pw:str, host_name:str, query:str, db_name:str|None = None,):
    '''Establish and return a connector from a local mySQL connector'''
    con = establish_my_sql_connector(u_name=u_name,pw=pw,host_name=host_name,db_name=db_name)
    my_cursor = con.cursor()

    my_cursor.execute(query)
    results = my_cursor.fetchall()
    my_cursor.close()

    return results

def insert_my_sql(u_name:str,pw:str,host_name:str,db_name:str,query:str,items_to_insert:tuple):
    '''Insert {items_to_insert} given parameters to connect to db '''
    con = establish_my_sql_connector(u_name=u_name,pw=pw,host_name=host_name,db_name=db_name)
    my_cursor = con.cursor()

    my_cursor.execute(query,items_to_insert,multi=False)
    con.commit()

    con.close()

