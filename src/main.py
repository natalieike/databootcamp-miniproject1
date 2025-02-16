'''Main script to run app'''

from bank.bank_account import BankAccount
from bank.bank_product import BankProduct
from bank.bank_customer import BankCustomer
from bank.bank_employee import BankEmployee
from utils.errors import log_error


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
    # if choice == '1':
    #     create_customer()
    # elif choice == '2':
    #     create_employee()
    # elif choice == '3':
    #     employee_accounts()
    # elif choice == '4':
    #     employee_products()
    # elif choice == '5':
    #     main_menu()
    # else:
    #     print('Invalid choice')
    #     employee_menu()


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
        main_menu()
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
        main_menu()
    else:
        print('Invalid choice')
        customer_products(customer_id)


# Customer Accounts


def view_accounts(customer_id):
    '''View accounts for a customer'''
    accounts = BankAccount.get_all_by_customer_id(customer_id)
    if not accounts:
        print('No accounts found')
        log_error(f'No accounts found for customer ID {customer_id}')
    else:
        for account in accounts:
            print(
                f'Account ID: {account.id} - Type: {account.type} - Balance: {account.balance} - Can Overdraft: {account.can_overdraft}')
    customer_accounts(customer_id)


def create_account(customer_id):
    '''Create an account for a customer'''
    account_type = input('Enter 1 for savings or 2 for checking account: ')
    if account_type != '1' and account_type != '2':
        print('Invalid account type')
        log_error(
            f'Invalid account type: {account_type} for customer ID {customer_id}')
        return customer_accounts(customer_id)

    normalized_account_type = 'savings' if account_type == '1' else 'checking'

    balance = float(input('Enter the starting balance: '))
    can_overdraft = input('Can overdraft? (y/n): ').lower() == 'y'

    account = BankAccount(None, customer_id, normalized_account_type,
                          balance, can_overdraft)
    new_account = account.add_new()
    print(
        f'Account {new_account.id} created with a balance of {new_account.balance}')
    customer_accounts(customer_id)


def deposit(customer_id):
    '''Deposit money into an account'''
    account_id = input('Enter the account ID: ')
    amount = float(input('Enter the amount to deposit: '))

    account_details = BankAccount.get_by_id(account_id)
    account = BankAccount(account_details.id, account_details.customer_id, account_details.type,
                          account_details.balance, account_details.can_overdraft)

    if not account:
        print('Account not found')
        log_error(
            f'Account not found: {account_id} for customer ID {customer_id}')
        return customer_accounts(customer_id)

    account.make_deposit(amount)
    print(f'New balance: {account.balance}')
    customer_accounts(customer_id)


def withdraw(customer_id):
    '''Withdraw money from an account'''
    account_id = input('Enter the account ID: ')
    amount = float(input('Enter the amount to withdraw: '))

    account_details = BankAccount.get_by_id(account_id)
    account = BankAccount(account_details.id, account_details.customer_id, account_details.type,
                          account_details.balance, account_details.can_overdraft)

    if not account:
        print('Account not found')
        log_error(
            f'Account not found: {account_id} for customer ID {customer_id}')
        return customer_accounts(customer_id)

    try:
        account.make_withdrawal(amount)
        print(f'New balance: {account.balance}')
    except ValueError as error:
        print(f'Error withdrawing from account {account_id}: {error}')
        log_error(f'Error withdrawing from account {account_id}: {error}')

    customer_accounts(customer_id)


# Customer Products


def view_products(customer_id):
    '''View products for a customer'''
    products = BankProduct.get_all_by_customer_id(customer_id)
    if not products:
        print('No products found')
        log_error(f'No products found for customer ID {customer_id}')
    else:
        for product in products:
            print(
                f'Product ID: {product.id} - Type: {product.type} - Balance: {product.balance} - Minimum Payment: {product.min_payment}')
    customer_products(customer_id)


