from singleton import Singleton

def create():
    return Scene()


class Scene(Singleton):
    
    def initialize(self):
        self.objects = []
    
    def addObject(self, obj):
        self.objects.append(obj)
    
    def delObject(self, obj):
        self.objects.remove(obj)
