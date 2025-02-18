'''Test cases for BankAccount'''

import pytest
from src.bank.bank_account import BankAccount
from src.bank.bank_customer import BankCustomer


class TestBankAccount:
    '''Test cases for BankAccount'''
    test_customer = BankCustomer(None, 'first_name', 'last_name', 'email@test.com',
                                 'street_address', 'city', 'state', 'zip_code')
    test_customer = test_customer.add_new()

    test_account_1 = BankAccount(
        None, test_customer.id, 'checking', 1000, True)
    test_account_1 = test_account_1.add_new()

    test_account_2 = BankAccount(
        None, test_customer.id, 'savings', 2000, False)
    test_account_2 = test_account_2.add_new()

    def test_add_new_no_data(self,):
        '''Test add_new with no data => is not created'''
        with pytest.raises(AttributeError) as excInfo:
            BankAccount.add_new(None)
            assert excInfo.type is AttributeError

    def test_add_new_correct_data(self):
        '''Test add_new with correct data => is created'''
        new_account = BankAccount(
            None, self.test_customer.id, 'checking', 1000, True)
        result = BankAccount.add_new(new_account)
        assert result is not None
        assert result.id > 0
        assert result.customer_id == self.test_customer.id
        assert result.type == 'checking'
        assert result.balance == 1000
        assert result.can_overdraft is True

    def test_get_all(self):
        '''Test get_all => returns all accounts'''
        result = BankAccount.get_all()
        assert len(result) >= 2
        assert any(x.id == self.test_account_1.id for x in result)
        assert any(x.id == self.test_account_2.id for x in result)

    def test_get_all_by_customer_id(self):
        '''Test get_all_by_customer_id => returns all accounts for a customer'''
        result = BankAccount.get_all_by_customer_id(self.test_customer.id)
        assert len(result) >= 2
        assert any(x.id == self.test_account_1.id for x in result)
        assert any(x.id == self.test_account_2.id for x in result)

    def test_get_all_by_customer_id_not_exist(self):
        '''Test get_all_by_customer_id id does not exist => returns empty list'''
        result = BankAccount.get_all_by_customer_id(0)
        assert len(result) == 0

    def test_get_by_id(self):
        '''Test get_by_id => returns an account by ID'''
        result = BankAccount.get_by_id(self.test_account_1.id)
        assert result is not None
        assert result.id == self.test_account_1.id
        assert result.customer_id == self.test_customer.id
        assert result.type == 'checking'
        assert result.balance == 1000
        assert result.can_overdraft is True

    def test_get_by_id_not_exist(self):
        '''Test get_by_id for invalid ID => returns None'''
        result = BankAccount.get_by_id(0)
        assert result is None
