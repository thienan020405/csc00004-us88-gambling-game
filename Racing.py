import pygame
import sys
from random import randint, choice
from operator import attrgetter
from Settings import *
import os
from tesseract import tesseract_OCR

pygame.init()
screen  = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('US88')
font = pygame.font.SysFont('Consolas',20)
noti_font = pygame.font.SysFont('Consolas',40)
clock = pygame.time.Clock()
width = 1280
height = 720


final_rank2 = 5
class Car():
    def __init__(self, i, map, leaderboard, item_speed, chosen_car):
        global width, height
        width, height = screen.get_size()
        # shop item init
        self.item_speed = item_speed
        self.chosen_car = chosen_car
        
        
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

        global normal_1, normal_2, tangtoc_1, tangtoc_2, cham_1, cham_2, winner

        normal_1 = []
        normal_2 = []
        tangtoc_1 = []
        tangtoc_2 = []
        cham_1 = []
        cham_2 = []
        winner = []
        
        for j in range(5):
            normal_1.append(f'sets/set{map}/cars/car{j+1}/normal1.png')
        
        
        for j in range(5):
            normal_2.append(f'sets/set{map}/cars/car{j+1}/normal2.png')

        
        for j in range(5):
            tangtoc_1.append(f'sets/set{map}/cars/car{j+1}/boost1.png')

        
        for j in range(5):
            tangtoc_2.append(f'sets/set{map}/cars/car{j+1}/boost2.png')

        
        for j in range(5):
            cham_1.append(f'sets/set{map}/cars/car{j+1}/slow1.png')

        
        for j in range(5):
            cham_2.append(f'sets/set{map}/cars/car{j+1}/slow2.png')

        
        for j in range(5):
            winner.append(f'sets/set{map}/cars/car{j+1}/winner.png')


        # assign image to the car
        # if map == 1:
            
        surf1 = pygame.image.load(f'{normal_1[i]}').convert_alpha()
        surf2 = pygame.image.load(f'{normal_2[i]}').convert_alpha()
        self.surf = [surf1, surf2]
        self.index = 0
        self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 / 144))

        self.rect = self.image.get_rect(midleft = (0, i * height * 5 / 36 + height * 49 / 144))
        
        # random speed for each car
        self.sta_speed = randint(1,5)
        self.mid_speed1 = randint(5,10)
        self.mid_speed2 = randint(5,10)
        self.mid_speed3 = randint(7,13)
        self.fin_speed = randint(8,15)

    # return speed with no buff for each car according to timer
    def speed(self):
        if self.chosen_car == self.order + 1 and self.item_speed:
            if current_time <= 1:
                return self.sta_speed + 13
            elif current_time <= 5:
                return self.mid_speed1 + 13
            elif current_time <= 10:
                return self.mid_speed2 + 13
            elif current_time <= 15:
                return self.mid_speed3 + 13
            else: return self.fin_speed + 13
        else:
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
        if (self.rect.right >= width):
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
        global width, height
        width, height = screen.get_size()
        if current_time <= self.start_time + self.duration:
            if self.buff == 'bua_tang_toc':
                surf1 = pygame.image.load(f'{tangtoc_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{tangtoc_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))
                if current_time == self.start_time + self.duration: self.buff = None
                return self.speed() + 5
            if self.buff == 'bua_cham':
                surf1 = pygame.image.load(f'{cham_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{cham_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))
                if current_time == self.start_time + self.duration: self.buff = None
                return self.speed() - 5
            if self.buff == 'bua_di_lui':
                surf1 = pygame.image.load(f'{normal_1[self.order]}').convert_alpha()
                surf2 = pygame.image.load(f'{normal_2[self.order]}').convert_alpha()
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))
                if current_time == self.start_time + self.duration: self.buff = None
                return -5
        surf1 = pygame.image.load(f'{normal_1[self.order]}').convert_alpha()
        surf2 = pygame.image.load(f'{normal_2[self.order]}').convert_alpha()
        self.surf = [surf1, surf2]
        self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))
        return self.speed()
    
    # car movement
    def movement(self):
        global final_rank2
        global width, height
        width, height = screen.get_size()
        # playing winning animation if final rank is 1st
        if self.order == self.leaderboard.ranking[0].order and self.rect.right >= width:
                surf1 = pygame.image.load(f'{winner[self.order]}').convert_alpha()
                surf2 = pygame.transform.flip(surf1, True, False)
                self.surf = [surf1, surf2]
                self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))

        # flip the image if buff == 'bua_di_lui'
        if self.buff == 'bua_di_lui': screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else: screen.blit(self.image,self.rect)

        # move car to the right
        self.rect.right += (self.check_buff())

        # check if touching the screen border
        if(self.rect.right >= width):
            self.finish = True
            self.rect.right = width
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
        global width, height
        width, height = screen.get_size()
        self.index += 0.1
        if self.index  >= len(self.surf): self.index = 0
        self.image = pygame.transform.scale(self.surf[int(self.index)], (width * 5 / 64, height * 13 /144))

    # update function for car class
    def update(self):
        self.movement()
        self.animation_state()


