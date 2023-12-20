import unittest
import json
import sqlite3
from unittest.mock import patch, MagicMock
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database_manager import DatabaseManager
from data_exporter_json import DataExporterJson


class TestDatabaseManager(unittest.TestCase):
    @patch('database_manager.logging')
    def test_successful_connection(self, mock_logging):
        mock_logging.info = MagicMock()

        dbname = DB_NAME
        user = DB_USER
        password = DB_PASSWORD
        host = DB_HOST
        port = DB_PORT

        with DatabaseManager(dbname, user, password, host, port) as db_manager:
            mock_logging.info.assert_called_with("Successfully connected to the database")
            self.assertIsNotNone(db_manager.conn)




if __name__ == '__main__':
    unittest.main()
