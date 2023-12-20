from typing import Any, Dict, List

from psycopg2 import sql


class DatabaseManager:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_rooms_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms
                 (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)
        self.connection.commit()

    def create_students_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    birthday DATE NOT NULL,
                    sex CHAR(1) NOT NULL,
                    room_id INT REFERENCES rooms(id)
                );
            """)
        self.connection.commit()

    def insert_rooms_data(self, rooms_data: List[Dict[str, Any]]) -> None:
        with self.connection.cursor() as cursor:
            for room in rooms_data:
                cursor.execute(sql.SQL("""
                    INSERT INTO rooms (id, name)
                    VALUES (%s, %s);
                """), (room['id'], room['name']))
        self.connection.commit()

    def insert_students_data(self, students_data: List[Dict[str, Any]]) -> None:
        with self.connection.cursor() as cursor:
            for student in students_data:
                cursor.execute(sql.SQL("""
                    INSERT INTO students 
                    (id, name, birthday, sex, room_id)
                    VALUES 
                    (%s, %s, %s, %s, %s);
                """), (student['id'], student['name'], student['birthday'], student['sex'], student['room']))
        self.connection.commit()
