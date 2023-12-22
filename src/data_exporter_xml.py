import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
from database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExporterXml:
    """
    Класс для экспорта данных из базы данных в формат XML.

    Args:
        db_manager (DatabaseManager): Менеджер базы данных для работы с данными.

    Methods:
        prettify(elem) -> str:
            Возвращает красиво отформатированную XML-строку для элемента.

        export_rooms_data(output_file: str) -> None:
            Экспортирует данные о комнатах в файл XML.

        export_students_data(output_file: str) -> None:
            Экспортирует данные о студентах в файл XML.

        export_data_from_db(output_rooms_file: str, output_students_file: str) -> None:
            Экспортирует данные о комнатах и студентах из базы данных в файлы XML.
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

    def export_rooms_data(self, output_file: str) -> None:
        """
        Экспортирует данные о комнатах в файл XML.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting rooms data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM rooms;")
                rooms_data = cursor.fetchall()

        root = ET.Element("rooms")
        for room in rooms_data:
            room_element = ET.SubElement(root, "room")
            id_element = ET.SubElement(room_element, "id")
            id_element.text = str(room[0])
            name_element = ET.SubElement(room_element, "name")
            name_element.text = room[1]

        with open(output_file, 'w') as file:
            file.write(self.prettify(root))

    def export_students_data(self, output_file: str) -> None:
        """
        Экспортирует данные о студентах в файл XML.

        Args:
            output_file (str): Путь к файлу для сохранения данных.
        """
        logger.info(f"Exporting students data to file: {output_file}")
        with self.db_manager as db:
            with db.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students;")
                students_data = cursor.fetchall()

        root = ET.Element("students")
        for student in students_data:
            student_element = ET.SubElement(root, "student")
            id_element = ET.SubElement(student_element, "id")
            id_element.text = str(student[0])
            name_element = ET.SubElement(student_element, "name")
            name_element.text = student[1]
            birthday_element = ET.SubElement(student_element, "birthday")
            birthday_element.text = student[2].strftime("%Y-%m-%d") if student[2] else ""
            sex_element = ET.SubElement(student_element, "sex")
            sex_element.text = student[3]
            room_element = ET.SubElement(student_element, "room")
            room_element.text = str(student[4])

        with open(output_file, 'w') as file:
            file.write(self.prettify(root))

    def export_data_from_db(self, output_rooms_file: str, output_students_file: str) -> None:
        """
        Экспортирует данные о комнатах и студентах из базы данных в файлы XML.

        Args:
            output_rooms_file (str): Путь к файлу для сохранения данных о комнатах.
            output_students_file (str): Путь к файлу для сохранения данных о студентах.
        """
        logger.info("Exporting data from the database...")
        self.export_rooms_data(output_rooms_file)
        self.export_students_data(output_students_file)
        logger.info("Data export completed.")
