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

player_x = 50
player_y = 50
player_speed = 0.3  # 玩家速度


# 加载 .tmx 地图文件
tmx_data = pytmx.load_pygame("demo2.tmx")  # 将 'your_map.tmx' 替换为你的文件路径

# 创建一个地图渲染函数
def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# 游戏主循环
running = True
while running:
    draw_map()  # 绘制地图

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 处理键盘输入来移动玩家
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed  # 向左移动
        player_x = new_x

    if keys[pygame.K_RIGHT]:
        new_x += player_speed  # 向右移动
        player_x = new_x

    if keys[pygame.K_UP]:
        new_y -= player_speed  # 向上移动
        player_y = new_y

    if keys[pygame.K_DOWN]:
        new_y += player_speed  # 向下移动
        player_y = new_y

    # 限制玩家位置在屏幕内
    player_x, player_y = limit_position_to_screen(player_x, player_y, 32, 32)
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player_x, player_y, 32, 32))  # 32x32 是玩家的大小
    pygame.display.flip()  # 更新显示

pygame.quit()