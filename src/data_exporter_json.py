import json
import logging
from database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExporterJson:
    """
    Класс для экспорта данных из базы данных в формат JSON.

    Args:
        db_manager (DatabaseManager): Менеджер базы данных для работы с данными.

    Methods:
        export_rooms_data(output_file: str) -> None:
            Экспортирует данные о комнатах в файл JSON.

        export_students_data(output_file: str) -> None:
            Экспортирует данные о студентах в файл JSON.

        export_data_from_db(output_rooms_file: str, output_students_file: str) -> None:
            Экспортирует данные о комнатах и студентах из базы данных в файлы JSON.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует экземпляр класса DataExporterJson.

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для работы с данными.
        """
        self.db_manager = db_manager

    def export_rooms_data(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM rooms;")
                rooms_data = cursor.fetchall()

        formatted_rooms_data = [
            {
                "id": room[0],
                "name": room[1]
            }
            for room in rooms_data
        ]

        with open(output_file, 'w') as rooms_file:
            json.dump(formatted_rooms_data, rooms_file, default=str, indent=2)

    def export_students_data(self, output_file: str) -> None:
        """
        Экспортирует данные о студентах в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students;")
                students_data = cursor.fetchall()

        formatted_students_data = [
            {
                "id": student[0],
                "name": student[1],
                "birthday": student[2].strftime("%Y-%m-%d") if student[2] else None,
                "sex": student[3],
                "room": student[4]
            }
            for student in students_data
        ]

        with open(output_file, 'w') as students_file:
            json.dump(formatted_students_data, students_file, default=str, indent=2)

    def export_data_from_db(self, output_rooms_file: str, output_students_file: str) -> None:
        """
        Экспортирует данные о комнатах и студентах из базы данных в файлы JSON.

        Args:
            output_rooms_file (str): Путь к файлу для сохранения данных о комнатах.
            output_students_file (str): Путь к файлу для сохранения данных о студентах.
        """
        self.export_rooms_data(output_rooms_file)
        self.export_students_data(output_students_file)
