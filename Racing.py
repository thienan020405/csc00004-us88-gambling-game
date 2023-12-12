import pygame
import sys
from random import randint, choice
from operator import attrgetter
from Settings import *

pygame.init()
screen  = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
pygame.display.set_caption('US88')
font = pygame.font.SysFont('Consolas',20)
clock = pygame.time.Clock()
normal1_1 = ['cars/AS87/AS87_1.png', 'cars/NA4/NA4_1.png', 'cars/NA5/NA5_1.png', 'cars/NA6/NA6_1.png', 'cars/NA2/NA2_1.png']
normal1_2 = ['cars/AS87/AS87_2.png', 'cars/NA4/NA4_2.png', 'cars/NA5/NA5_2.png', 'cars/NA6/NA6_2.png', 'cars/NA2/NA2_2.png']
tangtoc1_1 = ['cars/AS87/AS87_tang_toc_1.png', 'cars/NA4/NA4_tang_toc_1.png', 'cars/NA5/NA5_tang_toc_1.png', 'cars/NA6/NA6_tang_toc_1.png', 'cars/NA2/NA2_tang_toc_1.png']
tangtoc1_2 = ['cars/AS87/AS87_tang_toc_2.png', 'cars/NA4/NA4_tang_toc_2.png', 'cars/NA5/NA5_tang_toc_2.png', 'cars/NA6/NA6_tang_toc_2.png', 'cars/NA2/NA2_tang_toc_2.png']
cham1_1 = ['cars/AS87/AS87_cham_1.png', 'cars/NA4/NA4_cham_1.png', 'cars/NA5/NA5_cham_1.png', 'cars/NA6/NA6_cham_1.png', 'cars/NA2/NA2_cham_1.png']
cham1_2 = ['cars/AS87/AS87_cham_2.png', 'cars/NA4/NA4_cham_2.png', 'cars/NA5/NA5_cham_2.png', 'cars/NA6/NA6_cham_2.png', 'cars/NA2/NA2_cham_2.png']
winner = ['cars/AS87/winner.png', 'cars/NA4/winner.png', 'cars/NA5/winner.png', 'cars/NA6/winner.png', 'cars/NA2/winner.png']
set2 = ['xe6.png', 'xe7.png', 'xe8.png', 'xe9.png', 'xe10.png']

final_rank2 = 5
class Car():
    def __init__(self, i, map, leaderboard):
        # general init
        self.order = i
        self.finish = False

        # buff 
        self.duration = 0
        self.start_time = 0
        self.buff = None

        # leaderboard setting up
        self.leaderboard = leaderboard
        self.final_rank1 = 0
        
        self.pos = 1
        self.time = 0
        # assign image to the car
        if map == 1:
            
            surf1 = pygame.image.load(f'{normal1_1[i]}').convert_alpha()
            surf2 = pygame.image.load(f'{normal1_2[i]}').convert_alpha()
            self.surf = [surf1, surf2]
            self.index = 0
            self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))

        self.rect = self.image.get_rect(midleft = (0, i * 100 + 245))
        
        # random speed for each car
        self.sta_speed = randint(1,5)
        self.mid_speed1 = randint(5,10)
        self.mid_speed2 = randint(5,10)
        self.mid_speed3 = randint(7,13)
        self.fin_speed = randint(8,15)

    # return speed with no buff for each car according to timer
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
    
    # return speed without assigning animation
    def return_speed(self):
        if (self.rect.right >= 1280):
            return 0
        if current_time <= self.start_time + self.duration:
            if self.buff == 'bua_tang_toc':
                return self.speed() + 5
            if self.buff == 'bua_cham':
                return self.speed() - 5
            if self.buff == 'bua_di_lui':
                return -5
        return self.speed()

    # return speed and playing animation
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
    
    # car movement
    def movement(self):
        global final_rank2
        # playing winning animation if final rank is 1st
        if self.order == self.leaderboard.ranking[0].order and self.rect.right >= 1280:
                surf1 = pygame.image.load(f'{winner[self.order]}').convert_alpha()
                surf2 = pygame.transform.flip(surf1, True, False)
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))

        # flip the image if buff == 'bua_di_lui'
        if self.buff == 'bua_di_lui': screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else: screen.blit(self.image,self.rect)

        # move car to the right
        self.rect.right += (self.check_buff())

        # check if touching the screen border
        if(self.rect.right >= 1280):
            self.finish = True
            self.rect.right = 1280
            # saving final_rank for sorting the leaderboard if multiple cars have self.rect.right = 1280
            if self.time == 0:
                self.time = real_time
            if self.final_rank1 == 0:
                self.final_rank1 = final_rank2
                final_rank2 -= 1
        
        # saving pos for sorting the leaderboard
        self.pos = self.rect.right
    
    # playing animation
    def animation_state(self):
        self.index += 0.1
        if self.index  >= len(self.surf): self.index = 0
        self.image = pygame.transform.scale(self.surf[int(self.index)], (100, 65))

    # update function for car class
    def update(self):
        self.movement()
        self.animation_state()


