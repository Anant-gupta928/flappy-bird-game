from ursina import *
import random

app = Ursina()

# Set up the game environment
Sky()
ground = Entity(model='plane', texture='white_cube', color=color.green, scale=(20, 1, 1), y=-3)

# Define the bird
bird = Entity(
    model='cube',
    color=color.orange,
    collider='box',
    scale=(1, 1, 1),
    y=0,
    z=0
)

# Define the pipes
pipe_speed = 5
pipe_gap = 3
pipe_frequency = 2
pipe_distance = 20

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

# Score
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.5, 0.4), scale=2)

# Gravity and flap settings
gravity = 1
flap_strength = 0.4

# Game States
game_over = False

def reset_game():
    global score, game_over, pipes, bird
    score = 0
    score_text.text = f'Score: {score}'
    game_over = False
    bird.y = 0
    bird.x = 0
    bird.z = 0
    
    # Destroy existing pipes
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            destroy(pipe)
    pipes = []
    
    # Create initial pipes
    pipes.append(create_pipe())

def update():
    global score, game_over

    if game_over:
        if held_keys['r']:
            reset_game()
        return

    # Bird movement and physics
    bird.y -= gravity * time.dt

    if held_keys['space']:
        bird.y += flap_strength

    # Pipe movement and collision detection
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pipe.x -= pipe_speed * time.dt
            if pipe.x < -10:
                destroy(pipe)
                pipes.remove(pipe_pair)
                score += 1
                score_text.text = f'Score: {score}'

    # Check for collision with pipes
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            if bird.intersects(pipe).hit:
                game_over = True
                print("Game Over")
                return

    # Check for collision with ground
    if bird.y < -2:
        game_over = True
        print("Game Over")

    # Spawn new pipes if needed
    if len(pipes) == 0 or pipes[-1][0].x < pipe_distance:
        # Position new pipes after the last pipe
        new_x = pipes[-1][0].x + pipe_distance if pipes else 10
        pipes.append(create_pipe(new_x))
app.run()