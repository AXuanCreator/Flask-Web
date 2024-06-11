import re

from Config import Regex, User


class RuleCheck:
    gender_set = {'男', '女', '男人', '女人', '男性',
                  '女性', '沃尔玛购物袋', '武装直升机', 'man', 'lady'}

    @staticmethod
    def check_username_not_repeat(username: str):
        return User.query.filter_by(username=username).first() is None

    @staticmethod
    def check_username_in_rules(username: str):
        return len(username) <= 80 and re.match(Regex.username_pattern, username) is not None

    @staticmethod
    def check_password_in_rules(password: str):
        return len(password) <= 80 and re.match(Regex.password_pattern, password) is not None

    @staticmethod
    def check_gender_in_rules(gender: str):
        return len(gender) <= 20 and gender.lower() in RuleCheck.gender_set

    @staticmethod
    def check_mail_in_rules(mail: str):
        return len(mail) <= 80 and re.match(Regex.mail_pattern, mail) is not None

    @staticmethod
    def check_mail_not_repeat(mail: str):
        return User.query.filter_by(mail=mail).first() is None
