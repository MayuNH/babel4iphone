import sys; sys.path.insert(0, "..")
import pygegl

class Player(pygegl.gobj.gobj):
    
    i = 0.3
    
    def draw(self):
        self.i += 0.01
        
        self.surface.rotate(0)
        self.surface.colorize(255.0, 255.0, 255.0, 255.0)
        self.surface.scale(self.i)
        
        rect = self.surface.get_rect()
        #rect.x = self.i
        pygegl.draw.rect(rect, [255, 255, 255])
        self.surface.draw()

if __name__ == '__main__':
    sc = pygegl.scene.create("title", [800, 600])
    sc.addObject(Player("mike.png", [300, 300]))
    sc.mainloop(0.08)
