class Event:
    def __init__(self, id, name, start, url):
        self.id = id
        self.name = name
        self.start = start
        self.url = url
    def isFuture(self):
        from datetime import datetime
        if datetime.strptime(self.start, '%Y-%m-%dT%H:%M:%SZ') > datetime.utcnow():
            return True
        else:
            return False

class Contact:
    def __init__(self, number, optins):
        self.number = number
        self.optins = optins
    def is_optin(self, orgid):
        return True if orgid in self.optins else False