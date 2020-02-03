from flask import request
from flask_restful import Resource

from bankr.controllers.accounts import get_accounts, get_transactions, search_account, number_of_transactions, \
    get_account_by_balance, seen_transaction, categories
from bankr.tasks.accounts import retrieve_accounts


class Accounts(Resource):
    def get(self):
        retrieve_accounts.delay()
        bank = request.args.get('bank')
        transactions = request.args.get('transactions')
        account = request.args.get('account_search')
        accounts = [account.get_small_data() for account in get_accounts(bank)]
        number = request.args.get('number', 'false') == 'true'
        balance = request.args.get('balance')

        if transactions:
            for account in accounts:
                account['transactions'] = []
                transactions = get_transactions(account['id'])

                for transaction in transactions:
                    account['transactions'].append(transaction)

        if account is not None:
            accounts = [account.get_small_data() for account in search_account(account, bank=bank)]
        if balance is not None:
            accounts = [account.get_small_data() for account in get_account_by_balance(balance, bank=bank)]
        if number:
            for account in accounts:
                account['number of transactions'] = []
                numbers = number_of_transactions(account['id'])

                for number in numbers:
                    account['number of transactions'].append(number)
        return accounts

    def post(self):
        retrieve_accounts.delay()

        bank = request.args.get('bank')
        seen = request.args.get('seen', 'false') == 'true'
        transaction = request.args.get('transaction_id')
        category = request.args.get('category')
        accounts = [account.get_small_data() for account in get_accounts(bank)]

        if seen:
            seen_transaction(transaction)
            accounts = ['seen transaction']
        if category is not None:
            categories(transaction, category)
            accounts = {'transaction_id': transaction, 'category': category}
        return accounts
