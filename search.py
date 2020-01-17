# It returns the search results and shows more details about it providing with an option to book
# if the User is logged in.

import datetime
import database
import login


def init(search_term):
    # it should return items somewhat like this\n1. Saw  $25\n2. Cutter  $34
    items = database.select("SELECT * FROM tools WHERE name LIKE '%" +
                            search_term + "%' AND status = 'available' AND t_condition = 'good'")
    if items:
        item_count = 1
        for x in items:
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
    else:
        print('No Results! Do an empty search to view all items')


# It will show more details about any item and will ask whether or not to book it.


def view(_id):
    print('View more details\n', ('-' * 30))
    item = database.select("SELECT * FROM tools WHERE id = " + str(_id))
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
            decision2 = input('Enter mode of collection: (Collect/Drop off)')

            date = datetime.datetime.now()
            bdate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
            if decision2 == '':
                sql = "INSERT INTO bookings (item_id, username, date) VALUES ('" \
                      + str(_id) + "', '" + username + "', '" + bdate + "')"
            else:
                sql = "INSERT INTO bookings (item_id, username, date, mode) VALUES ('" \
                      + str(_id) + "', '" + username + "', '" + bdate + "', '" + decision2 + "')"
            sql2 = database.insert("UPDATE tools SET status = 'hired' WHERE id = '" + str(_id) + "'")
            database.insert(sql)
            database.insert(sql2)
            print('Order Executed\n', ('-' * 30))
        login.logged_user(username)
    else:
        print('Log in to book this item')
