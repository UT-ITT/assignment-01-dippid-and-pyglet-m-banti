import pyglet
from pyglet import window, shapes
import random
from DIPPID import SensorUDP
PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Marina Doodle")

main_batch = pyglet.graphics.Batch()

player = shapes.Rectangle(400, 50, 50, 50, (255, 0, 0), batch=main_batch)


player_dy = 0

GRAVITY = 0.4

JUMP_FORCE = 12


platforms = []

for i in range(10):

    random_x = random.randint(0, WINDOW_WIDTH - 100)
    y_position = i * 80

    plat = shapes.Rectangle(random_x, y_position, 100, 15, (50, 220, 50), batch=main_batch)
    platforms.append(plat)


def update(dt):
    global player_dy


    player_dy -= GRAVITY

    player.y += player_dy

    if player.y <= 0:
        player.y = 0
        player_dy = JUMP_FORCE

    if sensor.has_capability('gravity'):
        gravity_data = sensor.get_value('gravity')

        if gravity_data is not None:
            gravity_x = -float(gravity_data['x'])

            bound = 1.5
            max_speed = 5
            speed_factor = 1.5

            if abs(gravity_x) > bound:
                if gravity_x > 0:
                    movement = gravity_x - bound
                else:
                    movement = gravity_x + bound
                
                current_speed = movement * speed_factor

                if current_speed > max_speed:
                    current_speed = max_speed
                # throttling of current speed to max_speed (left movement)
                elif current_speed < -max_speed:
                    current_speed = -max_speed
                
                player.x += current_speed


    


"""def update(dt):
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
        max_speed = 5

        if abs(gravity_x) > bound: # type: ignore

        # for better movement handling
            speed_factor = 1.5

            if gravity_x > 0: # type: ignore
                movement = gravity_x - bound # type: ignore
            else:
                movement = gravity_x + bound # type: ignore

            current_speed = movement * speed_factor
            #to avoid infinite acceleration of player based on phone incline
            # throttling of current speed to max_speed (right movement)
            if current_speed > max_speed:
                current_speed = max_speed
            # throttling of current speed to max_speed (left movement)
            elif current_speed < -max_speed:
                current_speed = -max_speed

            # adds speed to the movement
            player.x += current_speed # type: ignore
        else:
            pass
    # left game border
    if player.x < 0:
        player.x = 0

    # right game border
    # width needs to be multiplied by 2 
    # otherwise the border will appear in the middle of the window (half window size)
    # if the player starts from the left border moving to the right
    elif player.x > WINDOW_WIDTH*2 - player.width:
        player.x = WINDOW_WIDTH*2 - player.width

    if sensor.has_capability('button_1'):
        button_pressed = sensor.get_value('button_1')
        if button_pressed == 1:
            player.y += 7
"""

@win.event
def on_draw():
    win.clear()
    player.draw()

pyglet.app.run()
