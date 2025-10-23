import pytest


class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1


@pytest.fixture
def set_initial_value():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_set_initial_amount(set_initial_value):
    assert set_initial_value.balance == 0
