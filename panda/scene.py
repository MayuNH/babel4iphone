from pandac.PandaModules import CollisionTraverser, CollisionNode
from pandac.PandaModules import CollisionHandlerQueue, CollisionRay
from pandac.PandaModules import BitMask32, PandaNode, NodePath
from direct.task.Task import Task

import event

def load(you, name):
    return Scene(you, name)


class Scene(object):
    
    def __init__(self, you, name):
        self.you = you
        
        self.model = loader.loadModel(name)      
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 0)
        
        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        
        self.events = event.Event()
        taskMgr.add(self.move, "moveTask")
        
        # Game state variables
        self.isMoving = False
        
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
        
        self.cTrav = CollisionTraverser()
        
        self.youGroundRay = CollisionRay()
        self.youGroundRay.setOrigin(0,0,1000)
        self.youGroundRay.setDirection(0,0,-1)
        self.youGroundCol = CollisionNode('ralphRay')
        self.youGroundCol.addSolid(self.youGroundRay)
        self.youGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.youGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.youGroundColNp = self.you.attachNewNode(self.youGroundCol)
        self.youGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.youGroundColNp, self.youGroundHandler)
        
        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)
        
        # Uncomment this line to see the collision rays
        #self.youGroundColNp.show()
        #self.camGroundColNp.show()
        
        #Uncomment this line to show a visual representation of the 
        #collisions occuring
        #self.cTrav.showCollisions(render)
    
    def init_camera(self):
        # Set up the camera
        base.disableMouse()
        base.camera.setPos(self.you.getX(), self.you.getY() + 10, 2)        
    
    def get_point(self, label_point):
        return self.model.find("**/%s" % label_point).getPos()
    
    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):
        
        # Get the time elapsed since last frame. We need this
        # for framerate-independent movement.
        elapsed = globalClock.getDt()
        
        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.
        
        base.camera.lookAt(self.you)
        if (self.events.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -(elapsed*20))
        if (self.events.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +(elapsed*20))

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.
        
        startpos = self.you.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

        if (self.events.keyMap["left"]!=0):
            self.you.setH(self.you.getH() + elapsed*300)
        if (self.events.keyMap["right"]!=0):
            self.you.setH(self.you.getH() - elapsed*300)
        if (self.events.keyMap["forward"]!=0):
            self.you.setY(self.you, -(elapsed*25))

        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.events.keyMap["forward"]!=0) or (self.events.keyMap["left"]!=0) or (self.events.keyMap["right"]!=0):
            if self.isMoving is False:
                self.you.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.you.stop()
                self.you.pose("walk",5)
                self.isMoving = False

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.you.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

        # Now check for collisions.

        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.youGroundHandler.getNumEntries()):
            entry = self.youGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.you.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.you.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.
        
        entries = []
        for i in range(self.camGroundHandler.getNumEntries()):
            entry = self.camGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
        if (base.camera.getZ() < self.you.getZ() + 2.0):
            base.camera.setZ(self.you.getZ() + 2.0)
            
        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        
        self.floater.setPos(self.you.getPos())
        self.floater.setZ(self.you.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        return Task.cont
    
    def __repr__(self):
        return self.model
