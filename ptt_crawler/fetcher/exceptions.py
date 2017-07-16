class RequestError(Exception):
    def __init__(self, message, res):
        self.response = res
        super(RequestError, self).__init__(message)


class RetryError(Exception):
    def __init__(self, message, retry_count):
        self.retry_count = retry_count
        super(RetryError, self).__init__(message)
