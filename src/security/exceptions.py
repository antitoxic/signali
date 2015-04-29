from social.exceptions import AuthException

class WrongPasswordException(AuthException):
    def __str__(self):
        return 'Invalid password'
