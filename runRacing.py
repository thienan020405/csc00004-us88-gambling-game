from Settings import *
from Racing import Racing

class runRacing():
    def __init__(self, cars_name):

        # general
        pygame.init()
        pygame.display.set_caption('US88')
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.cars_name = cars_name
        self.racing = Racing(self.cars_name)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display_surface.fill((0, 0, 0))
            self.racing.run()
        
            pygame.display.update()
            self.clock.tick(60)

