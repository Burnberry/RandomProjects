import pyglet
from pyglet.window import mouse
from pyglet.gl import gl
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

#from Code.Clock import Clock
from pyglet import clock
from random import randint


window = pyglet.window.Window()

@window.event
def on_mouse_press(x, y, button, modifier):
    if button == mouse.LEFT:
        print(x, y, "The Left Mouse Was Pressed")

    elif button == mouse.RIGHT:
        print("Right Mouse Was Pressed")

label = pyglet.text.Label('0',
                          font_name='Times New Roman',
                          font_size=10,
                          x=3*window.width//4, y=window.height//2,
                          anchor_x='center', anchor_y='center')
pic = pyglet.image.load("Assets/Overlay/MoveButton.png")
pic2 = pyglet.image.load("Assets/Overlay/AttackButton.png")
#clock = Clock()
n1 = 3
n = 100
batch = pyglet.graphics.Batch()
sprites = []
x= 0
frame = 0
for i in range(n+n1):
    sprite = pyglet.sprite.Sprite(pic, randint(0, 500), randint(0, 500), batch=batch)
    sprite.scale = 16
    sprite.opacity = (100*i)%256
    sprites.append(sprite)
    #sprite.color = (0 + 255*(i==1), 0 + 255*(i==2), 0 + 255*(i==3))
ka = 0
while(True):
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    dt = clock.tick()
    x += dt
    frame += 1

    window.dispatch_events()
    window.dispatch_event('on_draw')

    window.clear()
    label.text = str(frame) + " " + str(x)[:6] + " " + str(dt)[:6]#str(clock.ticks) + " " + str(clock.timeSkips) + " " + str(clock.timeSkipped/10**9)
    if frame%60 == 0:
        print(frame, x, sprites[0].opacity)
    nSprites = []
    for sprite in sprites:
        spr = pyglet.sprite.Sprite(pic, sprite.x, sprite.y, batch=batch)
        nSprites.append(spr)
        sprite.delete()
    sprites = nSprites
    batch.draw()
    window.flip()