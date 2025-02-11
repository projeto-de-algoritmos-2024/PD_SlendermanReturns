import pygame
import sys
from collections import defaultdict
import main

# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Slenderman - Returns")

# Cores
BLACK = (0, 0, 0)
RED = (162, 35, 35)
WHITE = (255, 255, 255)

# Fonte personalizada
font2 = pygame.font.Font("./img/assets/fonts/Slender.ttf", 60)
font = pygame.font.Font("./img/assets/fonts/youmurdererbb_reg.ttf", 60)
small_font = pygame.font.Font("./img/assets/fonts/youmurdererbb_reg.ttf", 40)

# Carregar imagem de fundo
background = pygame.image.load("./img/assets/images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Sons
pygame.mixer.init()
hover_sound = pygame.mixer.Sound("./img/assets/sounds/hover.wav")
click_sound = pygame.mixer.Sound("./img/assets/sounds/click.wav")
bg_music = pygame.mixer.Sound("./img/assets/sounds/ambient_terror.wav")
bg_music.set_volume(0.5)
bg_music.play(-1)  # Loop infinito

# Função para desenhar texto com sombra
def draw_text_with_shadow(text, font2, text_color, shadow_color, x, y):
    shadow_surface = font2.render(text, True, shadow_color)
    screen.blit(shadow_surface, (x + 2, y + 2))
    text_surface = font2.render(text, True, text_color)
    screen.blit(text_surface, (x, y))

# Ajustar a classe Button para permitir tamanhos diferentes
class Button:
    def __init__(self, text, x, y, width=300, height=70):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        # Desenhar o botão com texto
        draw_text_with_shadow(self.text, font if self.is_hovered() else small_font,
                              RED if self.is_hovered() else WHITE, BLACK,
                              self.x + (self.width // 6), self.y + (self.height // 8))

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x <= mouse_pos[0] <= self.x + self.width and \
               self.y <= mouse_pos[1] <= self.x + self.width and \
               self.y <= mouse_pos[1] <= self.y + self.height

    def handle_event(self):
        if self.is_hovered():
            hover_sound.play()
            return True
        return False

    # Criar botões com tamanhos e posições ajustados
import pygame
import sys
from collections import defaultdict
import main

# ... (código anterior permanece o mesmo)

# Atualizar a lista de botões
buttons = [
    Button("Novo Jogo", (WIDTH - 350) // 2, HEIGHT - 200),
    Button("Instrucoes", (WIDTH - 350) // 2, HEIGHT - 120)
]

def show_instructions():
    instruction_screen = True
    while instruction_screen:
        screen.fill(BLACK)
        
        draw_text_with_shadow("Instruções", font2, WHITE, BLACK, (WIDTH - font2.size("Instruções")[0]) // 2, HEIGHT // 6)
        
        instructions = [
            "O jogo se passa em um mundo distópico onde você é",
            "perseguido por Slenderman.",
            "Seu objetivo é coletar todas as notas sem ser pego",
            "para conseguir sobreviver.",
            "",
            "Controles:",
            "W/Seta para cima: Mover para cima",
            "S/Seta para baixo: Mover para baixo",
            "A/Seta para esquerda: Mover para esquerda",
            "D/Seta para direita: Mover para direita",
            "ESC: Sair do jogo",
            "",
            "Pressione ESC para voltar ao menu principal"
        ]
        
        for i, line in enumerate(instructions):
            draw_text_with_shadow(line, small_font, WHITE, BLACK, WIDTH // 10, HEIGHT // 4 + i * 40)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                instruction_screen = False
        
        pygame.display.update()

def start_game():
    game_instance = main.Game()
    game_instance.intro_screen()
    game_instance.new()
    while game_instance.running:
        game_instance.main()
        game_instance.game_over()

def main_menu():
    running = True
    while running:
        screen.blit(background, (0, 0))  # Desenhar o fundo

        # Título do jogo
        draw_text_with_shadow("SLENDERMAN", font2, RED, BLACK, (WIDTH - font2.size("SLENDERMAN")[0]) // 2, HEIGHT // 6)

        # Desenhar botões
        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.handle_event():
                        click_sound.play()
                        if button.text == "Novo Jogo":
                            pygame.quit()  # Encerra o Pygame atual
                            start_game()
                            return
                        elif button.text == "Instrucoes":
                            show_instructions()

        pygame.display.update()

    pygame.quit()
    sys.exit()

main_menu()

