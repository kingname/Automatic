from . import app
from . import Controller

controller = Controller.Controller()


@app.route('/')
def index():
    return '找到更多好玩的东西：http://kingname.info'


@app.route('/<user>/register')
def register(user):
    return controller.register(user)


@app.route('/<user>')
def check(user):
    return controller.check_find_phone_status(user)


@app.route('/<user>/find')
def find_phone(user):
    return controller.set_find_status(user, 'find_phone_enable')


@app.route('/<user>/cancel')
def cancel_find(user):
    return controller.set_find_status(user, 'find_phone_disable')


@app.route('/<user>/alarm')
def alarm(user):
    return controller.check_alarm_status(user)


@app.route('/<user>/alarm_set')
def alarm_cancel(user):
    return controller.set_alarm_status(user)
