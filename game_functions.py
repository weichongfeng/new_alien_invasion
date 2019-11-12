import sys, random, time
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮开始游戏"""

    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:

        # 影藏鼠标
        pygame.mouse.set_visible(False)

        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人,并让飞船居中
        # create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)


def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button, background):
    """更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环时重新绘制屏幕
    # screen.fill(ai_setting.bg_color)
    screen.blit(background, (0, 0))

    # 在飞船和外星人后面重绘所有子弹
    # for bullet in bullets.sprites():
    #     bullet.draw_bullet()
    bullets.draw(screen)

    # 绘制飞船
    ship.blitme()

    # 绘制外星人
    aliens.draw(screen)

    # 绘制记分板
    sb = sb
    sb.show_score()

    # 如果游戏处于非活动状态,就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """跟新子弹位置,并删除一消失的子弹"""
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)

    # 检查屏幕上是否还存在外星人
    if len(aliens) == 0:
        pass
        # 删除现有的子弹并新建一群外星人
        # bullets.empty()

        # 提高等级
        # stats.level += 1
        # sb.prep_level()



def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allow:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens):
   """创建第一个外星人并将其加入当前行"""
   alien = Alien(ai_settings, screen)
   alien.rect.x = random.randint(0,alien.screen_rect.width - alien.rect.width)
   alien.rect.y = 0
   aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, stats):
    """创建外星人群"""

    # 判断屏幕上现在有多少个外星人
    if len(aliens) < ai_settings.max_alien_num and round(time.time(),1) - ai_settings.last_add_alien_time > ai_settings.add_alien_time:
        create_alien(ai_settings, screen, aliens)
        ai_settings.update_add_alien_time()

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘,并更新整群外星人位置"""
    for alien in aliens:
        if alien.rect.bottom >= alien.screen_rect.height:
            aliens.remove(alien)
    aliens.update()

    # 检测外星人和飞船之前的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""

    if stats.ships_left > 0:
        # 将ships_left 减一
        stats.ships_left -= 1

        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人, 并将飞船放到屏幕底端中央
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()