from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.orm import Session

from FiledEcommerce.Api.startup import fixtures
import pyodbc
import os

SQL_CONNECTION = None


class SqlManager:
    __cursor = None
    __server: str = "stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com"
    __port: str = "1433"
    __username: str = "filed_admin"
    __password: str = "dvserv3#rathena"
    __database: str = "Dev3.Filed.ProductCatalogs2"
    __driver: str = "{ODBC Driver 17 for SQL Server}"

    @classmethod
    def __connection_string(cls):
        return f"DRIVER={cls.__driver};" \
               f"SERVER={cls.__server},{cls.__port};" \
               f"DATABASE={cls.__database};" \
               f"UID={cls.__username};" \
               f"PWD={cls.__password}"

    @classmethod
    def __enter__(cls):
        global SQL_CONNECTION
        if SQL_CONNECTION is None:
            SQL_CONNECTION = pyodbc.connect(cls.__connection_string())

        cls.__cursor = SQL_CONNECTION.cursor()
        return cls.__cursor

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls.__cursor.close()
