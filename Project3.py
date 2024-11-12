import json
import os
import mysql.connector
from mysql.connector import Error

def login_prompt():
    db_host = input("Enter the database host: ")
    db_name = input("Enter the database name: ")
    db_user = input("Enter the username: ")
    db_password = input("Enter the password: ")

    try:
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )

        if connection.is_connected():
            print("Login successful!")
            list_options(connection)
            connection.close()
        else:
            print("Connection failed. Please check your credentials.")

    except Error as e:
        print(f"Error: {e}")


def list_options(db_connection):
    print("1. Display all the digital displays")
    print("2. Search digital displays given a scheduler system")
    print("3. Insert a new digital display")
    print("4. Delete a digital display")
    print("5. logout")

    user_input = input("Enter choice #: ")

    if user_input.isdigit():
        user_input = int(user_input)

        if user_input <= 0:
            print("Invalid choice. Try again")
            list_options(db_connection)

        if user_input > 5:
            print("Invalid choice. Try again")
            list_options(db_connection)

        option_selection(db_connection, user_input)
    else:
        print("Invalid input. Please try again.\n")
        list_options(db_connection)


def option_selection(db_connection, selected_option):
    if selected_option == 1:
        display_all(db_connection)
    elif selected_option == 2:
        print("2. Search digital displays given a scheduler system")
    elif selected_option == 3:
        print("3. Insert a new digital display")
    elif selected_option == 4:
        print("4. Delete a digital display")
    elif selected_option == 5:
        logout(db_connection)
    else:
        print("Invalid input. Please try again.\n")
        list_options(db_connection)


def display_all(db_connection):
    print("Displaying all digital displays")
    dbCursor = db_connection.cursor()

    dbCursor.execute("SELECT * FROM DigitalDisplay;")

    result = dbCursor.fetchall()

    for row in result:
        print("\t", row)

    print("\n --done-- \n")

    list_options(db_connection)

def logout(db_connection):
    print("Logging out")
    db_connection.close()

if __name__ == "__main__":
    login_prompt()
