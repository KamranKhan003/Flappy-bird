import pygame
from random import choice



def get_floor():
    screen.blit(ground_surf,(ground_pos,500))
    screen.blit(ground_surf,(ground_pos + 476,500))

def create_pipe():
    height = choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop = (500,height))
    top_pipe = pipe_surf.get_rect(midbottom = (500,height-150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surf,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):        
            bg_music.play()
            return False
        if bird_rect.top <= -50 or bird_rect.bottom >= 600:
            bg_music.play()
            return False
    return True

def bird_animation():
    new_bird = bird_frams[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50,bird_rect.centery))
    return new_bird, new_bird_rect

def roted_bird(bird):
    new_bird = pygame.transform.rotate(bird,-gravity*3)
    return new_bird

def display_score(state):
    score_surf = game_font.render(f'Score {int(score)}', False, (255,255,255))
    score_rect = score_surf.get_rect(center=(238,50))
    screen.blit(score_surf,score_rect)

ground_pos = 0
gravity = 0
pipe_height = (400,200,300)
game_active = True
score = 0

pygame.init()
clock = pygame.time.Clock()

# Music
bg_music = pygame.mixer.Sound(r'mypygame\flappy-brid\sound\sfx_die.wav')

# Set Window
screen = pygame.display.set_mode((476,600))
pygame.display.set_caption("Flappy Brid")

game_font = pygame.font.Font(r'mypygame\flappy-brid\04B_19.TTF', 32)

bg_surf = pygame.image.load(r'mypygame\flappy-brid\assets\background-day.png')
bg_surf = pygame.transform.scale(bg_surf,(476,600))

ground_surf = pygame.image.load(r'mypygame\flappy-brid\assets\base.png')
ground_surf = pygame.transform.scale2x(ground_surf)


bird_down = pygame.image.load(r'mypygame\flappy-brid\assets\bluebird-downflap.png')
bird_mid = pygame.image.load(r'mypygame\flappy-brid\assets\bluebird-midflap.png')
bird_up = pygame.image.load(r'mypygame\flappy-brid\assets\bluebird-upflap.png')
bird_frams = [bird_down,bird_mid,bird_up]
bird_index = 0
bird_surf = bird_frams[bird_index]
bird_rect = bird_surf.get_rect(center=(50,300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surf = pygame.image.load(r'mypygame\flappy-brid\assets\pipe-green.png')
pipe_surf = pygame.transform.scale(pipe_surf,(50,400))
pipe_list = list()


SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

over_surf = pygame.image.load(r'mypygame\flappy-brid\assets\message.png')
over_rect = over_surf.get_rect(center=(238,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                gravity = -10
            
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,300)
                gravity = 0
                score = 0
        
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surf,bird_rect = bird_animation()
    
    screen.blit(bg_surf,(0,0))

    if game_active:        
        
        # Bird
        rote_bird = roted_bird(bird_surf)
        screen.blit(rote_bird,bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipe(pipe_list)

        # Score
        score += 0.01
        display_score(game_active)
    
    else:
        screen.blit(over_surf,over_rect)
        display_score(game_active)
    
    # Floor
    ground_pos -= 1
    get_floor()
    if ground_pos <= -476:
        ground_pos = 0

    gravity += 0.25
    bird_rect.y += gravity


    pygame.display.update()
    clock.tick(120)