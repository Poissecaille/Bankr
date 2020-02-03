from weboob.capabilities.bank import CapBank
from weboob.core import Weboob

from bankr.core import logger
from bankr.models.account import Account
from bankr.models.bank import Bank
from . import celery
from ..models.transaction import Transaction
from ..models.user import User


@celery.task
def retrieve_accounts():
    w = Weboob()
    w.load_backends(caps=(CapBank,))

    for i in w.load_backends(CapBank).keys():
        Bank.get_or_create(name=i)

    user1 = User.get_or_none(username='foo', password='bar')
    user2 = User.get_or_none(username='pi', password='314159')
    if user1 is None:
        user1 = User.create(username='foo', password='bar')
    if user2 is None:
        user2 = User.create(username='pi', password='314159')

    for bank in Bank.select():
        bank_backend = w.get_backend(bank.name)

        accounts = bank_backend.iter_accounts()

        for account in accounts:
            logger.info(
                f'[Accounts] Retrieving account {account.id} - {account.label} - {account.balance} from {bank.name}')

            db_account = Account.get_or_none(bank=bank, account_id=account.id)
            if db_account is None:
                if Account.select().where(Account.bank == 3):
                    db_account = Account.create(bank=bank, account_id=account.id, user=user2.id, label=account.label,
                                                balance=account.balance)
                else:
                    db_account = Account.create(bank=bank, account_id=account.id, user=user1.id, label=account.label,
                                                balance=account.balance)
            else:
                db_account.label = account.label
                db_account.balance = account.balance
                db_account.save()

            transactions = bank_backend.iter_history(bank)

            for transaction in transactions:
                logger.info(
                    f'[Transactions] Retrieving account {transaction.label} - {transaction.amount} from {bank.name}')
                db_transaction = Transaction.get_or_none(account=db_account, label=transaction.label)
                if db_transaction is None:
                    db_transaction = Transaction.create(account=db_account, label=transaction.label,
                                                        amount=transaction.amount, vu=False)
                else:
                    db_transaction.label = transaction.label
                    db_transaction.amount = transaction.amount
                    db_transaction.save()