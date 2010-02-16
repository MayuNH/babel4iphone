import time

# Class for callLater, step() need called in main loop

class Reactor(object):
    
    def __init__(self):
        self.__fn = []
    
    def callLater(self, t, fn, *args):
        self.__fn.append((time.time() + t, fn, args))
    
    def step(self):
        if self.__fn:
            fn = self.__fn.pop(0)
            if time.time() >= fn[0]:
                try:
                    fn[1](*fn[2])
                except Exception, e:
                    print "No callable method"
            else:
                self.__fn.append(fn)

reactor = Reactor()
