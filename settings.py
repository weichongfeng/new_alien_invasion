import time

class Settings():
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed_factor = 1
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allow = 30

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人点数提高的速度
        self.score_scale = 1.5
        # 外星人刷新速度
        self.add_alien_time = 0.5
        # 屏幕上最多外星人数量
        self.max_alien_num = 10

        self.initialize_dynamic_settings()
        # fleet_direction为1表示向右移动,为-1表示向左移
        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行而变化设置"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.alien_points = 50
        # 存储上次刷新外星人时间
        self.last_add_alien_time = round(time.time(),1)

    def update_add_alien_time(self):
        self.last_add_alien_time = round(time.time(),1)