class Mystery(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        mystery = [1, 2, 3]
        self.image = pygame.image.load(f'mystery/mystery{choice(mystery)}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect(midleft = (x_pos, y_pos))

    # assign buff attribute to the car
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
        car.duration = 1
        car.start_time = current_time
    
    # check collistion between the car and mystery box
    # random the buff
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

    # update function for Mystery class
    def update(self, car):
        self.collide(car)

    
class Leaderboard():
    def __init__(self, cars_name):
        self.ranking = []
        self.cars_name = cars_name
        self.order = []
    
    # append all the car to the leaderboard
    def append(self, car, i):
        self.ranking.append(car)
        self.order.append(i)
    
    # sort the leaderboard
    def sort(self):
        self.ranking = sorted(self.ranking, key = attrgetter('final_rank1', 'pos'), reverse = True)
    

    def update(self):
        self.sort()
        # blit leaderboard stats to the screen
        if self.ranking:
            # blit unchanged stats
            maps_x = 50
            for i in range(5):
                text_surf = font.render(f'Làn {i + 1}: ',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, 25))
                profile_border = pygame.image.load('Profile Border.png').convert_alpha()
                profile_border = pygame.transform.scale(profile_border, (230, 150))
                profile_bg = pygame.image.load('Profile BackGround.png').convert_alpha()
                profile_bg = pygame.transform.scale(profile_bg, (230, 150))
                profile_bg.set_alpha(120)
                screen.blit(profile_border, (text_rect.x - 15 , text_rect.y - 15))
                screen.blit(profile_bg, (text_rect.x - 15 , text_rect.y - 15))
                screen.blit(text_surf, text_rect)

                text_surf = font.render(f'{self.cars_name[i]}',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, 50))
                screen.blit(text_surf, text_rect)

                car_surf = pygame.image.load(f'{normal1_1[self.order[i]]}').convert_alpha()
                car_surf = pygame.transform.scale(car_surf, (75, 50))
                car_rect = car_surf.get_rect(topright = (maps_x + 200, 25))
                screen.blit(car_surf, car_rect)
                maps_x += 250
            
            # blit changed stats
            for j in range(5):
                maps_x = 50 + self.ranking[j].order * 250
                s = f'Hạng: {j + 1}'
                if j + 1 == 1:
                    s = s + 'st'
                elif j + 1 == 2:
                    s = s + 'nd'
                elif j + 1 == 3:
                    s = s + 'rd'
                else: s = s + 'th'
                text_surf = font.render(s,False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, 75))
                screen.blit(text_surf, text_rect)
                if self.ranking[j].buff == None:
                    text_surf = font.render(f'Hiệu ứng: không có',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, 100))
                elif self.ranking[j].buff == 'bua_tang_toc':
                    text_surf = font.render(f'Hiệu ứng: tăng tốc',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, 100))
                elif self.ranking[j].buff == 'bua_cham':
                    text_surf = font.render(f'Hiệu ứng: chậm',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, 100))
                elif self.ranking[j].buff == 'bua_di_lui':
                    text_surf = font.render(f'Hiệu ứng: đi lùi',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, 100))
                screen.blit(text_surf, text_rect)
                text_surf = font.render(f'Tốc độ: {self.ranking[j].return_speed()}',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, 125))
                screen.blit(text_surf, text_rect)



