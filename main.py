import pygame
from pygame.locals import *
import time
import random
import os

# Resolve paths relative to the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPLE_IMG = os.path.join(BASE_DIR, "apple.jpg")
BLOCK_IMG = os.path.join(BASE_DIR, "block.jpg")
SOUND_DING = os.path.join(BASE_DIR, "ding.mp3")
SOUND_CRASH = os.path.join(BASE_DIR, "crash.mp3")

SIZE = 20
inc = 0.2
class Apple:
    def __init__(self,parent_screen):
        self.image_rezie = pygame.image.load(APPLE_IMG)
        self.image = pygame.transform.scale(self.image_rezie,(20,20))
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,33) * SIZE
        self.y = random.randint(0,28) * SIZE

class Snack:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.normal_block = pygame.image.load(BLOCK_IMG).convert()
        self.length = length
        self.block = pygame.transform.scale(self.normal_block,(20,20))
        
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length 
        self.direction = 'right'

    def draw(self):
        self.parent_screen.fill(((0,0,0)))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    
        
    def increase_lenght(self):
        self.inc = 0.2
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length -1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
            self.draw()

        if self.direction == 'down':
            self.y[0] += SIZE
            self.draw()


        if self.direction == 'right':
            self.x[0] += SIZE
            self.draw()

        if self.direction == 'left':
            self.x[0] -= SIZE
            self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # self.background_play_music()
        self.surface =  pygame.display.set_mode((700,600))
        self.surface.fill((0,0,0))
        self.snack = Snack(self.surface,1)
        self.apple = Apple(self.surface)
        self.snack.draw()
        self.apple.draw()
        self.snake_speed = 0.2  # Initial speed

    def adjust_speed(self):
        self.snake_speed = max(0.05, 0.2 - (self.snack.length * 0.001))  # Speed up as the snake grows


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    



    

    # def background_play_music(self):
    #     pygame.mixer.music.load('music_1.mp3')
    #     pygame.mixer.music.play()

    def play_sound(self,sound):
        play_sound = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(play_sound)


    def play(self):
        self.snack.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.snack.x[0], self.snack.y[0], self.apple.x, self.apple.y):
            self.play_sound(SOUND_DING)
            self.snack.increase_lenght()
            self.apple.move()

        for i in range(1,self.snack.length):
            if self.is_collision(self.snack.x[0],self.snack.y[0],self.snack.x[i],self.snack.y[i]):
                self.play_sound(SOUND_CRASH)
                raise "Game over"
        if not (0 <= self.snack.x[0] <= 700 and 0 <= self.snack.y[0] <= 600):
            self.play_sound(SOUND_CRASH)
            raise "Hit the boundry error"


    def show_game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial',20)
        line1 = font.render(f"Game over! your total score is {self.snack.length}",True,(255,255,255))
        self.surface.blit(line1,(200,250))
        line2 = font.render("To play agin press enter button or q to exit",True,(255,255,255))
        self.surface.blit(line2,(200,280))
        pygame.display.flip()
        # pygame.mixer.music.pause()

    def reset(self):
        self.snack = Snack(self.surface,1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f'Score:{self.snack.length}',True,(255,255,255))
        self.surface.blit(score,(600,10))

    def run(self):
        running = True
        pause = False

        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        running = False

                    if event.key == K_RETURN:
                        # pygame.mixer.music.unpause()
                        pause = False
                    if not pause:    
                        if event.key == K_UP:
                            self.snack.move_up()

                        if event.key == K_DOWN:
                            self.snack.move_down()
            
                        if event.key == K_RIGHT:
                            self.snack.move_right()
                
                        if event.key == K_LEFT:
                            self.snack.move_left()
                            
                elif event.type == QUIT:
                    running = False 
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                
            self.adjust_speed()  # Adjust speed based on snake length
            time.sleep(self.snake_speed)  # Add delay


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(str(e))
        print("An error occurred. Check error_log.txt for details.")

    