import pygegl

class Player(object):
    
    def __init__(self, x = 100, y = 100):
        self.angle = 0.0
        self.alpha = 200.0
        self.scale = 0.75
        self.image = pygegl.surface.load("mike.png")
        [self.x, self.y] = [x, y]
    
    def draw(self):
        self.image.rotate(self.angle)
        self.image.colorize(255.0, 255.0, 255.0, self.alpha)
        self.image.scale(self.scale)
        self.image.draw([self.x, self.y])

def main():
    pygegl.display.init(800, 600)
    pygegl.display.set_caption("provaaaa")
    
    sc = pygegl.scene.create()
    
    sc.addObject(Player())
    sc.addObject(Player(110, 110))
    
    pygegl.display.mainLoop()


if __name__ == "__main__":
    main()
