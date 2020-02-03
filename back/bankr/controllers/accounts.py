from peewee import fn

from bankr.errors.not_found import BankNotFoundError, AccountNotFoundError, TransactionNotFoundError
from bankr.models.account import Account
from bankr.models.transaction import Transaction
from bankr.models.bank import Bank
from bankr.models.category import Category


def search_bank(bank_name=None):
    bank = Bank.select().where(Bank.name == bank_name)
    return bank


def get_accounts(bank=None):
    accounts = Account.select()
    if bank is not None:
        db_bank = Bank.get_or_none(name=bank)
        if db_bank is None:
            raise BankNotFoundError(bank)

        accounts = accounts.where(Account.bank == db_bank)

    return accounts


def get_transactions(account_id):
    transactions = Transaction.select().where(Transaction.account == account_id)
    result = [transaction.get_small_data() for transaction in transactions]
    return result


def search_account(account_id, bank=None):
    account = Account.select().where(Account.label.contains(account_id))

    if bank is not None:
        bank = Bank.get_or_none(name=bank)
        account = account.where(Account.bank == bank)
    return account


def search_transaction(transaction_amount, bank=None, account_id=None):
    transaction = Transaction.select().where(Transaction.amount.contains(transaction_amount))
    # account = Account.select().where(Account.label.contains(account_id))
    # if bank is not None:
    #     bank = Bank.get_or_none(name=bank)
    #     account = account.where(Account.bank == bank)
    if account_id is not None:
        account_id = Account.get_or_none(name=account_id)
        transaction = transaction.where(Transaction.account == account_id)
    return transaction


def get_account_by_balance(number, bank=None):
    accounts = Account.select().where(Account.balance <= number)

    if bank is not None:
        bank = Bank.get_or_none(name=bank)
        if bank is not None:
            accounts = accounts.where(Account.bank == bank)

    return accounts


def sum_of_balances(user_id):
    sums_of_balances = Account.select(fn.SUM(Account.balance).alias('sum_of_balances')).where(Account.user == user_id)
    for i in sums_of_balances:
        return (i.sum_of_balances)


def seen_transaction(transaction_id=None):
    transaction = Transaction.select()
    if transaction_id is not None:
        transaction = Transaction.get_or_none(id=transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(transaction_id)
        transaction = Transaction.update(seen="seen").where(Transaction.id == transaction_id).execute()
    return transaction


def number_of_transactions(account_id):
    number = Transaction.select(fn.Count(Transaction.id).alias('nb')).where(Transaction.account == account_id)
    result = [i.nb for i in number]
    return result


def categories(transaction_id, category_id):
    transaction = Transaction.select()
    if transaction_id is not None:
        transaction = Transaction.get_or_none(id=transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(transaction_id)

        category = Category.select()
        if category is not None:
            category = Category.get_or_none(id=category_id)
            if category is None:
                Category.create(id=category_id)
        transaction = Transaction.update(category=category).where(Transaction.id == transaction_id.execute())
    print(transaction)
    return transaction


if __name__ == '__main__':
    get_transactions('2')
