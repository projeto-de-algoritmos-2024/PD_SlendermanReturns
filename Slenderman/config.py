WIN_WIDTH = 620
WIN_HEIGHT = 465
TILESIZE = 31
FPS = 120

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 2.4
ENEMY_SPEED = 0.4

RED = (255, 0, 0)
BLACK = (0 , 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

tilemap = [ 
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB.E.....BBBBBBBBBBBBBBBBBBB.BB..............BB...NBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB.............BB.N..BB.....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBB.............BB..BB....................BB........BBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBN.BB............BB..BB....BBBBBBBBBB......BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....BBBBBBBBBB......BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB....BB..........BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB......BB........BB..BB.........P..........BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB........BB......BB..BB....................BB........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBB.........B.............BB...BB....BB................BBBBBBBBBBBBBB',
    'BBBBBBBBBBBNBB...BB.................BB....BB....BB.................BBBBBBBBBBBBB',
    'BBBBBBBBBBB.......BB............BBBBB......BB....BB..B..............NBBBBBBBBBBB',
    'BBBBBBBBBBBB.......BB.......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB........BB......BBB..................BB.....B........BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB.......BB.....BBB..................BB.....B........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB.......BB.....BB..................BB.....B........BBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB..........BB..BB..............BB.......BB....B............BBBBBBBBBBB',
    'BBBBBBBBBBB........B...BBB..........B....BB.........BB.....B........BBBBBBBBBBBB',
    'BBBBBBBBBBBB.....B..B..B..B..B..B.......BB...........BB...........BBBBBBBBBBBBBB',
    'BBBBBBBBBBBB..........................BB...........BB...........BBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB...B..B..B..B..B..B.......BB...........BB...........BBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB..........................BB...........BB...........BBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB..B....B...B..B....B...B...BB...B.......BB..B..B..B...BBBBBBBBBBBBBBB',
    'BBBBBBBBBBBB...B....B...B..B..B..B...BB...........BB...........BBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB..B..B..B..B....B..B...B...BB............B....B..B..B...BBBBBBBBBBBBB',
    'BBBBBBBBBBBB..B....B...B..B.B....B..BB...........BB...........BBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBB..B...B..B....B....B..B..BBB.........B...BB....B..B..B..BBBBBBBBBBBBB',
    'BBBBBBBBBBBB..B.......B..B.B....B....BB...........BB...........BBBBBBBBNBBBBBBBB',
    'BBBBBBBBBBBN.....B...B....B....B..BBN...........B.........B...B.......BBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

# Definição dos pesos para cada tipo de tile (você pode ajustar conforme desejado)
TILE_WEIGHTS = {
    '.': 1,   # chão normal
    'E': 1,   # célula onde um inimigo pode estar (apesar de ser gerada dinamicamente, o valor pode ser 1)
    'N': 3,   # notas podem ter um custo um pouco maior (fazendo o Slenderman “evitar” esses caminhos, se for desejado)
    'P': 1,
    'B': 999   # célula do jogador (destino final do pathfinding)
    # outros tipos de tile podem ser adicionados aqui se necessário
}