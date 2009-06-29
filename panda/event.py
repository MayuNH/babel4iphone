import singleton
import os, sys

class Event(singleton.Singleton):
    
    def initialize(self):
        self.keyMap = {"left": 0, 
                       "right": 0, 
                       "forward": 0, 
                       "cam-left": 0, 
                       "cam-right": 0}
        
        base.accept("escape", sys.exit)
        base.accept("arrow_left", self.setKey, ["left", 1])
        base.accept("arrow_right", self.setKey, ["right", 1])
        base.accept("arrow_up", self.setKey, ["forward", 1])
        base.accept("a", self.setKey, ["cam-left", 1])
        base.accept("s", self.setKey, ["cam-right", 1])
        base.accept("arrow_left-up", self.setKey, ["left", 0])
        base.accept("arrow_right-up", self.setKey, ["right", 0])
        base.accept("arrow_up-up", self.setKey, ["forward", 0])
        base.accept("a-up", self.setKey, ["cam-left", 0])
        base.accept("s-up", self.setKey, ["cam-right", 0])
    
    def setKey(self, key, value):
        self.keyMap[key] = value
