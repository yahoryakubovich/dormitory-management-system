import argparse

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from data_exporter_json import DataExporterJson
from data_exporter_xml import DataExporterXml
from database_manager import DatabaseManager


def main():
    """
    Основная функция скрипта для экспорта данных из базы данных в различные форматы.

    Использует argparse для обработки командной строки, а также классы DataExporterJson и DataExporterXml
    для экспорта данных в форматах JSON и XML соответственно.

    Command-line Arguments:
        export_format (str): Формат экспорта данных ('json' или 'xml').

    Usage:
        Примеры запуска из командной строки:
        python main.py json
        python main.py xml
    """
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
