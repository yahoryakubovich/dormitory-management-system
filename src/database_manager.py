import logging
from typing import Union
import psycopg2


class DatabaseManager:
    """
    Менеджер базы данных для управления подключением к PostgreSQL.

    Args:
        dbname (str): Имя базы данных.
        user (str): Имя пользователя базы данных.
        password (str): Пароль для доступа к базе данных.
        host (str): Адрес хоста базы данных.
        port (Union[int, str]): Номер порта для подключения к базе данных.

    Attributes:
        dbname (str): Имя базы данных.
        user (str): Имя пользователя базы данных.
        password (str): Пароль для доступа к базе данных.
        host (str): Адрес хоста базы данных.
        port (Union[int, str]): Номер порта для подключения к базе данных.
        conn (psycopg2.extensions.connection): Объект подключения к базе данных.

    Methods:
        __enter__() -> 'DatabaseManager':
            Возвращает сам объект менеджера при использовании в контексте.

        __exit__(exc_type, exc_value, traceback):
            Закрывает соединение с базой данных при завершении работы с контекстом.

        connect() -> None:
            Устанавливает соединение с базой данных.

        close() -> None:
            Закрывает соединение с базой данных.

    Usage:
        # Пример использования в контексте
        with DatabaseManager(dbname='mydb', user='user', password='password', host='localhost', port=5432) as db:
            # Выполнение операций с базой данных внутри контекста
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: Union[int, str]):
        """
        Инициализирует экземпляр класса DatabaseManager.

        Args:
            dbname (str): Имя базы данных.
            user (str): Имя пользователя базы данных.
            password (str): Пароль для доступа к базе данных.
            host (str): Адрес хоста базы данных.
            port (Union[int, str]): Номер порта для подключения к базе данных.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def __enter__(self) -> 'DatabaseManager':
        """
        Возвращает сам объект менеджера при использовании в контексте.

        Returns:
            DatabaseManager: Объект менеджера базы данных.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закрывает соединение с базой данных при завершении работы с контекстом.

        Args:
            exc_type: Тип исключения (если есть).
            exc_value: Значение исключения (если есть).
            traceback: Стек вызовов (если есть).
        """
        self.close()

    def connect(self) -> None:
        """
        Устанавливает соединение с базой данных.

        Raises:
            psycopg2.Error: Если произошла ошибка при подключении к базе данных.
        """
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
        """
        Закрывает соединение с базой данных.
        """
        if self.conn and self.conn.closed == 0:
            self.conn.close()
