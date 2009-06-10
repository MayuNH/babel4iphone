import sys; sys.path.insert(0, "..")
import pygegl

x = 150
y = 200
pos = [x, y]

class Player(pygegl.gobj.gobj):
    
    def __init__(self, *args):
         pygegl.gobj.gobj.__init__(self, *args)
    
    def draw(self):
        scale = 0.6
        self.image.rotate(0)
        self.image.colorize(255.0, 255.0, 255.0, 255.0)
        self.image.scale(scale)
        
        #x = 150
        #y = 200
        #pos = [x, y]
        
        size = [pos[0] + self.image.center[0], 
                self.image.win_size[1] - pos[1] - self.image.center[1],
                self.image.get_width(), 
                self.image.get_height()]
        size = [x + self.image.get_width() / 2, 
                y  + self.image.get_height() / 2, 
                self.image.get_width(), 
                self.image.get_height()]
        #print size
        pygegl.draw.rect(size, [255, 255, 255])
        self.image.draw(pos)


if __name__ == '__main__':
    sc = pygegl.scene.create("title", [800, 600])
    sc.addObject(Player("prova.png", pos))
    sc.mainloop(0.08)
