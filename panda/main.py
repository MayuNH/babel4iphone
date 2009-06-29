import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

import display, player, scene

class Main(DirectObject):

    def __init__(self):
        
        display.init()
        
        # Set up the environment
        #
        # This environment model contains collision meshes.  If you look
        # in the egg file, you will see the following:
        #
        #    <Collide> { Polyset keep descend }
        #
        # This tag causes the following mesh to be converted to a collision
        # mesh -- a mesh which is optimized for collision, not rendering.
        # It also keeps the original mesh, so there are now two copies ---
        # one optimized for rendering, one for collisions.  
        
        # Create the main character, Ralph
        you = player.load("models/ralph",
                            {"run": "models/ralph-run",
                             "walk": "models/ralph-walk"})
        sc = scene.load(you, "models/world")
        pos = sc.get_point("start_point")
        you.setPos(pos)
        
        sc.init_camera()

if __name__=="__main__":
    m = Main()
    run()
