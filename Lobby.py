import pygame
import sys
import pickle

from pygame.constants import MOUSEMOTION
import tetris_main
from Game import Game
from tesseract import tesseract_OCR
from login2 import FaceRecognitionApp

import player

class Menu:
    def __init__(self):
        pygame.init()

        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Consolas', 75)
        self.font_item = pygame.font.SysFont('Consolas',24)
        self.current_screen = 'menu'
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
            'lichsu_eng': pygame.image.load('Graphic/lichsu_eng.png').convert()
        }
        self.buttons = []
        
        self.item_speed = 0
        self.item_x2 = 0
        self.item_sale = 0
        self.sound = pygame.mixer.music.load('Sound/menusound.mp3')
        # pygame.mixer.music.play(-1)
        self.music_playing = True  
        
    def add_button(self, action, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)
        self.buttons.append((button_rect, action))

    def check_button_click(self, mouse_pos):
        for button in self.buttons:
            if button[0].collidepoint(mouse_pos):
                return button[1]
        return None

    def menu_screen(self, money):
        # in money
        money_surf = self.font.render(f'{money}', False, 'Red')
        money_rect = money_surf.get_rect(topleft = (1000, 250))
        self.screen.blit(money_surf, money_rect)
        
        self.buttons = []
        
        self.add_button('play', 873, 321, 272, 110)
        self.add_button('back', 24, 28, 85, 51)
        self.add_button('minigame', 831, 451, 355, 108)
        self.add_button('instruction', 838, 576, 341, 103)
        self.add_button('settings', 1188, 21, 68, 68)
        self.add_button('history',1189,114,68,68)
        self.add_button('shop',153,185,365,240)
        pass

    def chonmap_screen(self):
        self.buttons = []  # Xóa danh sách các button cũ
    
        # Thêm các button mới
        self.add_button('map1', 63,  205,177,232 )
        self.add_button('map2', 292, 205,177,232)
        self.add_button('map3', 546, 205,177,232)
        self.add_button('map4', 798, 205,177,232)
        self.add_button('map5', 1053,205,177,232)
        self.add_button('back', 24, 28, 85, 51)
        pass

    def setting_screen(self):
         self.buttons = []  # Xóa danh sách các button cũ
    
        # Thêm các button mới
         self.add_button('sound', 471, 288, 69, 69)
         self.add_button('language', 471, 399, 68, 68)
         self.add_button('resize',469,509,68,68)
         self.add_button('back', 24, 28, 85, 51)
         
         pass

    def instruction_screen(self):
        self.buttons = []
        
        self.add_button('back', 24, 28, 85, 51)
        pass

    def shop_screen(self, money):
        money_surf = self.font.render(f'{money}', False, 'Red')
        money_rect = money_surf.get_rect(topleft = (1000, 250))
        self.screen.blit(money_surf, money_rect)
        self.buttons = []
        
        self.add_button('shop', 153, 185, 365, 240)
        pass
    
    def error_screen(self):
        self.buttons = []
        self.add_button('Ok',564,457,172,68)
        self.add_button('back', 24, 28, 85, 51)
    
    def buying_screen(self):
        #in số lượng item
        item1_surf = self.font_item.render(f'{self.item_speed}', False, 'White')
        item1_rect =item1_surf.get_rect(topleft = (485, 462))
        self.screen.blit(item1_surf,  item1_rect)
        
        item2_surf = self.font_item.render(f'{self.item_x2}', False, 'White')
        item2_rect =item2_surf.get_rect(topleft = (666, 462))
        self.screen.blit(item2_surf,  item2_rect)
        
        item3_surf = self.font_item.render(f'{self.item_sale}', False, 'White')
        item3_rect =item3_surf.get_rect(topleft = (862, 462))
        self.screen.blit(item3_surf,  item3_rect)

        self.buttons = []
        self.add_button('back', 24, 28, 85, 51)
        self.add_button('item1', 412,405,107,37)
        self.add_button('item2',605,405,107,37 )
        self.add_button('item3',798,405,107,37)

    def resize_screen(self):
        self.buttons = []
        
        self.add_button('1280x720' , 458,294,50,51)
        self.add_button('1920x1080',458,363,50,51)
        self.add_button('1440x900',458,433,50,51)
        self.add_button('1280x960',458,503,50,51)
        self.add_button('1024x768',458,573,50,51)
        self.add_button('back', 24, 28, 85, 51)
        pass

    def history_screen(self):
        self.buttons = []
        self.add_button('back', 24, 28, 85, 51)
        pass

    # hàm tắt mở nhạc nền
    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
            print("Music paused")
        else:
            pygame.mixer.music.play(-1) 
            self.music_playing = True
            print("Music unpaused")
        pass

    def run(self, username, money):
        while True:
            
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
                            money += Game(1, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(2, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(3, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(4, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(5, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(1, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(2, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(3, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(4, money, tmp1, tmp2,tmp3).run()
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
                            money += Game(5, money, tmp1, tmp2, tmp3).run()
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
                        
                    #màn hình resize TV
                    elif self.current_screen == 'chonscreen':
                        if clicked_button == '1280x720':
                            print("Change screen size to 1280x720")
                            # ghép resize
                        elif clicked_button == '1920x1080':
                            print("Change screen size to 1920x1080")
                            # ghép resize
                        elif clicked_button == '1440x900':
                            print("Change screen size to 1440x900")
                            # ghép resize
                        elif clicked_button == '1280x960':
                            print("Change screen size to 1280x960")
                            # ghép resize
                        elif clicked_button == '1024x768':
                            print("Change screen size to 1024x768")    
                            # ghép resize
                        elif clicked_button == 'back':
                            self.current_screen = 'setting'

                    #màn hình resize TA
                    elif self.current_screen == 'chonscreen_eng':
                        if clicked_button == 'back':
                            self.current_screen = 'setting_eng'
                        elif clicked_button == '1280x720':
                            print("Change screen size to 1280x720")
                            # ghép resize
                        elif clicked_button == '1920x1080':
                            print("Change screen size to 1920x1080")
                            # ghép resize
                        elif clicked_button == '1440x900':
                            print("Change screen size to 1440x900")
                            # ghép resize
                        elif clicked_button == '1280x960':
                            print("Change screen size to 1280x960")
                            # ghép resize
                        elif clicked_button == '1024x768':
                            print("Change screen size to 1024x768")
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
            # update money to database
            for i in range(len(data)):
                if username == list(data[i].keys())[0]:
                    data[i][f'{username}'] = money
            with open('data.pickle', 'wb') as file:
                pickle.dump(data, file)
            
            # in ảnh ra màn hình    
            self.screen.blit(self.backgrounds[self.current_screen], (0, 0))

            # in username
            name_surf = self.font_item.render(f'{username}', False, 'Red')
            name_rect = name_surf.get_rect(center = (1065, 50))
            self.screen.blit(name_surf, name_rect)

            # điều kiện chuyển màn hình                
            if self.current_screen == 'menu' or self.current_screen == 'menu_eng':
                self.menu_screen(money)
               
            if self.current_screen == 'chonmap' or self.current_screen == 'chonmap_eng': 
                self.chonmap_screen()
                
            if self.current_screen == 'instruction' or self.current_screen == 'instruction_eng': 
                self.instruction_screen()
                
            if self.current_screen == 'setting' or self.current_screen == 'setting_eng': 
                self.setting_screen()    
                
            if self.current_screen == 'shop_mo' or self.current_screen == 'shop_mo_eng' :
                self.shop_screen(money)
                
            if self.current_screen == 'error' or self.current_screen == 'error_eng' :
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
    with open('data.pickle', 'rb') as file:
        data = pickle.load(file)
    # menu = FaceRecognitionApp()
    # menu.main_screen()
    # if menu.confirm:
    #     for i in range(len(data)):
    #         if menu.name == list(data[i].keys())[0]:
    #             player.NAME = menu.name
    #             player.MONEY = data[i][f'{menu.name}']
    #             Menu().run(menu.name, data[i][f'{menu.name}'])
    player.NAME = "Admin"
    player.MONEY = data[0]["Admin"]
    print(player.NAME, player.MONEY)
    Menu().run("Admin", data[0]["Admin"])
     