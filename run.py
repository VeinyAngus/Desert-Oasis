import pygame
from world_gen import World
from player import Player


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
main_font = pygame.font.SysFont('arial', 25)

player = Player(debug=False)
levels = dict()

desert_raw = pygame.image.load('img/desert_tile.jpg').convert_alpha()
desert = pygame.transform.scale(desert_raw, (100, 100))

oasis_raw = pygame.image.load('img/oasis_tile.jpg').convert_alpha()
oasis = pygame.transform.scale(oasis_raw, (100, 100))

mountain_raw = pygame.image.load('img/mountain_tile.jpg').convert_alpha()
mountain = pygame.transform.scale(mountain_raw, (100, 100))

mined_mountain_raw = pygame.image.load('img/mined_mountain.png').convert_alpha()
mined_mountain = pygame.transform.scale(mined_mountain_raw, (100, 100))

hut_tile_raw = pygame.image.load('img/hut_tile.png').convert_alpha()
hut_tile = pygame.transform.scale(hut_tile_raw, (100, 100))

house_tile_raw = pygame.image.load('img/house_tile.png').convert_alpha()
house_tile = pygame.transform.scale(house_tile_raw, (100, 100))

well_tile_raw = pygame.image.load('img/well_tile.png').convert_alpha()
well_tile = pygame.transform.scale(well_tile_raw, (100, 100))

farm_tile_raw = pygame.image.load('img/farm_tile.png').convert_alpha()
farm_tile = pygame.transform.scale(farm_tile_raw, (100, 100))

grass_tile_raw = pygame.image.load('img/grass_developed_tile.png').convert_alpha()
grass_tile = pygame.transform.scale(grass_tile_raw, (100, 100))

delete_x = pygame.image.load('img/delete_x.png').convert_alpha()

toolbar_raw = pygame.image.load('img/toolbar.png').convert_alpha()
toolbar = pygame.transform.scale(toolbar_raw, (800, 100))

structure_bar_raw = pygame.image.load('img/toolbar_structure_selector.png').convert_alpha()
structure_bar = pygame.transform.scale(structure_bar_raw, (100, 600))

tile_bar_raw = pygame.image.load('img/tile_toolbar.png').convert_alpha()
tile_bar = pygame.transform.scale(tile_bar_raw, (100, 300))

industry_bar_raw = pygame.image.load('img/industry_toolbar.png').convert_alpha()
industry_bar = pygame.transform.scale(industry_bar_raw, (100, 200))

resource_bar = pygame.image.load('img/resource_bar.png').convert_alpha()


tool_bar_click = pygame.mixer.Sound('audio/tool_bar_click.ogg')
build_hut_house = pygame.mixer.Sound('audio/build_hut_house.ogg')
mine_sound = pygame.mixer.Sound('audio/stone_break.ogg')
well_sound = pygame.mixer.Sound('audio/well_sound.ogg')
grass_sound = pygame.mixer.Sound('audio/grass_sound.ogg')
bulldozer = pygame.mixer.Sound('audio/bulldozer.ogg')
pygame.mixer.music.load('audio/theme.mp3')
pygame.mixer.music.set_volume(.4)
pygame.mixer.music.play(-1)

struct_bar_rect = pygame.Rect(0, 700, 100, 100)
tile_bar_rect = pygame.Rect(100, 700, 100, 100)
industry_bar_rect = pygame.Rect(200, 700, 100, 100)
delete_rect = pygame.Rect(300, 700, 100, 100)
up_rect = pygame.Rect(400, 700, 100, 100)
down_rect = pygame.Rect(500, 700, 100, 100)
left_rect = pygame.Rect(600, 700, 100, 100)
right_rect = pygame.Rect(700, 700, 100, 100)

