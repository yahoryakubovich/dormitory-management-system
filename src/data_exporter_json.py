import argparse
import json
import logging
from database_manager import DatabaseManager
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExporterJson:
    """
    Класс для экспорта данных из базы данных в формат JSON.

    Args:
        db_manager (DatabaseManager): Менеджер базы данных для работы с данными.

    Methods:
        export_rooms_with_student_count(output_file: str) -> None:
            Экспортирует данные о комнатах с количеством студентов в файл JSON.

        export_rooms_with_average_age(output_file: str) -> None:
            Экспортирует данные о комнатах с средним возрастом студентов в файл JSON.

        export_rooms_with_age_difference(output_file: str) -> None:
            Экспортирует данные о комнатах с разницей возраста студентов в файл JSON.

        export_rooms_with_multiple_sex(output_file: str) -> None:
            Экспортирует данные о комнатах с разными полами студентов в файл JSON.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует экземпляр класса DataExporterJson.

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для работы с данными.
        """
        self.db_manager = db_manager

    def export_rooms_with_student_count(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с количеством студентов в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with student count data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT rooms.id, rooms.name, COUNT(students.id) AS student_count
                    FROM rooms
                    LEFT JOIN students ON rooms.id = students.room_id
                    GROUP BY rooms.id, rooms.name
                    ORDER BY rooms.id;
                """)
                rooms_data = cursor.fetchall()

        formatted_rooms_data = [
            {
                "id": room[0],
                "name": room[1],
                "student_count": room[2]
            }
            for room in rooms_data
        ]

        with open(output_file, 'w') as rooms_file:
            json.dump(formatted_rooms_data, rooms_file, indent=2)
            logger.info("Data export completed.")

    def export_rooms_with_average_age(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с средним возрастом студентов в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with average age data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT rooms.id, rooms.name, AVG(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) AS average_age
                    FROM rooms
                    LEFT JOIN students ON rooms.id = students.room_id
                    GROUP BY rooms.id, rooms.name
                    ORDER BY average_age ASC
                    LIMIT 5;
                """)
                rooms_data = cursor.fetchall()

        formatted_rooms_data = [
            {
                "id": room[0],
                "name": room[1],
                "average_age": room[2]
            }
            for room in rooms_data
        ]

        with open(output_file, 'w') as rooms_file:
            json.dump(formatted_rooms_data, rooms_file, indent=2)
            logger.info("Data export completed.")

    def export_rooms_with_age_difference(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с разницей возраста студентов в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with age difference data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT rooms.id, rooms.name,
                        MAX(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) -
                        MIN(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) AS age_difference
                    FROM rooms
                    LEFT JOIN students ON rooms.id = students.room_id
                    GROUP BY rooms.id, rooms.name
                    ORDER BY age_difference DESC
                    LIMIT 5;
                """)
                rooms_data = cursor.fetchall()

        formatted_rooms_data = [
            {
                "id": room[0],
                "name": room[1],
                "age_difference": room[2]
            }
            for room in rooms_data
        ]

        with open(output_file, 'w') as rooms_file:
            json.dump(formatted_rooms_data, rooms_file, indent=2)
            logger.info("Data export completed.")

    def export_rooms_with_multiple_sex(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с разными полами студентов в файл JSON.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with multiple sexes data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex);
                    SELECT rooms.id, rooms.name
                    FROM rooms
                    INNER JOIN students ON rooms.id = students.room_id
                    GROUP BY rooms.id, rooms.name
                    HAVING COUNT(DISTINCT students.sex) > 1;
                """)
                rooms_data = cursor.fetchall()

        formatted_rooms_data = [
            {
                "id": room[0],
                "name": room[1]
            }
            for room in rooms_data
        ]

        with open(output_file, 'w') as rooms_file:
            json.dump(formatted_rooms_data, rooms_file, indent=2)
            logger.info("Data export completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export data to JSON files.")
    parser.add_argument("--export_rooms_with_student_count", action="store_true", help="Export rooms with student count.")
    parser.add_argument("--export_rooms_with_average_age", action="store_true", help="Export rooms with average age.")
    parser.add_argument("--export_rooms_with_age_difference", action="store_true", help="Export rooms with age difference.")
    parser.add_argument("--export_rooms_with_multiple_sex", action="store_true", help="Export rooms with multiple sexes.")

    args = parser.parse_args()

    db_manager = DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    exporter = DataExporterJson(db_manager)

    if args.export_rooms_with_student_count:
        output_file = "output_rooms_with_student_count.json"
        exporter.export_rooms_with_student_count(output_file)

    if args.export_rooms_with_average_age:
        output_file = "output_rooms_with_average_age.json"
        exporter.export_rooms_with_average_age(output_file)

    if args.export_rooms_with_age_difference:
        output_file = "output_rooms_with_age_difference.json"
        exporter.export_rooms_with_age_difference(output_file)

    if args.export_rooms_with_multiple_sex:
        output_file = "output_rooms_with_multiple_sex.json"
        exporter.export_rooms_with_multiple_sex(output_file)
