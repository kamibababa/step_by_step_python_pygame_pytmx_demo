import math
import random

import pygame

# 限制物体在屏幕内
import pytmx


def limit_position_to_screen(x, y, width, height):
    """限制物体在屏幕内"""
    x = max(0, min(x, SCREEN_WIDTH - width))  # 限制x坐标
    y = max(0, min(y, SCREEN_HEIGHT - height))  # 限制y坐标
    return x, y

pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pytmx Demo")


# 加载 .tmx 地图文件
tmx_data = pytmx.load_pygame("demo2.tmx")  # 将 'your_map.tmx' 替换为你的文件路径

# player.x = 50
# player.y = 50
player_speed = 3  # 玩家速度
# 设置玩家的初始位置
player = None
# 找到玩家对象（在 Object Layer 中）
for obj in tmx_data.objects:
    if obj.name == "player":
        player = obj
        break

if player is None:
    raise ValueError("Player object not found in the Object Layer")

# 检查某个位置是否有墙体
def check_collision(x, y):
    # 获取该位置的瓦片 ID
    dic = None
    try:
        x_pos = math.floor(x / tmx_data.tilewidth)
        y_pos = math.floor(y / tmx_data.tileheight)
        # print(x, y)
        print(x_pos, y_pos)
        dic = tmx_data.get_tile_properties(x_pos, y_pos, layer=1)
    except Exception as e:
        pass

    # print(gid)
    if dic:
        return dic['Collidable'] == True
    else:
        return False

# 设置敌人类
class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = 1
        self.width = 32  # 敌人宽度
        self.height = 32  # 敌人高度

    def move_towards_player(self, player, enemies):
        """简单的敌人行为：朝玩家方向移动"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        # 检查敌人移动后是否与墙体发生碰撞
        if not check_collision(self.x + move_x, self.y) and not self.check_overlap(self.x + move_x, self.y, enemies):
            self.x += move_x
        if not check_collision(self.x, self.y + move_y) and not self.check_overlap(self.x, self.y + move_y, enemies):
            self.y += move_y

    def check_overlap(self, new_x, new_y, enemies):
        """检查新位置是否与其他敌人重叠"""
        for enemy in enemies:
            if enemy != self and (enemy.x < new_x + self.width and enemy.x + enemy.width > new_x) and \
                    (enemy.y < new_y + self.height and enemy.y + enemy.height > new_y):
                return True
        return False

    def draw(self):
        """绘制敌人"""
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.x, self.y, self.width, self.height))

# 随机生成敌人并确保它们位于有效位置
def generate_enemies(num_enemies):
    enemies = []
    for _ in range(num_enemies):
        # 随机选择一个位置直到找到一个有效位置
        while True:
            spawn_x = random.randint(0, SCREEN_WIDTH - 32)  # 32 为敌人的宽度
            spawn_y = random.randint(0, SCREEN_HEIGHT - 32)  # 32 为敌人的高度
            if not check_collision(spawn_x, spawn_y) and not any(enemy.check_overlap(spawn_x, spawn_y, enemies) for enemy in enemies):  # 检查新的位置是否有墙体
                break  # 找到有效位置，跳出循环
        speed = random.randint(1, 3)  # 敌人速度在 1 到 3 之间随机
        enemies.append(Enemy(spawn_x, spawn_y, speed))
    return enemies

# 创建敌人
enemies = generate_enemies(5)  # 生成 5 个敌人

# 创建一个地图渲染函数
def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if layer.name == 'wall':
                continue

            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# 游戏主循环
running = True
while running:
    clock = pygame.time.Clock()
    draw_map()  # 绘制地图

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 处理键盘输入来移动玩家
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed  # 向左移动
        if not check_collision(new_x, new_y):
            player.x = new_x

    if keys[pygame.K_RIGHT]:
        new_x += player_speed  # 向右移动
        if not check_collision(new_x, new_y):
            player.x = new_x

    if keys[pygame.K_UP]:
        new_y -= player_speed  # 向上移动
        if not check_collision(new_x, new_y):
            player.y = new_y

    if keys[pygame.K_DOWN]:
        new_y += player_speed  # 向下移动
        if not check_collision(new_x, new_y):
            player.y = new_y

    # 限制玩家位置在屏幕内
    player.x, player.y = limit_position_to_screen(player.x, player.y, 32, 32)
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player.x, player.y, 32, 32))  # 32x32 是玩家的大小

    # 移动并绘制敌人
    for enemy in enemies:
        enemy.move_towards_player(player, enemies)  # 敌人朝玩家移动并检查碰撞
        enemy.x, enemy.y = limit_position_to_screen(enemy.x, enemy.y, enemy.width, enemy.height)  # 限制敌人位置
        enemy.draw()  # 绘制敌人

    pygame.display.flip()  # 更新显示
    # 控制帧率
    clock.tick(30)

pygame.quit()