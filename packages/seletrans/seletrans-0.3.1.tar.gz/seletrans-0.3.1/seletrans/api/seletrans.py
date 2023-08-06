APIs = {}


def register(name, _class):
    APIs[name.lower()] = _class


def Seletrans(name):
    return APIs[name.lower()]
