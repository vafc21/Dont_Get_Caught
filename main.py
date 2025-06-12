### Title: Dont get caught The Game ###
import pygame
import timeit
import random
import math
import enemy 
import player

pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
running = True

game_box_cords = pygame.math.Vector2(150, 50)
game_box_size = pygame.math.Vector2(550, 450)
player_pos = pygame.math.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_speed = 5
default_size = 20
player_hearts = 3

# debugging
mouse_debug = False
if mouse_debug == True:
    print("Mouse Debugging is on")

# level 
level = 0
level_complete = True
# Create enemy objects
enemies = []

# Player list for drawing them

players = []
# create player
first_pl = player.Player(screen,"Player 1","Red", player_pos, 20, "Black", True, "up")
players.append(first_pl)
#enemie_1 = enemy.Enemy(screen,"enemy_1", pygame.math.Vector2(100,100), "Blue", 20, "Black")
#
#enemies.append(enemie_1)

time = 0

def start_game_timer():
    time = timeit.default_timer()
    return time

def end_game_timer():
    end_time = timeit.default_timer()

def stop():
    running = False

def new_level(level):
    difficulty = level * 10
    #list = [difficulty, level]
    return difficulty


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

def enemy_can_see_player(enemy_pos, p_pos):
    distance = math.sqrt(math.exp2(enemy_pos.x - p_pos.x) + math.exp2(enemy_pos.y - p_pos.y))
    if distance <= 70:  # distance 
        return True
    else:
        return False

def enemy_hits_player(enemy_pos, p_pos):
    distance = (math.sqrt(math.exp2(enemy_pos.x - p_pos.x) + math.exp2(enemy_pos.y - p_pos.y)))//1
    
    distance//=1
    print(distance)
    if distance <= 0:  # distance
        print('hit')
        return True
    else:
        #print('no hit')
        return False

while running:
    start_game_timer()
    for playe in players:
        if playe.name == "Player 1":
            player1_pos = playe.pos
        elif playe.name == "Player 2":
            player2_pos = playe.pos
        else:
            print('Unknown player: ' + str(playe.name))
            stop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("Gold")
    keys = pygame.key.get_pressed()
    if(mouse_debug == True):
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
    if keys[pygame.K_ESCAPE]:
                running = False
    for playe in players:
        if playe.pos.x <= 20:
            playe.pos.x = 20
        if playe.pos.x > screen.get_width() - 20:
            playe.pos.x = screen.get_width() - 20
        if playe.pos.y <= 20:
            playe.pos.y = 20
        if playe.pos.y > screen.get_height() - 20:
            playe.pos.y = screen.get_height() - 20
        if playe.name == "Player 1":
            if keys[pygame.K_LSHIFT]:
                playe.speed = 10
            else:
                playe.speed = 5
            if keys[pygame.K_w]:
                playe.pos.y -= player_speed
            if keys[pygame.K_s]:
                playe.pos.y += player_speed
            if keys[pygame.K_a]:
                playe.pos.x -= player_speed
            if keys[pygame.K_d]:
                playe.pos.x += player_speed
            
            
    
    
    for playe in players:
        playe.draw()

    for enem in enemies:
        enem.draw()  # Draw the enemy
        if enem.pos.x < 50:
            enem.pos.x = 50
        if enem.pos.x > screen.get_width() - 50:
            enem.pos.x = screen.get_width() - 50
        if player1_pos.x >= 50 and player1_pos.x <= screen.get_width() - 50:
            
            hits = enemy_hits_player(enem.pos, player1_pos)
            if hits == True:
            
                enemies.remove(enem)
                player_hearts -= 1
                if player_hearts <= 0:
                    print("Game Over")
                    running = False
                else:
                    print("You have " + str(player_hearts) + " hearts left")
            
            if enemy_can_see_player(enem.pos,player1_pos) == True:  # Check if the enemy can see the player
                enem.random_pos = None  # Reset random position when chasing the player
                enem.move_towards_target(player1_pos, speed=player_speed - 2)  # Move toward the player
                
            
            
            if enemy_can_see_player(enem.pos, player1_pos) == False:  # If the enemy can't see the player
                # Generate a random position only once
                if not hasattr(enem, "random_pos") or enem.random_pos is None:
                    enem.random_pos = get_random_pos()

                # Check if the enemy is close to the random position
                if enem.pos.distance_to(enem.random_pos) < 10:  # Threshold for "close enough"
                    enem.random_pos = get_random_pos()  # Generate a new random position

                # Move toward the random position
                enem.move_towards_target(enem.random_pos, speed=player_speed - 2)
            
            
        
    if player1_pos.x >= screen.get_width() - 50 :
        level_complete = True
    
    

    
    if level_complete == True:
        player1_pos = pygame.math.Vector2(20, screen.get_height() / 2)
        if level > 0:
            print("Level " + str(level) + " complete")
        level += 1
        level_complete = False
        difficulty = new_level(level)
        player_hearts = 3
        enemies.clear()
        make_level(difficulty)
        
    

    #make_level(10)
    pygame.display.flip()
    clock.tick(60)


