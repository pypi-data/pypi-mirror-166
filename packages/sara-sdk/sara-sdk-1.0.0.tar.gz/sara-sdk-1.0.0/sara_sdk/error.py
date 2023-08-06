class SaraSdkError(Exception):
    pass


class Error(SaraSdkError):

    def __init__(self, code, message):
        super(Exception, self).__init__(
            "{code}: {message}".format(code=code, message=message))
        self.code = code
        self.message = message


class InternalServerError(SaraSdkError):

    def __init__(self, message="Internal Server Error"):
        super(Exception, self).__init__(message)


class UnknownError(SaraSdkError):

    def __init__(self, message):
        super(Exception, self).__init__(
            "Unkown exception encountered: {}".format(message))


class AuthorizationError(SaraSdkError):

    def __init__(self, message="Session not auth, try using sara_sdk.auth(access_key, secret_key) before calling functions"):
        super(Exception, self).__init__(message)


class InvalidSignatureError(SaraSdkError):
    pass
