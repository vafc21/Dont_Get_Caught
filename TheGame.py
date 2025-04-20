### Title: Dont get caught The Game ###
import pygame
import timeit
import random
import math
import enemy 

pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
running = True

game_box_cords = pygame.math.Vector2(150, 50)
game_box_size = pygame.math.Vector2(550, 450)
player_pos = pygame.math.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_speed = 5
default_size = 20
player_harts = 3

# debugging
mouse_debug = False
if mouse_debug == True:
    print("Mouse Debugging is on")

# level 
level = 0
level_complete = True
# Create enemy objects
enemies = []


#enemie_1 = enemy.Enemy(screen,"enemy_1", pygame.math.Vector2(100,100), "Blue", 20, "Black")
#
#enemies.append(enemie_1)

time = 0

def start_game_timer():
    time = timeit.default_timer()
    return time

def end_game_timer():
    end_time = timeit.default_timer()

def new_level(level):
    difficulty = level * 10
    #list = [difficulty, level]
    return difficulty

def draw_player(color, player_pos, size, eye_color, eyebrows, eyebrowsUpOrDown):
    left_eye = pygame.math.Vector2(player_pos.x - 5, player_pos.y - 5)
    right_eye = pygame.math.Vector2(player_pos.x + 5, player_pos.y - 5)
    pygame.draw.circle(screen, color, player_pos, size)
    pygame.draw.circle(screen, eye_color, left_eye, 3)
    pygame.draw.circle(screen, eye_color, right_eye, 3)
    if eyebrows == True:
        if eyebrowsUpOrDown == "up":
            pygame.draw.line(screen, "Black", (player_pos.x - 12, player_pos.y - 9), (player_pos.x - 2, player_pos.y - 15), width=3)
            pygame.draw.line(screen, "Black", (player_pos.x + 12, player_pos.y - 9), (player_pos.x + 2, player_pos.y - 15), width=3)
        elif eyebrowsUpOrDown == "down":
            pygame.draw.line(screen, "Black", (player_pos.x - 12, player_pos.y - 15), (player_pos.x - 2, player_pos.y - 9), width=3)
            pygame.draw.line(screen, "Black", (player_pos.x + 12, player_pos.y - 15), (player_pos.x + 2, player_pos.y - 9), width=3)

def make_level(difficulty):
    #game_box_top = pygame.draw.line(screen, "Black", (game_box_cords.x, game_box_cords.y), (game_box_cords.x + game_box_size.x, game_box_cords.y), width=3)
    #game_box_bottom = pygame.draw.line(screen, "Black", (game_box_cords.x, game_box_cords.y + game_box_size.y), (game_box_cords.x + game_box_size.x, game_box_cords.y + game_box_size.y), width=3)
    #game_box_left = pygame.draw.line(screen, "Black", (game_box_cords.x, game_box_cords.y), (game_box_cords.x, game_box_cords.y + game_box_size.y), width=3)
    #game_box_right = pygame.draw.line(screen, "Black", (game_box_cords.x + game_box_size.x, game_box_cords.y), (game_box_cords.x + game_box_size.x, game_box_cords.y + game_box_size.y), width=3)
    
    for i in range(difficulty//4):
        e = enemy.Enemy(screen, "enemy_" + str(i), pygame.math.Vector2(random.randrange(20,screen.get_width()+20), random.randrange(20,screen.get_height()+20)), "Blue", 20, "Black")
        enemies.append(e)

def get_random_pos():
    x = random.randrange(50,screen.get_width()-40)
    y = random.randrange(20,screen.get_height()+20)
    return pygame.math.Vector2(x,y)

def enemy_can_see_player(enemy_pos, p_pos = player_pos):
    distance = p_pos - enemy_pos
    if distance.length() < 150:  # Adjust the distance threshold as needed
        return True
    else:
        return False

def enemy_hits_player(enemy_pos, p_pos = player_pos):
    distance = p_pos - enemy_pos
    if distance.length() < 20:  # Adjust the distance threshold as needed
        return True
    else:
        return False

while running:
    start_game_timer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("Gold")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if(mouse_debug == True):
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)
    if player_pos.x <= 20:
        player_pos.x = 20
    if player_pos.x > screen.get_width() - 20:
        player_pos.x = screen.get_width() - 20
    if player_pos.y <= 20:
        player_pos.y = 20
    if player_pos.y > screen.get_height() - 20:
        player_pos.y = screen.get_height() - 20
    player = draw_player("Red", player_pos, 20, "Black", True, "up")
    
    for enem in enemies:
        enem.draw()  # Draw the enemy
        if enem.pos.x < 50:
            enem.pos.x = 50
        if enem.pos.x > screen.get_width() - 50:
            enem.pos.x = screen.get_width() - 50
        if player_pos.x >= 50 and player_pos.x <= screen.get_width() - 50:
            
            
            if enemy_can_see_player(enem.pos) == False:  # If the enemy can't see the player
                # Generate a random position only once
                if not hasattr(enem, "random_pos") or enem.random_pos is None:
                    enem.random_pos = get_random_pos()

                # Check if the enemy is close to the random position
                if enem.pos.distance_to(enem.random_pos) < 10:  # Threshold for "close enough"
                    enem.random_pos = get_random_pos()  # Generate a new random position

                # Move toward the random position
                enem.move_towards_target(enem.random_pos, speed=player_speed - 2)
            elif enemy_can_see_player(enem.pos) == True:  # Check if the enemy can see the player
                enem.random_pos = None  # Reset random position when chasing the player
                enem.move_towards_target(player_pos, speed=player_speed - 2)  # Move toward the player
            if enemy_hits_player(enem.pos) == True:
                enemies.remove(enem)
                player_harts -= 1
                if player_harts <= 0:
                    print("Game Over")
                    running = False
                else:
                    print("You have " + str(player_harts) + " harts left")
        
    if player_pos.x >= screen.get_width() - 50 :
        level_complete = True
    
    

    if keys[pygame.K_LSHIFT]:
        player_speed = 10
    else:
        player_speed = 5
    if keys[pygame.K_w]:
        player_pos.y -= player_speed
    if keys[pygame.K_s]:
        player_pos.y += player_speed
    if keys[pygame.K_a]:
        player_pos.x -= player_speed
    if keys[pygame.K_d]:
        player_pos.x += player_speed
    if level_complete == True:
        player_pos = pygame.math.Vector2(20, screen.get_height() / 2)
        if level > 0:
            print("Level " + str(level) + " complete")
        level += 1
        level_complete = False
        difficulty = new_level(level)
        player_harts = 3
        enemies.clear()
        make_level(difficulty)
        
    

    #make_level(10)
    pygame.display.flip()
    clock.tick(60)