running = True
show_structure_bar = False
show_tile_bar = False
show_industry_bar = False
holding_hut = False
holding_house = False
holding_well = False
holding_farm = False
holding_grass_tile = False
holding_oasis_tile = False
holding_mine_tile = False
holding_delete = False
map_x = 0
map_y = 0
world = World()
levels[(map_x, map_y)] = world.tiles
level_timer = 0
while running:
    clock.tick(60)
    level_timer += 1
    if level_timer >= 300:
        player.water += player.water_sources
        for farm in range(player.farms):
            player.food += 1
        player.minerals += player.mines
        level_timer = 0
    # Get mouse coordinates and update mouse rect
    mouse_pos = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 2, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                holding_hut = False
                holding_house = False
                holding_well = False
                holding_grass_tile = False
                holding_mine_tile = False
                holding_delete = False
                holding_farm = False
        if event.type == pygame.MOUSEBUTTONUP:
            if holding_hut:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        if tile.tile_name == 'grass developed tile':
                            if player.minerals >= 3 and player.food >= 5 and player.water_sources >= 2:
                                build_hut_house.play()
                                tile.img = hut_tile
                                tile.tile_name = 'hut'
                                holding_hut = False
                                player.water_sources -= 2
                                player.minerals -= 3
                                player.food -= 5
                                player.population += 1
            if holding_well:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        for inner_tile in levels[(map_x, map_y)]:
                            if inner_tile.tile_name == 'oasis':
                                if abs(inner_tile.img_rect.x - tile.img_rect.x) <= 100:
                                    if abs(inner_tile.img_rect.y - tile.img_rect.y) <= 100:
                                        if tile.tile_name == 'grass developed tile':
                                            if player.minerals > 2 and player.food > 2:
                                                well_sound.play()
                                                tile.img = well_tile
                                                tile.tile_name = 'well'
                                                holding_well = False
                                                player.water_sources += 1
                                                player.minerals -= 2
                                                player.food -= 2
            if holding_farm:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        if tile.tile_name == 'grass developed tile':
                            if player.water_sources >= 1 and player.food >= 2 and player.water >= 10:
                                build_hut_house.play()
                                tile.img = farm_tile
                                tile.tile_name = 'farm'
                                holding_farm = False
                                player.water_sources -= 1
                                player.food -= 2
                                player.water -= 10
                                player.farms += 1
            if holding_mine_tile:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        if tile.tile_name == 'mountain':
                            if player.water >= 5 and player.minerals >= 2 and player.food >= 5:
                                mine_sound.play()
                                tile.img = mined_mountain
                                tile.tile_name = 'mined mountain'
                                holding_mine_tile = False
                                player.food -= 5
                                player.water -= 5
                                player.mines += 1
            if holding_oasis_tile:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        if tile.tile_name == 'desert':
                            if player.water >= 50 and player.minerals >= 10 and player.food >= 15:
                                tile.img = oasis
                                tile.tile_name = 'oasis'
                                holding_oasis_tile = False
                                player.food -= 15
                                player.water -= 50
            if holding_grass_tile:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        for inner_tile in levels[(map_x, map_y)]:
                            if inner_tile.tile_name == 'oasis' or inner_tile.tile_name == 'well':
                                if abs(inner_tile.img_rect.x - tile.img_rect.x) <= 100:
                                    if abs(inner_tile.img_rect.y - tile.img_rect.y) <= 100:
                                        if tile.tile_name == 'desert':
                                            if player.food >= 1 and player.water >= 5:
                                                tile.img = grass_tile
                                                tile.tile_name = 'grass developed tile'
                                                grass_sound.play()
                                                holding_grass_tile = False
                                                player.food -= 1
                                                player.water -= 5
                                                break
            if holding_delete:
                for tile in levels[(map_x, map_y)]:
                    if mouse_rect.colliderect(tile.img_rect):
                        if tile.tile_name in ['hut', 'house', 'grass developed tile', 'well']:
                            bulldozer.play()
                            tile.img = desert
                            tile.tile_name = 'desert'
            if mouse_rect.colliderect(struct_bar_rect):
                tool_bar_click.play()
                if not holding_delete:
                    if show_structure_bar:
                        show_structure_bar = False
                    else:
                        show_structure_bar = True
                        bar_rect_one = pygame.Rect(0, 600, 100, 100)
                        bar_rect_two = pygame.Rect(0, 500, 100, 100)
                        bar_rect_three = pygame.Rect(0, 400, 100, 100)
                        if show_tile_bar:
                            show_tile_bar = False
            if mouse_rect.colliderect(tile_bar_rect):
                tool_bar_click.play()
                if not holding_delete:
                    if show_tile_bar:
                        show_tile_bar = False
                    else:
                        show_tile_bar = True
                        grass_tile_bar = pygame.Rect(100, 600, 100, 100)
                        oasis_tile_bar = pygame.Rect(100, 400, 100, 100)
                        if show_structure_bar:
                            show_structure_bar = False
            if mouse_rect.colliderect(industry_bar_rect):
                tool_bar_click.play()
                if not holding_delete:
                    if show_industry_bar:
                        show_industry_bar = False
                    else:
                        show_industry_bar = True
                        mine_tile_bar = pygame.Rect(200, 600, 100, 100)
            if show_structure_bar:
                if mouse_rect.colliderect(bar_rect_one):
                    show_structure_bar = False
                    holding_well = True
                if mouse_rect.colliderect(bar_rect_two):
                    show_structure_bar = False
                    holding_farm = True
                if mouse_rect.colliderect(bar_rect_three):
                    show_structure_bar = False
                    holding_hut = True
            if show_tile_bar:
                if mouse_rect.colliderect(grass_tile_bar):
                    show_tile_bar = False
                    holding_grass_tile = True
                if mouse_rect.colliderect(oasis_tile_bar):
                    show_tile_bar = False
                    holding_oasis_tile = True
            if show_industry_bar:
                if mouse_rect.colliderect(mine_tile_bar):
                    show_industry_bar = False
                    holding_mine_tile = True
            if mouse_rect.colliderect(delete_rect):
                tool_bar_click.play()
                if holding_delete:
                    holding_delete = False
                else:
                    holding_delete = True
                    show_structure_bar = False
            if mouse_rect.colliderect(up_rect):
                tool_bar_click.play()
                map_y -= 1
                if (map_x, map_y) not in levels.keys():
                    world = World()
                    levels[(map_x, map_y)] = world.tiles
            if mouse_rect.colliderect(down_rect):
                tool_bar_click.play()
                map_y += 1
                if (map_x, map_y) not in levels.keys():
                    world = World()
                    levels[(map_x, map_y)] = world.tiles
            if mouse_rect.colliderect(left_rect):
                tool_bar_click.play()
                map_x -= 1
                if (map_x, map_y) not in levels.keys():
                    world = World()
                    levels[(map_x, map_y)] = world.tiles
            if mouse_rect.colliderect(right_rect):
                tool_bar_click.play()
                map_x += 1
                if (map_x, map_y) not in levels.keys():
                    world = World()
                    levels[(map_x, map_y)] = world.tiles
    for tile in levels[(map_x, map_y)]:
        screen.blit(tile.img, tile.img_rect)
    screen.blit(toolbar, (0, 700))
    if show_structure_bar:
        screen.blit(structure_bar, (0, 100))
    if show_tile_bar:
        screen.blit(tile_bar, (100, 400))
    if show_industry_bar:
        screen.blit(industry_bar, (200, 500))
    for tile in levels[(map_x, map_y)]:
        if holding_delete:
            if mouse_rect.colliderect(tile.img_rect):
                if tile.tile_name in ['hut', 'house', 'grass developed tile', 'well']:
                    pygame.draw.rect(screen, (255, 153, 0), tile.img_rect, 4)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), tile.img_rect, 6)
                    screen.blit(delete_x, (tile.img_rect.x, tile.img_rect.y))
        elif holding_farm:
            if mouse_rect.colliderect(tile.img_rect):
                if tile.tile_name == 'grass developed tile':
                    pygame.draw.rect(screen, (0, 150, 0), tile.img_rect, 4)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), tile.img_rect, 6)
        elif holding_well:
            for new_tile in levels[(map_x, map_y)]:
                if mouse_rect.colliderect(new_tile.img_rect):
                    for inner_tile in levels[(map_x, map_y)]:
                        if inner_tile.tile_name == 'oasis':
                            if abs(inner_tile.img_rect.x - new_tile.img_rect.x) <= 100:
                                if abs(inner_tile.img_rect.y - new_tile.img_rect.y) <= 100:
                                    if new_tile.tile_name == 'grass developed tile':
                                        pygame.draw.rect(screen, (0, 150, 0), new_tile.img_rect, 4)
                                    else:
                                        pygame.draw.rect(screen, (255, 0, 0), new_tile.img_rect, 6)
        elif holding_hut:
            if mouse_rect.colliderect(tile.img_rect):
                if tile.tile_name == 'grass developed tile':
                    pygame.draw.rect(screen, (0, 150, 0), tile.img_rect, 4)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), tile.img_rect, 6)
        elif holding_mine_tile:
            if mouse_rect.colliderect(tile.img_rect):
                if tile.tile_name == 'mountain':
                    pygame.draw.rect(screen, (0, 150, 0), tile.img_rect, 4)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), tile.img_rect, 6)
        elif holding_grass_tile:
            for new_tile in levels[(map_x, map_y)]:
                if mouse_rect.colliderect(new_tile.img_rect):
                    for inner_tile in levels[(map_x, map_y)]:
                        if inner_tile.tile_name == 'oasis' or inner_tile.tile_name == 'well':
                            if abs(inner_tile.img_rect.x - new_tile.img_rect.x) <= 100:
                                if abs(inner_tile.img_rect.y - new_tile.img_rect.y) <= 100:
                                    if new_tile.tile_name == 'desert':
                                        pygame.draw.rect(screen, (0, 150, 0), new_tile.img_rect, 4)
                                    else:
                                        pygame.draw.rect(screen, (255, 0, 0), new_tile.img_rect, 6)
        else:
            if show_structure_bar:
                pass
            elif show_tile_bar:
                pass
            else:
                if mouse_rect.colliderect(tile.img_rect):
                    pygame.draw.rect(screen, (255, 255, 0), tile.img_rect, 4)
    location_label = main_font.render(f'{map_x}, {map_y}', True, (0, 0, 0))
    water_sources_label = main_font.render(f'{player.water_sources}', True, (255, 255, 255))
    water_label = main_font.render(f'{player.water}', True, (255, 255, 255))
    mineral_label = main_font.render(f'{player.minerals}', True, (255, 255, 255))
    food_label = main_font.render(f'{player.food}', True, (255, 255, 255))
    pop_label = main_font.render(f'{player.population}', True, (255, 255, 255))
    screen.blit(location_label, (20, 10))
    screen.blit(resource_bar, (350, 0))
    screen.blit(water_sources_label, (425, 0))
    screen.blit(water_label, (495, 0))
    screen.blit(mineral_label, (575, 0))
    screen.blit(food_label, (655, 0))
    screen.blit(pop_label, (715, 0))
    pygame.display.update()
