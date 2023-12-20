import argparse
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Класс для загрузки данных из JSON-файлов в базу данных.

    Args:
        db_manager (DatabaseManager): Менеджер базы данных для работы с данными.

    Methods:
        insert_rooms_data(rooms_data: List[Dict[str, Any]]) -> None:
            Вставляет данные о комнатах в базу данных.

        insert_students_data(students_data: List[Dict[str, Any]]) -> None:
            Вставляет данные о студентах в базу данных.

        load_rooms_data(rooms_file_path: str) -> None:
            Загружает данные о комнатах из JSON-файла и вставляет их в базу данных.

        load_students_data(students_file_path: str) -> None:
            Загружает данные о студентах из JSON-файла и вставляет их в базу данных.

        load_data_to_db(rooms_file_path: str, students_file_path: str) -> None:
            Загружает данные о комнатах и студентах из JSON-файлов в базу данных.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует экземпляр класса DataLoader.

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для работы с данными.
        """
        self.db_manager = db_manager

    def insert_rooms_data(self, rooms_data: List[Dict[str, Any]]) -> None:
        """
        Вставляет данные о комнатах в базу данных.

        Args:
            rooms_data (List[Dict[str, Any]]): Список словарей, представляющих данные о комнатах.
        """
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                for room in rooms_data:
                    cursor.execute("""
                        INSERT INTO rooms (id, name)
                        VALUES (%s, %s);
                    """, (room['id'], room['name']))
            db.conn.commit()

    def insert_students_data(self, students_data: List[Dict[str, Any]]) -> None:
        """
        Вставляет данные о студентах в базу данных.

        Args:
            students_data (List[Dict[str, Any]]): Список словарей, представляющих данные о студентах.
        """
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                for student in students_data:
                    birthday_str = student.get('birthday', '')  # Handle missing birthday field
                    birthday = datetime.strptime(birthday_str, "%Y-%m-%dT%H:%M:%S.%f") if birthday_str else None
                    cursor.execute("""
                        INSERT INTO students (id, name, birthday, sex, room_id)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (student['id'], student['name'], birthday, student['sex'], student['room']))
            db.conn.commit()

    def load_rooms_data(self, rooms_file_path: str) -> None:
        """
        Загружает данные о комнатах из JSON-файла и вставляет их в базу данных.

        Args:
            rooms_file_path (str): Путь к JSON-файлу с данными о комнатах.
        """
        logger.info(f"Loading rooms data from file: {rooms_file_path}")
        with open(rooms_file_path, 'r') as rooms_file:
            rooms_data = json.load(rooms_file)
        self.insert_rooms_data(rooms_data)

    def load_students_data(self, students_file_path: str) -> None:
        """
        Загружает данные о студентах из JSON-файла и вставляет их в базу данных.

        Args:
            students_file_path (str): Путь к JSON-файлу с данными о студентах.
        """
        logger.info(f"Loading students data from file: {students_file_path}")
        with open(students_file_path, 'r') as students_file:
            students_data = json.load(students_file)
        self.insert_students_data(students_data)

    def load_data_to_db(self, rooms_file_path: str, students_file_path: str) -> None:
        """
        Загружает данные о комнатах и студентах из JSON-файлов в базу данных.

        Args:
            rooms_file_path (str): Путь к JSON-файлу с данными о комнатах.
            students_file_path (str): Путь к JSON-файлу с данными о студентах.
        """
        logger.info("Loading data to the database...")
        self.load_rooms_data(rooms_file_path)
        self.load_students_data(students_file_path)
        logger.info("Data loading completed.")


def parse_args():
    """
    Разбирает аргументы командной строки.

    Returns:
        argparse.Namespace: Разобранные аргументы командной строки.
    """
    parser = argparse.ArgumentParser(description='Load data from JSON files to a database.')
    parser.add_argument('rooms_file', help='Path to the rooms JSON file')
    parser.add_argument('students_file', help='Path to the students JSON file')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    dbname = DB_NAME
    user = DB_USER
    password = DB_PASSWORD
    host = DB_HOST
    port = DB_PORT

    db_manager = DatabaseManager(dbname, user, password, host, port)

    data_loader = DataLoader(db_manager)

    rooms_file_path = args.rooms_file
    students_file_path = args.students_file

    data_loader.load_data_to_db(rooms_file_path, students_file_path)
