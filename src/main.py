import argparse
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database_manager import DatabaseManager
from data_exporter_json import DataExporterJson
from data_exporter_xml import DataExporterXml


def main():
    parser = argparse.ArgumentParser(description='Export data from the database in different formats.')
    parser.add_argument('export_format', choices=['json', 'xml'], help='Export format (json or xml)')

    args = parser.parse_args()

    dbname = DB_NAME
    user = DB_USER
    password = DB_PASSWORD
    host = DB_HOST
    port = DB_PORT

    db_manager = DatabaseManager(dbname, user, password, host, port)

    if args.export_format == 'json':
        json_exporter = DataExporterJson(db_manager)
        json_exporter.export_data_from_db('output_rooms.json', 'output_students.json')
    elif args.export_format == 'xml':
        xml_exporter = DataExporterXml(db_manager)
        xml_exporter.export_data_from_db('output_rooms.xml', 'output_students.xml')


if __name__ == "__main__":
    main()
