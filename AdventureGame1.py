import sys, pygame, pyautogui, time

# Starter code for an adventure game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors:
# Minh Tri Ho
# Phan Duy Anh Mai
pygame.mixer.init()
# Load the music file and sound effect
pygame.mixer.music.load("music/main_music.ogg")
pygame.mixer.music.set_volume(0.3)
start_sound_effect = pygame.mixer.Sound("music/start_button_effect.wav")
death_sound_effect = pygame.mixer.Sound("music/death_sound_effect.wav")
complete_sound_effect = pygame.mixer.Sound("music/complete_effect.wav")
collect_sound_effect = pygame.mixer.Sound("music/collect_effect.wav")
# Start playing the music
pygame.mixer.music.play(-1)

def pixel_collision(mask1, rect1, mask2, rect2):
    '''
    Check if the non-transparent pixels of one mask contacts the non-transparent pixels of another.
    :param mask1:
    :param rect1:
    :param mask2:
    :param rect2:
    :return:
    '''
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap != None

def load_deaths_from_file():
    try:
        with open("deaths.txt", "r") as f:
            num_deaths_str = f.read().strip()
            if num_deaths_str:
                return int(num_deaths_str)
            else:
                return 0
    except FileNotFoundError:
        return 0

def save_deaths_to_file(num_deaths):
    '''
    Record the number of deaths to a seperate text file
    :param num_deaths:
    :return: None
    '''
    with open("deaths.txt", "w") as f:
        f.write(str(num_deaths))
    
def game_over(screen_width,screen_height,screen,death):
    '''
    Display game over screen with different game over messages depending on how many
    death you have
    :param screen_width:
    :param screen_height:
    :param screen:
    :param death:
    :return: Game over screen
    '''
    # Set background color
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 70)
    # Render game over message
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
    death_text = font.render(f"Death: {death}", True, (255,0,0))
    death_rect = death_text.get_rect(center=(screen_width/2, screen_height/2))
    lower_5_death_text = font.render("Unlucky, keep it up, you are good in this game :))", True, (255,0,0))
    lower_10_death_text = font.render("You are not so good!, but don't give up!", True, (255,0,0))
    lower_15_death_text = font.render("Hmm............!",True, (255,0,0))
    lower_20_death_text = font.render("Still trying ??????", True, (255,0,0))
    lower_30_death_text = font.render("Go to sleep T-T !!", True, (255,0,0))
    upper_30_death_text = font.render("Respect for your patience", True, (255,0,0))
    if death <5:
        text = lower_5_death_text
        text_rect = lower_5_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
    elif death <10:
        text = lower_10_death_text
        text_rect = lower_10_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
    elif death <15:
        text = lower_15_death_text
        text_rect = lower_15_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
    elif death <20:
        text = lower_20_death_text
        text_rect = lower_20_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
    elif death <30:
        text = lower_30_death_text
        text_rect = lower_30_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
    else:
        text = upper_30_death_text
        text_rect = upper_30_death_text.get_rect(center=(screen_width/2, screen_height/2+50))
     # Draw messages to screen
    screen.blit(death_text,death_rect)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(text,text_rect)

    # Update display surface
    pygame.display.flip()
    # Wait for 4 seconds
    death_sound_effect.play()
    time.sleep(2)

def restart_game():
    '''
    This just restarts the game all over again
    :return: None
    '''
    main()

