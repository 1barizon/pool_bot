import pygame
import math




class Ball:
    def __init__(self, pos : pygame.Vector2, color, radius: int):
        self.pos = pos
        self.color = color
        self.radius = radius
        self.vel = pygame.Vector2((0,0))

    def render_ball(self, screen):
        pygame.draw.circle(screen, self.color, self.pos,self.radius) 

    def move(self): 
        # so pode mover se estiver dentro do limite da mesa 
        self.pos.x += self.vel.x
        self.pos.y+= self.vel.y
        # sempre diminuindo a velocidade
        if self.vel.x > 0:
            self.vel.x -= 1
        if self.vel.y > 0:
            self.vel.y -= 1









class Table:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.center_x = self.width//2
        self.center_y = self.height//2
        self.line_width = 10
        self.table_width = 1000
        self.table_height = 500
        self.aim = [[200,200], 0] # pos , angle



    def draw_table(self):
        self.top_left = (self.center_x - self.table_width// 2, self.center_y - self.table_height// 2)
        self.top_right = (self.center_x + self.table_width// 2, self.center_y - self.table_height// 2)
        self.bottom_left = (self.center_x - self.table_width// 2, self.center_y + self.table_height//2)
        self.bottom_right = (self.center_x + self.table_width// 2, self.center_y + self.table_height// 2)
        pygame.draw.line(self.screen, GREEN, self.top_left, self.top_right, self.line_width)
        # Reta Inferior
        pygame.draw.line(self.screen, GREEN, self.bottom_left, self.bottom_right, self.line_width)
        # Reta Esquerda
        pygame.draw.line(self.screen, GREEN, self.top_left, self.bottom_left, self.line_width)
        # Reta Direita
        pygame.draw.line(self.screen, GREEN, self.top_right, self.bottom_right, self.line_width)



    def change_angle(self, click_pos, new_pos):
        if len(click_pos) > 0:
            delta_y = (click_pos[1] - new_pos[1])
            delta_x = (click_pos[0] - new_pos[0])
            angle = 0.00005 * delta_y
            self.aim[1] += angle



    
    def draw_aim(self, origin_point, angle , count): # projecao do ponto
        pygame.draw.circle(self.screen, BLACK, (origin_point), 10, 10)
        # parametrizacao do ponto inicial (self.aim[0])
        # caso de intersecao bordas verticais 
        # 140 = self.aim[0][0] + t * cos(self.aim[1])
        direction_vector = pygame.Vector2(math.cos(angle), math.sin(angle))
        t1, t2, t3, t4 = float("inf") , float("inf"), float("inf"), float("inf") 
       
        p1 = self.top_left[0] # 140
        p2 = self.top_right[0] # 1140
        p3 = self.top_left[1] # 110
        p4 = self.bottom_right[1] # 610
        if direction_vector.x != 0:
            t1 = (p1 - origin_point[0]) / math.cos(angle) # x dentro do limite
            t2 = (p2 - origin_point[0]) / math.cos(angle) # x dentro do limite 
        if direction_vector.y != 0:
            t3 = (p3 - origin_point[1])/ math.sin(angle)
            t4 = (p4 - origin_point[1])/ math.sin(angle)
        
        table_points  = [p1, p2, p3, p4]
 
        T = [t1, t2, t3, t4]
        # gather valid intersection candidates (t, point)
        candidates = []
        left_x, right_x, top_y, bottom_y = p1, p2, p3, p4
        for i, t in enumerate(T):
            # consider only forward intersections
            if not (t > 0 and t != float('inf')):
                continue
            if i == 0 or i == 1:
                px = table_points[i]
                py = origin_point[1] + t * math.sin(angle)
                if top_y <= py <= bottom_y:
                    candidates.append((t, [px, py]))
            else:
                py = table_points[i]
                px = origin_point[0] + t * math.cos(angle)
                if left_x <= px <= right_x:
                    candidates.append((t, [px, py]))

        point = None
        if candidates:
            
            candidates.sort(key=lambda x: x[0])
            point = candidates[0][1] # ponto masi proximo de intersecao

        if point is not None:
            pygame.draw.line(self.screen,(0,0,0) ,origin_point, point, 3)
            if count < 5:
                count += 1
                
                aim_direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                if abs(point[0] - left_x) < 1e-6 or abs(point[0] - right_x) < 1e-6:
                    aim_direction.x *= -1
                if abs(point[1] - top_y) < 1e-6 or abs(point[1] - bottom_y) < 1e-6:
                    aim_direction.y *= -1

                reflected_angle = math.atan2(aim_direction.y, aim_direction.x)
                self.draw_aim(point, reflected_angle, count)



            






 



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Define as cores
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# mouse 
click_pos= []

# game variable
table = Table(screen)
mouse_x , mouse_y = 0, 0
ball0 = Ball(pygame.Vector2(250,250), GREEN,10)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = event.pos
                ball0.vel = pygame.Vector2((10, 10))
        
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = []

    screen.fill(WHITE)

    new_mouse_x, new_mouse_y = pygame.mouse.get_pos()
    if new_mouse_x != mouse_x or new_mouse_y != mouse_y:
           table.change_angle(click_pos, [mouse_x, mouse_y])
           mouse_x , mouse_y = new_mouse_x, new_mouse_y

    
    # render game   
    table.draw_table()
    table.draw_aim(table.aim[0], table.aim[1], 0)
    ball0.render_ball(screen)
    ball0.move()
 
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
