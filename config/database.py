import sys
import os
import configparser
from PyQt6 import QtSql

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_INI = os.path.join(CONFIG_DIR, "config.ini")


class DB(QtSql.QSqlDatabase):
    def __init__(self):
        super().__init__()

        config = configparser.ConfigParser()
        config.read(CONFIG_INI)
        self.connect = self.addDatabase("QPSQL", connectionName="pgsql_connection")
        self.connect.setHostName(config["postgresql"]["host"])
        self.connect.setUserName(config["postgresql"]["user"])
        self.connect.setPassword(config["postgresql"]["pass"])
        self.connect.setDatabaseName(config["postgresql"]["db"])
        self.connect.setPort(int(config["postgresql"]["port"]))
        if not self.connect.open():
            print("Cannot open database:")
            print(self.connect.lastError().text())
            sys.exit(1)

    def __del__(self):
        self.connect.close()
