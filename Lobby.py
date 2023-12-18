import pygame
import sys
import pickle
import Settings
from pygame.constants import MOUSEMOTION
import tetris_main
from Game import Game

from login2 import FaceRecognitionApp

import player

class Player:
    def __init__(self, name):
        self.name = name
        if self.name == 'Admin':
            self.money = 99999
        else:
            self.money = 400
        self.history_index = []
        self.history_profit = []
        self.item_sale = 0
        self.item_x2 = 0
        self.item_speed = 0
        

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Game Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Consolas', 75)
        self.his_font = pygame.font.SysFont('Consolas', 45)
        self.font_item = pygame.font.SysFont('Consolas',round(self.screen_width * 3 /160))
        
        self.backgrounds = {
            'menu': pygame.image.load('Graphic/menuchinh.png').convert(),
            'chonmap': pygame.image.load('Graphic/chonmap.png').convert(),
            'setting': pygame.image.load('Graphic/setting.png').convert(),
            'instruction': pygame.image.load('Graphic/huongdan.png').convert(),
            'menu_eng': pygame.image.load('Graphic/menuchinh_eng.png').convert(),
            'chonmap_eng': pygame.image.load('Graphic/chonmap_eng.png').convert(),
            'setting_eng': pygame.image.load('Graphic/setting_eng.png').convert(),
            'instruction_eng': pygame.image.load('Graphic/huongdan_eng.png').convert(),
            'shop_mo': pygame.image.load('Graphic/shopmo.png').convert(),
            'shop_mo_eng': pygame.image.load('Graphic/shopmo_eng.png').convert(),
            'error': pygame.image.load('Graphic/error_minigame.png').convert(),
            'error_eng': pygame.image.load('Graphic/error_minigame_eng.png').convert(),
            'insideshop': pygame.image.load('Graphic/insideshop.png').convert(),
            'insideshop_eng': pygame.image.load('Graphic/insideshop_eng.png').convert(),
            'chonscreen': pygame.image.load('Graphic/chonscreen.png').convert(),
            'chonscreen_eng': pygame.image.load('Graphic/chonscreen_eng.png').convert(),
            'lichsu': pygame.image.load('Graphic/lichsu.png').convert(),
            'lichsu_eng': pygame.image.load('Graphic/lichsu_eng.png').convert(),
            'error_shop': pygame.image.load('Graphic/error_shop.png').convert(),
            'error_shop_eng': pygame.image.load('Graphic/error_shop_eng.png').convert()
        }
        self.buttons = []
        
        self.history_index = player.HISTORY_INDEX
        self.history_profit = player.HISTORY_PROFIT
        self.item_speed = player.ITEM_SPEED
        self.item_x2 = player.ITEM_X2
        self.item_sale = player.ITEM_SALE
        self.sound = pygame.mixer.Sound('Sound/menusound.mp3')
        self.sound.play(-1)
        self.music_playing = player.MUSIC 
        self.language = player.LANGUAGE
        if self.language == 'VN':
            self.current_screen = 'menu'
        elif self.language == 'ENG':
            self.current_screen = 'menu_eng'

    def add_button(self, action, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)
        self.buttons.append((button_rect, action))

    def check_button_click(self, mouse_pos):
        for button in self.buttons:
            if button[0].collidepoint(mouse_pos):
                return button[1]
        return None

    def menu_screen(self, username,  money):
        self.screen_width, self.screen_height = self.screen.get_size()
        # in money
        self.font = pygame.font.SysFont('Consolas', round(self.screen_width * 75 / 1280))
        money_surf = self.font.render(f'{money}', False, 'Red')
        money_rect = money_surf.get_rect(topleft = (self.screen_width * 950 / 1280, self.screen_height * 250 / 720))
        self.screen.blit(money_surf, money_rect)
        
        # in username
        name_surf = self.font_item.render(f'{username}', False, 'Red')
        name_rect = name_surf.get_rect(center = (self.screen_width * 1065 / 1280, self.screen_height * 50 / 720))
        self.screen.blit(name_surf, name_rect)
        
        self.buttons = []
        
        self.add_button('play', self.screen_width * 873 / 1280, self.screen_height * 107 / 240, self.screen_width * 17 / 80, self.screen_height * 11 /72)
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        self.add_button('minigame', self.screen_width * 831 / 1280, self.screen_height * 451 / 720, self.screen_width * 71 / 256, self.screen_height * 3 / 20)
        self.add_button('instruction', self.screen_width * 838 / 1280, self.screen_height * 576 / 720, self.screen_width * 341 / 1280, self.screen_height * 103 / 720)
        self.add_button('settings', self.screen_width * 1188 / 1280, self.screen_height * 21 / 720, self.screen_width * 68 / 1280, self.screen_height * 68 / 1280)
        self.add_button('history',self.screen_width * 1189 / 1280, self.screen_height * 114 / 720,self.screen_width * 68 / 1280,self.screen_height * 68 / 1280)
        self.add_button('shop',self.screen_width * 153 / 1280,self.screen_height * 185 / 720,self.screen_width * 365 / 1280,self.screen_height * 240 / 1280)
        pass

    def chonmap_screen(self):
        self.buttons = []  # Xóa danh sách các button cũ
    
        # Thêm các button mới
        self.add_button('map1', self.screen_width * 63 / 1280,  self.screen_height * 205 / 720, self.screen_width * 177 / 1280, self.screen_height * 232 / 1280)
        self.add_button('map2', self.screen_width * 292 / 1280, self.screen_height * 205 / 720, self.screen_width * 177 / 1280, self.screen_height * 232 / 1280)
        self.add_button('map3', self.screen_width * 546 / 1280, self.screen_height * 205 / 720, self.screen_width * 177 / 1280, self.screen_height * 232 / 1280)
        self.add_button('map4', self.screen_width * 798 / 1280, self.screen_height * 205 / 720, self.screen_width * 177 / 1280, self.screen_height * 232 / 1280)
        self.add_button('map5', self.screen_width * 1053 / 1280,self.screen_height * 205 / 720, self.screen_width * 177 / 1280, self.screen_height * 232 / 1280)
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        pass

    def setting_screen(self):
         self.buttons = []  # Xóa danh sách các button cũ
    
        # Thêm các button mới
         self.add_button('sound', self.screen_width * 471 / 1280, self.screen_height * 288 / 720, self.screen_width * 69 / 1280, self.screen_height * 69 / 720)
         self.add_button('language', self.screen_width * 471 / 1280, self.screen_height * 399 / 720, self.screen_width * 68 / 1280, self.screen_height * 68 / 720)
         self.add_button('resize',self.screen_width * 469 / 1280, self.screen_height * 509 / 720, self.screen_width * 68 / 1280, self.screen_height * 68 / 720)
         self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
         
         pass

    def instruction_screen(self):
        self.screen_width, self.screen_height = self.screen.get_size()
        self.buttons = []
        
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        pass

    def shop_screen(self, username, money):
        # in ảnh ra màn hình  
        self.screen_width, self.screen_height = self.screen.get_size() 
        bg = pygame.transform.scale(self.backgrounds[self.current_screen], (self.screen_width, self.screen_height))
        self.screen.blit(bg, (0, 0))

        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = pygame.font.SysFont('Consolas', round(self.screen_width * 75 / 1280))
        money_surf = self.font.render(f'{money}', False, 'Red')
        money_rect = money_surf.get_rect(topleft = (self.screen_width * 950 / 1280, self.screen_height * 250 / 720))
        self.screen.blit(money_surf, money_rect)

        # in username
        name_surf = self.font_item.render(f'{username}', False, 'Red')
        name_rect = name_surf.get_rect(center = (self.screen_width * 1065 / 1280, self.screen_height * 50 / 720))
        self.screen.blit(name_surf, name_rect)

        self.buttons = []
        
        self.add_button('shop', self.screen_width * 153 / 1280, self.screen_height * 185 / 720, self.screen_width * 365 / 1280, self.screen_height * 240 / 720)
        pass
    
    def error_screen(self):
        self.screen_width, self.screen_height = self.screen.get_size()
        self.buttons = []
        self.add_button('Ok', self.screen_width * 564 / 1280, self.screen_height * 457 / 720, self.screen_width * 172 / 1280, self.screen_height * 68 / 720)
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
    
    def buying_screen(self):
        self.screen_width, self.screen_height = self.screen.get_size()
        #in số lượng item
        item1_surf = self.font_item.render(f'{self.item_speed}', False, 'White')
        item1_rect =item1_surf.get_rect(topleft = (self.screen_width * 485 / 1280, self.screen_height * 462 / 720))
        self.screen.blit(item1_surf,  item1_rect)
        
        item2_surf = self.font_item.render(f'{self.item_x2}', False, 'White')
        item2_rect =item2_surf.get_rect(topleft = (self.screen_width * 666 / 1280, self.screen_height * 462 / 720))
        self.screen.blit(item2_surf,  item2_rect)
        
        item3_surf = self.font_item.render(f'{self.item_sale}', False, 'White')
        item3_rect =item3_surf.get_rect(topleft = (self.screen_width * 862 / 1280, self.screen_height * 462 / 720))
        self.screen.blit(item3_surf,  item3_rect)

        self.buttons = []
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        self.add_button('item1', self.screen_width * 412 / 1280, self.screen_height * 405 / 720, self.screen_width * 107 / 1280, self.screen_height * 37 / 720)
        self.add_button('item2', self.screen_width * 605 / 1280, self.screen_height * 405 / 720, self.screen_width * 107 / 1280, self.screen_height * 37 / 720)
        self.add_button('item3', self.screen_width * 798 / 1280, self.screen_height * 405 / 720, self.screen_width * 107 / 1280, self.screen_height * 37 / 720)

    def resize_screen(self):
        self.screen_width, self.screen_height = self.screen.get_size()
        self.buttons = []
        
        self.add_button('1280x720' , self.screen_width * 458 / 1280,self.screen_height * 294 / 720, self.screen_width * 50 / 1280,self.screen_height * 17 /240)
        self.add_button('1920x1080', self.screen_width * 458 / 1280,self.screen_height * 363 / 720,self.screen_width * 50 / 1280,self.screen_height * 17 /240)
        self.add_button('1440x900', self.screen_width * 458 / 1280,self.screen_height * 433 / 720, self.screen_width * 50 / 1280,self.screen_height * 17 /240)
        self.add_button('1280x960', self.screen_width * 458 / 1280,self.screen_height * 503 / 720, self.screen_width * 50 / 1280,self.screen_height * 17 /240)
        self.add_button('1024x768', self.screen_width * 458 / 1280,self.screen_height * 573 / 720, self.screen_width * 50 / 1280,self.screen_height * 17 /240)
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        pass

    def history_screen(self):
        # show history 
        if self.history_index:
            for i in range(len(self.history_index)):
                scale_num = 0.85
                cord = (400, 200, 500, 400)
                his1_surf = pygame.image.load(f'history/history_{self.history_index[i]}.png').convert_alpha()
                his1_surf = pygame.transform.scale_by(his1_surf, scale_num)
                self.screen.blit(his1_surf, (425 * i, 261), tuple([scale_num * x for x in cord]))
                if self.history_profit[i] > 0:
                    money_surf = self.his_font.render(f'+{self.history_profit[i]}', False, 'Green')
                else:
                    money_surf = self.his_font.render(f'{self.history_profit[i]}', False, 'Red')
                money_rect = money_surf.get_rect(topleft = (425 * i, 260))
                self.screen.blit(money_surf, money_rect)


        
        self.buttons = []
        self.add_button('back', self.screen_width * 3 /160, self.screen_height * 7 /160, self.screen_width * 17 / 144, self.screen_height * 17 /240)
        pass

    # hàm tắt mở nhạc nền
    def toggle_music(self):
        if self.music_playing:
            self.sound.stop()
            self.music_playing = False
            print("Music paused")
        else:
            self.sound.play(-1)
            self.music_playing = True
            print("Music unpaused")
        pass

    def run(self, username, money):
        while True:
            print(self.language, player.LANGUAGE)
            
            print(player.NAME, player.HISTORY_INDEX)
            with open('data.pickle', 'rb') as file:
                data = pickle.load(file)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    motion_button = self.check_button_click(mouse_pos)
                    if self.current_screen == 'menu':
                       if motion_button == 'shop':
                          self.current_screen = 'shop_mo'
                    elif self.current_screen == 'shop_mo':
                       if motion_button != 'shop':
                           self.current_screen = 'menu'
                    elif self.current_screen == 'menu_eng':
                       if motion_button == 'shop':
                          self.current_screen = 'shop_mo_eng'
                    elif self.current_screen == 'shop_mo_eng':
                       if motion_button != 'shop':
                           self.current_screen = 'menu_eng'
                           
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_button = self.check_button_click(mouse_pos)  
                    
                    # màn hình menu TV
                    if self.current_screen == 'menu' :
                        if clicked_button == 'instruction': 
                            pygame.display.set_caption("Instruction")
                            self.current_screen = 'instruction'
                        elif clicked_button == 'minigame':
                            pygame.display.set_caption("Minigame")
                            if self.music_playing == True:
                                self.toggle_music()
                                player.MUSIC = True
                            else:
                                player.MUSIC = False   
                            self.minigame = tetris_main.Main()
                            self.minigame.music.set_volume(0.05)
                            self.minigame.run()

                            # if money < 100:
                            #     print("Play minigame")
                            #     self.minigame = tetris_main.Main()
                            #     self.minigame.music.set_volume(0.05)
                            #     self.minigame.run()
                            # elif money >=100:
                            #     pygame.display.set_caption("Error")
                            #     self.current_screen = 'error_eng' 
                            # gọi minigame nếu k đủ tiền
                        elif clicked_button == 'play':
                            if money >= 100:
                                pygame.display.set_caption("Choose map")
                                print("Start Game")
                                self.current_screen = 'chonmap'
                        elif clicked_button == 'settings':
                            pygame.display.set_caption("Settings")
                            self.current_screen = 'setting'
                        elif clicked_button == 'history':
                            pygame.display.set_caption("History")
                            self.current_screen='lichsu'
                            #dẫn lịch sử
                        elif clicked_button == 'back':
                            return

                        
                    # màn hình menu TA 
                    elif self.current_screen == 'menu_eng' :
                        if clicked_button == 'instruction': 
                            pygame.display.set_caption("Instruction")
                            self.current_screen = 'instruction_eng'
                            print("Instruction in English")
                        elif clicked_button == 'minigame':
                            pygame.display.set_caption("Minigame")
                            self.toggle_music()
                            self.minigame = tetris_main.Main()
                            self.minigame.music.set_volume(0.05)
                            self.minigame.run()
                            self.music_playing = False
                            self.toggle_music()

                            # if money < 100:
                            #     print("Play minigame")
                            #     self.minigame = tetris_main.Main()
                            #     self.minigame.music.set_volume(0.05)
                            #     self.minigame.run()
                            # elif money >=100:
                            #     pygame.display.set_caption("Error")
                            #     self.current_screen = 'error_eng' 
                            # gọi minigame nếu k đủ tiền
                        elif clicked_button == 'play':
                            pygame.display.set_caption("Choose map")
                            print("Start Game")
                            self.current_screen = 'chonmap_eng'
                        elif clicked_button == 'settings':
                            pygame.display.set_caption("Settings")
                            self.current_screen = 'setting_eng'
                        elif clicked_button == 'shop':
                            pygame.display.set_caption("Shops")
                            self.current_screen = 'insideshop_eng'
                        elif clicked_button == 'history':
                            pygame.display.set_caption("History")
                            self.current_screen='lichsu_eng'
                            #dẫn lịch sử ván chơi   
                        elif clicked_button == 'back':
                            return   
                            
                            
                    #màn hình chọn map chơi TV
                    elif self.current_screen == 'chonmap' :
                        if clicked_button == 'map1':
                            print("Map university")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(1, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map2':
                            print("Map grass field")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(2, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map3':
                            print("Map galaxy")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(3, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map4':
                            print("Map city")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(4, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map5':
                            print("Map ocean")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(5, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            #dẫn game zô
                        elif clicked_button == 'back':
                                pygame.display.set_caption("Game Menu")
                                self.current_screen = 'menu'
                    
                    #màn hình chọn map chơi TA
                    elif self.current_screen == 'chonmap_eng' :
                        if clicked_button == 'map1':
                            print("Map university")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(1, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map2':
                            print("Map grass field")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(2, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map3':
                            print("Map galaxy")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(3, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map4':
                            print("Map city")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(4, money, tmp1, tmp2,tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            # dẫn gem zô
                        elif clicked_button == 'map5':
                            print("Map ocean")
                            tmp1, tmp2, tmp3 = False, False, False
                            if(self.item_speed >= 1):
                                self.item_speed -= 1
                                tmp1 = True
                            if(self.item_x2 >= 1):
                                self.item_x2 -= 1
                                tmp2 = True
                            if(self.item_sale >= 1):
                                self.item_sale -= 1
                                tmp3 = True
                            self.toggle_music()
                            money += Game(5, money, tmp1, tmp2, tmp3, self.history_index, self.history_profit, self.language).run()
                            self.toggle_music()
                            self.current_screen = 'menu'
                            #dẫn game zô
                        elif clicked_button == 'back':
                                pygame.display.set_caption("Game Menu")
                                self.current_screen = 'menu_eng'
                                
                    #màn hình hướng dẫn TV
                    elif self.current_screen == 'instruction':
                        if clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu'
                            
                    #màn hình hướng dẫn TA
                    elif self.current_screen == 'instruction_eng':
                        if clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu_eng'

                    #màn hình cài đặt TV sang TA
                    elif self.current_screen == 'setting' :
                        if clicked_button == 'sound':
                            print("Turn off/on music")
                            self.toggle_music()
                        elif clicked_button == 'language':
                            print("Change to English")
                            self.current_screen = 'setting_eng'
                            self.language = 'ENG'
                            player.LANGUAGE = 'ENG'
                        elif clicked_button=='resize':
                            self.current_screen ='chonscreen'    
                        elif clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu'
                            
                    #màn hình cài đặt TA sang TV
                    elif self.current_screen == 'setting_eng' :
                        if clicked_button == 'sound':
                            print("Turn off/on music")
                            self.toggle_music()
                        elif clicked_button == 'language':
                            print("Change to Vietnamese")
                            self.current_screen = 'setting'
                            self.language = 'VN'
                            player.LANGUAGE = 'VN'
                        elif clicked_button=='resize':
                            self.current_screen ='chonscreen_eng'    
                        elif clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu_eng'
                    
                    #màn hình error TV
                    elif self.current_screen == 'error':
                        if clicked_button == 'Ok' or clicked_button =='back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu'
                            
                    #màn hình error TA
                    elif self.current_screen == 'error_eng':
                        if clicked_button == 'Ok' or clicked_button =='back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu_eng'
                            
                    #màn hình shop mở TV
                    elif self.current_screen == 'shop_mo':
                        if clicked_button == 'shop':
                            pygame.display.set_caption("Shops")
                            self.current_screen = 'insideshop'
                            
                     #màn hình shop mở TA
                    elif self.current_screen == 'shop_mo_eng':
                        if clicked_button == 'shop':
                            pygame.display.set_caption("Shops")
                            self.current_screen = 'insideshop_eng'
                            
                    #màn hình mua đồ TV
                    elif self.current_screen == 'insideshop':
                        if clicked_button == 'item1' and money >=100:
                            self.item_speed +=1
                            money -=100
                        elif clicked_button == 'item2' and money >=100:
                            self.item_x2 +=1
                            money -=100
                        elif clicked_button == 'item3' and money >=100:
                            self.item_sale += 1
                            money -=100
                        elif clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu'
                        elif (clicked_button=='item1' or clicked_button=='item2' or clicked_button=='item3') and money <100:
                            pygame.display.set_caption("Error")
                            self.current_screen = 'error_shop'
                            
                    #màn hình mua đồ TA
                    elif self.current_screen == 'insideshop_eng':
                        if clicked_button == 'item1' and money >=100:
                            self.item_speed +=1
                            money -=100
                        elif clicked_button == 'item2' and money >=100:
                            self.item_x2 +=1
                            money -=100
                        elif clicked_button == 'item3' and money >=100:
                            self.item_sale += 1
                            money -=100
                        elif clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu_eng'
                        elif (clicked_button=='item1' or clicked_button=='item2' or clicked_button=='item3') and money <100:
                            pygame.display.set_caption("Error")
                            self.current_screen = 'error_shop_eng'
                        
                    #màn hình resize TV
                    elif self.current_screen == 'chonscreen':
                        if clicked_button == '1280x720':
                            print("Change screen size to 1280x720")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1280, 720
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1920x1080':
                            print("Change screen size to 1920x1080")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1920, 1080
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1440x900':
                            print("Change screen size to 1440x900")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1440, 900
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1280x960':
                            print("Change screen size to 1280x960")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1280, 960
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1024x768':
                            print("Change screen size to 1024x768")    
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1024, 768
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            
                            # ghép resize
                        elif clicked_button == 'back':
                            self.current_screen = 'setting'

                    #màn hình resize TA
                    elif self.current_screen == 'chonscreen_eng':
                        if clicked_button == '1280x720':
                            print("Change screen size to 1280x720")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1280, 720
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1920x1080':
                            print("Change screen size to 1920x1080")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1920, 1080
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1440x900':
                            print("Change screen size to 1440x900")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1440, 900
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1280x960':
                            print("Change screen size to 1280x960")
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1280, 960
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                        elif clicked_button == '1024x768':
                            print("Change screen size to 1024x768")    
                            Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT = 1024, 768
                            self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
                            # ghép resize
                    
                    #màn hình history TV
                    elif self.current_screen == 'lichsu':
                        if clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu'
                            
                    #màn hình history TA
                    elif self.current_screen == 'lichsu_eng':
                        if clicked_button == 'back':
                            pygame.display.set_caption("Game Menu")
                            self.current_screen = 'menu_eng'

                    #màn hình error shop TV
                    elif self.current_screen == 'error_shop':
                        if clicked_button == 'Ok' or clicked_button =='back':
                            pygame.display.set_caption("Shops")
                            self.current_screen = 'insideshop'
                            
                    #màn hình error TA
                    elif self.current_screen == 'error_eng':
                        if clicked_button == 'Ok' or clicked_button =='back':
                            pygame.display.set_caption("Shops")
                            self.current_screen = 'insideshop_eng' 
                                   
            # update data to the database
            for i in range(len(data)):
                if username == data[i].name:
                    data[i].money = money
                    data[i].item_sale = self.item_sale
                    data[i].item_speed = self.item_speed
                    data[i].item_x2 = self.item_x2
                    data[i].history_index = self.history_index
                    data[i].history_profit = self.history_profit
                    player.NAME = data[i].name
                player.MONEY = data[i].money
                player.HISTORY_INDEX = data[i].history_index
                player.ITEM_SALE = data[i].item_sale
                player.ITEM_X2 = data[i].item_x2
                player.ITEM_SPEED = data[i].item_speed
            with open('data.pickle', 'wb') as file:
                pickle.dump(data, file)
                
            print(self.history_index)
            print(self.history_profit)

            
            # in ảnh ra màn hình  
            self.screen_width, self.screen_height = self.screen.get_size() 
            bg = pygame.transform.scale(self.backgrounds[self.current_screen], (self.screen_width, self.screen_height))
            self.screen.blit(bg, (0, 0))
            

            # điều kiện chuyển màn hình                
            if self.current_screen == 'menu' or self.current_screen == 'menu_eng':    
                self.menu_screen(username, money)
               
            if self.current_screen == 'chonmap' or self.current_screen == 'chonmap_eng': 
                self.chonmap_screen()
                
            if self.current_screen == 'instruction' or self.current_screen == 'instruction_eng': 
                self.instruction_screen()
                
            if self.current_screen == 'setting' or self.current_screen == 'setting_eng': 
                self.setting_screen()    
                
            if self.current_screen == 'shop_mo' or self.current_screen == 'shop_mo_eng' :
                self.shop_screen(username, money)
                
            if self.current_screen == 'error' or self.current_screen == 'error_eng' or self.current_screen == 'error_shop' or self.current_screen == 'error_shop_eng':
                self.error_screen()
                
            if self.current_screen == 'insideshop' or self.current_screen == 'insideshop_eng' :
                self.buying_screen()
                
            if self.current_screen == 'chonscreen' or self.current_screen == 'chonscreen_eng':
                self.resize_screen()
            
            if self.current_screen == 'lichsu' or self.current_screen == 'lichsu_eng':
                self.history_screen()
            

            # update screen
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    menu = FaceRecognitionApp()
    menu.main_screen()
    with open('data.pickle', 'rb') as file:
        data = pickle.load(file)
    if menu.confirm:
        for i in range(len(data)):
            print(data[i].name)
            if menu.name == data[i].name:
                player.NAME = data[i].name
                player.MONEY = data[i].money
                player.HISTORY_INDEX = data[i].history_index
                player.ITEM_SALE = data[i].item_sale
                player.ITEM_X2 = data[i].item_x2
                player.ITEM_SPEED = data[i].item_speed
                Menu().run(player.NAME, player.MONEY)

    # player.NAME = data[0].name
    # player.MONEY = data[0].money
    # player.HISTORY_INDEX = data[0].history_index
    # player.HISTORY_PROFIT = data[0].history_profit
    # player.ITEM_SALE = data[0].item_sale
    # player.ITEM_X2 = data[0].item_x2
    # player.ITEM_SPEED = data[0].item_speed
    # Menu().run(player.NAME, player.MONEY)
     