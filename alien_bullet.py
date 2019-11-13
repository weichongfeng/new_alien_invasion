import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """外星人子弹"""

    def __init__(self, ai_settings, screen, alien, ship):
        super(AlienBullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0,ai_settings.bullet_width,
                                ai_settings.bullet_height)

        # 在(0,0)处创建一个表示子弹的矩形, 再设置正确的位置
        self.image = pygame.image.load('images/alien_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.color = ai_settings.bullet_color
        self.y_speed_factor = ai_settings.alien_bullet_speed
        self.x_speed_factor = self.y_speed_factor * (ship.rect.centerx - alien.rect.centerx) / (ship.rect.centery - alien.rect.centery)

    def update(self):
        """向上移动"""
        # 更新表示子弹位置的小数
        self.y += self.y_speed_factor
        self.x += self.x_speed_factor
        # 更新子弹的y坐标
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)