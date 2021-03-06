# Handles Login Authentication

import database
import search
import user


def is_logged_in():
    username = database.select("SELECT username FROM users WHERE status = 'active'")
    if username:
        return username
    else:
        return 0


def is_supplier(username):
    usertype = database.select("SELECT is_supplier FROM users WHERE username = '" + username + "'")
    if usertype[0][0] == 'y':
        return 1
    else:
        return 0


# This is shown when User is not Logged In

def show_login():
    print('Enter your Credentials below')
    username = input('Username: ')
    password = input('Password: ')
    print('-' * 30)
    print('Trying to log you in...')

    # validation
    sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    if database.select(sql):
        database.insert("UPDATE users SET status='active' WHERE username= '" + username + "'")
        print('Login Successful')
        print('-' * 30)
        logged_user(username)
    else:
        print('Incorrect Information! Try Again')
        show_login()

    # options available for logged in customers


# Shows Appropriate Menu Items according to User Type

def logged_user(username):
    print('Welcome, ' + username)
    print('Choose any option below to continue\n')
    if is_supplier(username):
        print('1. Book Tools\n2. Add Tools\n3. View Bookings\n4. Invoices\n5. Logout\n')
    else:
        print('1. Book Tools\n2. View Bookings\n3. Invoices\n4. Logout\n')
    choice = input('Enter your choice: ')
    if is_supplier(username):
        if choice == '1':
            search.init(input('What are you looking for?'))
        elif choice == '2':
            user.add_tools(username)
        elif choice == '3':
            user.view_bookings(username)
        elif choice == '4':
            user.invoice(username)
        elif choice == '5':
            logout()
        else:
            print('Wrong Input! Try Again')
    else:
        if choice == '1':
            search.init(input('What are you looking for?'))
        elif choice == '2':
            user.view_bookings(username)
        elif choice == '3':
            user.invoice(username)
        elif choice == '4':
            logout()
        else:
            print('Wrong Input! Try Again')


def logout():
    database.insert("UPDATE users SET status='inactive' WHERE status = 'active'")
    print('Successfully logged out')
