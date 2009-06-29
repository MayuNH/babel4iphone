from direct.actor.Actor import Actor

def load(*args, **kwargs):
    return Player(*args, **kwargs)


class Player(Actor):
    
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.reparentTo(render)
        self.setScale(.2)
