import json
import sqlite3
import unittest
from unittest.mock import MagicMock, patch

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from data_exporter_json import DataExporterJson
from database_manager import DatabaseManager


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
