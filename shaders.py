from typing import Text
from gl import *
from lib import color, writebmp
from model import Texture


def gourad(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_texture.get_color(tx, ty)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  if tcolor == []:
    return color(0,0,0)
  else:
    r = int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0
    g = int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0
    b = int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    #print(tcolor[2], tcolor[1], tcolor[0])
    if r > 255:
      r = 255
    if g > 255:
      g = 255
    if b > 255:
      b = 255
    return color(r,g,b)

def fragment(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  tcolor = (255,255,255)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  if tcolor == []:
    return color(0,0,0)
  else:
    r = int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0
    g = int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0
    b = int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    #print(tcolor[2], tcolor[1], tcolor[0])
    if r > 255:
      r = 255
    if g > 255:
      g = 255
    if b > 255:
      b = 255
    return color(r,g,b)
  

def sun_shader(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tcolor = (255,255,0)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  if tcolor == []:
    return color(0,0,0)
  else:
    r = int(tcolor[0] * intensity) if tcolor[0] * intensity > 0 else 0
    g = int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0
    b = 0
    #print(tcolor[2], tcolor[1], tcolor[0])
    if r > 255:
      r = 255
    if g > 255:
      g = 255
    return color(r,g,b)

def sky_shader(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tcolor = (137,209,254)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  if tcolor == []:
    return color(0,0,0)
  else:
    r = int(tcolor[0] * intensity) if tcolor[0] * intensity > 0 else 0
    g = int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0
    b = int(tcolor[2] * intensity) if tcolor[2] * intensity > 0 else 0
    #print(tcolor[2], tcolor[1], tcolor[0])
    if r > 137:
      r = 137
    if g > 209:
      g = 209
    if g > 254:
      g = 254
    return color(r,g,b)

r = Render()
r.glInit()
r.glCreateWindow(1400, 1400)
r.glViewPort(0, 0, 1400, 1400)
t1 = Texture('./models/fox.bmp')
""" t2 = Texture('./models/omni.bmp') """
t3 = Texture('./models/digimon.bmp')
t4 = Texture('./models/hulk.bmp')
t5 = Texture('./models/venom.bmp')
t6 = Texture('./models/trooper.bmp')
t7 = Texture('./models/grass.bmp')
t8 = Texture('./models/sun.bmp')
r.light = norm(V3(1, -2.5, 2))
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
""" r.load('./models/model.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)) """
""" r.load('./models/sphere.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)) """
""" r.active_texture = t2
r.load('./models/omni.obj', translate=(0, 0, 0), scale=(0.1, 0.1, 0.1), rotate=(1.5, 0, 0))
r.draw_arrays('TRIANGLES') """
r.active_texture = t1
r.load('./models/fox.obj', translate=(-0.7, -0.9, 0.2), scale=(0.004, 0.004, 0.004), rotate=(0, -0.5, 0))
r.draw_arrays('TRIANGLES')
""" r.active_texture = t3
r.load('./models/digimon.obj', translate=(-0.25, -0.9, 0), scale=(0.45, 0.45, 0.45), rotate=(1, 0.2, 0.2))
r.draw_arrays('TRIANGLES') """
r.active_texture = t4
r.load('./models/hulk.obj', translate=(-0.4, -0.8, -0.2), scale=(0.4, 0.4, 0.4), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.active_texture = t5
r.load('./models/cosaVenom.obj', translate=(0.6, -0.8, 0), scale=(0.12, 0.12, 0.12), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.active_texture = t6
r.load('./models/trooper.obj', translate=(0.15, -0.8, 0), scale=(0.12, 0.12, 0.12), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.active_texture = t7
r.load('./models/escenario.obj', translate=(-0.15, -0.68, -0.5), scale=(1.2, 0.4, 0.1), rotate=(0, 0.19, 0))
r.draw_arrays('TRIANGLES')
r.active_texture = t8
r.active_shader = gourad
r.load('./models/sun.obj', translate=(0, 0.5, 0), scale=(0.3, 0.3, 0.3), rotate=(-1.3, 0, 0))
r.draw_arrays('TRIANGLES')
r.active_shader = sky_shader
r.load('./models/escenario.obj', translate=(-0.1, 0.3, -0.6), scale=(1.2, 0.8, 0.1), rotate=(0, 0.19, 0))
r.draw_arrays('TRIANGLES')
writebmp('a.bmp', 1400, 1400, r.framebuffer)