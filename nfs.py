#на зачете надо будет дописать в прогу заданное преподавателем

#Добавить боольше полос, боты двигаются по правилам, боты обгоняют


import pygame

background1 = pygame.image.load('background.png')
background2 = pygame.image.load('background.png')
car_sprite = pygame.image.load('car.png')
enemy_car_down  = pygame.image.load('car_red2.png')
enemy_car_up  = pygame.image.load('car_red1.png')

display_w = 800
display_h = 600
game_exit = False

pygame.init()
my_font = pygame.font.Font("Pixel.ttf", 24)
game_display = pygame.display.set_mode((display_w, display_h))

background_y = 0
world_speed = 0
car_line = 1 
space = False
score = 0

pygame.display.set_caption('Need for Speed')
clock = pygame.time.Clock()

class car:
    image = None
    line = 1
    speed = 0
    car_y = 400

    def __init__(self, image, line = 1, speed = 0 , car_y = 400):
        self.image = image
        self.line = line
        self.speed = speed
        self.car_y = car_y
                     
class player_car(car):
    def __init__(self):
        self.image = car_sprite
        self.line = 1
        self.speed = 0
        self.car_y = 400
        
    def draw(this):
        global world_speed, space, score
        score += world_speed/100
        if space:
            world_speed -= 2
            if world_speed < 0:
                world_speed = 0
        game_display.blit(this.image, (335 + this.line * 75, this.car_y))        
        
class enemy_car(car):
    direction = 0 
    visible = False
    
    def __init__(self,direction, line = 1, speed = 1):
            self.direction = direction
            if direction == 0 :
                self.image = enemy_car_down
                self.car_y = -100
            else:
                self.image = enemy_car_up
                self.car_y = display_h + 30
            self.line = line
            self.speed = speed
            
    def draw(this):
        if this.visible:
            game_display.blit(this.image, (335 + this.line * 75, this.car_y))
            if this.direction == 0 :
                this.car_y += this.speed + world_speed
            else:
                this.car_y -= this.speed + world_speed
                
            if (this.car_y > display_h+30) or (this.car_y < -100):
                    this.visible = False
    
    def reset(this):
        import random
        this.visible = True
        this.speed = random.randint(1,5)
        this.direction = random.randint(0,1)
        this.line = random.randint(0,1)
        
        if this.direction == 0 :
            this.image = enemy_car_down
            this.car_y = -100
        else:
            this.image = enemy_car_up
            this.car_y = display_h + 30        
            
    def collide_check(this, car2):
        if this.visible:
            car_rect = this.image.get_rect().move(335 + this.line * 75, this.car_y)
            car2_rect = car2.image.get_rect().move(335 + car2.line * 75, car2.car_y)
            
            if car_rect.colliderect(car2_rect):
                this.visible = False
                return True
            return False
            
player = player_car()
enemys_cars = [enemy_car(0), enemy_car(0), enemy_car(0), enemy_car(0)]

def draw_enemys():
    global score
    import random
    
    for car in enemys_cars:
        if car.visible == False:
            if random.randint(1,200) == 50:
                car.reset()
        if car.collide_check(player):
            score -= 20
            
    for car in enemys_cars:
        car.draw()

def draw_background():
    global background_y
    
    game_display.blit(background1, (0, background_y))
    game_display.blit(background1, (0, background_y - 2352))
    background_y += world_speed
    
    if background_y >= display_h:
        background_y = display_h - 2352
        
def draw_ui():
    global score
    
    text_image = my_font.render("Score:" + str(int(score)), True, (255,255,255))
    game_display.blit(text_image, (10,10))

def process_keyboard(event):
    global player, world_speed, space
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            if world_speed != 0:
                player.line = 0
        if event.key == pygame.K_RIGHT:
            if world_speed != 0:
                player.line = 1
            
        if event.key == pygame.K_UP:
            if world_speed == 40:
                world_speed += 0
            else:
                world_speed += 5
                
        if event.key == pygame.K_DOWN:
            if world_speed == 5:
                world_speed -= 0
            else:
                world_speed -= 5
        
        if event.key == pygame.K_SPACE:
            space = not(space)
              
def game_loop(update_time):
    global game_exit, score

    while not game_exit:
        for event in pygame.event.get():
            process_keyboard(event)
            if event.type == pygame.QUIT:
                game_exit = True
                quit()
                
        draw_background()
        player.draw()
        draw_enemys()
        draw_ui()
        pygame.display.update()
        clock.tick(update_time)

game_loop(30)
pygame.quit()
quit()

