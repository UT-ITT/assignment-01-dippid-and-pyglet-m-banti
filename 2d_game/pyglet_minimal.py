import pyglet
from pyglet import window, shapes
import random
from DIPPID import SensorUDP
PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Marina Doodle")

# functions as collection to draw a batch
main_batch = pyglet.graphics.Batch()

player = shapes.Rectangle(400, 50, 50, 50, (255, 0, 0), batch=main_batch)

# delta movement x-axis
player_dx = 0
# delta movement y-axis
player_dy = 0

GRAVITY = 0.4 # player can fall
JUMP_FORCE = 12 # force of contact with floor/platttform

platforms = []

for i in range(10):
    # sets random plattform position
    random_x = random.randint(0, WINDOW_WIDTH - 100)
    y_position = i * 80
    # generates plattform
    plat = shapes.Rectangle(random_x, y_position, 100, 15, (50, 220, 50), batch=main_batch)
    platforms.append(plat)


def update(dt):
    global player_dy, player_dx

    # apply gravity to player frfom start
    player_dy -= GRAVITY

    player.y += player_dy

    #floor collision
    # player jumps continously without input from floor
    if player.y <= 0:
        player.y = 0
        player_dy = JUMP_FORCE


    #plattform collision
    # player jumps continously without input from plattform
    if player_dy < 0:
        for p in platforms:
            # check if player and plattforms overlap
            if(player.x < p.x + p.width and player.x + player.width > p.x and
            player.y < p.y + p.height and player.y + player.height > p.y):
                # jump off plattform
                player.y = p.y + p.height
                player_dy = JUMP_FORCE
                player_dx *= 0.5
                # since player can jump only from one plattform at once
                break
    # get gravity x-axis data for left/right movement
    if sensor.has_capability('gravity'):
        gravity_data = sensor.get_value('gravity')

        if gravity_data is not None:
            gravity_x = -float(gravity_data['x'])

            bound = 0.5 
            max_speed = 5
            speed_factor = 2

            # for better movement handling
            if abs(gravity_x) > bound:
                if gravity_x > 0:
                    movement = gravity_x - bound
                else:
                    movement = gravity_x + bound
                
                current_speed = movement * speed_factor
        

                # throttling of current speed to max_speed
                # right movement
                if current_speed > max_speed:
                    current_speed = max_speed
                # left movement
                elif current_speed < -max_speed:
                    current_speed = -max_speed

                player.x += current_speed
    # player out of frame warp
    # left border
    if player.x < -player.width:
        player.x = WINDOW_WIDTH
    # right border
    elif player.x > WINDOW_WIDTH:
        player.x = -player.width

    # endless scroll and plattform set up when player reaches window mid-height
    if player.y > WINDOW_HEIGHT / 2:
        
        difference = player.y - (WINDOW_HEIGHT / 2)

        player.y = WINDOW_HEIGHT / 2

        for p in platforms:
            p.y -= difference
            # plattform recycling for scrolling
            if p.y < 0:
                p.y = WINDOW_HEIGHT + random.randint(10, 50)
                p.x = random.randint(0, WINDOW_WIDTH - int(p.width))

@win.event
def on_draw():
    win.clear()
    main_batch.draw()
# frame update
pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
