from ursina import *
import random

app = Ursina()
app.icon = 'my_icon.ico'  # Add your icon here

Sky()
ground = Entity(model='plane', texture='white_cube', color=color.green, scale=(20, 1, 1), y=-3)

bird = Entity(
    model='cube',
    color=color.orange,
    collider='box',
    scale=(1, 1, 1),
    y=0,
    z=0
)

pipe_speed = 5
pipe_gap = 3
pipe_distance = 15  

def create_pipe(x_pos):
    y_pos = random.uniform(-2, 2)
    pipe_top = Entity(
        model='cube',
        color=color.green,
        collider='box',
        scale=(1, 5, 1),
        x=x_pos,
        y=y_pos + pipe_gap / 2,
        z=0
    )
    pipe_bottom = Entity(
        model='cube',
        color=color.green,
        collider='box',
        scale=(1, 5, 1),
        x=x_pos,
        y=y_pos - pipe_gap / 2 - 5,
        z=0
    )
    return [pipe_top, pipe_bottom]

pipes = []
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.5, 0.4), scale=2)
game_over_text = Text(text='', position=(0, 0), scale=2, color=color.red)
gravity = 1
flap_strength = 0.4
game_over = False

def reset_game():
    global score, game_over, pipes, bird
    score = 0
    score_text.text = f'Score: {score}'
    game_over = False
    game_over_text.text = ''  # Clear game over text
    bird.y = 0
    bird.x = 0
    bird.z = 0
    
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            destroy(pipe)
    pipes.clear()  # Clear the pipe list
    
    pipes.append(create_pipe(10))

def update():
    global score, game_over

    if game_over:
        if held_keys['r']:  
            reset_game()
        return

    # Bird movement and gravity
    bird.y -= gravity * time.dt
    if held_keys['space']:
        bird.y += flap_strength

    # Move pipes and check for score
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pipe.x -= pipe_speed * time.dt
            if pipe.x < -10:
                destroy(pipe)
                pipes.remove(pipe_pair)
                score += 1
                score_text.text = f'Score: {score}'

    # Check for collisions
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            if bird.intersects(pipe).hit:
                game_over = True
                game_over_text.text = f'Game Over! Final Score: {score}'  # Show final score
                print("Game Over")
                return

    # Check for ground collision
    if bird.y < -2:
        game_over = True
        game_over_text.text = f'Game Over! Final Score: {score}'  # Show final score

    # Spawn new pipes if needed
    if len(pipes) == 0 or pipes[-1][0].x < pipe_distance:
        new_x = pipes[-1][0].x + pipe_distance if pipes else 10
        pipes.append(create_pipe(new_x))

app.run()
