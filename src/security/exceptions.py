from social.exceptions import AuthException

class WrongPasswordException(AuthException):
    def __str__(self):
        return 'Invalid password'


class UserExistsException(AuthException):
    def __str__(self):
        return 'User already exists'
