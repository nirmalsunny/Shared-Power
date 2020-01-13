import login
import database


def unique_user(temp):
    user = database.select("SELECT * FROM users WHERE username = '" + temp + "'")
    if user:
        return 0
    else:
        return 1


def register():
    database.insert("INSERT INTO users (username, password, full_name, is_supplier) VALUES ('"
                    + uname + "', '" + passwrd + "', '" + name + "', '" + is_supplier + "')")
    print('Registration Successful')
    login.logged_user(uname)


def fname():
    temp = input('Full Name: ')
    if temp == '':
        return 0
    else:
        global name
        name = temp
        return 1


def username():
    temp = input('Username: ')
    if temp != '' and unique_user(temp):
        global uname
        uname = temp
        return 1
    else:
        return 0


def supplier():
    temp = input('Are you a Supplier? (y/n) ')
    if str.lower(temp) == 'y' or str.lower(temp) == 'n':
        global is_supplier
        is_supplier = temp
        return 1
    else:
        return 0


def password():
    temp = input('Password: ')
    cpass = input('Confirm Password: ')
    if temp != '' and cpass != '':
        if temp == cpass:
            global passwrd
            passwrd = temp
            return 1
    else:
        return 0


def show_reg():
    print('Fill all the information required\n', ('-' * 30))
    wrong = 1
    while wrong:
        if fname():
            wrong = 0
            if username():
                wrong = 0
                if password():
                    wrong = 0
                    if supplier():
                        wrong = 0
                        register()
                    else:
                        print('Enter either y or n')
                        wrong = 1
                else:
                    print('Enter a Password/ Enter the Same Password')
                    wrong = 1
            else:
                print('Invalid or Existing Username!')
                wrong = 1
        else:
            print('No name provided! Enter your name to continue')