class Mystery(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        global width, height
        width, height = screen.get_size()
        mystery = [1, 2, 3]
        self.image = pygame.image.load(f'mystery/mystery{choice(mystery)}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width * 13 / 256, height * 13 /144))
        self.rect = self.image.get_rect(midleft = (x_pos / 1280 * width, y_pos / 720 * height))

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
        car.duration = 2
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
    def __init__(self, cars_name, chosen_car, item_speed, language):
        global width, height
        width, height = screen.get_size()
        self.language = language
        self.chosen_car = chosen_car
        self.item_speed = item_speed
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
        global width, height
        width, height = screen.get_size()
        font = pygame.font.SysFont('Consolas', round(width / 65))
        self.sort()
        # blit leaderboard stats to the screen
        if self.ranking:
            # blit unchanged stats
            maps_x = width * 5 / 128
            for i in range(5):
                if self.language == 'VN':
                    text_surf = font.render(f'Làn {i + 1}: ',False,'White')
                else:
                    text_surf = font.render(f'Lane {i + 1}: ',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 144))
                profile_border = pygame.image.load('Profile Border.png').convert_alpha()
                profile_border = pygame.transform.scale(profile_border, (width * 23 / 128, height * 5 / 24))
                profile_bg = pygame.image.load('Profile BackGround.png').convert_alpha()
                profile_bg = pygame.transform.scale(profile_bg, (width * 23 / 128, height * 5 / 24))
                profile_bg.set_alpha(120)
                screen.blit(profile_border, (text_rect.x - width * 3 / 256 , text_rect.y - height / 48))
                screen.blit(profile_bg, (text_rect.x - width * 3 / 256 , text_rect.y - height / 48))
                screen.blit(text_surf, text_rect)

                text_surf = font.render(f'{self.cars_name[i]}',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 72))
                screen.blit(text_surf, text_rect)

                car_surf = pygame.image.load(f'{normal_1[self.order[i]]}').convert_alpha()
                car_surf = pygame.transform.scale(car_surf, (width * 15 / 256, height * 5 / 72))
                car_rect = car_surf.get_rect(topright = (maps_x + width * 5 / 32, height * 5 / 144))
                screen.blit(car_surf, car_rect)
                maps_x += width * 25 / 128
            
            # blit changed stats
            for j in range(5):
                maps_x = width * 5 / 128 + self.ranking[j].order * width * 25 / 128
                if self.language == 'VN':
                    if j + 1 == 1:
                        s = 'Hạng: nhất'
                    elif j + 1 == 2:
                        s = 'Hạng: nhì'
                    elif j + 1 == 3:
                        s = 'Hạng: ba'
                    elif j + 1 == 4:
                        s = 'Hạng: tư'
                    elif j + 1 == 5:
                        s = 'Hạng: năm'
                else: 
                    s = f'Rank: {j + 1}'
                    if j + 1 == 1:
                        s = s + 'st'
                    elif j + 1 == 2:
                        s = s + 'nd'
                    elif j + 1 == 3:
                        s = s + 'rd'
                    else: s = s + 'th'
                text_surf = font.render(s,False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 /48))
                screen.blit(text_surf, text_rect)
                if self.ranking[j].buff == None:
                    if self.language == 'VN':
                        text_surf = font.render(f'Hiệu ứng: không có',False,'White')
                    else:
                        text_surf = font.render(f'Effect: None',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 36))
                elif self.ranking[j].buff == 'bua_tang_toc':
                    if self.language == 'VN':
                        text_surf = font.render(f'Hiệu ứng: tăng tốc',False,'White')
                    else:
                        text_surf = font.render(f'Effect: acceleration',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 36))
                elif self.ranking[j].buff == 'bua_cham':
                    if self.language == 'VN':
                        text_surf = font.render(f'Hiệu ứng: chậm',False,'White')
                    else:
                        text_surf = font.render(f'Effect: deceleration',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 36))
                elif self.ranking[j].buff == 'bua_di_lui':
                    if self.language == 'VN':
                        text_surf = font.render(f'Hiệu ứng: đi lùi',False,'White')
                    else:
                        text_surf = font.render(f'Effect: backwards',False,'White')
                    text_rect = text_surf.get_rect(midleft = (maps_x, height * 5 / 36))
                screen.blit(text_surf, text_rect)
                if self.language == 'VN':
                    text_surf = font.render(f'Tốc độ: {self.ranking[j].return_speed()}',False,'White')
                else:
                    text_surf = font.render(f'Speed: {self.ranking[j].return_speed()}',False,'White')
                text_rect = text_surf.get_rect(midleft = (maps_x, height * 25 / 144))
                screen.blit(text_surf, text_rect)



