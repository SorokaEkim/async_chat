from settings import USERS_JSON
from module_for_json import *

class User:

    USERS = []
    @staticmethod
    def get_all_users():
        """Получаем всех пользователей"""
        data = read_json_file(USERS_JSON)
        for user_hash in data:
            new_user = User(user_hash)
            User.USERS.append(new_user)

        return User.USERS

    @staticmethod
    def user_authorization(user_hash: dict):
        """Находим зарегестрированного пользователя"""
        for user in [user for user in User.USERS if user_hash == user.user_hash]:
            return user

    def __init__(self, user_hash: dict):
        self.user_name = user_hash['username']
        self.user_password = user_hash['username']
        self.user_hash = user_hash

    def __str__(self):
        return f"Пользователь: {self.user_name}"

    def add_new_user(self):
        """Добавление нового пользователя в json"""
        data = read_json_file(USERS_JSON)
        if self.user_hash not in data:
            data.append(self.user_hash)
            write_json_file(USERS_JSON, data)
        else:
            return data
