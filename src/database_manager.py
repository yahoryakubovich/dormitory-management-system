import logging
import psycopg2
from typing import Union


class DatabaseManager:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: Union[int, str]):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def __enter__(self) -> 'DatabaseManager':
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self) -> None:
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            logging.info("Successfully connected to the database")
        except psycopg2.Error as e:
            logging.exception(f"Error connecting to the database {e}")

    def close(self) -> None:
        if self.conn and self.conn.closed == 0:
            self.conn.close()
