from models import User

def authorized(msg):
    return User.from_telegram_id(msg.from_user.id) is not None

def not_authorized(msg):
    return not authorized(msg)

def everything(msg):
    return True

def callback(data):
    def f(msg):
        print("data", data)
        return msg.text == data
    return f
