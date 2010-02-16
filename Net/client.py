# Client object

class Client(object):
    
    def __init__(self, s, u, name):
        self.socket = s
        self.uid = u
        self.name = name