class Background():
    def __init__(self, map_number):

        self.sky_surf = pygame.image.load(f'maps/sky{map_number}.png').convert()
        self.sky_rect = self.sky_surf.get_rect(topleft = (0,0))

        self.racetrack_surf = pygame.image.load(f'maps/racetrack{map_number}.jpg').convert()
        self.racetrack_rect = self.racetrack_surf.get_rect(topleft = (0, 170))
    
        self.fin_surf = pygame.image.load('finish_line.jpg').convert()
        self.fin_rect = self.fin_surf.get_rect(bottomright = (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.max_pos = 0
        self.max_speed = 0
        self.count = 0
        self.amount = 0
    
    
    def update(self):
        screen.blit(self.sky_surf, self.sky_rect)

        screen.blit(self.racetrack_surf, self.racetrack_rect)

        screen.blit(self.fin_surf, self.fin_rect)

class AfterRace():
    def __init__(self, car1, car2, car3, car4, car5, leaderboard, chosen_car, coin_betted, cars_name):
        
        self.stage_surf = pygame.image.load('stage.png').convert_alpha()
        self.stage_surf = pygame.transform.scale_by(self.stage_surf, 1.5)
        self.stage_rect = self.stage_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))

        self.stage_bg_surf = pygame.image.load('ChoosingCarBackground.png').convert_alpha()
        self.stage_bg_rect = self.stage_bg_surf.get_rect(topleft = (0,0))

        # button to ldb screen
        self.button1_surf = pygame.image.load('wodden_button.png').convert_alpha()
        self.button1_rect = self.button1_surf.get_rect(bottomright = (1280,720))

        # button to noti screen
        self.button2_surf = pygame.image.load('wodden_button.png').convert_alpha()
        self.button2_rect = self.button2_surf.get_rect(bottomright = (1280,720))
        
        self.ldb_surf = pygame.image.load('ldb.png').convert_alpha()
        self.ldb_rect = self.ldb_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        self.noti_surf = pygame.image.load('notification.png').convert_alpha()
        self.noti_rect = self.noti_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        self.cam_surf = pygame.image.load('cam_button.png').convert_alpha()
        self.cam_rect = self.cam_surf.get_rect(topleft = (1188, 21))

        self.ok_surf = pygame.image.load('wodden_button.png').convert_alpha()
        self.ok_rect = self.ok_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 175))
        self.stage = True
        self.ldb = False
        self.noti = False
        self.car1 = car1
        self.car2 = car2
        self.car3 = car3
        self.car4 = car4
        self.car5 = car5

        self.leaderboard = leaderboard
        self.chosen_car = chosen_car
        self.coin_betted = coin_betted
        self.cars_name = cars_name
    def run(self):
        state = 'Win'
        ldb_active = True
        while ldb_active:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if self.button2_rect.collidepoint(mouse_pos) and self.stage == False and self.noti == False:
                            self.stage = False
                            self.ldb = False
                            self.noti = True
                        
                        if self.button1_rect.collidepoint(mouse_pos) and self.ldb == False and self.noti == False:
                            self.stage = False
                            self.ldb = True
                            self.noti = False
                        
                        if self.ok_rect.collidepoint(mouse_pos):
                            if state == 'Win':
                                return True
                            else:
                                return False
                        
                        
                    
            if self.stage:
                screen.blit(self.stage_bg_surf, self.stage_bg_rect)
                screen.blit(self.stage_surf, self.stage_rect)
                screen.blit(self.button1_surf, self.button1_rect)
                screen.blit(self.cam_surf, self.cam_rect)
                if self.car1.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal1_1[0]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (65, 65))
                    first_rect = first_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 125))
                elif self.car1.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal1_1[0]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (65, 65))
                    second_rect = second_surf.get_rect(center = (WINDOW_WIDTH/2 - 175, WINDOW_HEIGHT/2 - 35))
                elif self.car1.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal1_1[0]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (65, 65))
                    third_rect = third_surf.get_rect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT/2 - 35))

                if self.car2.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal1_1[1]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (65, 65))
                    first_rect = first_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 125))
                elif self.car2.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal1_1[1]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (65, 65))
                    second_rect = second_surf.get_rect(center = (WINDOW_WIDTH/2 - 175, WINDOW_HEIGHT/2 - 35))
                elif self.car2.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal1_1[1]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (65, 65))
                    third_rect = third_surf.get_rect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT/2 - 35))
                
                if self.car3.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal1_1[2]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (65, 65))
                    first_rect = first_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 125))
                elif self.car3.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal1_1[2]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (65, 65))
                    second_rect = second_surf.get_rect(center = (WINDOW_WIDTH/2 - 175, WINDOW_HEIGHT/2 - 35))
                elif self.car3.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal1_1[2]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (65, 65))
                    third_rect = third_surf.get_rect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT/2 - 35))

                if self.car4.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal1_1[3]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (65, 65))
                    first_rect = first_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 125))
                elif self.car4.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal1_1[3]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (65, 65))
                    second_rect = second_surf.get_rect(center = (WINDOW_WIDTH/2 - 175, WINDOW_HEIGHT/2 - 35))
                elif self.car4.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal1_1[3]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (65, 65))
                    third_rect = third_surf.get_rect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT/2 - 35))

                if self.car5.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal1_1[4]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (65, 65))
                    first_rect = first_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 125))
                elif self.car5.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal1_1[4]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (65, 65))
                    second_rect = second_surf.get_rect(center = (WINDOW_WIDTH/2 - 175, WINDOW_HEIGHT/2 - 35))
                elif self.car5.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal1_1[4]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (65, 65))
                    third_rect = third_surf.get_rect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT/2 - 35))

                screen.blit(first_surf, first_rect)
                screen.blit(second_surf, second_rect)
                screen.blit(third_surf, third_rect)
             
            if self.ldb:
                screen.blit(self.stage_bg_surf, self.stage_bg_rect)
                screen.blit(self.ldb_surf, self.ldb_rect)
                screen.blit(self.button2_surf, self.button2_rect)
                screen.blit(self.cam_surf, self.cam_rect)
                for i in range(5):
                    img_surf = pygame.image.load(f'{normal1_1[self.leaderboard.ranking[i].order]}').convert_alpha()
                    img_surf = pygame.transform.scale(img_surf, (150, 50))
                    img_rect = img_surf.get_rect(center = (550, 275 + i * 75))
                    screen.blit(img_surf, img_rect)
                    text_surf = font.render(f'{self.cars_name[self.leaderboard.ranking[i].order]}', False, 'Red')
                    text_rect = text_surf.get_rect(center = (700, 275 + i * 75))
                    screen.blit(text_surf, text_rect)
                    text_surf = font.render(f'{self.leaderboard.ranking[i].time}ms', False, 'Red')
                    text_rect = text_surf.get_rect(center = (850, 275 + i * 75))
                    screen.blit(text_surf, text_rect)
            
            if self.noti:
                screen.blit(self.stage_bg_surf, self.stage_bg_rect)
                screen.blit(self.noti_surf, self.noti_rect)
                screen.blit(self.cam_surf, self.cam_rect)
                screen.blit(self.ok_surf, self.ok_rect)
                text_surf = font.render('THÔNG BÁO', False, 'Red')
                text_surf = pygame.transform.scale_by(text_surf, 2)
                text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 120))
                screen.blit(text_surf, text_rect)
                if self.car1.final_rank1 == 5 and self.chosen_car == 1:
                    text_surf = font.render('BẠN ĐÃ CHIẾN THẮNG', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    screen.blit(text_surf, text_rect)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    
                elif self.car2.final_rank1 == 5 and self.chosen_car == 2:
                    text_surf = font.render('BẠN ĐÃ CHIẾN THẮNG', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    screen.blit(text_surf, text_rect)
                    
                elif self.car3.final_rank1 == 5 and self.chosen_car == 3:
                    text_surf = font.render('BẠN ĐÃ CHIẾN THẮNG', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    screen.blit(text_surf, text_rect)

                elif self.car4.final_rank1 == 5 and self.chosen_car == 4:
                    text_surf = font.render('BẠN ĐÃ CHIẾN THẮNG', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    screen.blit(text_surf, text_rect)

                elif self.car5.final_rank1 == 5 and self.chosen_car == 5:
                    text_surf = font.render('BẠN ĐÃ CHIẾN THẮNG', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    screen.blit(text_surf, text_rect)

                else:
                    state = 'Lose'
                    text_surf = font.render('BẠN ĐÃ THẤT BẠI', False, 'Red')
                    text_surf = pygame.transform.scale_by(text_surf, 2)
                    text_rect = text_surf.get_rect(center = (self.noti_rect.centerx, self.noti_rect.centery - 50))
                    screen.blit(text_surf, text_rect)
                
            pygame.display.update()
            clock.tick(60)



class Racing():
    def __init__(self, cars_name, map_number, chosen_car, coin_betted):
        # init the rank
        self.final_rank = 5 

        self.chosen_car = chosen_car
        self.coin_betted = coin_betted

        # init the timer for the buff
        self.start_time = pygame.time.get_ticks()
        self.current_time = 0

        # assign the names into the game
        self.cars_name = cars_name
        self.leaderboard = Leaderboard(self.cars_name)

        # init the background
        self.bg = Background(map_number)

        # init cars
        self.car1 = Car(0,1, self.leaderboard)
        self.car2 = Car(1,1, self.leaderboard)
        self.car3 = Car(2,1, self.leaderboard)
        self.car4 = Car(3,1, self.leaderboard)
        self.car5 = Car(4,1, self.leaderboard)
        
        # push cars into leaderboard
        self.leaderboard.append(self.car1, 0)
        self.leaderboard.append(self.car2, 1)
        self.leaderboard.append(self.car3, 2)
        self.leaderboard.append(self.car4, 3)
        self.leaderboard.append(self.car5, 4)

        # blit mystery box randomly on the screen
        self.mystery_list = pygame.sprite.Group()
        for i in range(5):
            self.mystery_list.add(Mystery(randint(250, 350), i * 100 + 245))
        for i in range(5):
            self.mystery_list.add(Mystery(randint(700, 900), i * 100 + 245))

        # notification
        self.noti_surf = pygame.image.load('notification.png').convert_alpha()
        self.noti_rect = self.noti_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        
    # timer
    def display_time(self):
        global current_time, real_time
        real_time = pygame.time.get_ticks()  - self.start_time
        current_time = int(pygame.time.get_ticks() / 1000)  - int(self.start_time/1000) 
        print(real_time)

    # blit map
    def display_map(self):
        self.bg.update()

    def run(self):       
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # blit the background and timer   
            self.display_map()
            self.display_time()

            # draw mystery and update collision 
            self.mystery_list.draw(screen)
            self.mystery_list.update(self.car1)
            self.mystery_list.update(self.car2)
            self.mystery_list.update(self.car3)
            self.mystery_list.update(self.car4)
            self.mystery_list.update(self.car5)

            # update the leaderboard
            self.leaderboard.update()

            # update car movement
            self.car1.update()
            self.car2.update()
            self.car3.update()
            self.car4.update()
            self.car5.update()

            print(self.car1.finish, self.car2.finish, self.car3.finish, self.car4.finish, self.car5.finish)
            # blit stage and leaderboard
            if(self.car1.finish and self.car2.finish and self.car3.finish and self.car4.finish and self.car5.finish):
                self.after = AfterRace(self.car1, self.car2, self.car3, self.car4,self.car5, self.leaderboard, self.chosen_car, self.coin_betted, self.cars_name)
                global final_rank2
                final_rank2 = 5
                if self.after.run():
                    return self.coin_betted
                else:
                    return -self.coin_betted
                
            pygame.display.update()
            clock.tick(60)
        
        
