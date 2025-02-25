import sqlite3


# Define DBOperation class to manage all data into the database.
class DBOperations:
    sql_tables = [] # List of strings of table "create" queries
    sql_schema_info = {} # Dictionary of table names and tuples of attributes and their types
    sql_schema_info_query = "SELECT NAME FROM sqlite_master WHERE TYPE ='table'"
    sql_flight_schedule_schema = """CREATE TABLE IF NOT EXISTS flight_schedule (
        flight_id INTEGER NOT NULL,
        flight_date TEXT NOT NULL,
        status TEXT NOT NULL,
        aircraft_id INTEGER NOT NULL,
        pilot_id1 INTEGER NOT NULL,
        pilot_id2 INTEGER,
        pilot_id3 INTEGER,
        pilot_id4 INTEGER,
        PRIMARY KEY (flight_id, flight_date),
        FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
        FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id),
        FOREIGN KEY (pilot_id1) REFERENCES pilot(pilot_id),
        FOREIGN KEY (pilot_id2) REFERENCES pilots(pilot_id),
        FOREIGN KEY (pilot_id3) REFERENCES pilots(pilot_id),
        FOREIGN KEY (pilot_id4) REFERENCES pilots(pilot_id)
        )"""
    sql_flight_info_schema = """CREATE TABLE IF NOT EXISTS flight_details (
        flight_id INTEGER PRIMARY KEY,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        duration INTEGER NOT NULL,
        FOREIGN KEY (flight_id) REFERENCES FlightSchedule(flight_id)
        )"""
    sql_pilots_schema = """CREATE TABLE IF NOT EXISTS pilots (
        pilot_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        flight_hours INTEGER NOT NULL,
        salary INTEGER NOT NULL,
        status TEXT NOT NULL,
        aircraft_id1 INTEGER,
        aircraft_id2 INTEGER,
        aircraft_id3 INTEGER,
        aircraft_id4 INTEGER,
        aircraft_id5 INTEGER,
        FOREIGN KEY (aircraft_id1) REFERENCES Aircraft(aircraft_id),
        FOREIGN KEY (aircraft_id2) REFERENCES Aircraft(aircraft_id),
        FOREIGN KEY (aircraft_id3) REFERENCES Aircraft(aircraft_id),
        FOREIGN KEY (aircraft_id4) REFERENCES Aircraft(aircraft_id),
        FOREIGN KEY (aircraft_id5) REFERENCES Aircraft(aircraft_id)
        )"""
    sql_aircrafts_schema = """CREATE TABLE IF NOT EXISTS aircrafts (
        aircraft_id INTEGER PRIMARY KEY,
        model TEXT NOT NULL,
        status TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        range INTEGER NOT NULL
        )"""
    sql_insert = "" # Set within method as dependent on user Input
    sql_select_all = "" # Set within method as dependent on user Input
    sql_search = ""  # Set within method as dependent on user Input
    sql_update_data = ""  # Set within method as dependent on user Input
    sql_delete_data = "" # Set within method as dependent on user Input
    sql_drop_table = "" # Set within method as dependent on user Input

    # Constructor method to initialise the object
    def __init__(self):
        try:
            self.conn = sqlite3.connect("AirlinesDB.db")
            self.cur = self.conn.cursor()
            self.conn.commit()
        except Exception as e:
            print("Exception Occurred while constructing object:")
            print(e)
        finally:
            self.conn.close()

    # Establish a connection with the local Database
    def get_connection(self):
        self.conn = sqlite3.connect("AirlinesDB.db")
        self.cur = self.conn.cursor()

    # Aggregate tables into a list
    def create_table_schema(self):
        self.sql_tables.append(self.sql_flight_schedule_schema)
        self.sql_tables.append(self.sql_flight_info_schema)
        self.sql_tables.append(self.sql_pilots_schema)
        self.sql_tables.append(self.sql_aircrafts_schema)

    # Create database
    def create_database(self):
        try:
            self.get_connection()
            self.create_table_schema()
            for table in self.sql_tables:
                self.cur.execute(table)
            self.conn.commit()
            print("Database Tables & Logic created successfully")
        except Exception as e:
            print("Exception Occurred while establishing database logic:")
            print(e)
        finally:
            self.conn.close()

    # Method to construct a dictionary of table names and associated attributes
    def set_sql_schema_info(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_schema_info_query)
            tables = self.cur.fetchall()
            for table in tables:
                table_name = table[0]
                self.cur.execute(f"PRAGMA table_info({table_name})")
                columns = self.cur.fetchall()
                column_names = [col[1] for col in columns]
                column_types = [col[2] for col in columns]
                self.sql_schema_info[table_name] = [column_names, column_types]
        except Exception as e:
                print("Exception Occurred while retrieving database schema:")
                print(e)
        finally:
            self.conn.close()

    # Return dictionary with names of tables and associated attributes
    def get_sql_schema_info(self):
        self.set_sql_schema_info()
        return self.sql_schema_info

    # Method to insert data given an entry and a table to insert into
    def insert_data(self, entry, table_choice):
        number_of_attributes = ', '.join(['?' for _ in range(len(entry))])
        self.sql_insert = f"INSERT INTO {table_choice} VALUES ({number_of_attributes})"
        try:
            self.get_connection()
            self.cur.execute(self.sql_insert, entry)
            self.conn.commit()
            print("Data insert successful")
        except sqlite3.IntegrityError:
            print(f"Exception occurred while inserting data: Duplicate Primary Key(s) in {table_choice}!")
        except Exception as e:
            print("Exception occurred while inserting data: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Select and return all entries in a table
    def select_all(self, table_choice):
        self.sql_select_all = "SELECT * FROM "
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all + table_choice)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print("Exception occurred while selecting table: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Select and return entries from a specific table based on specific attributes and filter by specific values
    def search_data(self, table_choice, column_choice, att_value):
        # Add column filters to query
        if column_choice is None:
            columns = "*"
        else:
            columns = ", ".join(column_choice)
        # Add entry filters to query
        if att_value is None:
            where_clause = ""
        else:
            where_clause = " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in att_value.items()])
        self.sql_search = f"SELECT {columns} FROM {table_choice}{where_clause}"
        try:
            self.get_connection()
            self.cur.execute(self.sql_search)
            result = self.cur.fetchall()
            print("Data search successful")
            return result
        except Exception as e:
            print("Exception occurred while searching: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Update entry values of specified attributes filtered by specific keys
    def update_data(self, table_choice, keys, new_att_values):
        set_clause = " , ".join([f"{key} = '{value}'" for key, value in new_att_values.items()])
        where_clause = " AND ".join([f"{key} = '{value}'" for key, value in keys.items()])
        self.sql_update_data = f"UPDATE {table_choice} SET {set_clause} WHERE {where_clause}"
        try:
            self.get_connection()
            self.cur.execute(self.sql_update_data)
            self.conn.commit()
            print("Data update successful")
            return self.search_data(table_choice, new_att_values.keys(),keys)
        except sqlite3.IntegrityError:
            print(f"Exception occurred while inserting data: Duplicate Primary Key(s) in {table_choice}!")
        except Exception as e:
            print("Exception occurred: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Delete specified entries from table of choice
    def delete_data(self, table_choice, keys):
        where_clause = " AND ".join([f"{key} = '{value}'" for key, value in keys.items()])
        self.sql_delete_data = f"DELETE FROM {table_choice} WHERE {where_clause}"
        try:
            self.get_connection()
            self.cur.execute(self.sql_delete_data)
            print("Data deletion successful")
            self.conn.commit()
        except Exception as e:
            print("Exception occurred: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Delete a table of choice
    def drop_table(self, table_choice):
        self.sql_drop_table = f"DROP TABLE IF EXISTS {table_choice}"
        try:
            self.get_connection()
            self.cur.execute(self.sql_drop_table)
            print("Table deletion successful")
            self.conn.commit()
        except Exception as e:
            print("Exception occurred: ", end="")
            print(e)
        finally:
            self.conn.close()

    # Return a summary of pre-defined stats from the Database
    def summary(self):
        stats = {}
        sql_select_delayed_flight = "SELECT count(*) from flight_schedule where status = 'Delayed'"
        sql_select_airplanes = "SELECT count(*) from aircrafts"
        sql_select_flights_with_pilot_id_1 = "SELECT count(*) FROM flight_schedule WHERE pilot_id1 = '1' or pilot_id2 = '1' or pilot_id3 = '1' or pilot_id4 = '1'"
        try:
            self.get_connection()
            # Get number of delayed flights
            self.cur.execute(sql_select_delayed_flight)
            delayed_flights = self.cur.fetchone()[0]
            stats["Delayed Flights"] = delayed_flights
            # Get number of airplanes
            self.cur.execute(sql_select_airplanes)
            number_of_airplanes = self.cur.fetchone()[0]
            stats["Number of Airplanes"] = number_of_airplanes
            # Get flight_ids and flight_dates assigned to pilot with ID = 1
            self.cur.execute(sql_select_flights_with_pilot_id_1)
            flights_assigned_to_pilot_1 = self.cur.fetchone()[0]
            stats["Number of flights assigned to Pilot with ID 1"] = flights_assigned_to_pilot_1
            return stats
        except Exception as e:
            print("Exception occurred during summary generation: ", end="")
            print(e)
        finally:
            self.conn.close()


# The main function will parse arguments.
# These argument will be defined by the users on the console after tables and their structure are created
# The user will select a choice from the menu to interact with the database.

# Method to obtain user's table choice
def prompt_table():
    table_chosen = False
    table_choice = ""
    while not table_chosen:
        print("Choose a table:", end=" ")
        for tables in DB_schema.items():
            print(f"{tables[0]}", end = " ")
        table_choice = input().lower()
        if table_choice in DB_schema:
            table_chosen = True
        else:
            print(f"There is no table named '{table_choice}' in the schema\n")
    return table_choice

# Method to obtain user's attribute choices
def prompt_attributes(table_choice):
    chosen_attributes = {}
    lists_of_atts_and_types = DB_schema[table_choice]
    list_of_atts = lists_of_atts_and_types[0]
    list_of_types = lists_of_atts_and_types[1]
    enter = False
    for columns in DB_schema[table_choice][0]:
        print(f"{columns}", end="   ")
    print('\n')
    while not enter:
        attribute = input("Enter an attribute: ").lower()
        if attribute == ".":
            enter = True
        elif attribute == "*":
            enter = True
            for i in range(len(list_of_atts)):
                chosen_attributes[list_of_atts[i]] = list_of_types[i]
        elif attribute in chosen_attributes:
            print("You have already entered this attribute!")
        elif attribute in list_of_atts: # If the input attribute is in the list of attributes for table_choice
            att_index = list_of_atts.index(attribute)
            chosen_attributes[attribute] = list_of_types[att_index] # Add user chosen attribute to dict of chosen attributes and their corresponding types
        else:
            print("Enter a valid attribute name or (.) to enter or (*) to select all.")
    return chosen_attributes

# Method to prompt user to filter by pre-defined entries
def prompt_filter():
    filter_choice = ''
    acceptable_choice = ['y', 'n']
    while filter_choice not in acceptable_choice:
        filter_choice = input("Would you like to filter rows? (Y/N): ").lower()
    if filter_choice == 'y':
        return True
    else:
        return False

# Method to get attribute : value pairs from user
def prompt_values(table_choice):
    att_value = {}
    attribute_choice = prompt_attributes(table_choice) # Get the users attribute choices and their corresponding types (Dict)
    if attribute_choice is not None:
        for att in attribute_choice.keys():
            value = input(f"Enter a value for {att} ({attribute_choice[att]}): ") # Add values to each attributes
            #if check_values(table_choice, att_value):
            att_value[att] = value # Add Attribute:Value pairs to dictionary
    else:
        att_value = None
    return att_value

# Printer method to print entries
def printer(rows, column_choice, table_choice):
    if column_choice is None: # if column_choice is not user defined (option 2), then assign usual schema attributes
        column_choice = DB_schema[table_choice][0]
    for attribute in column_choice: # Print attribute headers with specified row width for presentation
        print(f"{attribute : <{15}}", end="")
    print("\n")
    if rows is not None:
        for row in rows: # Print entries with specified row width for presentation
            for item in row:
                if item is not None:
                    print(f"{item : <{15}}", end="")
                else:
                    item = " "
                    print(f"{item : <{15}}", end="")
            print("\n")

# Method to print overall Database Schema
def show_schema():
    print("Table Schema:")
    for table_name, table_info in DB_schema.items():
        list_length = len(table_info[0])
        print(f"Table: {table_name}\n       Attributes(Types):", end=" ")
        for i in range(list_length):
            print(f"{table_info[0][i]}({table_info[1][i]})", end =" ")
        print('\n', end ="")

# Method to obtain entry data from user
def insert_data():
    table_choice = prompt_table()
    attributes = DB_schema[table_choice][0]
    entry = []
    for attribute in attributes:
        entry.append (input(f"Enter {attribute}: "))
    db_ops.insert_data(entry, table_choice)

# Method to select and return a table of choice
def select_all(table_choice):
    if table_choice is None:
        table_choice = prompt_table()
    rows = db_ops.select_all(table_choice)
    column_choice = DB_schema[table_choice][0]
    printer(rows, column_choice, table_choice)

# Method to search the database based on pre-defined criteria (attributes and values)
def search_data():
    # Select Table to search
    table_choice = prompt_table()

    # Filter by columns (FROM clause in query)
    print("Which columns(s) would you like to show?,",end = "")
    print(" (one value per line) or Enter a full stop (.) to finalise selection, or (*) to choose all attributes:")
    column_choice = prompt_attributes(table_choice)

    if column_choice is not None:
        column_choice = column_choice.keys()

    # Check if user wants to filter entries by matching values of one or more attributes (WHERE clause in query)
    filter_by_values = prompt_filter()

    att_value = None
    # Get filter values
    if filter_by_values:
        print("Which attribute would you like to filter by? (Keys)", end="")
        print(" (one value per line) or Enter a full stop (.) to finalise selection, or (*) to choose all attributes:")
        att_value = prompt_values(table_choice)

    rows = db_ops.search_data(table_choice, column_choice, att_value)
    printer(rows,column_choice,table_choice)

# Method to update one or more attributes, with the option to filter by entries
def update_data():
    # Choose a table to update values from
    table_choice = prompt_table()

    # Choose one or more attributes to update
    print("Which attribute(s) would you like to update?",end = "")
    print(" (one value per line) or Enter a full stop (.) to finalise selection, or (*) to choose all attributes:")
    new_att_value = prompt_values(table_choice)

    # Choose row to update
    print("What keys would you like to use to find entries to update, and what are their values?",end = "")
    print(" (one value per line) or Enter a full stop (.) to finalise selection, or (*) to choose all attributes:")
    keys = prompt_values(table_choice)

    rows = db_ops.update_data(table_choice, keys, new_att_value)
    if rows is None:
        print("No entries matching the provided keys were found.")
    else:
        print("Updated data successfully")
        print(f"The following values for ", end="")
        for key, value in keys.items():
            print(f"{key} = {value}", end =" ")
        print(f"in {table_choice} have been updated:")
        printer(rows, new_att_value.keys(), table_choice)

# Method to delete entries within the table
def delete_data():
    # Choose a table to delete values from
    table_choice = prompt_table()

    # Choose entry to delete
    print("What are the keys for the entries you want to delete?",end = "")
    print(" (one value per line) or Enter a full stop (.) to finalise selection, or (*) to choose all attributes:")
    keys = prompt_values(table_choice)
    db_ops.delete_data(table_choice, keys)

    print(f"Updated {table_choice} table:")
    select_all(table_choice)

# Method to delete an entire table of choice
def delete_table():
    # Choose a table to delete
    table_choice = prompt_table()

    # Confirm user's choice
    confirm = ''
    acceptable_choice = ['y', 'n']
    while confirm not in acceptable_choice:
        confirm = input(f"Are you sure you want to delete {table_choice}? This action is irreversible! (Y/N)").lower()
    if confirm == 'y':
        db_ops.drop_table(table_choice)

# Method to retrieve pre-defined stats of the Database
def summarise():
    print(f"Database Stats:")
    stats = db_ops.summary()
    if stats is not None:
        for stat in stats:
            print(f"{stat} = {stats[stat]}")

def recreate_database():
    # Create database instance
    db_ops = DBOperations()
    # Create database schema
    db_ops.create_database()

def add_test_data():
    flight_schedules = [
        (1, '01/10/2023', 'On Time', 1, 1, 9, 7, None),
        (2, '02/10/2023', 'Delayed', 2, 2, 3, 6, 7),
        (3, '03/10/2023', 'On Time', 3, 2, None, None, None),
        (4, '04/10/2023', 'Cancelled', 4, 5, None, None, None),
        (5, '05/10/2023', 'On Time', 5, 1, 3, 5, None),
        (6, '06/10/2023', 'Delayed', 6, 10, None , None, None),
        (7, '07/10/2023', 'On Time', 7, 8, None, None, None),
        (8, '08/10/2023', 'On Time', 8, 9, 10, None, None),
        (9, '09/10/2023', 'Cancelled', 9, 4, 6, None, None),
        (10, '10/10/2023', 'Delayed', 10, 10, None, None, None)
    ]

    flight_details = [
        (1, 'JFK', 'LAX', '10:00', 300),
        (2, 'ORD', 'BOS', '14:00', 180),
        (3, 'LHR', 'CDG', '09:30', 90),
        (4, 'DXB', 'SIN', '23:00', 420),
        (5, 'HND', 'ICN', '08:00', 180),
        (6, 'JFK', 'DFW', '13:00', 240),
        (7, 'LAX', 'SFO', '17:00', 60),
        (8, 'BOM', 'DEL', '07:00', 120),
        (9, 'SYD', 'MEL', '06:00', 90),
        (10, 'JFK', 'MIA', '15:30', 180)
    ]

    pilots = [
        (1, 'John', 'Doe', '01/01/1980', 1500, 120000, 'Active', 1, 3, 4, 5, None),
        (2, 'Jane', 'Smith', '05/05/1985', 1200, 110000, 'Active', 2, 3, 4, None, None),
        (3, 'Mike', 'Johnson', '10/10/1975', 2000, 130000, 'Active', 2, 5, 7, None, None),
        (4, 'Emily', 'Jones', '20/12/1988', 1000, 100000, 'Active', 3, 9, 10, None, None),
        (5, 'Sarah', 'Taylor', '15/07/1990', 900, 95000, 'Active', 4, 4, 8, None, None),
        (6, 'David', 'Brown', '25/03/1982', 1800, 125000, 'Active', 2, 3, 9, None, None),
        (7, 'Chris', 'Davis', '30/01/1978', 1700, 127000, 'Active', 2, 1, None, None, None),
        (8, 'Katie', 'Wilson', '12/12/1985', 1100, 112000, 'Active', 7, 2, 9, None, None),
        (9, 'Steve', 'Moore', '05/06/1972', 2200, 140000, 'Active', 8, 10, 4, 1, None),
        (10, 'Anna', 'Taylor', '18/11/1983', 1300, 117000, 'Active', 9, 6, 7, 8, 10),

    ]

    aircrafts = [
        (1, 'Boeing 747', 'Operational', 400, 8000),
        (2, 'Airbus A320', 'Under Maintenance', 180, 6000),
        (3, 'Boeing 737', 'Operational', 200, 7000),
        (4, 'Airbus A380', 'Operational', 500, 15000),
        (5, 'Boeing 777', 'Operational', 300, 9000),
        (6, 'Cessna 172', 'Operational', 4, 800),
        (7, 'Gulfstream G550', 'Operational', 20, 12000),
        (8, 'Embraer E190', 'Under Maintenance', 100, 5000),
        (9, 'Boeing 787', 'Operational', 350, 10000),
        (10, 'Airbus A350', 'Operational', 325, 11000)
    ]

    for entry in flight_schedules:
        db_ops.insert_data(entry, 'flight_schedule')

    for entry in flight_details:
        db_ops.insert_data(entry, 'flight_details')

    for entry in pilots:
        db_ops.insert_data(entry, 'pilots')

    for entry in aircrafts:
        db_ops.insert_data(entry, 'aircrafts')


# Create database instance
db_ops = DBOperations()
# Create database schema
db_ops.create_database()
# Get database schema (Dict of table names and a tuple of its attributes and their types)
DB_schema = db_ops.get_sql_schema_info()

# Main running loop, continues prompting until user exits
while True:
    print("\n Menu:")
    print("**********")
    print(" 1. View Database Schema")
    print(" 2. Insert data")
    print(" 3. Select all data")
    print(" 4. Search the Database")
    print(" 5. Update entry values")
    print(" 6. Delete entries")
    print(" 7. Delete table")
    print(" 8. Show Database Statistics")
    print(" 9. Add Test Data")
    print(" 10. Recreate Database and Schema")
    print(" 0. Exit\n")

    menu_chosen = False
    while menu_chosen is False:
        try:
            __choose_menu = int(input("Enter your choice: "))
            menu_chosen = True
        except Exception as e:
            print("Invalid input. Please enter a valid choice.")
    if __choose_menu == 1:
        show_schema()
    elif __choose_menu == 2:
        insert_data()
    elif __choose_menu == 3:
        select_all(None)
    elif __choose_menu == 4:
        search_data()
    elif __choose_menu == 5:
        update_data()
    elif __choose_menu == 6:
        delete_data()
    elif __choose_menu == 7:
        delete_table()
    elif __choose_menu == 8:
        summarise()
    elif __choose_menu == 9:
        add_test_data()
    elif __choose_menu == 10:
        recreate_database()
    elif __choose_menu == 11:
        exit(0)
    else:
        print("Invalid input. Please enter a valid choice.")