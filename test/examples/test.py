import sys; sys.path.insert(0, "..")
import pygegl

class Player(pygegl.gobj.gobj):
    
    i = 0.3
    inc = 0
    
    def draw(self):
        self.i += self.inc
        
        #self.surface.rotate(self.i*30)
        #self.surface.colorize(255.0, 255.0, 255.0, 255.0)
        self.surface.scale(self.i)
        
        rect = self.surface.get_rect()
        #rect.x = self.i
        pygegl.draw.rect(rect, [255, 255, 255])
        self.surface.draw()

if __name__ == '__main__':
    sc = pygegl.scene.create("title", [800, 600])
    p = Player("vito.png", [300, 300])
    p.inc = 0.01
    sc.addObject(p)
    sc.addObject(Player("prova.png", [500, 500]))
    sc.mainloop(0.08)
