#PyGL2D - A 2D library for PyGame and PyOpenGL
#Copyright (C) 2008 - PyMike

from OpenGL.GL import *
from OpenGL.GLU import *

import display

from math import *

def flip_points(points):
    lowest = 0
    highest = 0
    for p in points:
        if p[1] <= lowest:
            lowest = p[1]
        elif p[1] >= highest:
            highest = p[1]
    height = highest - lowest
    new = []
    for p in points:
        new.append([p[0], (highest + p[1]) - height])
    return new

def line(point1, point2, color, width=1, aa=True, alpha=255.0):
    glLineWidth(width)
    if aa:
        glEnable(GL_LINE_SMOOTH)
    glDisable(GL_TEXTURE_2D)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    glBegin(GL_LINE_STRIP)
    offset = display.get_size()[1]
    glVertex3f(point1[0], offset - point1[1], 0)
    glVertex3f(point2[0], offset - point2[1], 0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)

def lines(points, color, width=1, aa=True, closed=0, alpha=255.0):
    glLineWidth(width)
    if aa:
        glEnable(GL_LINE_SMOOTH)
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_LINE_STRIP)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    offset = display.get_size()[1]
    points = flip_points(points)
    for p in points:
        glVertex3f(p[0], offset - p[1], 0)
    if closed:
        glVertex3f(points[0][0], offset - points[0][1], 0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glDisable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)

def polygon(points, color, aa=True, alpha=255.0):
    glDisable(GL_TEXTURE_2D)
    if aa:
        glEnable(GL_POLYGON_SMOOTH)
    glBegin(GL_POLYGON)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    offset = display.get_size()[1]
    points = flip_points(points)
    for p in points:
        glVertex3f(p[0], offset - p[1], 0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glDisable(GL_POLYGON_SMOOTH)
    glEnable(GL_TEXTURE_2D)

def rect(rectstyle, color, width=0, alpha=255.0):
    x, y, w, h = rectstyle
    points = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
    points = flip_points(points)
    offset = display.get_size()[1]
    if not width:
        polygon(points, color, aa=False, alpha=alpha)
    else:
        lines(points, color, width=width, aa=False, alpha=alpha, closed=1)

def circle(pos, radius, color, alpha=255.0):
    glDisable(GL_TEXTURE_2D)
    
    glBegin(GL_POLYGON)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    
    angle = 0.0
    points = []
    offset = display.get_size()[1]
    pos[1] = offset - pos[1]
    while angle <= 2.0*3.14:
        angle += 0.15
        points.append((pos[0] + sin(angle) * radius, 
                       pos[1] + cos(angle) * radius))
    for p in points:
        glVertex2f(*p)
    
    glEnd()
    glColor4f(1.0,1.0,1.0,1.0)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_POLYGON_SMOOTH)
    glEnable(GL_TEXTURE_2D)
