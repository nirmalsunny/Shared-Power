import datetime

import database

def days_between(d1, d2):
    return database.select("SELECT DATEDIFF('" + str(d2) +"', '" + str(d1) +"')")[0][0]

def view(booking_id, tool_id):
    print('View more details about your Booking\n', ('-' * 30))
    item = database.select("SELECT * FROM tools WHERE id = " + str(tool_id))
    #print(item)
    print((item[0][1]), '\nDescription: ', (item[0][2]), '\n', ('-' * 30))
    print('Full Day Rate: $', (item[0][3]), '\nHalf Day Rate: $', (item[0][4]))
    print('Status: ', (item[0][5]))
    booking = database.select("SELECT * FROM bookings WHERE id = " + str(booking_id))
    date = datetime.datetime.now()
    cdate = datetime.date(int(date.year), int(date.month), int(date.day))
    print('Booked On: ', (booking[0][3]))
    datediff = days_between(booking[0][3], cdate)
    total_charge = 0
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
                "UPDATE tools SET status = 'available', t_condition = '" + decision3 + "' WHERE id = '" + str(tool_id) + "'")

        database.insert(sql)
        database.insert(sql2)
        print(('Return Registered\n'), ('-' * 30))



def view_bookings(username):
    print('View your Bookings\n', ('-' * 30))
    bookings = database.select("SELECT * FROM bookings WHERE username = '" + username + "' AND total = 0 ORDER BY date DESC")

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
                    #view(bookings[int(choice) - 1][0])
                    view(bookings[int(choice) - 1][0], str(x[1]))
                else:
                    print('Invalid Response! Try again with any number shown above')
            else:
                print('Type in a digit! Try again with any number shown above')
    else:
        print('No Bookings Yet!')

def invoice():
    print()