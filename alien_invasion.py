import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from alien import Alien

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    background = pygame.image.load('images/space.bmp').convert()
    pygame.display.set_caption('alien invasion')

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "play")

    # 创建一个用于存储游戏统计信息的实例
    stats= GameStats(ai_settings)

    # 创建一个记分板
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个用户存储外星人的编组
    aliens = Group()

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            gf.create_fleet(ai_settings, screen, ship, aliens, stats)
            ship.update()
            bullets.update()
            gf.update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, background)

run_game()