class Background():
    def __init__(self, map_number):
        

        self.sky_surf = pygame.image.load(f'sets/set{map_number}/sky{map_number}.png').convert()
        # self.sky_rect = self.sky_surf.get_rect(topleft = (0,0))

        self.racetrack_surf = pygame.image.load(f'sets/set{map_number}/racetrack{map_number}.jpg').convert()
        # self.racetrack_surf = pygame.transform.scale(pygame.image.load(f'sets/set{map_number}/racetrack{map_number}.jpg').convert(), (width, height * 55 / 72))
        # self.racetrack_rect = self.racetrack_surf.get_rect(topleft = (0, height * 17 / 72))
    
        self.fin_surf = pygame.image.load('finish_line.jpg').convert()
        # self.fin_rect = self.fin_surf.get_rect(bottomright = (width, height))
        
    
    def update(self):
        global width, height
        width, height = screen.get_size()

        sky_surf = pygame.transform.scale(self.sky_surf, (width, height * 17 / 72))
        sky_rect = sky_surf.get_rect(topleft = (0, 0))

        screen.blit(sky_surf, sky_rect)

        racetrack_surf = pygame.transform.scale(self.racetrack_surf, (width, height * 55 / 72))
        racetrack_rect = racetrack_surf.get_rect(topleft = (0, height * 17 / 72))
        screen.blit(racetrack_surf, racetrack_rect)

        fin_surf = pygame.transform.scale(self.fin_surf, (width * 17 / 320, height * 55 / 72))
        fin_rect = fin_surf.get_rect(bottomright = (width, height))
        print(width)
        screen.blit(fin_surf, fin_rect)

