import pygame
import random
import sys
import os
import json

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_BASE_SPEED = 5
DOCTOR_SPEED = 1.5
SUGAR_SIZE = 30
FONT = pygame.font.Font(None, 36)
LEADERBOARD_FILE = "leaderboard.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sugar Rush: The Sweet Run")

# Load images
player_img = pygame.transform.scale(pygame.image.load("player.png"), (50, 50))
player2_img = pygame.transform.scale(pygame.image.load("player.png"), (50, 50))
doctor_img = pygame.transform.scale(pygame.image.load("doctor.png"), (50, 50))
cake_img = pygame.transform.scale(pygame.image.load("cake.png"), (30, 30))
chocolate_img = pygame.transform.scale(pygame.image.load("chocolate.png"), (30, 30))
salad_img = pygame.transform.scale(pygame.image.load("salad.png"), (30, 30))
vegetable_img = pygame.transform.scale(pygame.image.load("vegetable.png"), (30, 30))
icecream_img = pygame.transform.scale(pygame.image.load("icecream.png"), (30, 30))
background_img = pygame.transform.scale(pygame.image.load("background2.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, image, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT // 2
        self.health = 100
        self.speed = PLAYER_BASE_SPEED
        self.controls = controls

    def update(self, keys):
        if keys[self.controls['up']]:
            self.rect.y -= self.speed
        if keys[self.controls['down']]:
            self.rect.y += self.speed
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
        if keys[self.controls['right']]:
            self.rect.x += self.speed
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

class Doctor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = doctor_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = DOCTOR_SPEED

    def update(self, target_rect):
        if self.rect.x > target_rect.x:
            self.rect.x -= self.speed
        elif self.rect.x < target_rect.x:
            self.rect.x += self.speed
        if self.rect.y > target_rect.y:
            self.rect.y -= self.speed
        elif self.rect.y < target_rect.y:
            self.rect.y += self.speed

class Sugar(pygame.sprite.Sprite):
    def __init__(self, sugar_type):
        super().__init__()
        self.type = sugar_type
        self.image = {'cake': cake_img, 'chocolate': chocolate_img, 'salad': salad_img, 'vegetable': vegetable_img, 'icecream': icecream_img}[sugar_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, SCREEN_WIDTH - 100)
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 100)

def display_text(text, x, y, color=BLACK, center=False, font=FONT):
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)
    else:
        screen.blit(label, (x, y))

def countdown():
    for num in ["3", "2", "1", "GO!"]:
        screen.blit(background_img, (0, 0))
        display_text(num, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED, center=True, font=pygame.font.Font(None, 100))
        pygame.display.update()
        pygame.time.wait(1000)

def game_loop(multiplayer=False, game_duration=30000):
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    sugars = pygame.sprite.Group()
    player1 = Player(player_img, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})
    all_sprites.add(player1)
    score1 = 0

    if multiplayer:
        player2 = Player(player2_img, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
        all_sprites.add(player2)
        score2 = 0

    doctor = Doctor()
    all_sprites.add(doctor)

    warning_time1 = None
    warning_time2 = None

    countdown()

    start_time = pygame.time.get_ticks()
    running = True
    while running:
        clock.tick(FPS)
        elapsed_time = pygame.time.get_ticks() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if elapsed_time >= game_duration:
            return True

        keys = pygame.key.get_pressed()
        player1.update(keys)
        if multiplayer:
            player2.update(keys)

        target = player1 if not multiplayer or player1.health <= player2.health else player2
        doctor.update(target.rect)

        for player, score, warning_time in [(player1, score1, warning_time1)] + ([(player2, score2, warning_time2)] if multiplayer else []):
            collected = pygame.sprite.spritecollide(player, sugars, True)
            for sugar in collected:
                if sugar.type in ['cake', 'chocolate', 'icecream']:
                    player.health -= 15
                    player.speed = max(2, player.speed - 1)
                    if player == player1:
                        warning_time1 = pygame.time.get_ticks()
                    else:
                        warning_time2 = pygame.time.get_ticks()
                else:
                    player.health += 10
                    player.speed = min(8, player.speed + 1)
                if player == player1:
                    score1 += 1
                else:
                    score2 += 1

            if doctor.rect.colliderect(player.rect):
                display_text(f"{('Player 1' if player == player1 else 'Player 2')} Caught!", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, RED)
                pygame.display.update()
                pygame.time.wait(2000)
                return False

        if random.random() < 0.02:
            if random.random() < 2/6:
                sugar_type = random.choice(['cake', 'chocolate', 'icecream'])
            else:
                sugar_type = random.choice(['salad', 'vegetable'])
            new_sugar = Sugar(sugar_type)
            all_sprites.add(new_sugar)
            sugars.add(new_sugar)

        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        display_text(f"P1 Score: {score1} Health: {player1.health}", 10, 10)
        if multiplayer:
            display_text(f"P2 Score: {score2} Health: {player2.health}", 10, 40)
        if warning_time1 and pygame.time.get_ticks() - warning_time1 < 3000:
            display_text("\u26a0 P1 Energy Running Low!", SCREEN_WIDTH // 3, 80, RED)
        if multiplayer and warning_time2 and pygame.time.get_ticks() - warning_time2 < 3000:
            display_text("\u26a0 P2 Energy Running Low!", SCREEN_WIDTH // 3, 120, RED)

        time_left = max(0, (game_duration - elapsed_time) // 1000)
        display_text(f"Time Left: {time_left}s", SCREEN_WIDTH - 200, 10)

        pygame.display.update()

def start_screen():
    button_font = pygame.font.Font(None, 50)
    start_button = button_font.render("START SINGLE PLAYER", True, WHITE, BLUE)
    multi_button = button_font.render("START MULTIPLAYER", True, WHITE, BLUE)
    start_rect = start_button.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
    multi_rect = multi_button.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))

    while True:
        screen.blit(background_img, (0, 0))
        screen.blit(start_button, start_rect)
        screen.blit(multi_button, multi_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return False
                if multi_rect.collidepoint(event.pos):
                    return True

def end_screen():
    button_font = pygame.font.Font(None, 50)
    restart_button = button_font.render("PLAY NEXT LEVEL", True, WHITE, RED)
    restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

    while True:
        screen.blit(background_img, (0, 0))
        screen.blit(restart_button, restart_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(event.pos):
                return

if __name__ == "__main__":
    levels = [10000, 20000, 40000]  # 10s, 20s, 40s
    while True:
        multiplayer = start_screen()
        for duration in levels:
            success = game_loop(multiplayer, game_duration=duration)
            if not success:
                break
            end_screen()
