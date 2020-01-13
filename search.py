import datetime

import database
import login


def init(search_term):
    # print('it should return items somewhat like this\n1. Saw  $25\n2. Cutter  $34')
    items = database.select("SELECT * FROM tools WHERE name LIKE '%" + search_term + "%'")
    # print(items)
    item_count = 1
    for x in items:
        # print()
        print(str(item_count) + '. ' + x[1] + '  ---  $' + str(x[3]) + '/$' + str(x[4]))
        item_count += 1
    wrong = 1
    while wrong:
        choice = input('Enter any number to view more details: ')
        if str.isdigit(choice):
            if int(choice) < len(items) + 1:
                wrong = 0
                view(items[int(choice) - 1][0])
            else:
                print('Invalid Response! Try again with any number shown above')
        else:
            print('Type in a digit! Try again with any number shown above')


def view(_id):
    print('View more details\n', ('-' * 30))
    item = database.select("SELECT * FROM tools WHERE id = " + str(_id))
    #print(_id)
    print(item)
    print((item[0][1]), '\nDescription: ', (item[0][2]), '\n', ('-' * 30))
    print('Full Day Rate: $', (item[0][3]), '\nHalf Day Rate: $', (item[0][4]))
    print('Availability: ', (item[0][5]))
    print('Available Till: ', (item[0][6]))
    user = login.is_logged_in()
    if user:
        for x in user:
            username = x[0]
        decision = input('Do you want to book this tool?(y/n)')
        if str.lower(decision) == 'y':
            decision2 = input('Enter mode of collection: (Collect/Pick-up/Drop off)')
            date = datetime.datetime.now()
            bdate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)

            sql = "INSERT INTO bookings (item_id, username, date, mode) VALUES ('" \
                  + str(_id) + "', '" + username + "', '" + bdate + "', '" + decision2 + "') "
            #print(sql)
            database.insert(sql)
            print(('Order Executed\n'), ('-' * 30))
        login.logged_user(username)
    else:
        print('Log in to book this item')