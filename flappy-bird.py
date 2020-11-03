import pygame, sys, random

# Draw the Base for each Frame
def draw_base():
    screen.blit(base_surface,(base_x_pos,450))
    screen.blit(base_surface,(base_x_pos + 288,450))

# Placing Pipes at random height
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe =pipe_surface.get_rect(midtop= (350,random_pipe_pos))
    top_pipe =pipe_surface.get_rect(midbottom= (350,random_pipe_pos -150))
    return bottom_pipe,top_pipe

# Move Pipes to left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

# Drawing Pipes in the screen
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

# Check Collisions
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            collision_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True

# Rotate the 
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3 ,1)
    return new_bird

# Animation for Flapping Wing
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird,new_bird_rect

# Display the Score on the screen based on state of game
def score_display(game_state):
    if game_state == 'current_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

# Update the High Score
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

# Sound Player Init
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1,buffer = 512 )

# Init
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Parameters
game_active = False
score = 0
high_score = 0
new_game = True
# Physics Parameters
gravity = 0.20
bird_movement = 0

# Background Assets
bg_surface = pygame.image.load('assets/background-day.png').convert()
base_surface = pygame.image.load('assets/base.png').convert()
base_x_pos = 0

# Bird Assets
bird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

# Bird Flap Animation Event
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

# Pipe Assets 
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
pipe_height = [200,300,400]

# Spawn Pipe Event
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

# New Game Screen
new_game_surface = pygame.image.load('assets/message.png').convert_alpha()
new_game_rect = new_game_surface.get_rect(center = (144, 256))

# Game Over Screen
game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))

# Game Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# Main Game Loop
while True:
    # Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active :
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False :
                if new_game :
                    game_active = True
                    new_game = False
                else: 
                    new_game = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
        else:
            bird_index = 0

        bird_surface,bird_rect = bird_animation()
    # Background
    screen.blit(bg_surface,(0,0))
    
    # Core Logic
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_sound_countdown -= 1
        if score_sound_countdown <=0 :
            score_sound.play()
            score_sound_countdown = 100
        score_display('current_game')
    else :
        # New Game Display
        if new_game:
            bird_rect.center = (50,256)
            screen.blit(bird_surface, bird_rect)
            screen.blit(new_game_surface,new_game_rect)
        # Game Over Screen Display
        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')

    # Game Base Animation
    base_x_pos -= 1
    draw_base()
    if base_x_pos <= -288 :
        base_x_pos = 0

    pygame.display.update()
    clock.tick(90)
