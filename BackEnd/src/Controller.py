import re
import time
from . import Models
from datetime import date
from src import app
from flask import current_app


class Controller(object):
    def __init__(self):
        with app.app_context():
            self.message = current_app.config.get('MESSAGE')


    @property
    def current_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def check_user_valid(self, user):
        if re.search('^\w+$', user):
            return True
        return False

    def register(self, user):
        valid = self.check_user_valid(user)
        if not valid:
            return '账号只能是大小写字母或者数字或者下划线！'

        document = Models.Account.objects(user=user)
        if document and document.count() > 0:
            return '这个账号已经被人注册，请更换。'

        new_user = Models.Account(user=user,
                                  find_phone_status='不需要寻找手机',
                                  alarm_status='启动闹钟',
                                  register_time=self.current_time)
        new_user.save()
        return '添加账号成功！'

    def check_find_phone_status(self, user):
        if self.check_user_valid(user):
            document = Models.Account.objects(user=user)
            if document.count() > 0:
                return document[0].find_phone_status
            else:
                return '账号不存在!'
        return '用户名只能使用大小写英文字母数字和下划线！'

    def set_find_status(self, user, action):
        if self.check_user_valid(user):
            document = Models.Account.objects(user=user)
            if document.count() > 0:
                doc = document[0]
                doc.find_phone_status = self.message[action]
                doc.save()
                if action:
                    self.add_history(user, action)
                return self.message[action]
            else:
                return '账号不存在！'
        return '用户名只能使用大小写英文字母数字和下划线！'

    def check_alarm_status(self, user):
        if self.check_user_valid(user):
            document = Models.Account.objects(user=user)
            if document.count() > 0:
                alarm_date = document[0].alarm_status
                today = str(date.today())
                if alarm_date == today:
                    return self.message['alarm_enable']
                else:
                    return self.message['alarm_disable']
            else:
                return '账号不存在!'
        return '用户名只能使用大小写英文字母数字和下划线！'

    def set_alarm_status(self, user):
        if self.check_user_valid(user):
            document = Models.Account.objects(user=user)
            if document.count() > 0:
                doc = document[0]
                doc.alarm_status = str(date.today())
                doc.save()
                self.add_history(user, 'alarm_enable')
                return self.message['alarm_enable']
            else:
                return '账号不存在!'
        return '用户名只能使用大小写英文字母数字和下划线！'

    def add_history(self, user, action):
        doc = Models.History(user=user, action=action, time=self.current_time,)
        doc.save()
