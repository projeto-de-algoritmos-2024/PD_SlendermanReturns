import pygame
import sys
from collections import defaultdict

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slenderman - Bellman-Ford Edition")

# Cores
BLACK = (0, 0, 0)
RED = (162, 35, 35)
WHITE = (255, 255, 255)

# Fonte personalizada
font2 = pygame.font.Font("assets/fonts/Slender.ttf", 60)
font = pygame.font.Font("assets/fonts/youmurdererbb_reg.ttf", 60)
small_font = pygame.font.Font("assets/fonts/youmurdererbb_reg.ttf", 40)

# Carregar imagem de fundo
background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Sons
pygame.mixer.init()
hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
bg_music = pygame.mixer.Sound("assets/sounds/ambient_terror.wav")
bg_music.set_volume(0.5)
bg_music.play(-1)  # Loop infinito

# Implementação do algoritmo de Bellman-Ford
def bellman_ford(graph, source):
    distance = defaultdict(lambda: float('inf'))
    distance[source] = 0
    
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, w in graph[u].items():
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
    
    # Verificar ciclos negativos
    for u in graph:
        for v, w in graph[u].items():
            if distance[u] + w < distance[v]:
                return None  # Ciclo negativo detectado
    
    return distance

# Exemplo de grafo para o jogo
game_graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'D': 3, 'E': 1},
    'C': {'B': 1, 'D': 5},
    'D': {'E': 2},
    'E': {}
}

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
               self.y <= mouse_pos[1] <= self.y + self.height

    def handle_event(self):
        if self.is_hovered():
            hover_sound.play()
            return True
        return False

    # Criar botões com tamanhos e posições ajustados
buttons = [
    Button("Novo Jogo", (WIDTH - 350) // 2, HEIGHT - 150),  # Maior e centralizado na parte inferior
    Button("Continuar", (WIDTH - 300) // 2 - 150, HEIGHT - 90),  # Menor, à esquerda de "Novo Jogo"
    Button("Instrucoes", (WIDTH - 300) // 2 + 150, HEIGHT - 90),  # Menor, à direita de "Novo Jogo"
]


# Loop principal
def main_menu():
    running = True
    while running:
        screen.blit(background, (0, 0))  # Desenhar o fundo

        # Título do jogo
        draw_text_with_shadow("SLENDERMAN", font2, RED, BLACK, (WIDTH - 350) // 2, HEIGHT // 5)

        # Desenhar botões
        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.handle_event():
                        click_sound.play()
                        if button.text == "Novo Jogo":
                            start_game()
                        elif button.text == "Continuar":
                            print("Continuar jogo...")
                        elif button.text == "Instrucoes":
                            show_instructions()

        pygame.display.update()

def start_game():
    print("Iniciando novo jogo...")
    # Aqui você pode adicionar a lógica do jogo usando o algoritmo de Bellman-Ford
    shortest_paths = bellman_ford(game_graph, 'A')
    if shortest_paths:
        print("Caminhos mais curtos a partir do ponto inicial:")
        for node, distance in shortest_paths.items():
            print(f"Para {node}: {distance}")
    else:
        print("Ciclo negativo detectado no grafo do jogo!")

def show_instructions():
    print("Mostrando instruções...")
    # Adicione aqui a lógica para exibir as instruções do jogo

main_menu()