class AfterRace():
    def __init__(self, car1, car2, car3, car4, car5, leaderboard, chosen_car, coin_betted, cars_name, item_speed, item_x2, item_sale, history_index, history_profit, language):
        global width, height
        width, height = screen.get_size()
        self.language = language

        self.history_profit = history_profit
        self.history_index = history_index

        self.stage_surf = pygame.image.load('stage.png').convert_alpha() # 612 408
        self.stage_surf = pygame.transform.scale_by(self.stage_surf, 1.5)

        # self.stage_rect = self.stage_surf.get_rect(center = (width/2, height/2 + height*5/72))

        self.stage_bg_surf = pygame.image.load('ChoosingCarBackground.png').convert_alpha() #1280,721
        # self.stage_bg_rect = self.stage_bg_surf.get_rect(topleft = (0,0))

        # button to ldb screen
        if self.language == 'VN':
            self.button1_surf = pygame.image.load('tieptuc.png').convert_alpha() #274,111
        else:
            self.button1_surf = pygame.image.load('tieptuc_eng.png').convert_alpha() #273,111

        # self.button1_rect = self.button1_surf.get_rect(bottomright = (width,height))

        # button to noti screen
        if self.language == 'VN':
            self.button2_surf = pygame.image.load('tieptuc.png').convert_alpha()
        else:
            self.button2_surf = pygame.image.load('tieptuc_eng.png').convert_alpha()

        # self.button2_rect = self.button2_surf.get_rect(bottomright = (width, height))
        
        self.ldb_surf = pygame.image.load('ldb.png').convert_alpha() #701,601
        # self.ldb_rect = self.ldb_surf.get_rect(center = (width/2, height/2))

        self.noti_surf = pygame.image.load('notification.png').convert_alpha() #501,301
        # self.noti_rect = self.noti_surf.get_rect(center = (width/2, height/2))

        self.cam_surf = pygame.image.load('cam_button.png').convert_alpha() #69,69
        # self.cam_rect = self.cam_surf.get_rect(topleft = (width * 297 / 320, height * 7 / 240))

        self.ocr_surf = pygame.image.load('button_O.png').convert_alpha() #69,69
        # self.ocr_rect = self.ocr_surf.get_rect(topleft = (1189, 114))

        if self.language == 'VN':
            self.ok_surf = pygame.image.load('button_lobby.png').convert_alpha() #357,109
        else:
            self.ok_surf = pygame.image.load('button_lobby_eng.png').convert_alpha() #356,109
        # self.ok_rect = self.ok_surf.get_rect(center = (width/2, height/2 + height * 35 / 144))
            
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

        self.item_speed = item_speed
        self.item_x2 = item_x2
        self.item_sale = item_sale

    def run(self):
        
        # general init
        state = 'Win'
        ldb_active = True

        # Thư mục để lưu ảnh
        screenshot_folder = "screenshots"

        # Đảm bảo thư mục tồn tại
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        # Đường dẫn và biến đếm để lưu ảnh
        screenshot_base_name = "screenshot"
        screenshot_extension = ".png"
        screenshot_path = os.path.join(screenshot_folder, screenshot_base_name)
        screenshot_count = 0

        # Thư mục để lưu ảnh
        history_folder = "history"

        # Đảm bảo thư mục tồn tại
        if not os.path.exists(history_folder):
            os.makedirs(history_folder)

        # Đường dẫn và biến đếm để lưu ảnh
        history_base_name = "history"
        history_extension = ".png"
        history_path = os.path.join(history_folder, history_base_name)
        history_count = 0
        
        while ldb_active:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if button2_rect.collidepoint(mouse_pos) and self.stage == False and self.noti == False:
                            # save history
                            while os.path.exists(f"{history_path}_{history_count}{history_extension}"):
                                history_count += 1

                            new_history_path = f"{history_path}_{history_count}{history_extension}"
                            pygame.image.save(screen, new_history_path)
                            print("Lưu history: ", new_history_path)
                            
                            if len(self.history_index) < 3:
                                self.history_index.append(history_count)
                            else:
                                self.history_index[0] = self.history_index[1]
                                self.history_index[1] = self.history_index[2]
                                self.history_index[2] = history_count
                            
                            self.stage = False
                            self.ldb = False
                            self.noti = True
                        
                        if button1_rect.collidepoint(mouse_pos) and self.ldb == False and self.noti == False:
                            self.stage = False
                            self.ldb = True
                            self.noti = False
                        
                        if ok_rect.collidepoint(mouse_pos):
                            if state == 'Win':
                                return True
                            else:
                                return False
                        
                        if cam_rect.collidepoint(mouse_pos):
                            while os.path.exists(f"{screenshot_path}_{screenshot_count}{screenshot_extension}"):
                                screenshot_count += 1

                            new_screenshot_path = f"{screenshot_path}_{screenshot_count}{screenshot_extension}"
                            pygame.image.save(screen, new_screenshot_path)
                            print("Chụp màn hình và lưu ảnh tại:", new_screenshot_path)
                            pass

                        if ocr_rect.collidepoint(mouse_pos):
                            tesseract_OCR()
                        
            global width, height
            width, height = screen.get_size()

            stage_surf = pygame.transform.scale(self.stage_surf, (width * 918 / 1280, height * 612 / 720))
            stage_rect = stage_surf.get_rect(center = (width/2, height/2 + height*5/72))

            stage_bg_surf = pygame.transform.scale(self.stage_bg_surf, (width, height))
            stage_bg_rect = stage_bg_surf.get_rect(topleft = (0,0))

            button1_surf = pygame.transform.scale(self.button1_surf, (width * 274 / 1280, height * 111 / 720))
            button1_rect = button1_surf.get_rect(bottomright = (width,height))

            button2_surf = pygame.transform.scale(self.button2_surf, (width * 274 / 1280, height * 111 / 720))
            button2_rect = button2_surf.get_rect(bottomright = (width,height))

            ldb_surf = pygame.transform.scale(self.ldb_surf, (width * 701 / 1280, height * 601 / 720))
            ldb_rect = ldb_surf.get_rect(center = (width/2, height/2))

            noti_surf = pygame.transform.scale(self.noti_surf, (width * 501 / 1280, height * 301/ 720))
            noti_rect = noti_surf.get_rect(center = (width/2, height/2))

            cam_surf = pygame.transform.scale(self.cam_surf, (width * 69 / 1280, height * 69 / 720))
            cam_rect = cam_surf.get_rect(topleft = (width * 297 / 320, height * 7 / 240))

            ocr_surf = pygame.transform.scale(self.ocr_surf, (width * 69 / 1280, height * 69 / 720))
            ocr_rect = ocr_surf.get_rect(topleft = (width * 1189 / 1280, height * 114 / 720))
            
            ok_surf = pygame.transform.scale(self.ok_surf, (width * 357 / 1280, height * 109 / 720))
            ok_rect = ok_surf.get_rect(center = (width/2, height/2 + height * 35 / 144))

            if self.stage:
                screen.blit(stage_bg_surf, stage_bg_rect)
                screen.blit(stage_surf, stage_rect)
                screen.blit(button1_surf, button1_rect)
                screen.blit(cam_surf, cam_rect)
                if self.car1.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal_1[0]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (width * 13 / 256, height * 13 / 144))
                    first_rect = first_surf.get_rect(center = (width/2, height/2 - height * 25 / 144))
                elif self.car1.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal_1[0]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (width * 13 / 256, height * 13 / 144))
                    second_rect = second_surf.get_rect(center = (width/2 - width * 35 / 256, height/2 - height * 7 / 144))
                elif self.car1.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal_1[0]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (width * 13 / 256, height * 13 / 144))
                    third_rect = third_surf.get_rect(center = (width/2 + width * 35 / 256, height/2 - height * 7 / 144))

                if self.car2.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal_1[1]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (width * 13 / 256, height * 13 / 144))
                    first_rect = first_surf.get_rect(center = (width/2, height/2 - height * 25 / 144))
                elif self.car2.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal_1[1]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (width * 13 / 256, height * 13 / 144))
                    second_rect = second_surf.get_rect(center = (width/2 - width * 35 / 256, height/2 - height * 7 / 144))
                elif self.car2.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal_1[1]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (width * 13 / 256, height * 13 / 144))
                    third_rect = third_surf.get_rect(center = (width/2 + width * 35 / 256, height/2 - height * 7 / 144))
                
                if self.car3.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal_1[2]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (width * 13 / 256, height * 13 / 144))
                    first_rect = first_surf.get_rect(center = (width/2, height/2 - height * 25 / 144))
                elif self.car3.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal_1[2]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (width * 13 / 256, height * 13 / 144))
                    second_rect = second_surf.get_rect(center = (width/2 - width * 35 / 256, height/2 - height * 7 / 144))
                elif self.car3.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal_1[2]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (width * 13 / 256, height * 13 / 144))
                    third_rect = third_surf.get_rect(center = (width/2 + width * 35 / 256, height / 2 - height * 7 / 144))

                if self.car4.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal_1[3]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (width * 13 / 256, height * 13 / 144))
                    first_rect = first_surf.get_rect(center = (width/2, height/2 - height * 25 / 144))
                elif self.car4.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal_1[3]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (width * 13 / 256, height * 13 / 144))
                    second_rect = second_surf.get_rect(center = (width/2 - width * 35 / 256, height/2 - height * 7 / 144))
                elif self.car4.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal_1[3]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (width * 13 / 256, height * 13 / 144))
                    third_rect = third_surf.get_rect(center = (width/2 + width * 35 / 256, height / 2 - height * 7 / 144))

                if self.car5.final_rank1 == 5:
                    first_surf = pygame.image.load(f'{normal_1[4]}').convert_alpha()
                    first_surf = pygame.transform.scale(first_surf, (width * 13 / 256, height * 13 / 144))
                    first_rect = first_surf.get_rect(center = (width/2, height/2 - height * 25 / 144))
                elif self.car5.final_rank1 == 4:
                    second_surf = pygame.image.load(f'{normal_1[4]}').convert_alpha()
                    second_surf = pygame.transform.scale(second_surf, (width * 13 / 256, height * 13 / 144))
                    second_rect = second_surf.get_rect(center = (width/2 - width * 35 / 256, height/2 - height * 7 / 144))
                elif self.car5.final_rank1 == 3:
                    third_surf = pygame.image.load(f'{normal_1[4]}').convert_alpha()
                    third_surf = pygame.transform.scale(third_surf, (width * 13 / 256, height * 13 / 144))
                    third_rect = third_surf.get_rect(center = (width/2 + width * 35 / 256, height / 2 - height * 7 / 144))

                screen.blit(first_surf, first_rect)
                screen.blit(second_surf, second_rect)
                screen.blit(third_surf, third_rect)
             
            if self.ldb:
                screen.blit(stage_bg_surf, stage_bg_rect)
                screen.blit(ldb_surf, ldb_rect)
                screen.blit(button2_surf, button2_rect)
                screen.blit(cam_surf, cam_rect)
                screen.blit(ocr_surf, ocr_rect)
                for i in range(5):
                    print(self.leaderboard.ranking[i].order)
                    img_surf = pygame.image.load(f'{normal_1[self.leaderboard.ranking[i].order]}').convert_alpha()
                    img_surf = pygame.transform.scale(img_surf, (width * 15 /128, height * 5 / 72))
                    img_rect = img_surf.get_rect(center = (width * 55 / 128, height * 55 / 144 + i * height * 5 / 48))
                    
                    text1_surf = font.render(f'{self.cars_name[self.leaderboard.ranking[i].order]}', False, 'Red')
                    text1_rect = text1_surf.get_rect(center = (width * 35 / 64, height * 55 / 144 + i * height * 5 / 48))
                    
                    text_surf = font.render(f'{self.leaderboard.ranking[i].time}ms', False, 'Red')
                    text_rect = text_surf.get_rect(center = (width * 85 / 128, height * 55 / 144 + i * height * 5 / 48))
                    
                    if self.chosen_car - 1 == self.leaderboard.ranking[i].order:
                        hightlight_rect = (img_rect.left, img_rect.top, text_rect.right - img_rect.left, img_rect.bottom - img_rect.top)
                        highlight = pygame.draw.rect(screen,'Yellow', hightlight_rect)

                    screen.blit(img_surf, img_rect)
                    screen.blit(text1_surf, text1_rect)
                    screen.blit(text_surf, text_rect)
                    
                print('-----', self.chosen_car)
            if self.noti:
                screen.blit(stage_bg_surf, stage_bg_rect)
                screen.blit(noti_surf, noti_rect)
                screen.blit(cam_surf, cam_rect)
                screen.blit(self.ok_surf, ok_rect)
                if self.language == 'VN':
                    text_surf = font.render('THÔNG BÁO', False, 'Red')
                else:
                    text_surf = font.render('NOTIFICATION', False, 'Red')
                text_surf = pygame.transform.scale_by(text_surf, 2)
                text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height / 6))
                screen.blit(text_surf, text_rect)
                if self.car1.final_rank1 == 5 and self.chosen_car == 1:
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THẮNG CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU WON THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_x2:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted * 2}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted * 2}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)

                elif self.car2.final_rank1 == 5 and self.chosen_car == 2:
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THẮNG CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU WON THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_x2:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted * 2}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted * 2}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)
                    
                elif self.car3.final_rank1 == 5 and self.chosen_car == 3:
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THẮNG CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU WON THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_x2:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted * 2}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted * 2}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)

                elif self.car4.final_rank1 == 5 and self.chosen_car == 4:
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THẮNG CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU WON THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_x2:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted * 2}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted * 2}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)

                elif self.car5.final_rank1 == 5 and self.chosen_car == 5:
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THẮNG CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU WON THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_x2:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted * 2}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted * 2}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN NHẬN ĐƯỢC {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU RECIVED {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)

                else:
                    state = 'Lose'
                    if self.language == 'VN':
                        text_surf = noti_font.render('BẠN ĐÃ THUA CƯỢC', False, 'Red')
                    else:
                        text_surf = noti_font.render('YOU LOST THE BET', False, 'Red')
                    text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72))
                    screen.blit(text_surf, text_rect)
                    if self.item_sale:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN MẤT {int(self.coin_betted / 2)}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU LOST {int(self.coin_betted / 2)}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    else:
                        if self.language == 'VN':
                            text_surf = noti_font.render(f'BẠN MẤT {self.coin_betted}', False, 'Red')
                        else:
                            text_surf = noti_font.render(f'YOU LOST {self.coin_betted}', False, 'Red')
                        text_rect = text_surf.get_rect(center = (noti_rect.centerx, noti_rect.centery - height * 5 /72 + 50))
                    screen.blit(text_surf, text_rect)
            
            pygame.display.update()
            clock.tick(60)



