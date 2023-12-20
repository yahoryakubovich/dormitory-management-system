# Dormitory Management System

This project is a Dormitory Management System that enables you to load data from JSON files into a database and export
data in JSON or XML format.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yahoryakubovich/dormitory-management-system.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your database credentials in `config.py`:**

```python
DB_NAME = 'your_database_name'
DB_USER = 'your_database_user'
DB_PASSWORD = 'your_database_password'
DB_HOST = 'your_database_host'
DB_PORT = 'your_database_port'
```

## Usage

### Data Loader

Load data from JSON files to the database:

```bash
python data_loader.py /path/to/rooms.json /path/to/students.json
```

### Data Exporter

Export data from the database to JSON and XML files:

```bash
python main.py json
```

```bash
python main.py xml
```

## License

MIT License

Copyright (c) 2023 [GitHub Yahor Yakubovich](https://github.com/yahoryakubovich)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

