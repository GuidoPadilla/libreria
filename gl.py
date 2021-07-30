import struct
import random
from model import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(w):
    return struct.pack('=l', w)

class Render(object):
    def color(self, r, g, b):
        return bytes([int(b*self.color_range), int(g*self.color_range), int(r*self.color_range)])

    def glInit(self):
        self.color_range = 255
        self.current_color_clear = self.color(0,0,0)
        self.current_color = self.color(1, 1, 1)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [self.current_color_clear for x in range(self.width)]
            for y in range(self.width)
        ]

    def glClearColor(self, r, g, b):
        self.current_color_clear = self.color(r, g, b)

    def glViewPort(self, x, y, width, height):
        if x >= 0 and y >= 0 and width >= 0 and height >= 0 and x + width <= self.width and y + height <= self.height:
            self.xvp = x
            self.yvp = y
            self.wvp = width
            self.hvp = height

    def glFinish(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14+40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width*self.height*3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()

    def glColor(self, r, g, b):
        self.current_color = self.color(r, g, b)
    """ def glPoint(self, x, y, color = None):
        self.framebuffer[y][x] = self.current_color or color """
    def glVertex(self, x, y):
        if x >= -1 and x <= 1 and y >= -1 and y <= 1:
            self.framebuffer[int(self.yvp + y * (self.hvp / 2) + self.hvp / 2)][int(self.xvp + x * (self.wvp / 2) + self.wvp / 2)] = self.current_color
            
    def glLine(self, x0, y0, x1, y1):
        x0 = round(x0*self.wvp)
        y0 = round(y0*self.hvp)
        x1 = round(x1*self.wvp)
        y1 = round(y1*self.hvp)
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            dy = abs(y1 - y0)
            dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0
        
        # y = mx + b
        points = []
        for x in range(x0, x1):
            if steep:
                points.append([y/self.wvp, x/self.hvp])
            else:
                points.append([x/self.wvp, y/self.hvp])

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx
        for point in points:
            self.glVertex(*point)
    
    def load(self, filename, translate, scale):
        model = Obj(filename)
        for face in model.faces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = round((v1[0] + translate[0]) * scale[0])/self.wvp
                y1 = round((v1[1] + translate[1]) * scale[1])/self.hvp
                x2 = round((v2[0] + translate[0]) * scale[0])/self.wvp
                y2 = round((v2[1] + translate[1]) * scale[1])/self.hvp
                self.glLine(x1, y1, x2, y2)

r = Render()
r.glInit()
r.glCreateWindow(1920, 1080)
r.glViewPort(0, 0, 1920, 1080)
r.load('./models/dragon.obj',[250,0],[2.5,2.5])
""" r.glLine(-1,-1,1,0)
r.glLine(-1,-1,1,1)
r.glLine(-1,0,1,1)
r.glLine(0,-1,0,1)   """
""" r.current_color = color(255, 255, 255)
r.point(10, 10)
r.point(11, 10)
r.point(10, 11)
r.point(11, 11)
for x in range(1024):
    for y in range(768):
        if random.random() > 0.5:
            r.point(x, y) """
""" r.glVertex(0,0)
r.glVertex(1,1)
r.glVertex(0,1)
r.glVertex(0.2,1)
r.glVertex(0.4,1)
r.glVertex(0.6,1)
r.glVertex(0.8,1)
r.glVertex(1,0.2)
r.glVertex(1,0.4)
r.glVertex(1,0.6)
r.glVertex(1,0.8)
r.glColor(0, 0, 1)
r.glVertex(-1,1)
r.glVertex(-1,0)
r.glVertex(-0.2,1)
r.glVertex(-0.4,1)
r.glVertex(-0.6,1)
r.glVertex(-0.8,1)
r.glVertex(-1,0.2)
r.glVertex(-1,0.4)
r.glVertex(-1,0.6)
r.glVertex(-1,0.8)
r.glColor(0, 1, 0)
r.glVertex(1,-1)
r.glVertex(0,-1)
r.glVertex(1,-0.2)
r.glVertex(1,-0.4)
r.glVertex(1,-0.6)
r.glVertex(1,-0.8)
r.glVertex(0.2,-1)
r.glVertex(0.4,-1)
r.glVertex(0.6,-1)
r.glVertex(0.8,-1)
r.glColor(1, 0, 0)
r.glVertex(-1,-1)
r.glVertex(1,0)
r.glVertex(-0.2,-1)
r.glVertex(-0.4,-1)
r.glVertex(-0.6,-1)
r.glVertex(-0.8,-1)
r.glVertex(-1,-0.2)
r.glVertex(-1,-0.4)
r.glVertex(-1,-0.6)
r.glVertex(-1,-0.8) """
""" r.glClearColor(1,0,0)
r.glClear() """
r.glFinish('a.bmp')