from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import Vec4, TextNode

font = loader.loadFont("cmss12")

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text = msg, style = 1, fg = (1, 1, 1, 1), font = font,
                        pos = (-1.3, pos), align = TextNode.ALeft, 
                        scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text = text, style = 1, fg = (1, 1, 1, 1), font = font,
                        pos = (1.3, -0.95), align = TextNode.ARight, 
                        scale = .07)

def init():
    base.win.setClearColor(Vec4(0, 0, 0, 1))
    
    # Post the instructions
    title = addTitle("Panda3D Tutorial: Roaming Ralph")
    inst1 = addInstructions(0.95, "[ESC]: Quit")
    inst2 = addInstructions(0.90, "[Left Arrow]: Rotate Ralph Left")
    inst3 = addInstructions(0.85, "[Right Arrow]: Rotate Ralph Right")
    inst4 = addInstructions(0.80, "[Up Arrow]: Run Ralph Forward")
    inst6 = addInstructions(0.70, "[A]: Rotate Camera Left")
    inst7 = addInstructions(0.65, "[S]: Rotate Camera Right")
