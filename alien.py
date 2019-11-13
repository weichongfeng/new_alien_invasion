import pygame, time
from pygame.sprite import Sprite
from alien_bullet import AlienBullet

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""

        super(Alien,self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # 加载外星人图像,并设置其rect属性
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.y = float(self.rect.x)

        # 最后一次发射子弹的时间
        self.las_fire_time = round(time.time(),1)

    def blitme(self):
        """在指定的位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True

        elif self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.y += 0.2
        self.rect.y = self.y

    def update_last_fire_time(self):
        """更新最后开火时间"""
        self.las_fire_time = round(time.time(), 1)