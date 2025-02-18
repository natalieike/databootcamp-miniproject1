'''Test cases for BankProduct'''

import pytest
from src.bank.bank_product import BankProduct
from src.bank.bank_customer import BankCustomer


class TestBankProduct:
    '''Test cases for BankProduct'''
    test_customer = BankCustomer(None, 'first_name', 'last_name', 'email@test.com',
                                 'street_address', 'city', 'state', 'zip_code')
    test_customer = test_customer.add_new()

    test_product_1 = BankProduct(
        None, test_customer.id, 'credit card', 50, 25)
    test_product_1 = test_product_1.add_new()

    test_product_2 = BankProduct(
        None, test_customer.id, 'loan', 2000, 150)
    test_product_2 = test_product_2.add_new()

    def test_add_new_no_data(self,):
        '''Test add_new with no data => is not created'''
        with pytest.raises(AttributeError) as excInfo:
            BankProduct.add_new(None)
            assert excInfo.type is AttributeError

    def test_add_new_correct_data(self):
        '''Test add_new with correct data => is created'''
        new_product = BankProduct(
            None, self.test_customer.id, 'credit card', 1000, 50)
        result = BankProduct.add_new(new_product)
        assert result is not None
        assert result.id > 0
        assert result.customer_id == self.test_customer.id
        assert result.type == 'credit card'
        assert result.balance == 1000
        assert result.min_payment == 50

    def test_get_all(self):
        '''Test get_all => returns all products'''
        result = BankProduct.get_all()
        assert len(result) >= 2
        assert any(x.id == self.test_product_1.id for x in result)
        assert any(x.id == self.test_product_2.id for x in result)

    def test_get_all_by_customer_id(self):
        '''Test get_all_by_customer_id => returns all products for a customer'''
        result = BankProduct.get_all_by_customer_id(self.test_customer.id)
        assert len(result) >= 2
        assert any(x.id == self.test_product_1.id for x in result)
        assert any(x.id == self.test_product_2.id for x in result)

    def test_get_all_by_customer_id_not_exist(self):
        '''Test get_all_by_customer_id id does not exist => returns empty list'''
        result = BankProduct.get_all_by_customer_id(0)
        assert len(result) == 0

    def test_get_by_id(self):
        '''Test get_by_id => returns an product by ID'''
        result = BankProduct.get_by_id(self.test_product_1.id)
        assert result is not None
        assert result.id == self.test_product_1.id
        assert result.customer_id == self.test_customer.id
        assert result.type == self.test_product_1.type
        assert result.balance == self.test_product_1.balance
        assert result.min_payment == self.test_product_1.min_payment

    def test_get_by_id_not_exist(self):
        '''Test get_by_id for invalid ID => returns None'''
        result = BankProduct.get_by_id(0)
        assert result is None
