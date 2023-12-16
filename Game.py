from Settings import *
from Racing import Racing
class Game:
    def __init__(self, map_number, user_coin, item_speed, item_x2, item_sale):
        pygame.init()
        pygame.display.set_caption('US88')
        self.display_surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.width, self.height = self.display_surface.get_size()
        self.font = pygame.font.Font("CSFONT-TwistyPixel.ttf", round(self.width * 5 / 128))
        # Name for random choices
        self.Name = ['Hawkeye', 'Loki', 'Daredevil', 'Storm', 'Ultron', 'Groot', 'Magneto', 'Wanda', 'Wasp',
         'Shang-Chi', 'Yondu', 'Thanos', 'Hulk', 'X-Men', 'Nebula', 'Thor', 'Dr. Strange']

        # List of maps' images, list of cars' images and cars' rect
        self.maps_rect_list = []
        self.cars_image_list = []
        self.cars_rect_list = []

        self.cars_name_list = ['Bí danh: ', 'Bí danh: ', 'Bí danh: ', 'Bí danh: ', 'Bí danh: ']
        self.current_opponent = 0
        # self.name_x = self.width * 7 / 64

        self.coins_rect_list = []
        self.coins_list = ['100$', '200$', '300$', '400$']

        # cursor attributes
        self.mouse_pos = (0, 0)
        self.mouse_sound = pygame.mixer.Sound('mouseclick1.mp3')
        # pygame.mouse.set_visible(False)
        # self.cursor_img = pygame.image.load('normal.png')
        # self.cursor_img_rect = self.cursor_img.get_rect()

        # the number of map, car and coin that user choose
        self.map = map_number
        self.car = 0
        self.coin_betted = 0
        self.coin = user_coin


        # the state of each def
        self.chose_car = False
        self.changed_name = False
        self.changed_opponents = False
        self.displayed_information = False
        self.chose_coin = False

        # the image of map and coin
        self.map_image = 0
        self.coin_image = 0
 
        self.enter = False

        # background
        self.bg_temp = pygame.image.load('ChoosingCarBackground.png').convert_alpha()
        self.bg = pygame.image.load('ChoosingCarBackground.png').convert_alpha()
        self.bg_temp.set_alpha(120)

        self.item_speed = item_speed
        self.item_x2 = item_x2
        self.item_sale = item_sale

    def display_cursor(self):
        self.cursor_img_rect = pygame.mouse.get_pos()
        self.display_surface.blit(self.cursor_img, self.cursor_img_rect)


    def list_cars(self):

        if self.chose_car == False:
            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.bg, (0, 0))
            cars_x = self.width * 7 / 64

            text = self.font.render('HÃY CHỌN CHIẾN MÃ CỦA BẠN', False, 'Red')
            text_rect = text.get_rect(center = (self.width / 2, self.height * 5 / 36))
            self.display_surface.blit(text, text_rect)
           
            self.cars_rect_list = []
            for i in range(1, CARS + 1):                
                cars_image = pygame.transform.scale(pygame.image.load(f'sets/set{self.map}/cars/car{i}/normal.png').convert_alpha(), (self.width * 5 / 64, self.height * 13 / 144))
                cars_rect = cars_image.get_rect(center = (cars_x, self.height / 2))
                if len(self.cars_rect_list) != CARS:
                    self.cars_image_list.append(cars_image)
                    self.cars_rect_list.append(cars_rect)
                self.display_surface.blit(cars_image, cars_rect)

                cars_x += (self.width - self.width * 7 / 32) / (CARS - 1)

        if self.car > 0 and self.chose_car == False:
            # self.cars_image_list[self.car - 1] = pygame.transform.scale(pygame.image.load(f'xe{self.car}.png').convert_alpha(), (100, 65))
            self.chose_car = True


    def change_name(self):
        
        if self.chose_car and self.changed_name == False:
            self.cars_image_list = []

            for i in range(1, CARS + 1):                
                cars_image = pygame.transform.scale(pygame.image.load(f'sets/set{self.map}/cars/car{i}/normal.png').convert_alpha(), (self.width * 5 / 64, self.height * 13 / 144))
                self.cars_image_list.append(cars_image)

            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.bg, (0, 0))
            cars_x = self.width * 7 / 64
            name_x = self.width * 7 / 64

            text = self.font.render('HÃY CHỌN BÍ DANH CHO BẢN THÂN VÀ CÁC ĐỐI THỦ', False, 'Red')
            text_rect = text.get_rect(center = (self.width / 2, self.height * 5 / 36))
            self.display_surface.blit(text, text_rect)
             
            for i in range(CARS):
            
                cars_image = self.cars_image_list[i]
                name_surface = self.font.render(self.cars_name_list[i], True, (255, 255, 255))

                cars_rect = cars_image.get_rect(center = (cars_x, self.height / 2))
                name_rect = name_surface.get_rect(center = (cars_x, self.height * 25 / 36))
                                
                self.display_surface.blit(cars_image, cars_rect)
                self.display_surface.blit(name_surface, name_rect)

                if i == self.car - 1:
                    pygame.draw.rect(self.display_surface, COLOR, cars_rect, 1)
                
                cars_x += (self.width - self.width * 7 / 32) / (CARS - 1)

            for i in range(CARS):

                if i == self.current_opponent:

                    name_surface = self.font.render(self.cars_name_list[self.current_opponent], True, (255, 255, 255))

                    name_rect = name_surface.get_rect(center = (name_x + (self.width - self.width * 7 / 32) / (CARS - 1) * i, self.height * 25 / 36))

                    pygame.draw.rect(self.display_surface, COLOR, name_rect, 2)
                                
                    self.display_surface.blit(name_surface, name_rect)


    def bet_money(self):
        
        if self.changed_name and self.chose_coin == False:

            self.coins_rect_list = []
            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.bg, (0, 0))
            coins_x = self.width * 7 / 64

            text = self.font.render('HÃY CHỌN MỨC CƯỢC THÔI NÀO', False, 'Red')
            text_rect = text.get_rect(center = (self.width / 2, self.height * 5 / 36))
            self.display_surface.blit(text, text_rect)
           
            for i in range(1, COINS + 1):                
                coins_image = pygame.transform.scale(pygame.image.load(f'coins/coin{i}.png').convert_alpha(), (self.width * 5 / 64, self.height / 9))
                coins_rect = coins_image.get_rect(center = (coins_x, self.height / 2))

                price_surface = self.font.render(self.coins_list[i - 1], True, (255, 255, 255))
                price_rect = price_surface.get_rect(center = (coins_x, self.height * 25 / 36))

                
                self.coins_rect_list.append(coins_rect)

                self.display_surface.blit(coins_image, coins_rect)
                self.display_surface.blit(price_surface, price_rect)

                coins_x += (self.width - self.width * 7 / 32) / (COINS - 1)

        if self.coin_betted >= 100 and self.coin_betted <= self.coin and self.chose_coin == False:
            self.chose_coin = True
            

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # self.mouse_sound.play()

                    # Choose your car
                    if self.chose_car == False:
                        for j in range(len(self.cars_rect_list)):
                            if self.cars_rect_list[j].collidepoint(event.pos):
                                self.car = j + 1

                    # Choose your bet money
                    if self.chose_coin == False:
                        for k in range(len(self.coins_rect_list)):
                            if self.coins_rect_list[k].collidepoint(event.pos):
                                self.coin_betted = (k + 1) * 100

                if event.type == pygame.KEYDOWN:

                    self.enter = True

                    # Input name for each car
                    if self.chose_car and self.changed_opponents == False:

                        if event.key == pygame.K_BACKSPACE and len(self.cars_name_list[self.current_opponent]) >= 10:
                            self.cars_name_list[self.current_opponent] = self.cars_name_list[self.current_opponent][:-1]

                        elif event.key == pygame.K_RETURN and self.enter:
                            self.cars_name_list[self.current_opponent] = self.cars_name_list[self.current_opponent][9:]
                                                         
                            if len(self.cars_name_list[self.current_opponent]) == 0:
                                self.cars_name_list[self.current_opponent] = choice(self.Name)
                                self.Name.remove(self.cars_name_list[self.current_opponent])
                                

                            # self.name_x += (self.width - self.width * 7 / 32) / (CARS - 1)

                            self.current_opponent += 1

                            self.enter = False

                            if self.current_opponent == CARS:
                                self.changed_opponents = True

                        elif len(self.cars_name_list[self.current_opponent]) < 22:
                            self.cars_name_list[self.current_opponent] += event.unicode

                    if self.changed_opponents and self.changed_name == False:
                        if self.enter:
                            self.changed_name = True


            self.width, self.height = self.display_surface.get_size()
            self.bg = pygame.transform.scale(self.bg_temp, (self.width, self.height))
            self.font = pygame.font.Font("CSFONT-TwistyPixel.ttf", round(self.width * 5 / 128))

            if self.chose_coin == False:
                self.list_cars()
                self.change_name()
                self.bet_money()
            else:
                return Racing(self.cars_name_list, self.map, self.car, self.coin_betted, self.item_speed, self.item_x2, self.item_sale).run()
                
                

            pygame.display.update()
            self.clock.tick(60) 