class Racing():
    def __init__(self, cars_name, map_number, chosen_car, coin_betted, item_speed, item_x2, item_sale, history_index, history_profit, language):
        global width, height
        width, height = screen.get_size()
        self.language = language
        # init history
        self.history_index = history_index
        self.history_profit= history_profit

        # init shop item
        self.item_speed = item_speed
        self.item_x2 = item_x2
        self.item_sale = item_sale

        # init the rank
        self.final_rank = 5 

        self.chosen_car = chosen_car
        self.coin_betted = coin_betted

        # init the timer for the buff
        self.start_time = pygame.time.get_ticks()
        self.current_time = 0

        # assign the names into the game
        self.cars_name = cars_name
        self.leaderboard = Leaderboard(self.cars_name, self.chosen_car, self.item_speed, self.language)

        # init the background
        self.bg = Background(map_number)

        # init cars
        self.car1 = Car(0,map_number, self.leaderboard, self.item_speed, self.chosen_car)
        self.car2 = Car(1,map_number, self.leaderboard, self.item_speed, self.chosen_car)
        self.car3 = Car(2,map_number, self.leaderboard, self.item_speed, self.chosen_car)
        self.car4 = Car(3,map_number, self.leaderboard, self.item_speed, self.chosen_car)
        self.car5 = Car(4,map_number, self.leaderboard, self.item_speed, self.chosen_car)
        
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
        self.noti_rect = self.noti_surf.get_rect(center = (width/2, height/2))

        # Sound
        self.sound = pygame.mixer.Sound(f'map{map_number}.mp3')
        self.sound.play(-1)
        self.winner_sound = pygame.mixer.Sound('winner_sound.mp3')


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

            global width, height
            width, height = screen.get_size()  
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
                self.sound.stop()
                self.winner_sound.play(0)
                self.after = AfterRace(self.car1, self.car2, self.car3, self.car4,self.car5, self.leaderboard, self.chosen_car, self.coin_betted, self.cars_name, self.item_speed, self.item_x2, self.item_sale, self.history_index, self.history_profit, self.language)
                global final_rank2
                final_rank2 = 5
                if self.after.run():
                    if self.item_x2:
                        if len(self.history_profit) < 3:
                            self.history_profit.append(self.coin_betted * 2)
                        else:
                            self.history_profit[0] = self.history_profit[1]
                            self.history_profit[1] = self.history_profit[2]
                            self.history_profit[2] = self.coin_betted * 2
                        return self.coin_betted * 2
                    else:
                        if len(self.history_profit) < 3:
                            self.history_profit.append(self.coin_betted)
                        else:
                            self.history_profit[0] = self.history_profit[1]
                            self.history_profit[1] = self.history_profit[2]
                            self.history_profit[2] = self.coin_betted
                        return self.coin_betted
                else:
                    if self.item_sale:
                        if len(self.history_profit) < 3:
                            self.history_profit.append(-int(self.coin_betted / 2))
                        else:
                            self.history_profit[0] = self.history_profit[1]
                            self.history_profit[1] = self.history_profit[2]
                            self.history_profit[2] = -int(self.coin_betted / 2)
                        return - int(self.coin_betted/2)
                    else:
                        if len(self.history_profit) < 3:
                            self.history_profit.append(-self.coin_betted)
                        else:
                            self.history_profit[0] = self.history_profit[1]
                            self.history_profit[1] = self.history_profit[2]
                            self.history_profit[2] = -self.coin_betted
                        return -self.coin_betted
                
            pygame.display.update()
            clock.tick(60)
        
        
