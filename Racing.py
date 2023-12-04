import pygame
from random import randint, choice
from operator import attrgetter
from Settings import *

pygame.init()
screen  = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
pygame.display.set_caption('US88')
font = pygame.font.SysFont('Consolas',30)

normal1_1 = ['cars/AS87/AS87_1.png', 'cars/NA4/NA4_1.png', 'cars/NA5/NA5_1.png', 'cars/NA6/NA6_1.png', 'cars/NA2/NA2_1.png']
normal1_2 = ['cars/AS87/AS87_2.png', 'cars/NA4/NA4_2.png', 'cars/NA5/NA5_2.png', 'cars/NA6/NA6_2.png', 'cars/NA2/NA2_2.png']
tangtoc1_1 = ['cars/AS87/AS87_tang_toc_1.png', 'cars/NA4/NA4_tang_toc_1.png', 'cars/NA5/NA5_tang_toc_1.png', 'cars/NA6/NA6_tang_toc_1.png', 'cars/NA2/NA2_tang_toc_1.png']
tangtoc1_2 = ['cars/AS87/AS87_tang_toc_2.png', 'cars/NA4/NA4_tang_toc_2.png', 'cars/NA5/NA5_tang_toc_2.png', 'cars/NA6/NA6_tang_toc_2.png', 'cars/NA2/NA2_tang_toc_2.png']
cham1_1 = ['cars/AS87/AS87_cham_1.png', 'cars/NA4/NA4_cham_1.png', 'cars/NA5/NA5_cham_1.png', 'cars/NA6/NA6_cham_1.png', 'cars/NA2/NA2_cham_1.png']
cham1_2 = ['cars/AS87/AS87_cham_2.png', 'cars/NA4/NA4_cham_2.png', 'cars/NA5/NA5_cham_2.png', 'cars/NA6/NA6_cham_2.png', 'cars/NA2/NA2_cham_2.png']
winner = ['cars/AS87/winner.png', 'cars/NA4/winner.png', 'cars/NA5/winner.png', 'cars/NA6/winner.png', 'cars/NA2/winner.png']
set2 = ['xe6.png', 'xe7.png', 'xe8.png', 'xe9.png', 'xe10.png']

