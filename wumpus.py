import pygame
import random
import asyncio

# Inicializa o Pygame
pygame.init()

#BASE DE CONHECIMENTO
KB = []
have_gold = False
died = False
#Direção do DFS:
direction = 'right'

#Pontuação de um jogo
points = 0
#cell
cell = (0,0)

#Vetor que indica possibilidade das dimensões:
directions = [True,False,False,False]
#Pilha pra DFS e voltar ao começo
stack = [(0,0)]

# Define cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

last_position = (0,0)

visitado = 'V'

#Posição do wumpus pra atualizar ele no jogo(Personagem não sabe da wumpus_position)
wumpus_position = [0,0]

#Contador de quantas vezes o wumpus moveu:
count_wumpus_moves = 0

#número aleatório de turnos para mover o wumpus
random_number_up_to_5 = random.randint(3,5)

# Identificador não poço:
NP = 'NP'
# Identificador não poço deduzido:
NPD = 'NPD'
# identificador Não Brisa
NB ='NB'
# identificador Não Stink
NS ='NS'
# identificador Não Wumpus
NW ='NW'



# Configurações do jogo
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
CELL_SIZE = WIDTH // COLS

# pause
pause = False
# Define a janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mundo do Wumpus")

# Elementos do jogo
PLAYER = pygame.image.load("jogador.jpg")
WUMPUS = pygame.image.load("wumpus.jpg")
PIT = pygame.image.load("pit.jpg")
GOLD = pygame.image.load("gold.jpeg")
BREEZE = pygame.image.load("breeze.jpg")
STINK = pygame.image.load("stink.jpg")

# Redimensiona as imagens para caberem nas células
PLAYER = pygame.transform.scale(PLAYER, (CELL_SIZE, CELL_SIZE))
WUMPUS = pygame.transform.scale(WUMPUS, (CELL_SIZE, CELL_SIZE))
PIT = pygame.transform.scale(PIT, (CELL_SIZE, CELL_SIZE))
GOLD = pygame.transform.scale(GOLD, (CELL_SIZE, CELL_SIZE))
BREEZE = pygame.transform.scale(BREEZE, (CELL_SIZE, CELL_SIZE))
STINK = pygame.transform.scale(STINK, (CELL_SIZE, CELL_SIZE))

#Imagens de meia célula:
halfPLAYER = pygame.transform.scale(PLAYER, (CELL_SIZE/2, CELL_SIZE))
halfWUMPUS = pygame.transform.scale(WUMPUS, (CELL_SIZE/2, CELL_SIZE))
halfPIT = pygame.transform.scale(PIT, (CELL_SIZE/2, CELL_SIZE))
halfGOLD = pygame.transform.scale(GOLD, (CELL_SIZE/2, CELL_SIZE))
halfBREEZE = pygame.transform.scale(BREEZE, (CELL_SIZE/2, CELL_SIZE))
halfSTINK = pygame.transform.scale(STINK, (CELL_SIZE/2, CELL_SIZE))


# Matriz do jogo
world = [[[] for _ in range(COLS)] for _ in range(ROWS)]

#função pra retornar os vizinhos possíveis
def neighbours(x,y):
    resultados = [(x+1,y),(x,y+1) ,(x-1,y), (x,y-1)]
    resultados = filter(lambda x: validate_position(x[0],x[1]), resultados)
    return resultados


#Função pra limpar os dados do Wumpus da KB:
# def clear_wumpus_data():
#     for 'W?'+str(x)+str(y) in KB:

#     print("oi")


# Função para simular que o wumpus fez barulho ao mover:
def wumpus_make_noise():
    global KB
    print('KB antes de make noise: ',KB)
    # Limpeza inicial de 'NW' e 'NS'
    KB = [item for item in KB if  'NS' not in item]
    KB = [item for item in KB if  'NW' not in item]

    for x in range(ROWS):
        for y in range(COLS):
            pos = str(x) + str(y)

            # Atualiza 'W?' e suas vizinhanças
            if pos + 'W?' in KB:
                KB = [item for item in KB if pos + 'W?' not in item]
                neighbourhood = list(neighbours(x, y))
                for neighbour in neighbourhood:
                    position = str(neighbour[0]) + str(neighbour[1])
                    if position + 'W?D' not in KB:
                        KB.append(position + 'W?D')

            # Remove 'S' se presente
            if pos + 'S' in KB:
                KB = [item for item in KB if pos + 'S' not in item]

            # Atualiza 'W' e suas vizinhanças
            if pos + 'W' in KB:
                KB = [item for item in KB if pos + 'W' not in item]
                neighbourhood = list(neighbours(x, y))
                for neighbour in neighbourhood:
                    position = str(neighbour[0]) + str(neighbour[1])
                    if position + 'W?D' not in KB:
                        KB.append(position + 'W?D')

    # Substitui 'W?D' por 'W?'
    KB = [item.replace('W?D', 'W?') for item in KB]
    print("KB após make_noise: ",KB)
    # if any('W?' in item for item in KB):
    #     for x in range(ROWS):
    #         for y in range(COLS):
    #             pos = str(x) + str(y)
    #             if pos + 'W?' in KB:
    #                 string = pos + 'NW'
    #                 if string in KB:
    #                     KB = [item for item in KB if string != item]
                # else:
                #     string = pos + 'NW'
                #     if string not in KB:
                #         KB.append(string)
    # else:
    #     KB = [item for item in KB if  'NW' not in item]

    # print("KB atualizado:", KB)


