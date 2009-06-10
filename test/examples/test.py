import sys; sys.path.insert(0, "..")
import pygegl

class Player(pygegl.gobj.gobj):
    
    def draw(self):
        self.image.rotate(0)
        self.image.colorize(255.0, 255.0, 255.0, 255.0)
        self.image.scale(0.3)
        
        size = [self.rect.x, 
                self.rect.y, 
                self.rect.w, 
                self.rect.h]
        
        pygegl.draw.rect(size, [255, 255, 255])
        self.image.draw()


if __name__ == '__main__':
    sc = pygegl.scene.create("title", [800, 600])
    sc.addObject(Player("prova.png", [300, 300]))
    sc.mainloop(0.08)
