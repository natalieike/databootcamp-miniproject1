'''Main script to run app'''

from bank_account import BankAccount
from bank_product import BankProduct
from bank_customer import BankCustomer
from bank_employee import BankEmployee
from errors import log_error


def main_menu():
    '''Main menu for the bank app'''
    print('1. Customer Menu')
    print('2. Employee Menu')
    print('3. Exit')
    choice = input('Enter a choice: ')
    if choice == '1':
        customer_menu()
    elif choice == '2':
        employee_menu()
    elif choice == '3':
        print('Goodbye!')
    else:
        print('Invalid choice')
        main_menu()


def customer_menu():
    '''Customer menu for the bank app'''
    customer_id = input('Enter your customer ID: ')

    customer = BankCustomer.get_by_id(customer_id)

    if not customer:
        print('Customer not found - employee must create a new customer')
        log_error(f'Customer not found: {customer_id}')
        return main_menu()

    print('1. Bank Accounts')
    print('2. Products')
    print('3. Main Menu')
    print('4. Exit')
    choice = input('Enter a choice: ')
    if choice == '1':
        customer_accounts(customer_id)
    elif choice == '2':
        customer_products(customer_id)
    elif choice == '3':
        main_menu()
    elif choice == '4':
        print('Goodbye!')
    else:
        print('Invalid choice')
        customer_menu()


def employee_menu():
    '''Employee menu for the bank app'''
    employee_id = input('Enter your employee ID: ')

    employee = BankEmployee.get_by_id(employee_id)

    if not employee:
        print('Employee not found - another employee must create a new employee')
        log_error(f'Employee not found: {employee_id}')
        return main_menu()

    print('1. Create Customer')
    print('2. Create Employee')
    print('3. Bank Accounts')
    print('4. Products')
    print('5. Exit')
    choice = input('Enter a choice: ')
    if choice == '1':
        create_customer()
    elif choice == '2':
        create_employee()
    elif choice == '3':
        employee_accounts()
    elif choice == '4':
        employee_products()
    elif choice == '5':
        main_menu()
    else:
        print('Invalid choice')
        employee_menu()


def customer_accounts(customer_id):
    '''Menu for customer accounts'''
    print('1. View Accounts')
    print('2. Create Account')
    print('3. Depost')
    print('4. Withdraw')
    print('5. Exit')
    choice = input('Enter a choice: ')
    if choice == '1':
        view_accounts(customer_id)
    elif choice == '2':
        create_account(customer_id)
    elif choice == '3':
        deposit(customer_id)
    elif choice == '4':
        withdraw(customer_id)
    elif choice == '5':
        customer_menu()
    else:
        print('Invalid choice')
        customer_accounts(customer_id)


def customer_products(customer_id):
    '''Menu for customer products'''
    print('1. View Products')
    print('2. Create Product')
    print('3. Debit')
    print('4. Credit')
    print('5. Make Payment')
    print('6. Exit')
    choice = input('Enter a choice: ')
    if choice == '1':
        view_products(customer_id)
    elif choice == '2':
        create_product(customer_id)
    elif choice == '3':
        debit(customer_id)
    elif choice == '4':
        credit(customer_id)
    elif choice == '5':
        make_payment(customer_id)
    elif choice == '6':
        customer_menu()
    else:
        print('Invalid choice')
        customer_products(customer_id)


def view_accounts(customer_id):
    '''View accounts for a customer'''
    accounts = BankAccount.get_all_by_customer_id(customer_id)
    if not accounts:
        print('No accounts found')
    else:
        for account in accounts:
            print(account)
    customer_accounts(customer_id)


def create_account(customer_id):
    '''Create an account for a customer'''
    account_type = input('Enter 1 for savings or 2 for checking account: ')
    if account_type != '1' and account_type != '2':
        print('Invalid account type')
        return customer_accounts(customer_id)

    normalized_account_type = 'savings' if account_type == '1' else 'checking'

    balance = float(input('Enter the starting balance: '))
    can_overdraft = input('Can overdraft? (y/n): ').lower() == 'y'

    account = BankAccount(None, customer_id, normalized_account_type,
                          balance, can_overdraft)
    account.save()
    print(f'Account {account.id} created with a balance of {account.balance}')
    customer_accounts(customer_id)