# def wumpus_make_noise():
#     global KB  # Garante que estamos manipulando a variável global KB

#     # Cria uma nova lista para armazenar as marcações atualizadas
#     new_KB = []

#     # Primeiro, localiza todos os itens que têm 'W?' e prepara para remover
#     positions_to_expand = []
#     for item in KB:
#         if 'W?' in item:
#             # Adiciona a posição para expansão
#             pos = item.split('W?')[0]
#             x, y = int(pos[0]), int(pos[1])
#             positions_to_expand.append((x, y))

#     # Agora, expande 'W?' para os vizinhos
#     for (x, y) in positions_to_expand:
#         neighbours_list = neighbours(x, y)
#         for neighbour in neighbours_list:
#             nx, ny = neighbour
#             neighbour_pos = str(nx) + str(ny) + 'W?'
#             # Adiciona 'W?' aos vizinhos se ainda não estiverem marcados
#             if neighbour_pos not in KB and neighbour_pos not in new_KB:
#                 new_KB.append(neighbour_pos)

#         # Remove a posição original 'W?' e adiciona 'NW' em seu lugar
#         original_pos_NW = str(x) + str(y) + 'NW'
#         if original_pos_NW not in new_KB:
#             new_KB.append(original_pos_NW)

#     # Adiciona 'NW' para todas as outras posições que não foram marcadas
#     for x in range(ROWS):
#         for y in range(COLS):
#             pos = str(x) + str(y)
#             pos_NW = pos + 'NW'
#             pos_W = pos + 'W?'
            
#             # Verifica se não é uma célula marcada como 'W?' ou já convertida para 'NW'
#             if pos_NW not in new_KB and pos_W not in new_KB:
#                 new_KB.append(pos_NW)

#     # Atualiza KB com as novas marcações
#     KB = new_KB


#Limpa informações sobre o wumpus:
def clear_wumpus():
    global KB
    KB = [item for item in KB if 'W' not in item ]
    print("KB novo : ",KB)



# Função pra fazer o Wumpus mover:
def move_wumpus():
    print("MOVI O WUMPUS:")
    global wumpus_position
    print("wumpus position: ", wumpus_position)
    world[wumpus_position[0]][wumpus_position[1]].remove('W')
    Wumpus_possibilities = neighbours(wumpus_position[0],wumpus_position[1])
    Wumpus_possibilities = list(Wumpus_possibilities)

    for pos in Wumpus_possibilities:
        world[pos[0]][pos[1]].remove('S')

    wumpus_new_position = random.choice(Wumpus_possibilities) 
    print("Wumpus Possibilyties: ",Wumpus_possibilities)
    print("wumpus_new_position: ",wumpus_new_position)
    place_element(wumpus_new_position[0], wumpus_new_position[1], 'W')
    print("função pra mover o wumpus")
    wumpus_make_noise()


#Função pra encher kb
def percept(perception,possibility,x_position,y_position):
    identificadores_de_perigo = ['W','P']
    if (str(x_position)+str(y_position)+perception) not in KB:
            
            KB.append(str(x_position)+str(y_position)+perception)
            # if (str(x_position)+str(y_position)+'ok') not in KB:
            #     KB.append(str(x_position)+str(y_position)+'ok')
            if (str(x_position)+str(y_position)+ NP) not in KB:
                KB.append(str(x_position) + str(y_position) + NP)
            if (str(x_position)+str(y_position)+ NW) not in KB:
                KB.append(str(x_position) + str(y_position) + NW)
            

            for identificador in identificadores_de_perigo:
                string = str(x_position)+str(y_position)+identificador+'?'
                if (string) in KB:
                    KB.remove(string)

            if possibility == 'P?':
                if validate_positionKB((x_position+1),(y_position),possibility):
                    KB.append(str(x_position+1)+str(y_position)+possibility)

                if validate_positionKB((x_position-1),(y_position),possibility):
                    KB.append(str(x_position-1)+str(y_position)+possibility)

                if validate_positionKB((x_position),(y_position+1),possibility):
                    KB.append(str(x_position)+str(y_position+1)+possibility)

                if validate_positionKB((x_position),(y_position-1),possibility):
                    KB.append(str(x_position)+str(y_position-1)+possibility)

            elif possibility == 'W?':
                neighbourhood = list(neighbours(x_position,y_position))

                neighbourhood = [item for item in neighbourhood if str(x_position)+str(y_position)+possibility in KB]

                print("\n\nNeighbourhood: ",neighbourhood, "\n\n")

                if not neighbourhood:
                    if validate_positionKB((x_position+1),(y_position),possibility):
                        KB.append(str(x_position+1)+str(y_position)+possibility)

                    if validate_positionKB((x_position-1),(y_position),possibility):
                        KB.append(str(x_position-1)+str(y_position)+possibility)

                    if validate_positionKB((x_position),(y_position+1),possibility):
                        KB.append(str(x_position)+str(y_position+1)+possibility)

                    if validate_positionKB((x_position),(y_position-1),possibility):
                        KB.append(str(x_position)+str(y_position-1)+possibility)


