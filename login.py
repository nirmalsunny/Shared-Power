import Database

def show_login():
    print('Enter your Credentials below')
    username = input('Username: ')
    password = input('Password: ')
    print('-' * 30)
    print('Trying to log you in...')

    # validation
    sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    if Database.select(sql):
        logged_user(username)
    else:
        print('Incorrect Information! Try Again')
        show_login()

    # options available for logged in customers
def logged_user(username):
    print('Login Successful')
    print('-' * 30)
    print('Welcome ' + username)