import pygame
from config import *
import math
import random
from collections import deque

class Spritesheet():
    def __init__ (self, file):
            self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3,2,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.moving = False
        
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_note()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change = -PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change = PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change = -PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change = PLAYER_SPEED
            self.facing = 'down'

        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.moving = False

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.pages_collected = 0 
            for enemy in self.game.enemies:
                enemy.speed = 0
            self.game.playing = False 

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: 
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_note(self):
        hits = pygame.sprite.spritecollide(self, self.game.notes, True)
        if hits:
            self.game.notes_collected += 1

            if self.game.notes_collected == self.game.total_notes:
                self.game.playing = False 
                self.game.show_victory_screen()

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy (pygame.sprite.Sprite):
    def __init__ (self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.path = []
        self.speed = ENEMY_SPEED

        self.image = self.game.enemy_spritesheet.get_sprite(3,2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"


    def update(self):
        self.speed = ENEMY_SPEED + self.game.notes_collected * 0.1
        self.find_player()
        self.move_along_path()
        self.animate()
    
    def find_player(self):
        # Atualiza o caminho usando Bellman-Ford
        start = (self.rect.x // TILESIZE, self.rect.y // TILESIZE)
        goal = (self.game.player.rect.x // TILESIZE, self.game.player.rect.y // TILESIZE)
        self.path = self.bellman_ford(start, goal)

    def bellman_ford(self, start, goal):
        # Inicializa distâncias e predecessores
        distances = {}
        predecessors = {}
        # Obtém todas as coordenadas possíveis do tilemap
        nodes = [(x, y) for y in range(len(tilemap)) for x in range(len(tilemap[0]))]
        
        for node in nodes:
            distances[node] = float('inf')
            predecessors[node] = None
        distances[start] = 0

        # Relaxamento das arestas até V-1 vezes
        for _ in range(len(nodes) - 1):
            updated = False
            for node in nodes:
                x, y = node
                if not self.is_walkable(x, y):
                    continue
                # Verifica todos os vizinhos possíveis
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = (x + dx, y + dy)
                    if self.is_walkable(neighbor[0], neighbor[1]):
                        # Atualiza a distância se encontrar um caminho mais curto
                        if distances[neighbor] > distances[node] + 1:
                            distances[neighbor] = distances[node] + 1
                            predecessors[neighbor] = node
                            updated = True
            if not updated:
                break  # Otimização: para se não houver mais atualizações

        # Reconstrói o caminho do goal até o start
        path = []
        current = goal
        if distances.get(goal, float('inf')) == float('inf'):
            return path  # Caminho inalcançável

        while current != start:
            path.append(current)
            current = predecessors.get(current)
            if current is None:
                return []  # Não há caminho

        path.reverse()
        return path[1:] if len(path) > 1 else []  # Exclui a posição inicial


    def is_walkable(self, x, y):
        # Verifica se a célula é caminhável (não é um bloco)
        return 0 <= x < len(tilemap[0]) and 0 <= y < len(tilemap) and tilemap[y][x] != 'B'

    def move_along_path(self):
        # Move o inimigo ao longo do caminho encontrado
        if self.path:
            next_x, next_y = self.path[0]
            next_x *= TILESIZE
            next_y *= TILESIZE

            dx = next_x - self.rect.x
            dy = next_y - self.rect.y

            if dx > 0:
                self.rect.x += min(self.speed, dx)
            elif dx < 0:
                self.rect.x += max(-self.speed, dx)

            if dy > 0:
                self.rect.y += min(self.speed, dy)
            elif dy < 0:
                self.rect.y += max(-self.speed, dy)

            # Remove o próximo passo se atingido
            if self.rect.x == next_x and self.rect.y == next_y:
                self.path.pop(0)

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate (self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(352, 352, self.width, self.height)

        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y 

class Ground (pygame.sprite.Sprite):
    def __init__ (self, game, x, y):
        self.game = game 
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Note (pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.notes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.notes_spritesheet.get_sprite(3, 3, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y 

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Slender.ttf', fontsize)
        self.content = content
        self.selected = False

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(self.text, self.text_rect)
    
    def draw(self, screen):
        if self.selected:
            self.image.fill((200, 200, 200))
        else:
            self.image.fill(self.bg)

        self.image.blit(self.text, self.text_rect)
        screen.blit(self.image, (self.x, self.y))


    def is_pressed (self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False