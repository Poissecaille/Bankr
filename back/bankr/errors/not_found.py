class NotFoundError(Exception):
    def __init__(self, resource, resource_id):
        Exception.__init__(self)
        self.resource = resource
        self.resource_id = resource_id

    def get_dict(self):
        return {"error": f"{self.resource} {self.resource_id} not found"}


class BankNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Bank", resource_id)


class AccountNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Account", resource_id)


class TransactionNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Transaction", resource_id)
