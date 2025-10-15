import pygame
import math

class Table:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.center_x = self.width//2
        self.center_y = self.height//2
        self.line_width = 10
        self.table_width = 1000
        self.table_height = 500
        self.aim = [[200,200], (0.001)] # pos , angle



    def draw_table(self):
        self.top_left = (self.center_x - self.table_width// 2, self.center_y - self.table_height// 2)
        self.top_right = (self.center_x + self.table_width// 2, self.center_y - self.table_height// 2)
        self.bottom_left = (self.center_x - self.table_width// 2, self.center_y + self.table_height//2)
        self.bottom_right = (self.center_x + self.table_width// 2, self.center_y + self.table_height// 2)

        pygame.draw.line(screen, GREEN, self.top_left, self.top_right, self.line_width)
        # Reta Inferior
        pygame.draw.line(screen, GREEN, self.bottom_left, self.bottom_right, self.line_width)
        # Reta Esquerda
        pygame.draw.line(screen, GREEN, self.top_left, self.bottom_left, self.line_width)
        # Reta Direita
        pygame.draw.line(screen, GREEN, self.top_right, self.bottom_right, self.line_width)
        #print(self.top_left, self.top_right, self.bottom_left, self.bottom_right)

    def change_angle(self, click_pos, new_pos):
        if len(click_pos) > 0:
            delta_y = (click_pos[1] - new_pos[1])
            delta_x = (click_pos[0] - new_pos[0])
            angle = math.atan2(delta_y, delta_x)
            self.aim[1] = angle


    
    def draw_aim(self): # projecao do ponto
        pygame.draw.circle(self.screen, BLACK, (self.aim[0]), 10, 10)
        # parametrizacao do ponto inicial (self.aim[0])
        angle = self.aim[1] 
        # caso de intersecao bordas verticais 
        # 140 = self.aim[0][0] + t * cos(self.aim[1])

        p1 = self.top_left[0] # 140
        t1 = (p1 - self.aim[0][0]) / math.cos(angle) # x dentro do limite


        p2 = self.top_right[0] # 1140
        t2 = (p2 - self.aim[0][0]) / math.cos(angle) # x dentro do limite 

        p3 = self.top_left[1] # 110
        t3 = (p3 - self.aim[0][1])/ math.sin(angle)

        p4 = self.bottom_right[1] # 610
        t4 = (p4 - self.aim[0][1])/ math.sin(angle)
        
        origin_points = [p1, p2, p3, p4 ]
        T = [t1, t2, t3, t4]
        point = []
        for t in T:
            if t < 0:
                pass
            elif T.index(t) == 0 or T.index(t) == 1:
                py = self.aim[0][1] + t * math.sin(angle) # se 110 < y < 610
                px = origin_points[T.index(t)]
                if py < 110 or py > 610:
                    pass
                else:
                    point=[px, py]
            elif T.index(t) == 2 or T.index(t) == 3:
                px = self.aim[0][0] + t * math.cos(angle) # se 110 < y < 610
                py = origin_points[T.index(t)]
                if px < 110 or px > 610:
                    pass
                else:
                    point=[px, py]
 

        print(point) 


        pygame.draw.line(self.screen,(0,0,0) ,self.aim[0], point, 3)


            





 



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


table = Table(screen)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = event.pos
                print(f"cliclado em {click_pos}")
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = []

    screen.fill(WHITE)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # render game   
    table.draw_table()
    table.draw_aim()
    table.change_angle(click_pos, [mouse_x, mouse_y])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
