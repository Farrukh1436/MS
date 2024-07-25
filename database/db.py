import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "../database/database.db")

try:
    conn = sqlite3.connect(db_path)
    print("Opened Database successfully")
except Exception as e:
    print("Error during connection: ", str(e))

# Create a cursor object
cursor = conn.cursor()
#
## Create the table if it doesn't exist
#cursor.execute('''
#    CREATE TABLE IF NOT EXISTS incasators (
#        id INTEGER PRIMARY KEY,
#        Region TEXT,
#        Incasator TEXT,
#        Kiosks_n INTEGER,
#        MEI_n INTEGER,
#        ICT_n INTEGER,
#        NV_n INTEGER,
#        CASHCODE_n INTEGER,
#        CUSTOM1_n INTEGER,
#        CUSTOM2_n INTEGER,
#        MASON_n INTEGER,               
#        Touchscreen_n INTEGER,
#        Display_n INTEGER,
#        DDR3_n INTEGER,
#        Modem_n INTEGER,
#        Simcard_n INTEGER,
#        BA_board_n INTEGER,
#        motherboard_n INTEGER,
#        comport_board_n INTEGER,
#        power_supply_n INTEGER, 
#        paper_n INTEGER
#    )
#''')
#
## Insert data into the table
#cursor.execute('''
#    INSERT INTO incasators (Region, Incasator, Kiosks_n, MEI_n, ICT_n, NV_n, CASHCODE_n, CUSTOM1_n, CUSTOM2_n,
#               MASON_n, Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n,
#               comport_board_n, power_supply_n, paper_n)
#    VALUES ("Toshkent Shahar", "Xolnazar", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
#''')
#conn.commit()
#
## Query the data
#cursor.execute('SELECT id, Region, Incasator, Kiosks_n, MEI_n, ICT_n, NV_n, CASHCODE_n, CUSTOM1_n, CUSTOM2_n,'
#               'MASON_n, Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n,'
#               'comport_board_n, power_supply_n, paper_n FROM incasators')
#rows = cursor.fetchall()
#
## Print the content of the table
#for row in rows:
#    id, Region, Incasator, Kiosks_n, MEI_n, ICT_n, NV_n, CASHCODE_n, CUSTOM1_n, CUSTOM2_n, MASON_n, Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n, comport_board_n, power_supply_n, paper_n = row
#    print(f"id: {id}, Region: {Region}, Incasator: {Incasator}, Kiosks_number: {Kiosks_n},"
#          f" MEI_n: {MEI_n}, ICT_n: {ICT_n}, NV_n: {NV_n}, CASHCODE_n: {CASHCODE_n},"
#          f" CUSTOM1_n: {CUSTOM1_n}, CUSTOM2_n: {CUSTOM2_n}, MASON_n: {MASON_n},"
#          f" Touchscreen_n: {Touchscreen_n}, Display_n: {Display_n}, DDR3_n: {DDR3_n},"
#          f" Modem_n: {Modem_n}, Simcard_n: {Simcard_n}, BA_board_n: {BA_board_n},"
#          f" motherboard_n: {motherboard_n}, comport_board_n: {comport_board_n},"
#          f" power_supply_n: {power_supply_n}, paper_n: {paper_n}")
#
#Create the table if it doesn't exist
# Establish a database connection

# Step 1: Create a new table with the desired column names
# Empty the content of the table
# Empty the content of the table
#cursor.execute('DELETE FROM incasators')
#
## Commit the changes
#conn.commit()
#
## Close the current connection
#conn.close()
#
## Get the database path
#script_dir = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(script_dir, "../database/database.db")
#
## Reconnect to the database
#try:
#    conn = sqlite3.connect(db_path)
#    print("Opened Database successfully")
#    cursor = conn.cursor()  # Create a new cursor object
#except Exception as e:
#    print("Error during connection: ", str(e))
#
## Reset the auto-increment counter
#cursor.execute('VACUUM')
#
## Commit the changes and close the connection
#conn.commit()

def list_tables_and_columns(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve the names of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        
        # Retrieve the columns of the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for column in columns:
            column_id, column_name, column_type, not_null, default_value, primary_key = column
            print(f"  Column: {column_name}, Type: {column_type}, Not Null: {not_null}, Default: {default_value}, Primary Key: {primary_key}")
    
    # Close the connection
    conn.close()
def delete_table(db_path, table_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the SQL command to drop the table
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Commit the changes
        conn.commit()
        print(f"Table '{table_name}' has been deleted successfully.")
    
    except sqlite3.Error as error:
        print(f"Error occurred while deleting the table: {error}")
    
    finally:
        # Close the connection
        if conn:
            conn.close()
def add_columns(db_path, table_name, columns):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add each column to the table
        for column_name, column_type in columns.items():
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        
        # Commit the changes
        conn.commit()
        print(f"Columns have been added to the table '{table_name}' successfully.")
    
    except sqlite3.Error as error:
        print(f"Error occurred while adding the columns: {error}")
    
    finally:
        # Close the connection
        if conn:
            conn.close()


#cursor.execute('''
#    CREATE TABLE IF NOT EXISTS others (
#               id INTEGER PRIMARY KEY,
#               Touchscreen_n INTEGER,
#               Display_n INTEGER,
#               DDR3_n INTEGER,
#               Modem_n INTEGER,
#               Simcard_n INTEGER,
#               BA_board_n INTEGER,
#               motherboard_n INTEGER,
#               comport_board_n INTEGER,
#               power_supply_n INTEGER, 
#               paper_n INTEGER)
#''')
#cursor.execute('''
#    INSERT INTO others (Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n,
#               comport_board_n, power_supply_n, paper_n)
#    VALUES ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
#''')
#cursor.execute('SELECT id,  Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n,'
#               'comport_board_n, power_supply_n, paper_n FROM others')
#rows = cursor.fetchall()
#
## Print the content of the table
#for row in rows:
#    id, Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n, comport_board_n, power_supply_n, paper_n = row
#    print(f"id: {id},"
#          f" Touchscreen_n: {Touchscreen_n}, Display_n: {Display_n}, DDR3_n: {DDR3_n},"
#          f" Modem_n: {Modem_n}, Simcard_n: {Simcard_n}, BA_board_n: {BA_board_n},"
#          f" motherboard_n: {motherboard_n}, comport_board_n: {comport_board_n},"
#          f" power_supply_n: {power_supply_n}, paper_n: {paper_n}")


#delete_table(db_path, "kioks")
table_name = 'storage'
columns = {
    'Touchscreen_n': 'INTEGER',
    'Display_n': 'INTEGER',
    'DDR3_n': 'INTEGER',
    'Modem_n': 'INTEGER',
    'Simcard_n': 'INTEGER',
    'BA_board_n': 'INTEGER',
    'Motherboard_n': 'INTEGER',
    'Comport_board_n': 'INTEGER',
    'Power_supply_n': 'INTEGER',
    'Paper_n': 'INTEGER'
}

add_columns(db_path, table_name, columns)
list_tables_and_columns(db_path)
conn.close()