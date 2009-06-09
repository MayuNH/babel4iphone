import sys; sys.path.insert(0, "..")
import pygegl

class Player(object):
    
    def __init__(self):
        self.angle = 0
        self.alpha = 255.0
        self.scale = 0.75
        self.image = pygegl.surface.load("mike.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [100, 100]
    
    def draw(self):
        self.image.rotate(self.angle)
        self.image.colorize(255.0, 255.0, 255.0, self.alpha)
        self.image.scale(self.scale)
        self.image.draw(self.rect.topleft)


if __name__ == '__main__':
    sc = pygegl.scene.create("title", [800, 600])
    sc.addObject(Player())
    sc.mainloop(0.08)
