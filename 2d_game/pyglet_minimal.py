import pyglet
from pyglet import window, shapes
from DIPPID import SensorUDP
PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

player = shapes.Rectangle(400, 50, 50, 50, (255, 0, 0))

def update(dt):
    # get gravity x-axis data for left/right movement
    if sensor.has_capability('gravity'):
        gravity_data = sensor.get_value('gravity')

        if gravity_data is not None:
            # needs to be negative, since without left incline would lead to right movement and vice versa
            gravity_x = -float(gravity_data['x'])
        # avoids drifting problem on player
        # value between 0 and 9.81 (graity), high value = phone handling needs to be more steady, 
        # low value = phone handling is less sensitive

        bound = 1.5

        if abs(gravity_x) > bound: # type: ignore

        # for better movement handling
            speed_factor = 1.5

            if gravity_x > 0: # type: ignore
                movement = gravity_x - bound # type: ignore
            else:
                movement = gravity_x + bound # type: ignore
            # adds speed to the movement
            player.x += gravity_x * speed_factor # type: ignore
        else:
            pass

    if sensor.has_capability('button_1'):
        button_pressed = sensor.get_value('button_1')
        if button_pressed == 1:
            player.y += 7


@win.event
def on_draw():
    win.clear()
    player.draw()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
