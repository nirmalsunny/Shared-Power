import database


def view_bookings(username):
    print('View your Bookings\n', ('-' * 30))
    bookings = database.select("SELECT * FROM bookings WHERE username = '" + username + "' ORDER BY date DESC")

    for x in bookings:
        print(x)

def invoice():
    print()