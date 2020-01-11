import database

def init(search_term):
    #print('it should return items somewhat like this\n1. Saw  $25\n2. Cutter  $34')
    items = database.select("SELECT * FROM tools WHERE name LIKE '%" + search_term + "%'")
    #print(items)
    item_count = 1
    for x in items:
        #print()
        print(str(item_count) + '. ' + x[1] + '  ---  $' + str(x[3]) + '/$' + str(x[4]))
        item_count += 1
    wrong = 1
    while(wrong):
        choice = input('Enter any number to view more details: ')
        if str.isdigit(choice):
            if int(choice) < len(items)+1:
                wrong = 0
                view(items[int(choice)-1][0])
            else:
                print('Invalid Response! Try again with any number shown above')
        else:
            print('Type in a digit! Try again with any number shown above')


def view(id):
    print('View more details')
    item = database.select("SELECT * FROM tools WHERE id = " + str(id))
    print(id)
    print(item)