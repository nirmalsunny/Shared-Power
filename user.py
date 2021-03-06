# Handles many a function for Logged In User/Owner
import datetime
import re
import database


def days_between(d1, d2):
    return database.select("SELECT DATEDIFF('" + str(d2) + "', '" + str(d1) + "')")[0][0]


# Shows Booking Information and asks whether the User wants to Return the Item

def view(booking_id, tool_id):
    print('View more details about your Booking\n', ('-' * 30))
    item = database.select("SELECT * FROM tools WHERE id = " + str(tool_id))
    # print(item)
    print((item[0][1]), '\nDescription: ', (item[0][2]), '\n', ('-' * 30))
    print('Full Day Rate: $', (item[0][3]), '\nHalf Day Rate: $', (item[0][4]))
    print('Status: ', (item[0][5]))
    booking = database.select("SELECT * FROM bookings WHERE id = " + str(booking_id))
    date = datetime.datetime.now()
    cdate = datetime.date(int(date.year), int(date.month), int(date.day))
    print('Booked On: ', (booking[0][3]))
    datediff = days_between(booking[0][3], cdate)
    if datediff == 0:
        total_charge = item[0][4]
    elif datediff < 4:
        total_charge = datediff * item[0][3]
    else:
        total_charge = 3 * item[0][3]
        total_charge += (datediff - 3) * item[0][3] * 2
    print('Hire Charges: $', total_charge)
    if str.lower(booking[0][4]) == 'collect':
        print('Collection Charge: $0')
    else:
        total_charge += 5
        print('Drop Off Charge: $5')
    print('Total Charge: ', total_charge)
    decision = input('Do you want to return this item?  (y/n)')
    if str.lower(decision) == 'y':
        decision2 = input('Enter mode of return: (Store/Pick-Up)')
        decision3 = input('What is the current condition of the tool? (Good/Damaged)')
        if decision3 == '' or str.lower(decision3) == 'good':
            if decision2 == '' or str.lower(decision2) == 'store':
                sql = "UPDATE bookings SET total = " + str(total_charge) + ", return_condition = 'good' WHERE id = '" \
                      + str(booking[0][0]) + "'"
            else:
                total_charge += 5
                sql = "UPDATE bookings SET total = '" + str(total_charge) + "', return_mode = '" \
                      + decision2 + "', return_condition = 'good' WHERE id = '" + str(booking[0][0]) + "'"
            sql2 = database.insert(
                "UPDATE tools SET status = 'available', t_condition = 'good' WHERE id = '" + str(tool_id) + "'")
        else:
            if decision2 == '' or str.lower(decision2) == 'store':
                sql = "UPDATE bookings SET total = " + str(total_charge) + ", return_condition = '" \
                      + decision3 + "' WHERE id = '" \
                      + str(booking[0][0]) + "'"
            else:
                total_charge += 5
                sql = "UPDATE bookings SET total = '" + str(total_charge) + "', return_mode = '" \
                      + decision2 + "', return_condition = '" + decision3 + "' WHERE id = '" + str(booking[0][0]) + "'"
            sql2 = database.insert(
                "UPDATE tools SET status = 'available', t_condition = '" + decision3 + "' WHERE id = '" + str(
                    tool_id) + "'")

        database.insert(sql)
        database.insert(sql2)
        print('Return Registered\n', ('-' * 30))


# Shows all Bookings made by a User

def view_bookings(username):
    print('View your Bookings\n', ('-' * 30))
    bookings = database.select(
        "SELECT * FROM bookings WHERE username = '" + username + "' AND total = 0 ORDER BY date DESC")

    if bookings:
        booking_count = 1
        for x in bookings:
            item_name = database.select("SELECT name FROM tools WHERE id = '" + str(x[1]) + "'")
            print(str(booking_count) + '. ' + item_name[0][0] + '  -----  ' + str(x[3]) + '  -----  ' + str(x[4]))
            booking_count += 1
        wrong = 1
        while wrong:
            choice = input('Enter any number to view more details: ')
            if str.isdigit(choice):
                if int(choice) < len(bookings) + 1:
                    wrong = 0
                    view(bookings[int(choice) - 1][0], str(x[1]))
                else:
                    print('Invalid Response! Try again with any number shown above')
            else:
                print('Type in a digit! Try again with any number shown above')
    else:
        print('No Bookings Yet!')


