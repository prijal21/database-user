import sqlite3
import csv

DB_NAME = "users.sqlite3"
FILE_NAME = "sample_users.csv"

INPUT_STRING = """
Enter the options:
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from the TABLE
    5. QUERY user by id from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE users by id
    9. UPDATE user
    10. Press any key to EXIT

    Choose one Option:
"""

# 1
def create_table(conn):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(200) NOT NULL,
            address CHAR(300) NOT NULL,
            city CHAR(200) NOT NULL,
            county CHAR(200) NOT NULL,
            state CHAR(200) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(265) NOT NULL,
            phone2 CHAR(265) NOT NULL,
            email CHAR(300) NOT NULL,
            web text
        );
"""
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    conn.commit()
    print("Table created successfully")

#Function1
def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        # cur = conn.cursor()
        return conn
    except Exception as e:
        print(e)

#Function2
def read_csv():
    users = []

    with open(FILE_NAME, 'r') as f:
        data = csv.reader(f)
    
        for user in data:
            users.append(tuple(user))

    return users[1:] # Skip header row

#Function3
def insert_users(conn, users):
    user_add_query = """
    INSERT INTO users
    (
        first_name, last_name, company_name, address, city, county, state, zip, phone1, phone2, email, web
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
    cur = conn.cursor()
    cur.executemany(user_add_query, users)
    conn.commit()
    print("Data added successfully.")


COLUMNS = (
    "first_name", "last_name", "company_name", "address", "city", "county", "state", "zip", "phone1", "phone2", "email", "web"
)

#Function4
def select_users(conn):
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

#Function5
def select_user_by_id(conn, id):
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users where id = ?", (id,))
    for user in users:
        print(user)
    print("User gets displayed successfully.")

#Function6
def select_specified_users(conn, no_of_users = 0): # no of users = 5
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users")
    for i, user in enumerate(users):
        if no_of_users and no_of_users == i : # 5 == 0.... 5 == 4 , 5 == 5
            break
        print(i, user)

    print(f"Specific {i} no.of users displayed successfully.")

#Function7
def delete_all_users(conn):
    cur = conn.cursor()
    cur.execute("DELETE from users")
    conn.commit()
    print("ALL users deleted successfully")

#Function8
def delete_users_by_id(conn, id = None):
    cur = conn.cursor()
    cur.execute("DELETE FROM users where id = ?", (id,))
    conn.commit()
    print("User deleted successfully.")
    

#Function9
def update_user_by_id(conn, id, *column_name, **new_value):
    cur = conn.cursor()
    users = cur.execute(f"UPDATE users SET {column_name} = ? WHERE id = ?", (new_value, id))
    conn.commit()
    print("User updated successfully.")

# Main Function
def main():
    user_input = input(INPUT_STRING)
    conn = create_connection()
    if user_input == "1":
        create_table(conn)

    elif user_input == "2":
        users = read_csv()
        insert_users(conn, users)

    elif user_input == "3":
        input_data = []
        for column in COLUMNS:
            column_value = input(f"Enter {column}:")
            input_data.append(column_value)
        users = [tuple(input_data)]
    #   users = [input_data] We can also do this, we do tuple to make it immutable.
        insert_users(conn, users) # Add new user and insert the data into the table

    elif user_input == "4":
        select_users(conn)

    elif user_input == "5":
        user_id = input("Enter the user id: ")
        select_user_by_id(conn, user_id)

    elif user_input == "6":
        no_of_users = int(input("Enter the number of users to display: "))
        select_specified_users(conn, no_of_users)
    
    elif user_input == "7":
        delete_all_users(conn)

    elif user_input == "8":
        id = input("Enter the user id to delete: ")
        delete_users_by_id(conn, id)

    elif user_input == "9":
        id = int(input("Enter the user id to update: "))
        column_name = input(f"Make sure the column name are {COLUMNS}. Enter the column name to update:")
        if column_name in COLUMNS:
            new_value = input("Enter the new value to update: ")
            update_user_by_id(conn, id, column_name, new_value)

    else:
        exit("Exiting the program.")
        
       
            
# When you run a Python file directly, __name__ becomes "__main__"
if __name__ == "__main__":
    main()