#Função pra limpar KB de possibilidades já testadas
def clear_KB(pos_x,pos_y):
    global KB
    indentificadores_de_perigo = ['W','P']

    if(str(pos_x)+str(pos_y)+NP) in KB or (str(pos_x)+str(pos_y)+'P') in KB :
        string = str(pos_x)+str(pos_y)+'P'+'?'
        if(string) in KB:
                KB.remove(string)
    
    if(str(pos_x)+str(pos_y)+NW) in KB or (str(pos_x)+str(pos_y)+'W') in KB :
        string = str(pos_x)+str(pos_y)+'W'+'?'
        if(string) in KB:
                KB.remove(string)
    
    find_wumpus = False
    for item in KB:
        if 'W' in item and 'N' not in item and '?' not in item:
            print("Item: ",item,"\n\n\n\n\n\n\n")
            find_wumpus = True
    
    if find_wumpus:
        print("ACHEI O WUMPUS")

        # Filtra os itens que não queremos manter
        KB = [item for item in KB if 'NW' not in item and not ('W' in item and '?' in item)]

        print("KB após a filtragem:", KB)
          
    for i in range(ROWS):
        for j in range(COLS):
            if str(i)+str(j)+'NP' in KB:
                if str(i)+str(j)+'P?' in KB:
                    KB = [item for item in KB if item !=str(i)+str(j)+'P?']

    # if(str(pos_x)+str(pos_y)+'ok') in KB:
    #     for identificador in indentificadores_de_perigo:
    #         string = str(pos_x)+str(pos_y)+identificador+'?'
    #         if(string) in KB:
    #             KB.remove(string)
    

# Função lógica pra achar poço
def deduce_P():
    identificador = 'P'
    for i in range(ROWS):
        for j in range(COLS):
            pos = str(i)+str(j)  
            string = pos + identificador + '?'
            if string in KB:
                if verify_neighbor_B(i,j):
                    KB.remove(string)
                    string = pos + NP
                    if string not in KB:
                        KB.append(string)

# Função lógica pra achar wumpus
def deduce_S():
    identificador = 'W'
    for i in range(ROWS):
        for j in range(COLS):
            pos = str(i)+str(j)  
            string = pos + identificador + '?'
            if string in KB:
                if verify_neighbor_S(i,j):
                    KB.remove(string)
                    string = pos + NW
                    if string not in KB:
                        KB.append(string)


def verify_neighbor_B(x_position,y_position):
    if validate_position((x_position+1),(y_position)):
       if(str(x_position+1)+str(y_position)+'V') in KB and (str(x_position+1)+str(y_position)+'B') not in KB:
           return True

    if validate_position((x_position-1),(y_position)):
        if (str(x_position-1)+str(y_position)+'V') in KB and (str(x_position-1)+str(y_position)+'B') not in KB:
            return True

    if validate_position((x_position),(y_position+1)):
        if (str(x_position)+str(y_position+1)+'V') in KB and (str(x_position)+str(y_position+1)+'B') not in KB:
            return True

    if validate_position((x_position),(y_position-1)):
        if (str(x_position)+str(y_position-1)+"V") in KB and (str(x_position)+str(y_position-1)+'B') not in KB:
            return True
    return False



def verify_neighbor_S(x_position,y_position):
    if validate_position((x_position+1),(y_position)):
       if(str(x_position+1)+str(y_position)+'NS') in KB and (str(x_position+1)+str(y_position)+'S') not in KB:
           return True

    if validate_position((x_position-1),(y_position)):
        if (str(x_position-1)+str(y_position)+'NS') in KB and (str(x_position-1)+str(y_position)+'S') not in KB:
            return True

    if validate_position((x_position),(y_position+1)):
        if (str(x_position)+str(y_position+1)+'NS') in KB and (str(x_position)+str(y_position+1)+'S') not in KB:
            return True

    if validate_position((x_position),(y_position-1)):
        if (str(x_position)+str(y_position-1)+'NS') in KB and (str(x_position)+str(y_position-1)+'S') not in KB:
            return True
    return False





#Função pra verificar se vizinhos de (x,y) tem str(condicao):
def has_neighbor(x,y,condition):
    resultados = [(x+1,y),(x,y+1) ,(x-1,y), (x,y-1)]
    resultados = filter(lambda x: validate_position(x[0],x[1]), resultados)
    resultados = filter(lambda x: str(x[0])+str(x[1])+condition in KB,resultados)
    lr = list(resultados)
    # print("Reultados has_neighbor depois que tira os não poço: ",resultados)
    # print("Lista de Resultados has_neighbor depois que tira os não poço: ",lr)
    # print("Tamanho da lista: ",len(lr))
    if(len(lr) == 0):
        return False
    else:
        return True
    
#Função pra verificar só com os quadrados ao redor da briza, se tenho como deduzir onde está um poço
def super_deduction_Breeze():
    for i in range(ROWS):
        for j in range(COLS):
            pos = str(i) + str(j)
            if pos + 'B' in KB:
                neighborhood = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
                for neighbor in neighborhood:
                    if(has_neighbor(neighbor[0],neighbor[1],NB)):
                        string = str(neighbor[0]) + str(neighbor[1]) + NP
                        if string not in KB:
                            KB.append(string)
                        string = str(neighbor[0]) + str(neighbor[1]) + 'P?'
                        if string in KB:
                            KB.remove(string)


