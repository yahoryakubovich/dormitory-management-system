import json
from typing import Any, List

from psycopg2 import sql


class DataExporterJson:
    def __init__(self, connection) -> None:
        self.connection = connection

    def export_rooms_to_json(self, table_name: str, file_path: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        self._export_rooms_to_json(file_path, data)

    def export_students_to_json(self, table_name: str, file_path: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        self._export_students_to_json(file_path, data)

    def _export_rooms_to_json(self, file_path: str, data: List[Any]) -> None:
        formatted_data = [{"id": row[0], "name": row[1]} for row in data]
        with open(file_path, 'w') as file:
            json.dump(formatted_data, file, indent=2)

    def _export_students_to_json(self, file_path: str, data: List[Any]) -> None:
        formatted_data = []
        for row in data:
            formatted_row = {
                "id": row[0],
                "name": row[1],
                "birthday": str(row[2]),
                "sex": row[3],
                "room": row[4]
            }
            formatted_data.append(formatted_row)

        with open(file_path, 'w') as file:
            json.dump(formatted_data, file, indent=2)
