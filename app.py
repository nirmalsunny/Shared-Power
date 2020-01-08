# Index page of the prototype application
import search
import login
import register
import contact

print('---------- Welcome to Shared Power ----------\n')
print('Choose any option below to continue\n')
print('1. Search Tools\n2. Login\n3. Register\n4. Contact Us\n')
choice = input('Enter your choice: ')
if choice == '1':
    search.init(input('What are you looking for?'))
elif choice == '2':
    login.show_login()
elif choice == '3':
    register.show_reg()
elif choice == '4':
    contact.contact_form()
else:
    print('Wrong Input! Try Again')