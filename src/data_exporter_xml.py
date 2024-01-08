import argparse
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
from database_manager import DatabaseManager
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExporterXml:
    """
       Класс для экспорта данных из базы данных в формат XML.

       Args:
           db_manager (DatabaseManager): Менеджер базы данных для работы с данными.

       Methods:
           export_rooms_with_student_count(output_file: str) -> None:
               Экспортирует данные о комнатах с количеством студентов в файл XML.

           export_rooms_with_average_age(output_file: str) -> None:
               Экспортирует данные о комнатах с средним возрастом студентов в файл XML.

           export_rooms_with_age_difference(output_file: str) -> None:
               Экспортирует данные о комнатах с разницей возраста студентов в файл XML.

           export_rooms_with_multiple_sex(output_file: str) -> None:
               Экспортирует данные о комнатах с разными полами студентов в файл XML.
       """
    def __init__(self, db_manager: DatabaseManager):
        """
        Инициализирует экземпляр класса DataExporterXml.

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для работы с данными.
        """
        self.db_manager = db_manager

    def prettify(self, elem):
        """
        Возвращает красиво отформатированную XML-строку для элемента.

        Args:
            elem: Элемент XML.

        Returns:
            str: Красиво отформатированная XML-строка.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")

    def export_rooms_with_student_count(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с количеством студентов в файл XML.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with student count to file: {output_file}")
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

        root = ET.Element("rooms_with_student_count")
        for room in rooms_data:
            room_element = ET.SubElement(root, "room")
            id_element = ET.SubElement(room_element, "id")
            id_element.text = str(room[0])
            name_element = ET.SubElement(room_element, "name")
            name_element.text = room[1]
            student_count_element = ET.SubElement(room_element, "student_count")
            student_count_element.text = str(room[2])

        with open(output_file, 'w') as file:
            file.write(self.prettify(root))
            logger.info("Data export completed.")

    def export_rooms_with_average_age(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах со средним возрастом студентов в файл XML.
        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with average age to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);
                    SELECT rooms.id, rooms.name, AVG(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) AS average_age
                    FROM rooms
                    LEFT JOIN students ON rooms.id = students.room_id
                    GROUP BY rooms.id, rooms.name
                    ORDER BY average_age ASC
                    LIMIT 5;
                """)
                rooms_data = cursor.fetchall()
        root = ET.Element("rooms_with_average_age")
        for room in rooms_data:
            room_element = ET.SubElement(root, "room")
            id_element = ET.SubElement(room_element, "id")
            id_element.text = str(room[0])
            name_element = ET.SubElement(room_element, "name")
            name_element.text = room[1]
            average_age_element = ET.SubElement(room_element, "average_age")
            average_age_element.text = str(room[2])
        with open(output_file, 'w') as file:
            file.write(self.prettify(root))
            logger.info("Data export completed.")

    def export_rooms_with_age_difference(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с разницей в возрасте студентов в файл XML.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with age difference to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);
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

        root = ET.Element("rooms_with_age_difference")
        for room in rooms_data:
            room_element = ET.SubElement(root, "room")
            id_element = ET.SubElement(room_element, "id")
            id_element.text = str(room[0])
            name_element = ET.SubElement(room_element, "name")
            name_element.text = room[1]
            age_difference_element = ET.SubElement(room_element, "age_difference")
            age_difference_element.text = str(room[2])

        with open(output_file, 'w') as file:
            file.write(self.prettify(root))
            logger.info("Data export completed.")


    def export_rooms_with_multiple_sex(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах с несколькими полами студентов в файл XML.
        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms with multiple sexes to file: {output_file}")
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
        root = ET.Element("rooms_with_multiple_sex")
        for room in rooms_data:
            room_element = ET.SubElement(root, "room")
            id_element = ET.SubElement(room_element, "id")
            id_element.text = str(room[0])
            name_element = ET.SubElement(room_element, "name")
            name_element.text = room[1]
        with open(output_file, 'w') as file:
            file.write(self.prettify(root))
            logger.info("Data export completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export data to XML files.")
    parser.add_argument("--export_rooms_with_student_count", action="store_true", help="Export rooms with student count.")
    parser.add_argument("--export_rooms_with_average_age", action="store_true", help="Export rooms with average age.")
    parser.add_argument("--export_rooms_with_age_difference", action="store_true", help="Export rooms with age difference.")
    parser.add_argument("--export_rooms_with_multiple_sex", action="store_true", help="Export rooms with multiple sexes.")

    args = parser.parse_args()

    db_manager = DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    exporter = DataExporterXml(db_manager)

    if args.export_rooms_with_student_count:
        output_file = "output_rooms_with_student_count.xml"
        exporter.export_rooms_with_student_count(output_file)

    if args.export_rooms_with_average_age:
        output_file = "output_rooms_with_average_age.xml"
        exporter.export_rooms_with_average_age(output_file)

    if args.export_rooms_with_age_difference:
        output_file = "output_rooms_with_age_difference.xml"
        exporter.export_rooms_with_age_difference(output_file)

    if args.export_rooms_with_multiple_sex:
        output_file = "output_rooms_with_multiple_sex.xml"
        exporter.export_rooms_with_multiple_sex(output_file)