# Função pra deduzir quais quadrados ao redor da Stink podem ser wumpus:
def deduce_Stink():
    global KB
    S_neighbours = []
    for i in range(ROWS):
        for j in range(COLS):
            
            if(str(i)+str(j)+'S' in KB):

                resultados = [(i+1, j),(i, j+1) ,(i-1, j), (i, j-1)]
                resultados = filter(lambda x: validate_position(x[0],x[1]), resultados)
                # print("Resultados deduce_Breeze: ",list(resultados))
                resultados = filter(lambda x: ((str(x[0])+str(x[1])+NW) not in KB),resultados)
                lr = list(resultados)
                S_neighbours = lr
                # print("Reultados deduce_Breeze depois que tira os não poço: ",resultados)
                # print("Lista de Resultados deduce_Breeze depois que tira os não poço: ",lr)
                # print("Tamanho da lista: ",len(lr))
                if(len(lr) == 1):
                    if(str(lr[0][0])+str(lr[0][1])+'W' not in KB):
                        KB.append(str(lr[0][0])+str(lr[0][1])+'W')
                        if str(lr[0][0])+str(lr[0][1])+'W?' in KB:
                            KB.remove(str(lr[0][0])+str(lr[0][1])+'W?')

                resultadosNW = [(i+1, j),(i, j+1) ,(i-1, j), (i, j-1)]
                resultadosNW = filter(lambda x: validate_position(x[0],x[1]), resultadosNW)
                resultadosNW = filter(lambda x: has_neighbor(x[0],x[1],NS), resultadosNW)
                lrNW = list(resultadosNW)
                # print("Reultados deduce_Breeze depois que tira os não poço: ",resultadosNW)
                # print("Lista de Resultados deduce_Breeze depois que tira os não poço: ",lrNW)
                # print("Tamanho da lista: ",len(lrNW))
                if(len(lrNW) >= 1):
                    for pos in lrNW:
                        if(str(pos[0])+str(pos[1])+NW not in KB):
                          KB.append(str(pos[0])+str(pos[1])+NW)
                        if(str(pos[0])+str(pos[1])+'W?' in KB):
                          KB.remove(str(pos[0])+str(pos[1])+'W?')
    for i in range(ROWS):
        for j in range(COLS):
            if S_neighbours:
                if (i,j) not in S_neighbours:
                    stringAux = str(i) + str(j) + 'W?'
                    if stringAux in KB:
                        KB = [item for item in KB if item != stringAux]


# def stink_Clear_Possibilites():
#     global KB
#     for item in KB:
#         if 'S' in item and 'N' not in item:
#            pos = (int(item[0]),int(item[1]))
#            pos_neighborhood = list(neighbours(pos[0],pos[1]))
#            string_pos = str(pos_neighborhood[0]) + str(pos_neighborhood[1])
#            if 

# Função pra deduzir quais quadrados ao redor da Briza podem ser poços:
def deduce_Breeze():#Não usei ainda, mudar pra verificar poço

    for i in range(ROWS):
        for j in range(COLS):

            if(str(i)+str(j)+'B' in KB):

                resultados = [(i+1, j),(i, j+1) ,(i-1, j), (i, j-1)]
                resultados = filter(lambda x: validate_position(x[0],x[1]), resultados)
                # print("Resultados deduce_Breeze: ",list(resultados))
                resultados = filter(lambda x: ((str(x[0])+str(x[1])+NP) not in KB),resultados)
                lr = list(resultados)
                # print("Reultados deduce_Breeze depois que tira os não poço: ",resultados)
                # print("Lista de Resultados deduce_Breeze depois que tira os não poço: ",lr)
                # print("Tamanho da lista: ",len(lr))
                if(len(lr) == 1):
                    if(str(lr[0][0])+str(lr[0][1])+'P' not in KB):
                        KB.append(str(lr[0][0])+str(lr[0][1])+'P')
                        if str(lr[0][0])+str(lr[0][1])+'P?' in KB:
                            KB.remove(str(lr[0][0])+str(lr[0][1])+'P?')

                resultadosNP = [(i+1, j),(i, j+1) ,(i-1, j), (i, j-1)]
                resultadosNP = filter(lambda x: validate_position(x[0],x[1]), resultadosNP)
                resultadosNP = filter(lambda x: has_neighbor(x[0],x[1],NB), resultadosNP)
                lrNP = list(resultadosNP)
                # print("Reultados deduce_Breeze depois que tira os não poço: ",resultadosNP)
                # print("Lista de Resultados deduce_Breeze depois que tira os não poço: ",lrNP)
                # print("Tamanho da lista: ",len(lrNP))
                if(len(lrNP) >= 1):
                    for pos in lrNP:
                        if(str(pos[0])+str(pos[1])+NP not in KB):
                          KB.append(str(pos[0])+str(pos[1])+NP)
                        if(str(pos[0])+str(pos[1])+'P?' in KB):
                          KB.remove(str(pos[0])+str(pos[1])+'P?')



# Função para adicionar elementos e efeitos ao mundo
def place_element(row, col, element):
    world[row][col].append(element)
    global wumpus_position
    print(f'Wumpus collum:{col},row:{row}Wumpus:',wumpus_position)
    # Adiciona 'BREEZE' ao redor de 'PIT' e 'STINK' ao redor de 'WUMPUS'
    if element == 'W':
        wumpus_position = [row,col]
        print(f'Wumpus collum:{col},row:{row}Wumpus:',wumpus_position)
        if row + 1 < ROWS:
            place_element(row + 1, col, 'S')
        if row - 1 >= 0:
            place_element(row - 1, col, 'S')
        if col + 1 < COLS:
            place_element(row, col + 1, 'S')
        if col - 1 >= 0:
            place_element(row, col - 1, 'S')
    elif element == 'P':
        if row + 1 < ROWS:
            place_element(row + 1, col, 'B')
        if row - 1 >= 0:
            place_element(row - 1, col, 'B')
        if col + 1 < COLS:
            place_element(row, col + 1, 'B')
        if col - 1 >= 0:
            place_element(row, col - 1, 'B')