# Shows the Invoice

def invoice(username):
    print('View your Invoice\n', ('-' * 30), '\n\n', ('-' * 15), ' Shared Power ', ('-' * 15))
    user = database.select("SELECT * FROM users WHERE username = '" + username + "'")
    date = datetime.datetime.now()
    print('Full Name: ', user[0][3], ' ' * 10, 'Username: ', username)
    print('Invoice Date and Time: ', date)
    print('Invoice Period: 1-' + str(date.month) + '-' + str(date.year) + ' To ' + str(date.day) + "-" + str(date.month)
          + "-" + str(date.year)
          + '\n' + ('-' * 50))

    bookings = database.select("SELECT * FROM bookings WHERE username = '" + username
                               + "' AND NOT total = 0 AND date BETWEEN '" + str(date.year) + "-" + str(date.month)
                               + "-01' AND '" + str(date.year) + "-" + str(date.month)
                               + "-" + str(date.day) + "' ORDER BY date DESC")
    total = 0
    for booking in bookings:
        item = database.select("SELECT * FROM tools WHERE id = " + str(booking[1]))
        print('\nTool Name: ', item[0][1])
        print('Full Day Rate: $', (item[0][3]), '     Half Day Rate: $', (item[0][4]))
        print('Booked On: ', booking[3])
        print('Collection Mode: ', booking[4])
        print('Return Mode: ', booking[5])
        print('Return Condition: ', booking[6])
        print('Total Charge: $', booking[7])
        print('-' * 35)
        total += booking[7]
    print('\nTotal Amount: $' + str(total) + '\nInsurance: $5' + '\nAmount Due for Payment: $' + str(total + 5))


# Validation and Insertion of a new Tool by Owners

def add_tools(username):
    print('Add New Tools\n', ('-' * 40), '\n')
    print('Fill all the information required\n', ('-' * 30))
    wrong = 1
    while wrong:
        if tname():
            wrong = 0
            if description():
                wrong = 0
                if price():
                    wrong = 0
                    if hprice():
                        wrong = 0
                        if a_till():
                            wrong = 0
                            add(username)
                        else:
                            print('Enter a Date in \'YYYY-MM-DD\'')
                            wrong = 1
                    else:
                        print('Enter a Valid Half Day Price')
                        wrong = 1
                else:
                    print('Enter a Valid Price')
                    wrong = 1
            else:
                print('No Description provided! Enter a Description to continue')
                wrong = 1
        else:
            print('No Name provided! Enter your name to continue')


def add(username):
    database.insert("INSERT INTO tools (name, description, price, hprice, availability, username) VALUES ('"
                    + name + "', '" + des + "', '" + pprice + "', '" + phprice + "', '" + atill + "', '" + username + "')")
    print('New Tool Added')


def tname():
    temp = input('Tool Name: ')
    if temp == '':
        return 0
    else:
        global name
        name = temp
        return 1


def description():
    temp = input('Description: ')
    if temp == '':
        return 0
    else:
        global des
        des = temp
        return 1


def price():
    temp = input('Enter the Price:  ')
    if temp.isdigit():
        global pprice
        pprice = temp
        return 1
    else:
        return 0


def hprice():
    temp = input('Enter the Half Day Price:  ')
    if temp.isdigit():
        global phprice
        phprice = temp
        return 1
    else:
        return 0


def a_till():
    temp = input('Available Till: (YYYY-MM-DD)')
    if re.match('([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', temp):
        global atill
        atill = temp
        return 1
    else:
        return 0
