import json
import os
import sys
import mysql.connector
from mysql.connector import Error

db_connection = None

def login_prompt():
    global db_connection
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
            print()
            print("Login successful!")
            print()
            
            list_options()
            db_connection.close()
        else:
            print("Connection failed. Please check your credentials.")

    except Error as e:
        print(f"Error: {e}")


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

            if 0 >= user_input > 5:
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
    elif selected_option == 5:
        logout()
    else:
        print("Invalid input. Please try again.\n")


def display_all():
    print("Displaying all digital displays")
    dbCursor = db_connection.cursor()

    dbCursor.execute("SELECT * FROM DigitalDisplay;")

    result = dbCursor.fetchall()

    for row in result:
        print("\t", row)

    print("\n --done-- \n")

    list_options()
    
def scheduler_search():
    while True:
        print()
        print("Please select a scheduler system (Random, Smart, Virtue). Type Exit to exit")
        scheduler_type = input().capitalize()
        
        if (scheduler_type == "Random" or
            scheduler_type == "Smart" or
            scheduler_type == "Virtue"):
            with db_connection.cursor() as dbCursor:
                statement = "SELECT * FROM DigitalDisplay WHERE schedulerSystem = %s;"
                dbCursor.execute(statement, (scheduler_type,))
                result = dbCursor.fetchall()
                for row in result:
                    print("\t", row)
            break

        elif scheduler_type == "Exit" or scheduler_type == "exit":
            break
        else:
            print("Invalid input. Valid inputs are: Random, Smart, or Virtue")
    
def insert_display():

    with db_connection.cursor() as dbCursor:
        print()
        serialNo = input("Input the new display's serial number: ")
        
        if serialNo.isdigit():
            serialNo = int(serialNo)
            dbCursor.execute("SELECT serialNo FROM DigitalDisplay;")
            result = dbCursor.fetchall()
            for x in result:
                if int(x[0]) == serialNo:
                    print("\nInvalid Input. Serial number already in use.\n")
                    return
                    
        else:
            print("\nInvalid input. Please type in an integer.\n")
            return
        
        scheduler = input("Input the new display's scheduler system (Random, Smart, Virtue): ").capitalize()
        if not (scheduler == "Random" or scheduler == "Smart" or scheduler == "Virtue"):
            print("Invalid input: please input either Random, Smart, or Virtue")
            return
        
        modelNo = input("Input the new display's modelNo: ")
        dbCursor.execute("SELECT modelNo FROM Model;")
        result = dbCursor.fetchall()
        for x in result:
            if x[0] == modelNo:
                break
        else:
            print("\nInvalid Input. Model number not in list of valid models.\n")
            return
        
        statement = "insert into DigitalDisplay(serialNo, schedulerSystem, modelNo) values (%s, %s, %s)"
        dbCursor.execute(statement, (serialNo, scheduler, modelNo))
        print("\ndone!\n")
        
        
    

def logout():
    print("Logging out")
    db_connection.close()
    sys.exit()

if __name__ == "__main__":
    login_prompt()