# Coloca o Wumpus, ouro e poços aleatoriamente

def generate_start():
    x =random.randint(0, ROWS-1)
    y = random.randint(0,COLS-1)
    while x == 0 and y == 0:
        x =random.randint(0, ROWS-1)
        y = random.randint(0,COLS-1)
    return x,y

x_w_init,y_w_init = generate_start()
place_element(x_w_init, y_w_init, 'W')##########FAZENDO TESTES
x_g,y_g = generate_start()
place_element(x_g,y_g, 'G')
for _ in range(3):
    x_p_init,y_p_init = generate_start()
    place_element(x_p_init, y_p_init,'P')

# Posição inicial do jogador
player_pos = [0, 0]

# Última posição do jogador
last_position = player_pos

# Função para desenhar a matriz
def draw_world():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(window, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            # Desenha os elementos da célula
            for element in world[row][col]:
                if len(element) == 1:
                    if 'W' in element:
                        window.blit(WUMPUS, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'G' in element:
                        window.blit(GOLD, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'P' in element:
                        window.blit(PIT, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'B' in element:
                        window.blit(BREEZE, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'S' in element:
                        window.blit(STINK, (col * CELL_SIZE, row * CELL_SIZE))

                elif len(element) == 2:

                    if 'W' in element:
                        window.blit(halfWUMPUS, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'G' in element:
                        window.blit(halfGOLD, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'P' in element:
                        window.blit(halfPIT, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'B' in element:
                        window.blit(halfBREEZE, (col * CELL_SIZE, row * CELL_SIZE))
                    elif 'S' in element:
                        window.blit(halfSTINK, (col * CELL_SIZE, row * CELL_SIZE))

                    

    # Desenha o jogador
    window.blit(PLAYER, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE))

# Função para mover o jogador
def move_player(dx, dy):
    global last_position
    global player_pos
    last_position = player_pos
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if validate_position(new_x,new_y):
        player_pos[0], player_pos[1] = new_x, new_y

def validate_position(x,y):
    if 0 <= x < ROWS and 0 <= y < COLS:
            return True
    else:
        return False

def validate_positionKB(x,y,z):
    if 0 <= x < ROWS and 0 <= y < COLS:
        if(str(x)+str(y)+str(z)) not in KB:
            return True
            # if(str(x)+str(y)+'ok' not in KB):
            #     return True
            # else:
            #     return False   
        else:
            return False
    else:
        return False

for row in range(ROWS):
        for col in range(COLS):
            for element in world[row][col]:
                print("Elemento [",row,",",col,"]: ",element)

for row in range(ROWS):
        for col in range(COLS):
            for element in world[row][col]:
                
                print(len(element))
# Loop principal do jogo
running = True
count_player_moves = 0


#Pausar o jogo
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False  # Sai do loop quando 'P' é pressionado

        # Exemplo de texto indicando que o jogo está pausado
        # world.fill((0, 0, 0))
        # font = pygame.font.Font(None, 74)
        # text = font.render("Jogo Pausado. Aperte 'P' para continuar.", True, (255, 255, 255))
        # world.blit(text, (50, 250))
        # pygame.display.flip()



# def neighbours(x,y):
#     resultados = [(x+1,y),(x,y+1) ,(x-1,y), (x,y-1)]
#     resultados = filter(lambda x: validate_position(x[0],x[1]), resultados)
#     return resultados

# def move_player_validated(x,y):
#     global last_position
#     neighbourhood = list(neighbours(x,y))

#     for neighbour in neighbourhood:
#         pos = str(neighbour[0])+str(neighbour[1])

#         if pos + 'P' in KB or pos + 'P?' in KB or  pos + 'W' in KB or pos + 'W?' in KB:
#             continue
#         else:





















































def wumpus_close():
    global player_pos
    global stack
    neighbourhood = list(neighbours(player_pos))
    for neighbour in neighbourhood:
        if 'W' in neighbour or 'W?' in neighbour:
            return True
        
    return False
    # neighbourhood = [neighbour for neighbour in neighbourhood if 'W' not in neighbour and 'W?' not in neighbour and 'P' not in neighbour and 'P?' not in neighbour]
    # player_pos = neighbourhood[0]




def valid_go(new_pos_x,new_pos_y):
    # global player_pos
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    w_stringDoubt = str(new_pos_x)+str(new_pos_y)+'W?'
    p_string = str(new_pos_x)+str(new_pos_y)+'P'
    p_stringDoubt = str(new_pos_x)+str(new_pos_y)+'P?'
    is_visitado = str(new_pos_x)+str(new_pos_y)+'V'

    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and w_stringDoubt not in KB and p_string not in KB and p_stringDoubt not in KB and is_visitado not in KB :
        # player_pos = (new_pos_x,new_pos_y)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False


def valid_go_right(x,y):
    new_pos_x = x
    new_pos_y = y+1
    return valid_go(new_pos_x,new_pos_y)
    
def valid_go_down(x,y):
    new_pos_x = x+1
    new_pos_y = y
    return valid_go(new_pos_x,new_pos_y)

def valid_go_left(x,y):
    new_pos_x = x
    new_pos_y = y-1
    return valid_go(new_pos_x,new_pos_y)


def valid_go_up(x,y):
    new_pos_x = x-1
    new_pos_y = y
    return valid_go(new_pos_x,new_pos_y)

def valid_go_back(x,y):

    if valid_go_up(x,y) or valid_go_right(x,y) or valid_go_down(x,y) or valid_go_left(x,y):
        return False
    else:
        return True


def go(new_pos_x,new_pos_y):
    global player_pos
    global KB
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    w_stringDoubt = str(new_pos_x)+str(new_pos_y)+'W?'
    p_string = str(new_pos_x)+str(new_pos_y)+'P'
    p_stringDoubt = str(new_pos_x)+str(new_pos_y)+'P?'
    is_visitado = str(new_pos_x)+str(new_pos_y)+'V'
    
    print("KB usado para MOVER: ",KB)
    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and w_stringDoubt not in KB and p_string not in KB and p_stringDoubt not in KB and is_visitado not in KB :
        player_pos = (new_pos_x,new_pos_y)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False

def go_right(x,y):
    new_pos_x = x
    new_pos_y = y+1
    return go(new_pos_x,new_pos_y)
    
def go_down(x,y):
    new_pos_x = x+1
    new_pos_y = y
    return go(new_pos_x,new_pos_y)

def go_left(x,y):
    new_pos_x = x
    new_pos_y = y-1
    return go(new_pos_x,new_pos_y)

def go_up(x,y):
    new_pos_x = x-1
    new_pos_y = y
    return go(new_pos_x,new_pos_y)



def go_V(new_pos_x,new_pos_y):
    global player_pos
    global KB
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    w_stringDoubt = str(new_pos_x)+str(new_pos_y)+'W?'
    p_string = str(new_pos_x)+str(new_pos_y)+'P'
    p_stringDoubt = str(new_pos_x)+str(new_pos_y)+'P?'
    print("player pos no go_V_antes de mudar: ",player_pos)
    print("x,y:",new_pos_x," ",new_pos_y)
    print("KB usado para MOVER: ",KB)
    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and w_stringDoubt not in KB and p_string not in KB and p_stringDoubt not in KB :
        player_pos = (new_pos_x,new_pos_y)
        print("player pos no go_V: ",player_pos)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False

def go_right_V(x,y):
    new_pos_x = x
    new_pos_y = y+1
    return go_V(new_pos_x,new_pos_y)
    
def go_down_V(x,y):
    new_pos_x = x+1
    new_pos_y = y
    return go_V(new_pos_x,new_pos_y)

def go_left_V(x,y):
    new_pos_x = x
    new_pos_y = y-1
    return go_V(new_pos_x,new_pos_y)


def go_up_V(x,y):
    new_pos_x = x-1
    new_pos_y = y
    return go_V(new_pos_x,new_pos_y)


def go_VW(new_pos_x,new_pos_y):
    global player_pos
    global KB
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    p_string = str(new_pos_x)+str(new_pos_y)+'P'
    p_stringDoubt = str(new_pos_x)+str(new_pos_y)+'P?'
    print("player pos no go_VW_antes de mudar: ",player_pos)
    print("x,y:",new_pos_x," ",new_pos_y)
    print("KB usado para MOVER: ",KB)
    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and p_string not in KB and p_stringDoubt not in KB :
        player_pos = (new_pos_x,new_pos_y)
        print("player pos no go_VW: ",player_pos)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False

def go_right_VW(x,y):
    new_pos_x = x
    new_pos_y = y+1
    return go_VW(new_pos_x,new_pos_y)
    
def go_down_VW(x,y):
    new_pos_x = x+1
    new_pos_y = y
    return go_VW(new_pos_x,new_pos_y)

def go_left_VW(x,y):
    new_pos_x = x
    new_pos_y = y-1
    return go_VW(new_pos_x,new_pos_y)


def go_up_VW(x,y):
    new_pos_x = x-1
    new_pos_y = y
    return go_VW(new_pos_x,new_pos_y)





def go_VWP(new_pos_x,new_pos_y):
    global player_pos
    global KB
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    p_string = str(new_pos_x)+str(new_pos_y)+'P'
    # p_stringDoubt = str(new_pos_x)+str(new_pos_y)+'P?'
    print("player pos no go_VW_antes de mudar: ",player_pos)
    print("x,y:",new_pos_x," ",new_pos_y)
    print("KB usado para MOVER: ",KB)
    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and p_string not in KB :
        player_pos = (new_pos_x,new_pos_y)
        print("player pos no go_VW: ",player_pos)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False

def go_right_VWP(x,y):
    new_pos_x = x
    new_pos_y = y+1
    return go_VWP(new_pos_x,new_pos_y)
    
def go_down_VWP(x,y):
    new_pos_x = x+1
    new_pos_y = y
    return go_VWP(new_pos_x,new_pos_y)

def go_left_VWP(x,y):
    new_pos_x = x
    new_pos_y = y-1
    return go_VWP(new_pos_x,new_pos_y)


def go_up_VWP(x,y):
    new_pos_x = x-1
    new_pos_y = y
    return go_VWP(new_pos_x,new_pos_y)




    
# go_random:

def go_randon():
    global player_pos
    escolha = random.randint(0,3)
    player_pos_aux = (-1,-1)
    
    while not validate_position(player_pos_aux):
        match escolha:
            case 0:
                player_pos_aux = (player_pos[0]+1,player_pos[1])
            case 1:
                player_pos_aux = (player_pos[0],player_pos[1]+1)
            case 2:
                player_pos_aux = (player_pos[0]-1,player_pos[1])
            case 3:
                player_pos_aux = (player_pos[0],player_pos[1]-1)
    player_pos = player_pos_aux

def go_to(x,y):
    global player_pos
    global KB
    new_pos_x = x
    new_pos_y = y
    w_string = str(new_pos_x)+str(new_pos_y)+'W'
    w_stringDoubt = str(new_pos_x)+str(new_pos_y)+'W?'
    print("KB usado para MOVER: ",KB)
    if validate_position(new_pos_x,new_pos_y) and w_string not in KB and w_stringDoubt not in KB:
        player_pos = (new_pos_x,new_pos_y)
        # directions[0] = True
        return True
    else:
        # directions[0] = False
        return False

def dfs():
    global direction
    global stack
    global player_pos
    global directions
    x = player_pos[0]
    y = player_pos[1]
    

    match direction:
        case 'right':
            
            if(go_right(x,y)):
                
                print("\n\nFui pra direita",'new_player_pos: ',player_pos)
            else:
                direction = 'down'
        case 'down':
            if(go_down(x,y)):
                print("\n\nFui pra baixo",'new_player_pos: ',player_pos)
            else:
                if valid_go_right(player_pos[0],player_pos[1]):
                    direction = 'right'
                else:
                    direction = 'left'
        case 'left':
            if(go_left(x,y)):
                print("\n\nFui pra esquerda",'new_player_pos: ',player_pos)
            else:
                if valid_go_right(player_pos[0],player_pos[1]):
                    direction = 'right'
                elif valid_go_down(player_pos[0],player_pos[1]):
                    direction = 'down'
                else:
                    direction = 'up'
        case 'up':
            if(go_up(x,y)):
                print("\n\nFui pra cima",'new_player_pos: ',player_pos)
            else:
                direction = 'right'
       

def update_KB():
    global world
    global player_pos
    global cell
    global running
    global KB
    global have_gold
    global points
    global died

    cell = world[player_pos[0]][player_pos[1]]
    # print("cell: ",cell)
    # print("last_pos: ",last_position)
    # print("Player_position_pre_KB: ",player_pos)
    # print("KB: ",KB)
    # logic()
    
    if 'W' in cell:
        print("Você foi devorado pelo Wumpus!")
        died = True
        running = False
    elif 'P' in cell:
        print("Você caiu em um poço!")
        died =True
        running = False
    elif 'G' in cell:
        print("Você encontrou o ouro!")
        have_gold = True
        # running = False
    elif 'B' in cell or 'S' in cell:
        # string = (str(player_pos[0]) + str(player_pos[1]) + NW)
        # if string not in KB:
        #     KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + NW)
        if string not in KB:
            KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + NP)
        if string not in KB:
            KB.append(string)
        
        string = (str(player_pos[0]) + str(player_pos[1]) + visitado)
        if string not in KB:
            KB.append(string)

        if 'B' in cell:
            perception = 'B'
            possibility = 'P?'
            percept(perception,possibility,player_pos[0],player_pos[1])
        else:
            string = str(player_pos[0])+str(player_pos[1])+NB
            if string not in KB:
              KB.append(string)
        if 'S' in cell:
            perception = 'S'
            possibility = 'W?'
            percept(perception,possibility,player_pos[0],player_pos[1])
        else:
            string = (str(player_pos[0]) + str(player_pos[1]) + NS)
            if string not in KB:
                KB.append(string)
        
    else:
        # string = (str(player_pos[0]) + str(player_pos[1]) + 'ok')
        # if string not in KB:
        #     KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + NP)
        if string not in KB:
            KB.append(string)
        string = str(player_pos[0])+str(player_pos[1])+NB
        if string not in KB:
            KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + NW)
        if string not in KB:
            KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + NS)
        if string not in KB:
            KB.append(string)
        string = (str(player_pos[0]) + str(player_pos[1]) + visitado)
        if string not in KB:
            KB.append(string)




def valid_return_stack():
    global stack
    global player_pos
    global running
    # if valid_go_back()

def return_Stack():
    global stack
    global player_pos
    global running
    global direction

    direction = 'right'
        # print('player_pos do go back: ',player_pos)
    run_away = False
    if stack:
        stack.pop()
        if stack:
            player_pos_aux = stack.pop()
            pos = str(player_pos_aux[0])+str(player_pos_aux[1])
            dangers = ['W','W?']
            for danger in dangers:
                string = pos + danger
                if string in KB:
                    stack.append((player_pos_aux[0],player_pos_aux[1]))
                    if (player_pos[0],player_pos[1]) not in stack:
                        stack.append((player_pos[0],player_pos[1])) 
                    run_away = True
                    break
            if(run_away):
                print("\n\n\n\n\nCONDIÇÂO DE FUGA")
                if(go_right_V(player_pos[0],player_pos[1])):
                    print("Fugi pra direita")
                    print("player position: ",player_pos)

                elif(go_down_V(player_pos[0],player_pos[1])):
                    print("Fugi pra baixo")
                    print("player position: ",player_pos)

                elif(go_left_V(player_pos[0],player_pos[1])):
                    print("Fugi pra esquerda")
                    print("player position: ",player_pos)

                elif(go_up_V(player_pos[0],player_pos[1])):
                    print("Fugi pra cima")
                    print("player position: ",player_pos)
                else:
                    print("\n\n\n\n\nCONDIÇÂO DE FUGA Aleatória W?")
                    if(go_right_VW(player_pos[0],player_pos[1])):
                        print("Fugi pra direita")
                        print("player position: ",player_pos)

                    elif(go_down_VW(player_pos[0],player_pos[1])):
                        print("Fugi pra baixo")
                        print("player position: ",player_pos)

                    elif(go_left_VW(player_pos[0],player_pos[1])):
                        print("Fugi pra esquerda")
                        print("player position: ",player_pos)

                    elif(go_up_VW(player_pos[0],player_pos[1])):
                        print("Fugi pra cima")
                        print("player position: ",player_pos)
                        # print("ERRO")
                    else:
                        print("\n\n\n\n\nCONDIÇÂO DE FUGA Aleatória W?")
                        if(go_right_VWP(player_pos[0],player_pos[1])):
                            print("Fugi pra direita")
                            print("player position: ",player_pos)

                        elif(go_down_VWP(player_pos[0],player_pos[1])):
                            print("Fugi pra baixo")
                            print("player position: ",player_pos)

                        elif(go_left_VWP(player_pos[0],player_pos[1])):
                            print("Fugi pra esquerda")
                            print("player position: ",player_pos)

                        elif(go_up_VWP(player_pos[0],player_pos[1])):
                            print("Fugi pra cima")
                            print("player position: ",player_pos)
                            # print("ERRO")
                        else:
                            go_randon()
                            # print("FALTA IMPLEMENTAR O SEM P?")
            else:
                player_pos = player_pos_aux


        else:
            # print("Player_Position: ",player_pos)
            running = False
    else:
        # print("Player_Position: ",player_pos)
        running = False
    
            


def move_player_algorithyn():
    global player_pos
    global stack
    global running
    global direction
    global last_position
    global KB
    global have_gold

    last_position = player_pos
    # player_pos_aux = (0,0)

    if (player_pos[0],player_pos[1]) not in stack:
        stack.append((player_pos[0],player_pos[1]))  # Pilha empilha a posição atual

    if valid_go_back(player_pos[0],player_pos[1]) or have_gold: 
        return_Stack()
    else:
        dfs()
    
        
    

def logic():
    global player_pos
    clear_KB(player_pos[0],player_pos[1])
    deduce_Breeze()
    deduce_Stink()
    deduce_P()
    deduce_S()

while running:
    pygame.time.delay(500)
    
    # logic()
    # print("Wumpus_position:",wumpus_position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_UP:
            #     move_player(-1, 0)
            #     count_player_moves += 1
            # elif event.key == pygame.K_DOWN:
            #     move_player(1, 0)
            #     count_player_moves += 1
            # elif event.key == pygame.K_LEFT:
            #     move_player(0, -1)
            #     count_player_moves += 1
            # elif event.key == pygame.K_RIGHT:
            #     move_player(0, 1)
            #     count_player_moves += 1
            if event.key == pygame.K_p:  # Tecla "P" para pausar/despausar
                pause = not pause  # Alterna o estado de pausa
    



    # print("Player_position_pre_Kcelula: ",player_pos)
    # Verifica a célula atual
    update_KB()
        

    if pause:
        pause_game()
        pause = False
        # text = font.render('PAUSADO', True, (255, 255, 255))
        # world.blit(text, (350, 250))  # Posiciona o texto na tela
    # Desenha o jogo


    logic()
    print("KB antes do player mover: ",KB)
################# MOVER PLAYER #########################################################################################################################
    if count_player_moves <= random_number_up_to_5:
        logic()
        move_player_algorithyn()
        if(last_position != player_pos):
            count_player_moves += 1
            points -= 1
        update_KB()
        logic()
        print("KB logo após player_mover: ",KB)

        # print("PlayerPos: ",player_pos)
        # print("Direction: ",direction)
        
        
        
################# MOVER PLAYER #########################################################################################################################
    else:
################## MOVER WUMPUS ##################################################################################################################################
        random_number_up_to_5 = random.randint(3,5)
        # pygame.time.delay(1000)
        move_wumpus()
        # wumpus_make_noise()
        count_wumpus_moves+=1
        # pygame.time.delay(1000)
        #Apaga os dados do wumpus por ele fazer barulho ao mover:
        if(count_wumpus_moves > 3):
            clear_wumpus()
            count_wumpus_moves = 0
        update_KB()
        logic()
        print("KB depois do Wumpus mover: ",KB)
        count_player_moves = 0
################## MOVER WUMPUS ##################################################################################################################
    
    print("Stack: ",stack)
    print("player: ",player_pos)
    window.fill(BLACK)
    draw_world()
    pygame.display.update()

pygame.quit()

count_quadrados_visitados = 0 
quadrados_visitados = []

for item in KB:
    if 'V' in item:
        quadrados_visitados.append(item.split('V'))
        count_quadrados_visitados +=1
if(have_gold and not died):
    points += 100
if died:
    points -= 100
print("Quantidade de Quadrados visitados:",count_quadrados_visitados)
print("Quadrados visitados:",quadrados_visitados)
print("Pontuação do jogo: ",points)
