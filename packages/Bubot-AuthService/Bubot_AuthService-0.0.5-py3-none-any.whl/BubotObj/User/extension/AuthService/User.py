from BubotObj.User.User import User as BaseUser


class User(BaseUser):
    # name = 'User'
    extension = True
    file = __file__

    @property
    def db(self):
        return 'AuthService'
