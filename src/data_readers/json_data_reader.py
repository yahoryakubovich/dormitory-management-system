import json
from typing import Any


class JsonDataReader:
    @staticmethod
    def read(file_path: str) -> Any:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
