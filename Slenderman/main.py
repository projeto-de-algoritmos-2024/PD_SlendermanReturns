import pygame
from config import *
from sprites import *
import sys
import os

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centraliza a janela
        pygame.init()
        pygame.mixer.init()

        # Configurar a tela em modo FULLSCREEN
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        # Superfície virtual para renderizar o jogo na resolução original
        self.game_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('./Slender.ttf', 32)

        pygame.mixer.music.load('audio/background_music.mp3')
        pygame.mixer.music.set_volume(0.8)

        self.notes_collected = 0
        self.total_notes = 7

        self.character_spritesheet = Spritesheet ('img/character.png')
        self.terrain_spritesheet = Spritesheet ('img/terrain.png')
        self.enemy_spritesheet = Spritesheet ('img/enemy.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.go_background = pygame.image.load('./img/gameover.png')
        self.notes_spritesheet = Spritesheet ('./img/paper.png')

        self.lantern_radius = 200  # Raio da lanterna
        self.lantern_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))  # Superfície para a lanterna
        self.lantern_surface.fill((0, 0, 0))

    def draw_lantern(self, player):
        # Criar um círculo transparente onde a lanterna ilumina
        self.lantern_surface.fill((0, 0, 0))  # Limpa a superfície
        pygame.draw.circle(self.lantern_surface, (0, 0, 0), (player.rect.centerx, player.rect.centery), self.lantern_radius)
        self.lantern_surface.set_colorkey((0, 0, 0))  # Define a cor preta como transparente
        
        # Desenhar a máscara de lanterna sobre a tela
        self.screen.blit(self.lantern_surface, (0, 0))

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == 'B':
                    Block (self, j, i)
                if column == 'E':
                    Enemy(self,j,i)
                if column == 'P':
                    self.player = Player (self,j,i)
                if column == 'N':
                    Note (self,j,i)

    def new(self):
        self.playing = True

        self.notes_collected = 0  # Reinicia as páginas coletadas
        self.pages_collected = 0  # Assegure-se de que o contador de páginas está resetado
        self.total_notes = 7 

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.notes = pygame.sprite.LayeredUpdates()

        self.createTilemap()

        for enemy in self.enemies:
            enemy.speed = 0  # Ajuste inicial da velocidade do inimigo

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        # Mantém a câmera centralizada no jogador
        self.camera_x = self.player.rect.centerx - WIN_WIDTH // 2
        self.camera_y = self.player.rect.centery - WIN_HEIGHT // 2
        
    def draw(self):
        self.game_surface.fill(BLACK)

        # Desenha os elementos ajustados pela câmera
        for sprite in self.all_sprites:
            self.game_surface.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))

        # Desenha o placar
        score_text = self.font.render(f"{self.notes_collected}/{self.total_notes}", True, WHITE)
        score_rect = score_text.get_rect(topright=(WIN_WIDTH - 10, 10))
        self.game_surface.blit(score_text, score_rect)

        # Escala e desenha na tela principal
        scaled_surface = pygame.transform.scale(self.game_surface, (self.screen_rect.width, self.screen_rect.height))
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        large_font = pygame.font.Font('./Slender.ttf', 64)
        
        text = large_font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 40))

        # Posição dos botões centralizados abaixo do texto de Game Over
        button_width, button_height = 150, 50
        button_x = (WIN_WIDTH - button_width) // 2
        restart_button_y = WIN_HEIGHT / 2 + 20
        exit_button_y = restart_button_y + button_height + 20

        # Criação dos botões
        restart_button = Button(button_x, restart_button_y, button_width, button_height, WHITE, BLACK, 'Restart', 32)
        exit_button = Button(button_x, exit_button_y, button_width, button_height, WHITE, BLACK, 'Exit', 32)

        # Índice para controlar qual botão está selecionado
        selected_button_index = 0
        buttons = [restart_button, exit_button]

        # Limpa os sprites para exibir a tela de Game Over
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if selected_button_index == 0:  # Restart
                            self.new()
                            self.main()
                        elif selected_button_index == 1:  # Exit
                            self.running = False
                    elif event.key == pygame.K_DOWN:
                        selected_button_index = (selected_button_index + 1) % len(buttons)
                    elif event.key == pygame.K_UP:
                        selected_button_index = (selected_button_index - 1) % len(buttons)

            # Verifica clique do mouse nos botões
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            for i, button in enumerate(buttons):
                if button.is_pressed(mouse_pos, mouse_pressed):
                    if i == 0:
                        self.new()
                        self.main()
                    elif i == 1:
                        self.running = False

            # Desenha o fundo de Game Over e os botões
            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            for button in buttons:
                self.screen.blit(button.image, button.rect)

            # Desenha uma borda ao redor do botão selecionado
            selected_button = buttons[selected_button_index]
            border_rect = selected_button.rect.inflate(10, 10)
            pygame.draw.rect(self.screen, WHITE, border_rect, 2)

            # Atualiza a tela
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        button_width, button_height = 100, 50
        button_x = (WIN_WIDTH - button_width) // 2
        play_button_y = (WIN_HEIGHT - button_height) // 2
        info_button_y = play_button_y + 60

        large_font = pygame.font.Font('./Slender.ttf', 64)

        title = large_font.render('SLENDERMAN', True, WHITE)
        title_rect = title.get_rect(center=(WIN_WIDTH // 2, play_button_y - 40))

        play_button = Button(button_x, play_button_y, button_width, button_height, WHITE, BLACK, 'Play', 32)
        info_button = Button(button_x, info_button_y, button_width, button_height, WHITE, BLACK, 'Info', 32)

        selected_button_index = 0
        buttons = [play_button, info_button]

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if selected_button_index == 0:
                            intro = False
                            pygame.mixer.music.play(-1)
                        elif selected_button_index == 1:
                            self.show_info_screen()
                    elif event.key == pygame.K_DOWN:
                        selected_button_index = (selected_button_index + 1) % len(buttons)
                    elif event.key == pygame.K_UP:
                        selected_button_index = (selected_button_index - 1) % len(buttons)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for i, button in enumerate(buttons):
                if button.is_pressed(mouse_pos, mouse_pressed):
                    if i == 0:
                        intro = False
                    elif i == 1:
                        self.show_info_screen()

            # Desenha o fundo e os elementos da tela de introdução
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)

            # Desenha os botões
            for i, button in enumerate(buttons):
                self.screen.blit(button.image, button.rect)

            # Desenha a borda ao redor do botão selecionado
            selected_button = buttons[selected_button_index]
            border_rect = selected_button.rect.inflate(10, 10)
            pygame.draw.rect(self.screen, WHITE, border_rect, 2)

            # Atualiza a tela
            self.clock.tick(FPS)
            pygame.display.update()

    def show_info_screen(self):
        info = True
        info_text_lines = [
            'O jogo se passa em um mundo', 
            ' distopico onde voce eh', 
            'perseguido por Slenderman.',
            'Seu objetivo eh coletar', 
            'todas as notas sem ser pego', 
            'para conseguir sobreviver.',
            '',
            'Controles:',
            '',
            ' W                   ^',
            'A  D            <    >',
            ' S                  v',
            'Pressione Enter para voltar'
        ]

        small_font = pygame.font.Font('./Slender.ttf', 24)

        # Renderiza cada linha do texto de informações usando a fonte menor
        rendered_lines = [small_font.render(line, True, WHITE) for line in info_text_lines]

        while info:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    info = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        info = False

            self.screen.fill(BLACK)

            
            start_y = 30
            for i, line in enumerate(rendered_lines):
                line_rect = line.get_rect(center=(WIN_WIDTH // 2, start_y + i * 30))
                self.screen.blit(line, line_rect)

            pygame.display.update()
            self.clock.tick(FPS)


    def show_victory_screen(self):
        text = self.font.render('You Won', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        continue_button = Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, BLACK, 'EXIT', 32)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False  

            

            self.screen.fill(BLACK)
            self.screen.blit(text, text_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            pygame.display.update()
            self.clock.tick(FPS)



g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit() 