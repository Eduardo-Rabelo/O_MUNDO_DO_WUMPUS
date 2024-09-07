import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mundo do Wumpus")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Fonte para desenhar as letras
fonte = pygame.font.Font(None, 74)

# Letras que representam os elementos
elementos = {
    "player": "P",
    "wumpus": "W",
    "pit": "O",
    "gold": "G"
}

# Matriz do jogo (4x4)
jogo_matriz = [
    ["P", " ", " ", "G"],
    [" ", "W", " ", " "],
    [" ", " ", "O", " "],
    [" ", " ", " ", " "]
]

# Função para desenhar a matriz na tela
def desenhar_matriz():
    tela.fill(branco)
    for i in range(4):
        for j in range(4):
            texto = fonte.render(jogo_matriz[i][j], True, preto)
            tela.blit(texto, (j * 150 + 50, i * 150 + 50))
    pygame.display.flip()

# Loop principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
    
    desenhar_matriz()

pygame.quit()
