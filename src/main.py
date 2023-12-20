import argparse
from pathlib import Path

from config import *
from data_exporters.data_exporter_json import DataExporterJson
from data_exporters.data_exporter_xml import DataExporterXml
from data_readers.json_data_reader import JsonDataReader
from database.database_connector import DatabaseConnector
from database.database_manager import DatabaseManager


def process_data(students_file_path, rooms_file_path, output_format):
    # Connect to the database
    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    # Create a DatabaseManager instance
    database_manager = DatabaseManager(db_connector.connection)

    database_manager.create_rooms_table()
    database_manager.create_students_table()

    # Read data from JSON files
    rooms_data = JsonDataReader.read(rooms_file_path)
    students_data = JsonDataReader.read(students_file_path)

    try:
        # Insert data into the database
        database_manager.insert_rooms_data(rooms_data)
        database_manager.insert_students_data(students_data)
    except Exception as e:
        print(f"Error inserting data into the database: {e}"
              f"Perhaps you have already populated the database.")
        db_connector.close()

    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    if output_format == 'json':
        data_exporter_rooms = DataExporterJson(db_connector.connection)
        data_exporter_students = DataExporterJson(db_connector.connection)
        data_exporter_rooms.export_rooms_to_json('rooms', f'exported_data_rooms.{output_format}')
        data_exporter_students.export_rooms_to_json('students', f'exported_data_students.{output_format}')
        print("Exported JSON successfully!")
    elif output_format == 'xml':
        data_exporter_rooms = DataExporterXml(db_connector.connection)
        data_exporter_students = DataExporterXml(db_connector.connection)
        data_exporter_rooms.export_rooms_to_xml('rooms', f'exported_data_rooms.{output_format}')
        data_exporter_students.export_rooms_to_xml('students', f'exported_data_students.{output_format}')
        print("Exported XML successfully")
    else:
        raise ValueError("Invalid output format. Supported formats: 'json' or 'xml'.")

    # Close the database connection
    db_connector.close()


if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Process students and rooms data.')
    parser.add_argument('students', type=Path, help='Path to the students JSON file')
    parser.add_argument('rooms', type=Path, help='Path to the rooms JSON file')
    parser.add_argument('format', choices=['json', 'xml'], help='Output format (json or xml)')

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract values from command-line arguments
    students_file_path = args.students
    rooms_file_path = args.rooms
    output_format = args.format

    # Process data
    process_data(students_file_path, rooms_file_path, output_format)
