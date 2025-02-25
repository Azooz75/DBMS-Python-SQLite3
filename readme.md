# SQLite3 Database Management System

This project is a Python-based database management system for an imaginary airline.

# Purpose

The motivation behind this project was to practice the use of SQLite3 and Python to create a simple database management 
system, where users can interact with and modify a database via the CLI.
This project was subitted as part of the required coursework for the "Databases and Cloud" module at the University of Bath.

## Features

- Insert, update, delete, and search data within the DB
- View DB schema and pre-defined stats
- Add test data for illustration and testing purposes

## Requirements

- Python 3
- SQLite3

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Azooz75/DBMS-Python-SQLite3.git
    cd DBMS-Python-SQLite3
    ```

2. Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/).

## Usage

Run the `main.py` file to start the application:

```sh
python main.py
```

### Menu Options

1. **View Database Schema**: Displays the schema of the database.
2. **Insert Data**: Prompts the user to insert data into a selected table.
3. **Select All Data**: Displays all data from a selected table.
4. **Search the Database**: Allows the user to search for specific data based on attributes and values.
5. **Update Entry Values**: Updates specific entries in a selected table.
6. **Delete Entries**: Deletes specific entries from a selected table.
7. **Delete Table**: Deletes an entire table from the database.
8. **Show Database Statistics**: Displays predefined statistics from the database.
9. **Add Test Data**: Adds predefined test data to the database.
10. **Recreate Database and Schema**: Recreates the database and its schema.
11. **Exit**: Exits the application.

## Project Structure

- `main.py`: The main script that contains the `DBOperations` class and the menu-driven interface.
- `AirlinesDB.db`: The SQLite database file (created automatically).

## Class and Methods

### DBOperations

- `__init__()`: Initializes the database connection.
- `get_connection()`: Establishes a connection to the database.
- `create_table_schema()`: Aggregates table creation queries.
- `create_database()`: Creates the database schema.
- `set_sql_schema_info()`: Constructs a dictionary of table names and their attributes.
- `get_sql_schema_info()`: Returns the database schema information.
- `insert_data(entry, table_choice)`: Inserts data into a specified table.
- `select_all(table_choice)`: Selects and returns all entries from a specified table.
- `search_data(table_choice, column_choice, att_value)`: Searches for data based on specified attributes and values.
- `update_data(table_choice, keys, new_att_values)`: Updates data in a specified table.
- `delete_data(table_choice, keys)`: Deletes data from a specified table.
- `drop_table(table_choice)`: Deletes a specified table.
- `summary()`: Returns predefined statistics from the database.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Future Work

Future work may include:

1. **Error Handling and Logging**:
   - Improve error and exception handling.

2. **User Authentication**:
   - Introduce user authentication and authorisation.

3. **Data Validation**:
   - Implement data validation to ensure that the data being inserted or updated meets the required criteria.

4. **GUI**:
   - Develop a GUI to make interactions with the database more user-friendly.

5. **Data Export and Import**:
   - Add CSV import and export.

6. **Config Files**:
   - Import database configuration from a config file (such as the schema)

## License

MIT License

Copyright (c) 2024 - Mauz Bakri

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

