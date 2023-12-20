import xml.etree.ElementTree as ET
from xml.dom import minidom

from psycopg2 import sql


class DataExporterXml:
    def __init__(self, connection) -> None:
        self.connection = connection

    def export_rooms_to_xml(self, table_name, file_path):
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        self._export_rooms_to_xml(file_path, data)

    def export_students_to_xml(self, table_name, file_path):
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        self._export_students_to_xml(file_path, data)

    def _export_rooms_to_xml(self, file_path, data):
        root = ET.Element("data")
        for item in data:
            element = ET.SubElement(root, "item")
            for i, column_name in enumerate(('id', 'name')):
                sub_element = ET.SubElement(element, column_name)
                sub_element.text = str(item[i])

        xml_data = ET.tostring(root, encoding='utf-8', method='xml')
        parsed_xml = minidom.parseString(xml_data)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        with open(file_path, 'w') as file:
            file.write(pretty_xml)

    def _export_students_to_xml(self, file_path, data):
        root = ET.Element("data")
        for row in data:
            element = ET.SubElement(root, "item")
            for i, column_name in enumerate(('id', 'name', 'birthday', 'sex', 'room')):
                sub_element = ET.SubElement(element, column_name)
                sub_element.text = str(row[i])

        xml_data = ET.tostring(root, encoding='utf-8', method='xml')
        parsed_xml = minidom.parseString(xml_data)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        with open(file_path, 'w') as file:
            file.write(pretty_xml)
