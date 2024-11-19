import json
import os
import sys
import mysql.connector
from mysql.connector import Error

db_connection = None

def login_prompt():
    global db_connection
    while True:
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
                db_connection = connection
                print("\nLogin successful!\n")
                break
        except Error as e:
            print(f"Error: {e}")
            retry = input("Would you like to retry? (yes/no): ").lower()
            if retry != 'yes':
                sys.exit()

def list_options():
    
    while True:
        print("---------------------------------------------------------")
        print("1. Display all the digital displays")
        print("2. Search digital displays given a scheduler system")
        print("3. Insert a new digital display")
        print("4. Delete a digital display")
        print("5. logout")
        print("---------------------------------------------------------")

        user_input = input("Enter choice #: ")

        if user_input.isdigit():
            user_input = int(user_input)

            if not (1 <= user_input <= 5):
                print("Invalid choice. Try again")
                continue

            option_selection(user_input)
        else:
            print("Invalid input. Please try again.\n")
            continue

def option_selection(selected_option):
    if selected_option == 1:
        display_all()
    elif selected_option == 2:
        scheduler_search()
    elif selected_option == 3:
        print("3. Insert a new digital display")
        insert_display()
    elif selected_option == 4:
        print("4. Delete a digital display")
        delete_display()
    elif selected_option == 5:
        logout()
    else:
        print("Invalid input. Please try again.\n")

def display_all():
    print("Displaying all digital displays and their models:")
    dbCursor = db_connection.cursor()

    query = """
    SELECT serialNo, schedulerSystem, DigitalDisplay.modelNo, width, height, weight, depth, screenSize
    FROM DigitalDisplay
    LEFT JOIN Model ON DigitalDisplay.modelNo = Model.modelNo;
    """
    dbCursor.execute(query)
    result = dbCursor.fetchall()

    if not result:
        print("No digital displays found.\n")
        return

    for row in result:
        print(f"SerialNo: {row[0]}, SchedulerSystem: {row[1]}, ModelNo: {row[2]}, "
              f"Width: {row[3]}, Height: {row[4]}, Weight: {row[5]}, Depth: {row[6]}, ScreenSize: {row[7]}")
    print("\n--done--\n")
    
def scheduler_search():
    while True:
        print("\nPlease select a scheduler system (Random, Smart, Virtue). Type 'Exit' to exit.")
        scheduler_type = input().capitalize()

        if scheduler_type in ["Random", "Smart", "Virtue"]:
            dbCursor = db_connection.cursor()
            query = "SELECT * FROM DigitalDisplay WHERE schedulerSystem = %s;"
            dbCursor.execute(query, (scheduler_type,))
            result = dbCursor.fetchall()

            if not result:
                print("No digital displays found for the selected scheduler system.\n")
                return

            for row in result:
                print("\t", row)
            break
        elif scheduler_type.lower() == "exit":
            break
        else:
            print("Invalid input. Valid inputs are: Random, Smart, or Virtue.")
    
def insert_display():

    dbCursor = db_connection.cursor()

    serialNo = input("Input the new display's serial number: ")

    query = "SELECT serialNo FROM DigitalDisplay WHERE serialNo = %s;"
    dbCursor.execute(query, (serialNo,))
    if dbCursor.fetchone():
        print("\nInvalid Input. Serial number already in use.\n")
        return

    scheduler = input("Input the new display's scheduler system (Random, Smart, Virtue): ").capitalize()
    if scheduler not in ["Random", "Smart", "Virtue"]:
        print("Invalid input: please input either Random, Smart, or Virtue.")
        return

    modelNo = input("Input the new display's modelNo: ")

    query = "SELECT modelNo FROM Model WHERE modelNo = %s;"
    dbCursor.execute(query, (modelNo,))
    if not dbCursor.fetchone():
        print("Model not found. Adding new model...")
        width = get_float_input("Enter width: ")
        height = get_float_input("Enter height: ")
        weight = get_float_input("Enter weight: ")
        depth = get_float_input("Enter depth: ")
        screenSize = get_float_input("Enter screen size: ")
        insert_query = """
        INSERT INTO Model(modelNo, width, height, weight, depth, screenSize)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        dbCursor.execute(insert_query, (modelNo, width, height, weight, depth, screenSize))
        db_connection.commit()

    insert_query = """
    INSERT INTO DigitalDisplay(serialNo, schedulerSystem, modelNo)
    VALUES (%s, %s, %s);
    """
    dbCursor.execute(insert_query, (serialNo, scheduler, modelNo))
    db_connection.commit()
    print("Digital display inserted successfully.\n")

def delete_display():
    dbCursor = db_connection.cursor()

    serialNo = input("Enter the serial number of the display to delete: ")

    query = "SELECT modelNo FROM DigitalDisplay WHERE serialNo = %s;"
    dbCursor.execute(query, (serialNo,))
    result = dbCursor.fetchone()
    if not result:
        print("Serial number not found.\n")
        return

    modelNo = result[0]

    delete_query = "DELETE FROM DigitalDisplay WHERE serialNo = %s;"
    dbCursor.execute(delete_query, (serialNo,))
    
    count_query = "SELECT COUNT(*) FROM DigitalDisplay WHERE modelNo = %s;"
    dbCursor.execute(count_query, (modelNo,))
    count = dbCursor.fetchone()[0]
    if count == 0:
        delete_model_query = "DELETE FROM Model WHERE modelNo = %s;"
        dbCursor.execute(delete_model_query, (modelNo,))

    db_connection.commit()
    print("Digital display deleted successfully.\n")
        
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def logout():
    if db_connection.is_connected():
        db_connection.close()
    print("Logging out")
    sys.exit()

if __name__ == "__main__":
    login_prompt()
    list_options()
