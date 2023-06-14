import pygame,sys
from config import *
class Button:
    def __init__(self, x, y, w, h, text_color, bg, content, font_size):
        self.font = pygame.font.SysFont('freesansbold.ttf', font_size)
        self.content = content

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text_color = text_color
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def press(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class GameIntro:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.instruct = False
        self.play = False
        self.running = True

        self.background = pygame.image.load("bg/background1.png")
        self.instr_bg = pygame.image.load("bg/instruction.png")

    def check_to_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def menu(self):
        intro = True
        play_button = Button(width/2.6, height/2.5, 190, 50, WHITE, BLACK, 'PLAY', 28)
        instr_button = Button(width/2.6, height/1.7, 190, 50, WHITE, BLACK, 'INSTRUCTIONS', 28)
        while intro:
            self.check_to_quit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.press(mouse_pos, mouse_pressed):
                intro = False
                self.play = True
                self.instruct = False
            if instr_button.press(mouse_pos, mouse_pressed):
                intro = False
                self.instruct = True
                self.play = False

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(instr_button.image, instr_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def instruction(self):
        next_button = Button(width/2.5, height/1.25, 190, 50, WHITE, BLACK, 'NEXT', 28)
        while self.instruct:
            self.screen.blit(self.instr_bg, (0, 0))
            self.screen.blit(next_button.image, next_button.rect)
            self.check_to_quit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if next_button.press(mouse_pos, mouse_pressed):
                self.play = True
                self.instruct = False
            self.clock.tick(FPS)
            pygame.display.update()