def main():
    '''
    This function is the core part of the game and the comments within this function will guide you through different components of the game
    :return: None
    '''
    # Initialize pygame
    pygame.init()
    num_deaths = load_deaths_from_file()
    start = True
    current_map = 0
    # Get screen width and height
    screen_width, screen_height = pyautogui.size()
    rate = screen_width /1920
    # Load menu screen:
    menu = pygame.image.load("maps/menu.png")
    default_map = pygame.transform.scale(menu,(336*screen_height/252,screen_height))
    default_rect = default_map.get_rect() 
    # Load MAP 0:
    map0 = pygame.image.load("maps/map0.png")
    newmap0 = pygame.transform.scale(map0, (336*screen_height/252,screen_height))
    # Store window width and height in a tuple.
    map_size = width, height = newmap0.get_size()
    map_rect0 = newmap0.get_rect()
    # Load MAP 1:
    map1 = pygame.image.load("maps/map1.png")
    newmap1 = pygame.transform.scale(map1, (336*screen_height/252,screen_height))
    # Store window width and height in a tuple.
    map_rect1 = newmap1.get_rect()
    # Load MAP 2:
    map2 = pygame.image.load("maps/map2.png")
    newmap2 = pygame.transform.scale(map2, (336*screen_height/252,screen_height))
    # Store window width and height in a tuple.
    map_rect2 = newmap2.get_rect()
    # Load MAP 3:
    map3 = pygame.image.load("maps/map3.png")
    newmap3 = pygame.transform.scale(map3, (336*screen_height/252,screen_height))
    # Store window width and height in a tuple.
    map_rect3 = newmap3.get_rect()
    # Load winning screen:
    win = pygame.image.load("maps/winning.png")
    win = pygame.transform.scale(win, (336*screen_height/252,screen_height-10))
    win_rect = win.get_rect()

    # create the game window based on the map size
    screen = pygame.display.set_mode(map_size)
    default_map = default_map.convert_alpha()

    # Change white pixels in the map to transparent. If your map already has
    # a transparent path, you should not do this.

    # Menu collision:
    # This is to create a 'hitbox' for the start button so the player can press on it to start the game
    default_collision = pygame.image.load("map_collision/menu_collision.png")
    default_collision = pygame.transform.scale(default_collision, (336*screen_height/252,screen_height))
    default_mask = pygame.mask.from_surface(default_collision)
    # Collision map 0:
    # This is to create the collision of the walls in map 0
    collision_map0 = pygame.image.load("map_collision/collision0.png")
    collision_map0 = pygame.transform.scale(collision_map0, (336*screen_height/252,screen_height))
    map_mask0 = pygame.mask.from_surface(collision_map0)
    # Collision map 1:
    # # This is to create the collision of the walls in map 1
    collision_map1 = pygame.image.load("map_collision/collision1.png")
    collision_map1 = pygame.transform.scale(collision_map1, (336*screen_height/252,screen_height))
    map_mask1 = pygame.mask.from_surface(collision_map1)
    # Collision map 2:
    # This is to create the collision of the walls in map 2
    collision_map2 = pygame.image.load("map_collision/collision2.png")
    collision_map2 = pygame.transform.scale(collision_map2, (336*screen_height/252,screen_height))
    map_mask2 = pygame.mask.from_surface(collision_map2)
    # Collision map 3:
    # This is to create the collision of the walls in map 3
    collision_map3 = pygame.image.load("map_collision/collision3.png")
    collision_map3 = pygame.transform.scale(collision_map3, (336*screen_height/252,screen_height))
    map_mask3 = pygame.mask.from_surface(collision_map3)

    # You must replace these images with your own.
    # Create the player data
    # Player standing 1
    player_stand1 = pygame.image.load("player/stand1.png").convert_alpha()
    player_stand1 = pygame.transform.smoothscale(player_stand1, (450*rate,500*rate))
    # Player standing 2
    player_stand2 = pygame.image.load("player/stand2.png").convert_alpha()
    player_stand2 = pygame.transform.smoothscale(player_stand2, (450*rate,500*rate))
    # Player standing 3
    player_stand3 = pygame.image.load("player/stand3.png").convert_alpha()
    player_stand3 = pygame.transform.smoothscale(player_stand3, (450*rate,500*rate))
    # Player standing 4
    player_stand4 = pygame.image.load("player/stand4.png").convert_alpha()
    player_stand4 = pygame.transform.smoothscale(player_stand4, (450*rate,500*rate))
    # Player standing 5
    player_stand5 = pygame.image.load("player/stand5.png").convert_alpha()
    player_stand5 = pygame.transform.smoothscale(player_stand5, (450*rate,500*rate))
    # Player standing 6
    player_stand6 = pygame.image.load("player/stand6.png").convert_alpha()
    player_stand6 = pygame.transform.smoothscale(player_stand6, (450*rate,500*rate))
    
    players_stand = [player_stand1,player_stand2,player_stand3,player_stand4,player_stand5,player_stand6] 
    # Player stand from right:
    # Player stand_right1:
    player_stand_right1 = pygame.image.load("player/stand_right1.png").convert_alpha()
    player_stand_right1 = pygame.transform.smoothscale(player_stand_right1, (450*rate,500*rate))
    # Player stand_right2:
    player_stand_right2 = pygame.image.load("player/stand_right2.png").convert_alpha()
    player_stand_right2 = pygame.transform.smoothscale(player_stand_right2, (450*rate,500*rate))
    # Player stand_rihgt3:
    player_stand_right3 = pygame.image.load("player/stand_right3.png").convert_alpha()
    player_stand_right3 = pygame.transform.smoothscale(player_stand_right3, (450*rate,500*rate))
    # Player stand_right4:
    player_stand_right4 = pygame.image.load("player/stand_right4.png").convert_alpha()
    player_stand_right4 = pygame.transform.smoothscale(player_stand_right4, (450*rate,500*rate))
    # Player stand_right5:
    player_stand_right5 = pygame.image.load("player/stand_right5.png").convert_alpha()
    player_stand_right5 = pygame.transform.smoothscale(player_stand_right5, (450*rate,500*rate))
    # Player stand_right6:
    player_stand_right6 = pygame.image.load("player/stand_right6.png").convert_alpha()
    player_stand_right6 = pygame.transform.smoothscale(player_stand_right6, (450*rate,500*rate))
    players_stand_right = [player_stand_right1,player_stand_right2,player_stand_right3,player_stand_right4,player_stand_right5,player_stand_right6]

    # Player stand_left:
    # Player stand_left1:
    player_stand_left1 = pygame.image.load("player/stand_left1.png").convert_alpha()
    player_stand_left1 = pygame.transform.smoothscale(player_stand_left1, (450*rate,500*rate))
    # Player stand_left2:
    player_stand_left2 = pygame.image.load("player/stand_left2.png").convert_alpha()
    player_stand_left2 = pygame.transform.smoothscale(player_stand_left2, (450*rate,500*rate))
    # Player stand_left3:
    player_stand_left3 = pygame.image.load("player/stand_left3.png").convert_alpha()
    player_stand_left3 = pygame.transform.smoothscale(player_stand_left3, (450*rate,500*rate))
    # Player stand_left4:
    player_stand_left4 = pygame.image.load("player/stand_left4.png").convert_alpha()
    player_stand_left4 = pygame.transform.smoothscale(player_stand_left4, (450*rate,500*rate))
    # Player stand_left5:
    player_stand_left5 = pygame.image.load("player/stand_left5.png").convert_alpha()
    player_stand_left5 = pygame.transform.smoothscale(player_stand_left5, (450*rate,500*rate))
    # Player stand_left5:
    player_stand_left6 = pygame.image.load("player/stand_left6.png").convert_alpha()
    player_stand_left6 = pygame.transform.smoothscale(player_stand_left6, (450*rate,500*rate))
    players_stand_left = [player_stand_left1,player_stand_left2,player_stand_left3,player_stand_left4,player_stand_left5,player_stand_left6]

    # Player stand_back:
    # Player stand_back1:
    player_stand_back1 = pygame.image.load("player/stand_back1.png").convert_alpha()
    player_stand_back1 = pygame.transform.smoothscale(player_stand_back1, (450*rate,500*rate))
    # Player stand_back2:
    player_stand_back2 = pygame.image.load("player/stand_back2.png").convert_alpha()
    player_stand_back2 = pygame.transform.smoothscale(player_stand_back2, (450*rate,500*rate))
    # Player stand_back2:
    player_stand_back3 = pygame.image.load("player/stand_back3.png").convert_alpha()
    player_stand_back3 = pygame.transform.smoothscale(player_stand_back3, (450*rate,500*rate))
    # Player stand_back2:
    player_stand_back4 = pygame.image.load("player/stand_back4.png").convert_alpha()
    player_stand_back4 = pygame.transform.smoothscale(player_stand_back4, (450*rate,500*rate))
    # Player stand_back2:
    player_stand_back5 = pygame.image.load("player/stand_back5.png").convert_alpha()
    player_stand_back5 = pygame.transform.smoothscale(player_stand_back5, (450*rate,500*rate))
    # Player stand_back2:
    player_stand_back6 = pygame.image.load("player/stand_back6.png").convert_alpha()
    player_stand_back6 = pygame.transform.smoothscale(player_stand_back6, (450*rate,500*rate))
    players_stand_back = [player_stand_back1,player_stand_back2,player_stand_back3,player_stand_back4,player_stand_back5,player_stand_back6]

    # Player head:
    # Player head 1
    player_head1 = pygame.image.load("player/head1.png").convert_alpha()
    player_head1 = pygame.transform.smoothscale(player_head1, (450*rate,500*rate))
    # Player head 2
    player_head2 = pygame.image.load("player/head2.png").convert_alpha()
    player_head2 = pygame.transform.smoothscale(player_head2, (450*rate,500*rate))
    # Player head 3
    player_head3 = pygame.image.load("player/head3.png").convert_alpha()
    player_head3 = pygame.transform.smoothscale(player_head3, (450*rate,500*rate))
    # Player head 4
    player_head4 = pygame.image.load("player/head4.png").convert_alpha()
    player_head4 = pygame.transform.smoothscale(player_head4, (450*rate,500*rate))
    # Player head 5
    player_head5 = pygame.image.load("player/head5.png").convert_alpha()
    player_head5 = pygame.transform.smoothscale(player_head5, (450*rate,500*rate))
    # Player head 6
    player_head6 = pygame.image.load("player/head6.png").convert_alpha()
    player_head6 = pygame.transform.smoothscale(player_head6, (450*rate,500*rate))
    players_head = [player_head1,player_head2,player_head3,player_head4,player_head5,player_head6] 

    mouse = pygame.image.load("player/mouse.png").convert_alpha()
    mouse_width, mouse_height = mouse.get_size()
    mouse = pygame.transform.smoothscale(mouse, (mouse_width/11,mouse_height/11))

    player = pygame.image.load("player_mask.png")
    player_rect = player.get_rect()
    player = pygame.image.load("player_mask.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (450*rate,500*rate))
    player_mask = pygame.mask.from_surface(player)   
    # Define the desired coordinates where you want to move the mouse pointer

    # Get the user's screen resolution
    screen_width, screen_height = pyautogui.size()
    # Move the mouse pointer to the scaled target coordinates
    pyautogui.moveTo(width/28*16.5, height/21*1.5)

    # Player run right:
    # Player_right1:
    player_right1 = pygame.image.load("player/right1.png").convert_alpha()
    player_right1 = pygame.transform.smoothscale(player_right1, (450*rate,500*rate))
    # Player_right2:
    player_right2 = pygame.image.load("player/right2.png").convert_alpha()
    player_right2 = pygame.transform.smoothscale(player_right2, (450*rate,500*rate))
    # Player_right3:
    player_right3 = pygame.image.load("player/right3.png").convert_alpha()
    player_right3 = pygame.transform.smoothscale(player_right3, (450*rate,500*rate))
    # Player_right4:
    player_right4 = pygame.image.load("player/right4.png").convert_alpha()
    player_right4 = pygame.transform.smoothscale(player_right4, (450*rate,500*rate))
    # Player_right5:
    player_right5 = pygame.image.load("player/right5.png").convert_alpha()
    player_right5 = pygame.transform.smoothscale(player_right5, (450*rate,500*rate))
    # Player_right6:
    player_right6 = pygame.image.load("player/right6.png").convert_alpha()
    player_right6 = pygame.transform.smoothscale(player_right6, (450*rate,500*rate))
    players_right = [player_right1,player_right2,player_right3,player_right4,player_right5,player_right6]

    # Player run left:
    # Player_left1:
    player_left1 = pygame.image.load("player/left1.png").convert_alpha()
    player_left1 = pygame.transform.smoothscale(player_left1, (450*rate,500*rate))
    # Player_left2:
    player_left2 = pygame.image.load("player/left1.png").convert_alpha()
    player_left2 = pygame.transform.smoothscale(player_left1, (450*rate,500*rate))
    # Player_left3:
    player_left3 = pygame.image.load("player/left3.png").convert_alpha()
    player_left3 = pygame.transform.smoothscale(player_left3, (450*rate,500*rate))
    # Player_left4:
    player_left4 = pygame.image.load("player/left4.png").convert_alpha()
    player_left4 = pygame.transform.smoothscale(player_left4, (450*rate,500*rate))
    # Player_left5:
    player_left5 = pygame.image.load("player/left5.png").convert_alpha()
    player_left5 = pygame.transform.smoothscale(player_left5, (450*rate,500*rate))
    # Player_left6:
    player_left6 = pygame.image.load("player/left6.png").convert_alpha()
    player_left6 = pygame.transform.smoothscale(player_left6, (450*rate,500*rate))
    players_left = [player_left1,player_left2,player_left3,player_left4,player_left5,player_left6]

    # Player run back:
    # Player_back1:
    player_back1 = pygame.image.load("player/back1.png").convert_alpha()
    player_back1 = pygame.transform.smoothscale(player_back1, (450*rate,500*rate))
    # Player_back2:
    player_back2 = pygame.image.load("player/back2.png").convert_alpha()
    player_back2 = pygame.transform.smoothscale(player_back2, (450*rate,500*rate))
    # Player_back3:
    player_back3 = pygame.image.load("player/back3.png").convert_alpha()
    player_back3 = pygame.transform.smoothscale(player_back3, (450*rate,500*rate))
    # Player_back4:
    player_back4 = pygame.image.load("player/back4.png").convert_alpha()
    player_back4 = pygame.transform.smoothscale(player_back4, (450*rate,500*rate))
    # Player_back5:
    player_back5 = pygame.image.load("player/back5.png").convert_alpha()
    player_back5 = pygame.transform.smoothscale(player_back5, (450*rate,500*rate))
    # Player_back6:
    player_back6 = pygame.image.load("player/back6.png").convert_alpha()
    player_back6 = pygame.transform.smoothscale(player_back6, (450*rate,500*rate))
    players_back = [player_back1,player_back2,player_back3,player_back4,player_back5,player_back6]

    # Create fight action:
    # Cut front1:
    attacking = 0
    attack_cooldown = 0
    player_cut_front1 = pygame.image.load("player/cut_front1.png").convert_alpha()
    player_cut_front1 = pygame.transform.smoothscale(player_cut_front1, (450*rate,500*rate))
    # Cut front2:
    player_cut_front2 = pygame.image.load("player/cut_front2.png").convert_alpha()
    player_cut_front2 = pygame.transform.smoothscale(player_cut_front2, (450*rate,500*rate))
    # Cut front3:
    player_cut_front3 = pygame.image.load("player/cut_front3.png").convert_alpha()
    player_cut_front3 = pygame.transform.smoothscale(player_cut_front3, (450*rate,500*rate))
    # Cut front4:
    player_cut_front4 = pygame.image.load("player/cut_front4.png").convert_alpha()
    player_cut_front4 = pygame.transform.smoothscale(player_cut_front4, (450*rate,500*rate))
    players_cut_front = [player_cut_front1,player_cut_front2,player_cut_front3,player_cut_front4]

    # Cut back1:
    player_cut_back1 = pygame.image.load("player/cut_back1.png").convert_alpha()
    player_cut_back1 = pygame.transform.smoothscale(player_cut_back1, (450*rate,500*rate))
    # Cut front2:
    player_cut_back2 = pygame.image.load("player/cut_back2.png").convert_alpha()
    player_cut_back2 = pygame.transform.smoothscale(player_cut_back2, (450*rate,500*rate))
    # Cut front3:
    player_cut_back3 = pygame.image.load("player/cut_back3.png").convert_alpha()
    player_cut_back3 = pygame.transform.smoothscale(player_cut_back3, (450*rate,500*rate))
    # Cut front4:
    player_cut_back4 = pygame.image.load("player/cut_back4.png").convert_alpha()
    player_cut_back4 = pygame.transform.smoothscale(player_cut_back4, (450*rate,500*rate))
    players_cut_back = [player_cut_back1,player_cut_back2,player_cut_back3,player_cut_back4]

    # Cut right1:
    player_cut_right1 = pygame.image.load("player/cut_right1.png").convert_alpha()
    player_cut_right1 = pygame.transform.smoothscale(player_cut_right1, (450*rate,500*rate))
    # Cut right2:
    player_cut_right2 = pygame.image.load("player/cut_right2.png").convert_alpha()
    player_cut_right2 = pygame.transform.smoothscale(player_cut_right2, (450*rate,500*rate))
    # Cut front3:
    player_cut_right3 = pygame.image.load("player/cut_right3.png").convert_alpha()
    player_cut_right3 = pygame.transform.smoothscale(player_cut_right3, (450*rate,500*rate))
    # Cut front4:
    player_cut_right4 = pygame.image.load("player/cut_right4.png").convert_alpha()
    player_cut_right4 = pygame.transform.smoothscale(player_cut_right4, (450*rate,500*rate))
    players_cut_right = [player_cut_right1,player_cut_right2,player_cut_right3,player_cut_right4]

    # Cut left1:
    player_cut_left1 = pygame.image.load("player/cut_left1.png").convert_alpha()
    player_cut_left1 = pygame.transform.smoothscale(player_cut_left1, (450*rate,500*rate))
    # Cut right2:
    player_cut_left2 = pygame.image.load("player/cut_left2.png").convert_alpha()
    player_cut_left2 = pygame.transform.smoothscale(player_cut_left2, (450*rate,500*rate))
    # Cut front3:
    player_cut_left3 = pygame.image.load("player/cut_left3.png").convert_alpha()
    player_cut_left3 = pygame.transform.smoothscale(player_cut_left3, (450*rate,500*rate))
    # Cut front4:
    player_cut_left4 = pygame.image.load("player/cut_left4.png").convert_alpha()
    player_cut_left4 = pygame.transform.smoothscale(player_cut_left4, (450*rate,500*rate))
    players_cut_left = [player_cut_left1,player_cut_left2,player_cut_left3,player_cut_left4]

    # Menu:
    # create start_button:
    start_button = pygame.image.load("start_button.png")
    start_button = pygame.transform.scale(start_button, (width/14,height/21*2))
    start_button_rect = start_button.get_rect() 
    start_button_rect.center = (width/28*13,height/21*1.5)
    start_button_found = True
    # create start collision
    start_button_collision = pygame.image.load("start_collision.png")
    start_button_collision = pygame.transform.scale(start_button_collision, (336*screen_height/252,screen_height))
    start_button_collision_rect = start_button_collision.get_rect()
    start_button_collision_mask = pygame.mask.from_surface(start_button_collision)

    # Map 0 items:
    # Create exit for map0
    end = pygame.image.load("end/end_collision.png")
    end = pygame.transform.scale(end, (336*screen_height/252,screen_height))
    end_rect = end.get_rect()
    end_mask = pygame.mask.from_surface(end)
    
    # Map 1 items:
    # Create exit for map 1
    end1 = pygame.image.load("end/end_collision1.png")
    end1 = pygame.transform.scale(end1, (336*screen_height/252,screen_height))
    end1_rect = end1.get_rect()
    end_mask1 = pygame.mask.from_surface(end1)

    # Create key for player to obtain
    key = pygame.image.load("key.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (40, 40))
    key_rect = key.get_rect()
    key_rect.center = (width/28*21,height/2)
    key_mask = pygame.mask.from_surface(key)
    key_found = False

    # Create the door on top of the exit 'hitbox'
    door = pygame.image.load("door.png").convert_alpha()
    door = pygame.transform.smoothscale(door, (100, 100))
    door_rect = door.get_rect()
    door_rect.center = (width/28*23, height/21*19)

    # Map 2 items:
    # Create real exit 'hitbox' for map 2
    end2_real = pygame.image.load("end/real_end_collision_map2.png")
    end2_real = pygame.transform.scale(end2_real, (336*screen_height/252,screen_height))
    end2_rect = end2_real.get_rect()
    end_mask2 = pygame.mask.from_surface(end2_real)

    # Map 3 items:
    # Create the board 'hitbox'
    board = pygame.image.load("board_collision.png").convert_alpha()
    board = pygame.transform.scale(board, (336*screen_height/252,screen_height))
    board_rect = board.get_rect()
    board_mask = pygame.mask.from_surface(board)

    # Create font
    font = pygame.font.SysFont(None, 20)
    # Define plot box position and size
    plot_box_x = 150
    plot_box_y = 100
    plot_box_width = 500
    plot_box_height = 400

    # Create plot box surface
    plot_box_surface = pygame.Surface((plot_box_width, plot_box_height))
    plot_box_surface.fill((255, 255, 255))
    plot_box_surface.set_alpha(200)

    # Populate plot box with text
    text_lines = ['This is some text in the plot box.', 'It can be multiple lines.', 'Or just one line.']
    text_y = plot_box_y + 10
    for line in text_lines:
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(left=plot_box_x + 10, top=text_y)
        plot_box_surface.blit(text, text_rect)
        text_y += text_rect.height + 5

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    current_head = 'S'
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                is_alive = False
            
        # Create player movement
        # Position the player to the mouse location
        keys = pygame.key.get_pressed()
        # The player will move by mouse cursor if they are not at the final map
        if current_map <= 4:
            pos = pygame.mouse.get_pos()
            player_rect.center = pos
        #The player will move by 'WASD' if they are at the final map
        elif current_map == 5:
            if keys[pygame.K_a]:
                player_rect.move_ip(-7*rate, 0)
                current_head = 'A'
            if keys[pygame.K_d]:
                player_rect.move_ip(7*rate, 0)
                current_head = 'D'
            if keys[pygame.K_w]:
                player_rect.move_ip(0, -7*rate)
                current_head = 'W'
            if keys[pygame.K_s]:
                player_rect.move_ip(0, 7*rate)
                current_head = 'S'
        # Create exit button:
        if keys[pygame.K_ESCAPE]:
            is_alive = False

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, default_mask, default_rect):
            if 1 < current_map <= 4:
                # Comment out this line if you want to go through the walls without losing
                num_deaths += 1
                save_deaths_to_file(num_deaths)
                game_over(width,height,screen,num_deaths)
                restart_game()
                is_alive = False
                pass
            if current_map == 5:
                if keys[pygame.K_a]:
                    player_rect.move_ip(7*rate, 0)
                if keys[pygame.K_d]:
                    player_rect.move_ip(-7*rate, 0)
                if keys[pygame.K_w]:
                    player_rect.move_ip(0, 7*rate)
                if keys[pygame.K_s]:
                    player_rect.move_ip(0, -7*rate)
            # If they player click on the start button, the game will redirect them to the first map
            if current_map == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                current_map += 1
                start_sound_effect.play()
        
        if current_map == 1:
            start_button_found = False
            pyautogui.moveTo(width/28*17.5, height/21*0.5)
            default_map = newmap0
            default_rect = map_rect0
            default_mask = map_mask0
            current_map +=1
        if pixel_collision(player_mask, player_rect, end_mask, end_rect) and current_map == 2:
            complete_sound_effect.play()
            pyautogui.moveTo(width/28*27.5, height/21*1)
            default_map = newmap1
            default_rect = map_rect1
            default_mask = map_mask1
            current_map += 1
        if pixel_collision(player_mask, player_rect,key_mask, key_rect) and current_map == 3:
            collect_sound_effect.play()
            key_found = True

        if pixel_collision(player_mask, player_rect, end_mask1, end1_rect) and current_map == 3 and key_found:
            complete_sound_effect.play()
            pyautogui.moveTo(width/41*27.5, height/21*1)
            default_map = newmap2
            default_rect = map_rect2
            default_mask = map_mask2
            current_map +=1

        if pixel_collision(player_mask, player_rect, end_mask2, end2_rect) and current_map == 4:
            complete_sound_effect.play()
            player_rect.center = (width/28*4,height/21*6.5)
            default_map = newmap3
            default_rect = map_rect3
            default_mask = map_mask3
            current_map += 1
        if pixel_collision(player_mask, player_rect, board_mask, board_rect) and current_map == 5:
            default_map = win
            default_rect = win_rect
            current_map += 1

        # Draw the background
        screen.fill((0,0,0)) 
        screen.blit(default_map, default_rect)

        # Draw the player character
        if current_map == 0:
            screen.blit(mouse, player_rect)
        if keys[pygame.K_s] and attacking == 0 and current_map == 2:
            screen.blit(players_head[int(frame_count)%6], player_rect) 
        elif keys[pygame.K_d] and attacking == 0 and current_map == 2:
            screen.blit(players_right[int(frame_count)%6], player_rect) 
        elif keys[pygame.K_a] and attacking == 0 and current_map == 2:
            screen.blit(players_left[int(frame_count)%6], player_rect)
        elif keys[pygame.K_w] and attacking ==0 and current_map == 2:
            screen.blit(players_back[int(frame_count)%6], player_rect)
        elif current_map >= 1:
            if current_head == 'S' and attacking==0:
                screen.blit(players_stand[int(frame_count)%6], player_rect)
            elif current_head == 'D' and attacking ==0:
                screen.blit(players_stand_right[int(frame_count)%6], player_rect)
            elif current_head == "A" and attacking==0:
                screen.blit(players_stand_left[int(frame_count)%6], player_rect)
            elif current_head == "W" and attacking==0:
                screen.blit(players_stand_back[int(frame_count)%6], player_rect)
        
        if (keys[pygame.K_j] or attacking >0) and attack_cooldown ==0 and current_head=='S':
            if attacking == 0:
                screen.blit(players_cut_front[0], player_rect)
                attacking +=1
            elif attacking ==1:
                screen.blit(players_cut_front[1], player_rect)
                attacking +=1
            elif attacking ==2:
                screen.blit(players_cut_front[2], player_rect)
                attacking +=1
            elif attacking ==3:
                screen.blit(players_cut_front[3], player_rect)
                attacking +=1
            elif attacking ==4:
                screen.blit(players_stand[0], player_rect)
                attacking = 0
                attack_cooldown = 10

        if (keys[pygame.K_j] or attacking >0) and attack_cooldown ==0 and current_head =='W':
            if attacking == 0:
                screen.blit(players_cut_back[0], player_rect)
                attacking +=1
            elif attacking == 1:
                screen.blit(players_cut_back[1], player_rect)
                attacking +=1
            elif attacking ==2:
                screen.blit(players_cut_back[2], player_rect)
                attacking +=1
            elif attacking ==3:
                screen.blit(players_cut_back[3], player_rect)
                attacking +=1
            elif attacking ==4:
                screen.blit(players_stand[0], player_rect)
                attacking = 0
                attack_cooldown = 10

        if (keys[pygame.K_j] or attacking >0) and attack_cooldown ==0 and current_head=="D":
            if attacking == 0:
                screen.blit(players_cut_right[0], player_rect)
                attacking +=1
            elif attacking ==1:
                screen.blit(players_cut_right[1], player_rect)
                attacking +=1
            elif attacking ==2:
                screen.blit(players_cut_right[2], player_rect)
                attacking +=1
            elif attacking ==3:
                screen.blit(players_cut_right[3], player_rect)
                attacking +=1
            elif attacking ==4:
                screen.blit(players_stand[0], player_rect)
                attacking = 0
                attack_cooldown = 10

        if (keys[pygame.K_j] or attacking >0) and attack_cooldown ==0 and current_head=='A':
            if attacking == 0:
                screen.blit(players_cut_left[0], player_rect)
                attacking +=1
            elif attacking ==1:
                screen.blit(players_cut_left[1], player_rect)
                attacking +=1
            elif attacking ==2:
                screen.blit(players_cut_left[2], player_rect)
                attacking +=1
            elif attacking ==3:
                screen.blit(players_cut_left[3], player_rect)
                attacking +=1
            elif attacking ==4:
                screen.blit(players_stand[0], player_rect)
                attacking = 0
                attack_cooldown = 10
        if attack_cooldown > 0:
            attack_cooldown -=1

        if current_map == 3:
            screen.blit(door, door_rect)
        if not key_found and current_map == 3:
            screen.blit(key, key_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.

        # Every time through the loop, increase the frame count.
        frame_count += 0.4

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Start the program
main()
