import random
import math
from model import Obj
from lib import bbox, V2, V3, barycentric, norm, cross, sub, dot, length
from math import cos, sin 
import miNumpy

class Render(object):
    def color(self, r, g, b):
        return bytes([int(b*self.color_range), int(g*self.color_range), int(r*self.color_range)])

    def glInit(self):
        self.color_range = 255
        self.current_color_clear = self.color(0,0,0)
        self.current_color = self.color(1, 1, 1)
        self.light = V3(0,0,1)
        self.active_texture = None
        self.active_vertex_array = []

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [self.current_color_clear for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        self.current_color_clear = self.color(r, g, b)

    def glViewPort(self, x, y, width, height):
        if x >= 0 and y >= 0 and width >= 0 and height >= 0 and x + width <= self.width and y + height <= self.height:
            self.xvp = x
            self.yvp = y
            self.wvp = width
            self.hvp = height

    def glColor(self, r, g, b):
        self.current_color = self.color(r, g, b)
    def glPoint(self, x, y, color = None):
        self.framebuffer[y+self.yvp][x+self.xvp] = color or self.current_color
    def glVertex(self, x, y, color = None):
        if x >= -1 and x <= 1 and y >= -1 and y <= 1:
            self.framebuffer[int(self.yvp + y * (self.hvp / 2) + self.hvp / 2)][int(self.xvp + x * (self.wvp / 2) + self.wvp / 2)] = color or self.current_color
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
    def line(self, x0, y0, x1, y1):
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
        x = x0
        cont = 1
        if x0 > x1:
            cont = -1
        while x != x1:
            if steep:
                points.append([y, x])
            else:
                points.append([x, y])

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx
            x = x + cont
        for point in points:
            self.glPoint(*point)
    def shader(self, x, y, maxx, maxy):
        color = [55, 99, 172]
        point = [670, 470]
        if y < 1080 and y > 1080 - 225 - random.randint(0,5):
            color = [21, 29, 48]
        if y < 1080 - 235 + random.randint(0,20) and y > 1080 - 255 - random.randint(0,5):
            color = [31, 47, 73]
        if y < 1080 - 255 + random.randint(0,5) and y > 1080 - 265 - random.randint(0,5):
            color = [24, 39, 62]
        if y < 1080 - 265 + random.randint(0,5) and y > 1080 - 275 - random.randint(0,5): 
            color = [102, 138, 188]
        if y < 1080 - 275 + random.randint(0,5) and y > 1080 - 295 - random.randint(0,5): 
            color = [54,81,124]    
        if y < 1080 - 295 + random.randint(0,10) and y > 1080 - 335 - random.randint(0,15): 
            lista = [[70,99,145], [100,136,186]]
            color = lista[random.randint(0,1)]
        if y < 1080 - 335 + random.randint(0,10) and y > 1080 - 355 - random.randint(0,5): 
            color = [50,83,147]    
        if y < 1080 - 395 + random.randint(0,10) and y > 1080 - 425 - random.randint(0,10): 
            color = [95,156,236]    
        if y < 1080 - 465 + random.randint(0,10) and y > 1080 - 485 - random.randint(0,10): 
            color = [95,156,236]
        if y < 1080 - 485 + random.randint(0,5) and y > 1080 - 495 - random.randint(0,5): 
            color = [54,81,124] 
        if y < 1080 - 515 + random.randint(0,5) and y > 1080 - 535 - random.randint(0,5): 
            color = [180,237,252]
        if y < 1080 - 535 + random.randint(0,5) and y > 1080 - 555 - random.randint(0,5): 
            color = [133,182,254]
        if y < 1080 - 555 + random.randint(0,5) and y > 1080 - 575 - random.randint(0,5): 
            lista = [[107,152,220], [107,152,220], [107,152,220], [82,120,205]]
            color = lista[random.randint(0,3)]
        if y < 1080 - 575 + random.randint(0,10) and y > 1080 - 615 - random.randint(0,10): 
            color = [180,237,252]
        if y < 1080 - 620 + random.randint(0,10) and y > 1080 - 715 - random.randint(0,10): 
            if  (y > 1080 - 685- random.randint(0,10) and y <1080-665+ random.randint(0,10) and x > 1000- random.randint(0,10)) or (y > 1080 - 650- random.randint(0,10) and y <1080-640+ random.randint(0,10) and x > 1100- random.randint(0,10)):
                color = [43,70,119]
            else:
                color = [92,141,218]
        if y < 1080 - 715 + random.randint(0,10) and y > 1080 - 755 - random.randint(0,10): 
            color = [93,151,224]
        if y < 1080 - 755 + random.randint(0,5) and y > 1080 - 775 - random.randint(0,5): 
            color = [70,135,215]
        if y < 1080 - 785 + random.randint(0,5) and y > 1080 - 805 - random.randint(0,5): 
            color = [124,186,240]
        if y < 1080 - 805 + random.randint(0,10) and y > 1080 - 835 - random.randint(0,10): 
            color = [78,112,161]
        if y < 1080 - 865 + random.randint(0,10) and y > 1080 - 875 - random.randint(0,10): 
            color = [104,158,205]
        if y < 1080 - 885 + random.randint(0,10) and y > 1080 - 905 - random.randint(0,10): 
            color = [104,158,205]
        d = math.dist([point[0], point[1]], [x, y]) / 720
        d = 1-d
        color = [c*d for c in color]
        return self.glColor(color[0]/self.color_range,color[1]/self.color_range,color[2]/self.color_range)
    def triangle(self):
        A = next(self.active_vertex_array)
        B = next(self.active_vertex_array)
        C = next(self.active_vertex_array)

        if self.active_texture:
            tA = next(self.active_vertex_array)
            tB = next(self.active_vertex_array)
            tC = next(self.active_vertex_array)

        nA = next(self.active_vertex_array)
        nB = next(self.active_vertex_array)
        nC = next(self.active_vertex_array)

        """ if A.z == None:
            A.z = 0
        if B.z == None:
            B.z = 0
        if C.z == None:
            C.z = 0     """
        bbox_min, bbox_max = bbox(A, B, C)    
        normal = norm(cross(sub(B, A), sub(C, A)))
        intensity = dot(normal, self.light)
        if intensity < 0:
            return
        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:
                    continue
                if self.active_texture:
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u
                color = self.active_shader(
                    self,
                    triangle=(A, B, C),
                    bar=(w, v, u),
                    texture_coords=(tx, ty),
                    varying_normals=(nA, nB, nC)
                )

                z = A.z * w + B.z * v + C.z * u

                if x < 0 or y < 0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.glPoint(x, y, color)
                    self.zbuffer[x][y] = z

    def transform(self, vertex):
        augmented_vertex = [
            vertex.x,
            vertex.y,
            vertex.z,
            1
        ]
        tranformed_vertex = miNumpy.dot(miNumpy.dot(miNumpy.dot(miNumpy.dot(self.Viewport, self.Projection), self.View), self.Model), augmented_vertex)
        tranformed_vertex = [
            (tranformed_vertex[0][0]/tranformed_vertex[3][0]),
            (tranformed_vertex[1][0]/tranformed_vertex[3][0]),
            (tranformed_vertex[2][0]/tranformed_vertex[3][0])
        ]
        
        return V3(*tranformed_vertex)
    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        self.loadModelMatrix(translate, scale, rotate)

        model = Obj(filename)
        vertex_buffer_object = []
        for face in model.vfaces:
            for facepart in face:
                if facepart != [None]:
                    vertex = self.transform(V3(*model.vertices[facepart[0]]))
                    vertex_buffer_object.append(vertex)

            if self.active_texture:
                for facepart in face:
                    if facepart != [None]:
                        tvertex = V3(*model.tvertices[facepart[1]])
                        vertex_buffer_object.append(tvertex)

                for facepart in face:
                    if facepart != [None]:
                        nvertex = V3(*model.normals[facepart[2]])
                        vertex_buffer_object.append(nvertex)

        self.active_vertex_array = iter(vertex_buffer_object)
    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = [
        [1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        [0, 0, 0, 1],
        ]


        a = rotate.x
        rotation_matrix_x = [
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a),  cos(a), 0],
        [0, 0, 0, 1]
        ]

        a = rotate.y
        rotation_matrix_y = [
        [cos(a), 0,  sin(a), 0],
        [     0, 1,       0, 0],
        [-sin(a), 0,  cos(a), 0],
        [     0, 0,       0, 1]
        ]

        a = rotate.z
        rotation_matrix_z = [
        [cos(a), -sin(a), 0, 0],
        [sin(a),  cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]

        rotation_matrix = miNumpy.dot(miNumpy.dot(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)

        scale_matrix = [
        [scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, 1],
        ]

        self.Model = miNumpy.dot(miNumpy.dot(translation_matrix, rotation_matrix), scale_matrix)
    
    def loadViewMatrix(self, x, y, z, center):
        M = [
        [x.x, x.y, x.z,  0],
        [y.x, y.y, y.z, 0],
        [z.x, z.y, z.z, 0],
        [0,     0,   0, 1]
        ]

        O = [
        [1, 0, 0, -center.x],
        [0, 1, 0, -center.y],
        [0, 0, 1, -center.z],
        [0, 0, 0, 1]
        ]

        self.View = miNumpy.dot(M, O)
    def loadProjectionMatrix(self, coeff):
        self.Projection =  [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, coeff, 1]
        ]

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport =  [
        [self.width/2, 0, 0, x + self.width/2],
        [0, self.height/2, 0, y + self.height/2],
        [0, 0, 128, 128],
        [0, 0, 0, 1]
        ]

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1 / length(sub(eye, center)))
        self.loadViewportMatrix()

    def draw_arrays(self, polygon):
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
            except StopIteration:
                print('Done.')

    def fillPolygon(self, texto, traslado):
        puntos = texto[:-1].split(') ')
        separado = [punto[1:].split(', ') for punto in puntos]
        lista = []
        for punto in separado:
            lista.append([str(int(punto[0])+traslado[0]),str(int(punto[1])+traslado[1])])
        cont = 0
        minx = 1000000
        miny = 1000000
        maxx = 0
        maxy = 0
        while cont < len(lista):
            self.line(int(lista[cont][0]), int(lista[cont][1]), int(lista[(cont+1) % len(lista)][0]), int(lista[(cont+1) % len(lista)][1]))
            if minx>int(lista[cont][0]):
                minx = int(lista[cont][0])
            if maxx<int(lista[cont][0]):
                maxx = int(lista[cont][0])
            if miny>int(lista[cont][1]):
                miny = int(lista[cont][1])
            if maxy<int(lista[cont][1]):
                maxy = int(lista[cont][1])
            cont = cont + 1
        bandera = False
        for x in range(minx,maxx+1):
            for y in range(miny,maxy+1):
                if self.framebuffer[y][x] == self.current_color and not ([str(x),str(y)] in lista) and self.framebuffer[y+1][x] != self.current_color :
                    valor = False
                    for i in range(y+1, maxy+1):
                        if self.framebuffer[i][x] == self.current_color:
                            valor = True 
                    bandera = valor
                if bandera:
                    self.framebuffer[y][x] = self.current_color

""" r = Render()
r.glInit()
r.glCreateWindow(1920, 1080)
r.glViewPort(0, 0, 1920, 1080)
r.load('./models/sphere.obj',[1.2,0.65,10],[800,800,1])
r.glFinish('a.bmp') """