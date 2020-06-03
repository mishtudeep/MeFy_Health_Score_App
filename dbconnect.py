import mysql.connector
import configparser


def getConnection():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        connection = mysql.connector.connect(host=config['DB']['host'],
                                            database=config['DB']['database'],
                                            user=config['DB']['user'],
                                            password=config['DB']['password'])
        if connection.is_connected():
            return connection, connection.cursor()

    except Exception as e:
        print("Error while connecting to MySQL", e)
        connection.close()