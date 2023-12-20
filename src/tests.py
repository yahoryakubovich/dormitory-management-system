import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch

from src.data_exporters.data_exporter_json import DataExporterJson
from src.data_exporters.data_exporter_xml import DataExporterXml
from src.data_readers.json_data_reader import JsonDataReader
from src.database.database_connector import DatabaseConnector


class TestJsonDataReader(unittest.TestCase):
    def test_read_valid_json(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write('{"key": "value", "number": 42}')
            temp_file_path = temp_file.name
        reader = JsonDataReader()
        data = reader.read(temp_file_path)
        temp_file.close()
        self.assertEqual(data, {"key": "value", "number": 42})

    def test_read_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write('{"key": "value", "number": 42')
            temp_file_path = temp_file.name
        reader = JsonDataReader()
        temp_file.close()
        with self.assertRaises(json.JSONDecodeError):
            reader.read(temp_file_path)

    def test_read_nonexistent_file(self):
        reader = JsonDataReader()
        with self.assertRaises(FileNotFoundError):
            reader.read('nonexistent_file.json')


class TestDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.fake_host = "fake_host"
        self.fake_port = 5432
        self.fake_database = "fake_db"
        self.fake_user = "fake_user"
        self.fake_password = "fake_password"

        self.db_connector = DatabaseConnector(
            host=self.fake_host,
            port=self.fake_port,
            database=self.fake_database,
            user=self.fake_user,
            password=self.fake_password
        )

        self.mock_connection = MagicMock()
        self.db_connector.connection = self.mock_connection

    @patch('psycopg2.connect')
    def test_connect(self, mock_connect):
        db_connector = DatabaseConnector(
            host="fake_host",
            port="5432",
            database="fake_db",
            user="fake_user",
            password="fake_password"
        )

        db_connector.connect()

        mock_connect.assert_called_once_with(
            host="fake_host",
            port=5432,
            database="fake_db",
            user="fake_user",
            password="fake_password"
        )

    def test_close(self):
        self.db_connector.close()
        self.mock_connection.close.assert_called_once()

    def test_close_no_connection(self):
        self.db_connector.connection = None
        self.db_connector.close()


class DataExporterJsonTest(unittest.TestCase):
    def setUp(self):
        self.mock_connection = MagicMock()
        self.data_exporter = DataExporterJson(self.mock_connection)

    def test_export_rooms_to_json(self):
        fake_data = [(1, 'Room1'), (2, 'Room2')]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = fake_data
        self.mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        self.data_exporter.export_rooms_to_json('fake_table', 'fake_file.json')
        with open('fake_file.json') as file:
            data = json.load(file)
        expected_formatted_data = [{"id": 1, "name": "Room1"}, {"id": 2, "name": "Room2"}]
        self.assertEqual(data, expected_formatted_data)

    def test_export_students_to_json(self):
        fake_data = [(1, 'John', '1990-01-01', 'M', 'Room1'),
                     (2, 'Jane', '1992-05-15', 'F', 'Room2')]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = fake_data
        self.mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        self.data_exporter.export_students_to_json('fake_table', 'fake_file.json')

        with open('fake_file.json') as file:
            data = json.load(file)
        expected_formatted_data = [
            {"id": 1, "name": "John", "birthday": "1990-01-01", "sex": "M", "room": "Room1"},
            {"id": 2, "name": "Jane", "birthday": "1992-05-15", "sex": "F", "room": "Room2"}
        ]
        self.assertEqual(data, expected_formatted_data)


class DataExporterXmlTest(unittest.TestCase):
    def setUp(self):
        self.mock_connection = MagicMock()
        self.data_exporter = DataExporterXml(self.mock_connection)

    def test_export_rooms_to_xml(self):
        fake_data = [(1, 'Room1'), (2, 'Room2')]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = fake_data
        self.mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        self.data_exporter.export_rooms_to_xml('fake_table', 'fake_file.xml')
        root = ET.parse('fake_file.xml').getroot()
        expected_data = [{'id': '1', 'name': 'Room1'}, {'id': '2', 'name': 'Room2'}]
        for i, item in enumerate(root.iter('item')):
            for j, column_name in enumerate(('id', 'name')):
                sub_element = item.find(column_name)
                self.assertEqual(sub_element.text, expected_data[i][column_name])

    def test_export_students_to_xml(self):
        fake_data = [(1, 'John', '1990-01-01', 'M', 'Room1'),
                     (2, 'Jane', '1992-05-15', 'F', 'Room2')]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = fake_data
        self.mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        self.data_exporter.export_students_to_xml('fake_table', 'fake_file.xml')
        root = ET.parse('fake_file.xml').getroot()
        expected_data = [
            {'id': '1', 'name': 'John', 'birthday': '1990-01-01', 'sex': 'M', 'room': 'Room1'},
            {'id': '2', 'name': 'Jane', 'birthday': '1992-05-15', 'sex': 'F', 'room': 'Room2'}
        ]
        for i, item in enumerate(root.iter('item')):
            for j, column_name in enumerate(('id', 'name', 'birthday', 'sex', 'room')):
                sub_element = item.find(column_name)
                self.assertEqual(sub_element.text, expected_data[i][column_name])


if __name__ == '__main__':
    unittest.main()