class Car():
    def __init__(self, i, map, leaderboard, final_rank):
        self.order = i
        self.final_rank1 = 0
        self.final_rank2 = final_rank
        self.pos = 1
        self.duration = 0
        self.start_time = 0
        self.buff = None

        self.leaderboard = leaderboard
        
        if map == 1:
            surf1 = pygame.image.load(f'{normal1_1[i]}').convert_alpha()
            surf2 = pygame.image.load(f'{normal1_2[i]}').convert_alpha()
            self.surf = [surf1, surf2]
            self.index = 0
            self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))

        self.rect = self.image.get_rect(midleft = (0, i * 100 + 245))

        self.sta_speed = randint(1,5)
        self.mid_speed1 = randint(5,10)
        self.mid_speed2 = randint(5,10)
        self.mid_speed3 = randint(7,13)
        self.fin_speed = randint(8,15)

    def speed(self):
        if current_time <= 1:
            return self.sta_speed
        elif current_time <= 5:
            return self.mid_speed1
        elif current_time <= 10:
            return self.mid_speed2
        elif current_time <= 15:
            return self.mid_speed3
        else: return self.fin_speed
    
    def return_speed(self):
        if current_time <= self.start_time + self.duration:
            if self.buff == 'bua_tang_toc':
                return self.speed() + 5
            if self.buff == 'bua_cham':
                return self.speed() - 5
            if self.buff == 'bua_di_lui':
                return -5
        return self.speed()

    def check_buff(self):
        if current_time <= self.start_time + self.duration:
            if self.buff == 'bua_tang_toc':
                surf1 = pygame.image.load(f'{tangtoc1_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{tangtoc1_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
                if current_time == self.start_time + self.duration: self.buff = None
                return self.speed() + 5
            if self.buff == 'bua_cham':
                surf1 = pygame.image.load(f'{cham1_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{cham1_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
                if current_time == self.start_time + self.duration: self.buff = None
                return self.speed() - 5
            if self.buff == 'bua_di_lui':
                surf1 = pygame.image.load(f'{normal1_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{normal1_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
                if current_time == self.start_time + self.duration: self.buff = None
                return -5
        surf1 = pygame.image.load(f'{normal1_1[self.order]}').convert_alpha()
        surf2 = pygame.image.load(f'{normal1_2[self.order]}').convert_alpha()
        self.surf = [surf1, surf2]
        self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
        return self.speed()
    
    def movement(self):
        # global final_rank
        if self.order == self.leaderboard.ranking[0].order and self.rect.right >= 1280:
                surf1 = pygame.image.load(f'{winner[self.order]}').convert_alpha()
                surf2 = pygame.transform.flip(surf1, True, False)
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
        if self.buff == 'bua_di_lui': screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else: screen.blit(self.image,self.rect)
        self.rect.right += (self.check_buff())
        if(self.rect.right >= 1280):
            self.rect.right = 1280
            if self.final_rank1 == 0:
                self.final_rank1 = self.final_rank2
                self.final_rank2 -= 1
        self.pos = self.rect.right
    
    def animation_state(self):
        self.index += 0.1
        if self.index  >= len(self.surf): self.index = 0
        self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))
    def update(self):
        self.movement()
        self.animation_state()


class Mystery(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load('mystery.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect(midleft = (x_pos, y_pos))

    def bua_tang_toc(self, car):
        car.buff = 'bua_tang_toc'
        car.duration = 3
        car.start_time = current_time

    def bua_cham(self, car):
        car.buff = 'bua_cham'
        car.duration = 3
        car.start_time = current_time

    def bua_di_lui(self, car):
        car.buff = 'bua_di_lui'
        car.duration = 3
        car.start_time = current_time
    
    def collide(self, car):
        if self.rect.colliderect(car.rect):
            random = choice(['bua_cham', 'bua_di_lui', 'bua_tang_toc'])
            if random == 'bua_tang_toc':
                self.bua_tang_toc(car)
            elif random == 'bua_cham':
                self.bua_cham(car)
            elif random == 'bua_di_lui':
                self.bua_di_lui(car)
            self.kill()


    def update(self, car):
        self.collide(car)

    
class Leaderboard():
    def __init__(self, cars_name):
        self.ranking = []
        self.cars_name = cars_name
        
    
    def append(self, car):
        self.ranking.append(car)
    
    def sort(self):
        self.ranking = sorted(self.ranking, key = attrgetter('final_rank1', 'pos'), reverse = True)
    
    def update(self):
        self.sort()
        if self.ranking:
            maps_x = 140

            # for i in range(5):
            #     pygame.draw.rect(screen, 'White', (0, 0, 60, 40))
            for i in range(5):
                text_surf = font.render(f'{self.cars_name[self.ranking[i].order]}',False,'Red')
                text_rect = text_surf.get_rect(topright = (1280,i*35))
                screen.blit(text_surf, text_rect)

class Background():
    def __init__(self, map_number):

        self.sky_surf = pygame.image.load(f'maps/sky{map_number}.png').convert()
        self.sky_rect1 = self.sky_surf.get_rect(topleft = (0,0))
        self.sky_rect2 = self.sky_surf.get_rect(topleft = (self.sky_surf.get_width(),0))

        self.racetrack_surf = pygame.image.load(f'maps/racetrack{map_number}.jpg').convert()
        self.racetrack_rect1 = self.racetrack_surf.get_rect(topleft = (0, 170))
        self.racetrack_rect2 = self.racetrack_surf.get_rect(topleft = (self.racetrack_surf.get_width(), 170))
    
        self.max_pos = 0
        self.max_speed = 0
        self.count = 0
        self.amount = 0
    
        
    
    def update(self):
        screen.blit(self.sky_surf, self.sky_rect1)
        screen.blit(self.sky_surf, self.sky_rect2)
        screen.blit(self.racetrack_surf, self.racetrack_rect1)
        screen.blit(self.racetrack_surf, self.racetrack_rect2)


class Racing():
    def __init__(self, cars_name, map_number):

        self.final_rank = 5 
        self.start_time = 0
        self.current_time = 0

        
        self.cars_name = cars_name
        self.leaderboard = Leaderboard(self.cars_name)
        
        self.bg = Background(map_number)

        self.car1 = Car(0,1, self.leaderboard,self.final_rank)
        self.car2 = Car(1,1, self.leaderboard,self.final_rank)
        self.car3 = Car(2,1, self.leaderboard,self.final_rank)
        self.car4 = Car(3,1, self.leaderboard,self.final_rank)
        self.car5 = Car(4,1, self.leaderboard,self.final_rank)
        
        

        self.leaderboard.append(self.car1)
        self.leaderboard.append(self.car2)
        self.leaderboard.append(self.car3)
        self.leaderboard.append(self.car4)
        self.leaderboard.append(self.car5)

        self.mystery_list = pygame.sprite.Group()
        for i in range(5):
            self.mystery_list.add(Mystery(randint(250, 350), i * 100 + 245))
        for i in range(5):
            self.mystery_list.add(Mystery(randint(700, 900), i * 100 + 245))

    def display_time(self):
        global current_time
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        time_surf = font.render(f'Score: {current_time}',False,(64,64,64))
        time_rect = time_surf.get_rect(topleft = (0,0))
        screen.blit(time_surf, time_rect)

    def get_max(self):
        self.bg.max_pos = 0
        self.bg.max_pos = max(self.bg.max_pos, self.car1.rect.right)
        self.bg.max_pos = max(self.bg.max_pos, self.car2.rect.right)
        self.bg.max_pos = max(self.bg.max_pos, self.car3.rect.right)
        self.bg.max_pos = max(self.bg.max_pos, self.car4.rect.right)
        self.bg.max_pos = max(self.bg.max_pos, self.car5.rect.right)

        self.bg.max_speed = 0
        self.bg.max_speed = max(self.bg.max_speed, self.car1.return_speed())
        self.bg.max_speed = max(self.bg.max_speed, self.car2.return_speed())
        self.bg.max_speed = max(self.bg.max_speed, self.car3.return_speed())
        self.bg.max_speed = max(self.bg.max_speed, self.car4.return_speed())
        self.bg.max_speed = max(self.bg.max_speed, self.car5.return_speed())

    def display_map(self):
        self.bg.update()

    def run(self):           
        self.display_map()

        self.display_time()
        self.get_max()


        self.mystery_list.draw(screen)
        self.mystery_list.update(self.car1)
        self.mystery_list.update(self.car2)
        self.mystery_list.update(self.car3)
        self.mystery_list.update(self.car4)
        self.mystery_list.update(self.car5)

        self.leaderboard.update()
        self.car1.update()
        self.car2.update()
        self.car3.update()
        self.car4.update()
        self.car5.update()
        
        
