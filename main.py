from getpass import getpass
from login import Login
from system import System
from editor import Update,AddMovie
import sys
database_path = ""


def welcome():
    print('*'*100)
    print("* {:^96s} *".format("Movie System"))
    print("*"*100)


def login():
    userid = input("Enter ID: ")
    pwd = getpass("Enter password: ")

    # Try logging in
    log = Login(userid, pwd, database_path)
    success = log.login()
    while not success:
        print("Please select an option: ")
        print("1. Try again")
        print("2. Register as a new user")
        choice = input("Choice :")
        if choice == '1':
            userid = input("Enter ID: ")
            pwd = getpass("Enter password: ")
            log = Login(userid, pwd, database_path)
            success = log.login()
        elif choice == '2':
            userid = input("Enter ID: ")
            name = input("Enter your name: ")
            pwd = getpass("Enter password: ")
            log = Login(userid,pwd, database_path)
            success = log.signup(name)
            if success:
                success = log.login()
    return log


def login_screen():

    # Print the welcome sign
    welcome()

    # Try to login or register the user if the user can't login
    log = login()
    print("Welcome, " + log.name)

    if log.login_type == "c":
        choice = 0
        system_screen = System(log)
        while choice != 5:
            print("Please select from the following:")
            print("1. Start a session.")
            print("2. Search for movies.")
            print("3. End watching a movie.")
            print("4. End the session")
            print("5. Logout")
            choice = int(input("Choice : "))
            if choice == 1:
                system_screen.start_session()
            elif choice == 2:
                system_screen.search_movies()
            elif choice == 3:
                system_screen.end_movie()
            elif choice == 4:
                system_screen.end_session()
            elif choice == 5:
                return
    elif log.login_type == 'e':
        choice = 0
        while choice != 3:
            print("Please select from the following: ")
            print("1. Add a Movie")
            print("2. Update a recommendation")
            print("3. Logout")
            choice = int(input("Choice : "))
            if choice == 1:
                AddMovie(database_path)
            elif choice == 2:
                Update(database_path)
            elif choice == 3:
                return





def invalid():
    print("Invalid Arguments in cli!\nTry again by running in the format \'python3 main.py database-name.db\'")


def main():
    global database_path
    if len(sys.argv) != 2:
        invalid()
        return
    else:
        if '.db' not in sys.argv[1]:
            invalid()
            return
        else:
            database_path = "./" + sys.argv[1]
            while True:
                login_screen()

main()
