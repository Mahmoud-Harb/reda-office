from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # create the user profile automatically after creating
    # a User
    def ready(self):
        import users.signals