def create_product(customer_id):
    '''Create a product for a customer'''
    product_type = input(
        'Enter 1 for credit card or 2 for loan: ')
    if product_type != '1' and product_type != '2':
        print('Invalid product type')
        log_error(
            f'Invalid product type: {product_type} for customer ID {customer_id}')
        return customer_products(customer_id)
    normalized_product_type = 'credit card' if product_type == '1' else 'loan'

    product_balance = 0 if product_type == '1' else float(
        input('Enter the loan amount: '))
    if product_balance < 0:
        print('Invalid loan amount')
        log_error(
            f'Invalid loan amount: {product_balance} for customer ID {customer_id}')
        return customer_products(customer_id)

    product_min_payment = 25 if product_type == '1' else float(
        input('Enter the minimum payment: '))
    if product_min_payment < 0:
        print('Invalid minimum payment')
        log_error(
            f'Invalid minimum payment: {product_min_payment} for customer ID {customer_id}')
        return customer_products(customer_id)

    product = BankProduct(None, customer_id, normalized_product_type,
                          product_balance, product_min_payment)
    new_product = product.add_new()
    print(
        f'Account {new_product.id} created with a balance of {new_product.balance}')
    customer_products(customer_id)


def debit(customer_id):
    '''Debit money from a product'''
    product_id = input('Enter the product ID: ')
    amount = float(input('Enter the amount to debit: '))

    if amount < 0:
        print('Invalid amount')
        log_error(
            f'Invalid amount: {amount} for customer ID {customer_id}')
        return customer_products(customer_id)

    product_details = BankProduct.get_by_id(product_id)
    product = BankProduct(product_details.id, product_details.customer_id, product_details.type,
                          product_details.balance, product_details.min_payment)

    if not product:
        print('Product not found')
        log_error(
            f'Product not found: {product_id} for customer ID {customer_id}')
        return customer_products(customer_id)

    try:
        product.make_debit(amount)
        print(f'New balance: {product.balance}')
    except ValueError as error:
        print(f'Error debiting from product {product_id}: {error}')
        log_error(f'Error debiting from product {product_id}: {error}')

    customer_products(customer_id)


def credit(customer_id):
    '''Credit money to a product'''
    product_id = input('Enter the product ID: ')
    amount = float(input('Enter the amount to credit: '))

    if amount < 0:
        print('Invalid amount')
        log_error(
            f'Invalid amount: {amount} for customer ID {customer_id}')
        return customer_products(customer_id)

    product_details = BankProduct.get_by_id(product_id)
    product = BankProduct(product_details.id, product_details.customer_id, product_details.type,
                          product_details.balance, product_details.min_payment)

    if not product:
        print('Product not found')
        log_error(
            f'Product not found: {product_id} for customer ID {customer_id}')
        return customer_products(customer_id)

    product.make_credit(amount)
    print(f'New balance: {product.balance}')
    customer_products(customer_id)


def make_payment(customer_id):
    '''Credit at least the minimum payment to a product'''
    product_id = input('Enter the product ID: ')
    amount = float(input('Enter the payment amount: '))

    product_details = BankProduct.get_by_id(product_id)
    product = BankProduct(product_details.id, product_details.customer_id, product_details.type,
                          product_details.balance, product_details.min_payment)

    if not product:
        print('Product not found')
        log_error(
            f'Product not found: {product_id} for customer ID {customer_id}')
        return customer_products(customer_id)

    if amount < product.min_payment:
        print('Payment amount is less than the minimum payment')
        log_error(
            f'Payment amount is less than the minimum payment for product ID {product_id} and customer ID {customer_id}')
        return customer_products(customer_id)

    if amount > product.balance:
        print('Payment amount is greater than the balance - you are overpaying')
        log_error(
            f'Payment amount is greater than the balance for product ID {product_id} and customer ID {customer_id}')
        return customer_products(customer_id)
    product.make_credit(amount)
    print(f'New balance: {product.balance}')
    customer_products(customer_id)


# Entry point for app


main_menu()
