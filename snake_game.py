import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definição de cores
cor_fundo = (0, 0, 0)        # Preto
cor_cobra = (0, 255, 0)      # Verde
cor_comida = (255, 0, 0)     # Vermelho
cor_olhos = (255, 255, 255)  # Branco

# Configurações da janela e da cobra
largura, altura = 600, 400
tamanho_cobra = 20
velocidade = 15

# Configurações dos olhos da cobra
tamanho_olhos = 4
distancia_olhos = 6

# Inicialização da janela do jogo
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha')

# Função para desenhar a cobra
def desenhar_cobra(lista_cobra):
    for segmento in lista_cobra:
        pygame.draw.rect(janela, cor_cobra, (segmento[0], segmento[1], tamanho_cobra, tamanho_cobra))

# Função para desenhar os olhos da cobra
def desenhar_olhos(cabeca_cobra, direcao):
    olho_esquerdo = (cabeca_cobra[0] + tamanho_cobra // 3 - tamanho_olhos, cabeca_cobra[1] + tamanho_cobra // 3)
    olho_direito = (cabeca_cobra[0] + 2 * tamanho_cobra // 3 - tamanho_olhos, cabeca_cobra[1] + tamanho_cobra // 3)

    if direcao == 'direita':
        olho_esquerdo = (cabeca_cobra[0] + tamanho_cobra // 3 - tamanho_olhos + distancia_olhos, cabeca_cobra[1] + tamanho_cobra // 3)
        olho_direito = (cabeca_cobra[0] + 2 * tamanho_cobra // 3 - tamanho_olhos + distancia_olhos, cabeca_cobra[1] + tamanho_cobra // 3)
    elif direcao == 'esquerda':
        olho_esquerdo = (cabeca_cobra[0] + tamanho_cobra // 3 - tamanho_olhos - distancia_olhos, cabeca_cobra[1] + tamanho_cobra // 3)
        olho_direito = (cabeca_cobra[0] + 2 * tamanho_cobra // 3 - tamanho_olhos - distancia_olhos, cabeca_cobra[1] + tamanho_cobra // 3)
    elif direcao == 'cima':
        olho_esquerdo = (cabeca_cobra[0] + tamanho_cobra // 3, cabeca_cobra[1] + tamanho_cobra // 3 - distancia_olhos)
        olho_direito = (cabeca_cobra[0] + 2 * tamanho_cobra // 3, cabeca_cobra[1] + tamanho_cobra // 3 - distancia_olhos)
    elif direcao == 'baixo':
        olho_esquerdo = (cabeca_cobra[0] + tamanho_cobra // 3, cabeca_cobra[1] + tamanho_cobra // 3 + distancia_olhos)
        olho_direito = (cabeca_cobra[0] + 2 * tamanho_cobra // 3, cabeca_cobra[1] + tamanho_cobra // 3 + distancia_olhos)

    pygame.draw.circle(janela, cor_olhos, olho_esquerdo, tamanho_olhos)
    pygame.draw.circle(janela, cor_olhos, olho_direito, tamanho_olhos)

# Função para gerar comida para a cobra
def gerar_comida(lista_cobra):
    while True:
        x_comida = random.randint(0, largura - tamanho_cobra)
        y_comida = random.randint(0, altura - tamanho_cobra)
        comida = (x_comida // tamanho_cobra * tamanho_cobra, y_comida // tamanho_cobra * tamanho_cobra)
        if comida not in lista_cobra:
            return comida

# Função principal do jogo
def jogo():
    # Inicialização das variáveis do jogo
    jogo_ativo = True
    pontuacao = 0

    # Posição inicial da cobra e direção
    x_cobra, y_cobra = largura // 2, altura // 2
    delta_x, delta_y = tamanho_cobra, 0

    # Lista que armazena as partes do corpo da cobra
    lista_cobra = [(x_cobra, y_cobra)]
    comprimento_inicial = 1

    # Posição inicial da comida
    x_comida, y_comida = gerar_comida(lista_cobra)

    # Loop principal do jogo
    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and delta_x == 0:
                    delta_x = -tamanho_cobra
                    delta_y = 0
                elif evento.key == pygame.K_RIGHT and delta_x == 0:
                    delta_x = tamanho_cobra
                    delta_y = 0
                elif evento.key == pygame.K_UP and delta_y == 0:
                    delta_x = 0
                    delta_y = -tamanho_cobra
                elif evento.key == pygame.K_DOWN and delta_y == 0:
                    delta_x = 0
                    delta_y = tamanho_cobra

        # Atualização da posição da cobra
        x_cobra += delta_x
        y_cobra += delta_y

        # Verificação de colisão com a comida
        if x_cobra == x_comida and y_cobra == y_comida:
            pontuacao += 10
            comprimento_inicial += 1
            x_comida, y_comida = gerar_comida(lista_cobra)

        # Teletransporte da cobra para o lado oposto ao sair da tela
        if x_cobra >= largura:
            x_cobra = 0
        elif x_cobra < 0:
            x_cobra = largura - tamanho_cobra
        elif y_cobra >= altura:
            y_cobra = 0
        elif y_cobra < 0:
            y_cobra = altura - tamanho_cobra

        # Adicionar cabeça da cobra à lista de partes do corpo
        lista_cobra.append((x_cobra, y_cobra))

        # Remover partes do corpo conforme a cobra se move
        if len(lista_cobra) > comprimento_inicial:
            del lista_cobra[0]

        # Preencher a janela com a cor de fundo
        janela.fill(cor_fundo)

        # Desenhar comida e cobra na tela
        pygame.draw.rect(janela, cor_comida, (x_comida, y_comida, tamanho_cobra, tamanho_cobra))
        desenhar_cobra(lista_cobra)

        # Desenhar olhos na cabeça da cobra
        if delta_x > 0:
            desenhar_olhos(lista_cobra[-1], 'direita')
        elif delta_x < 0:
            desenhar_olhos(lista_cobra[-1], 'esquerda')
        elif delta_y > 0:
            desenhar_olhos(lista_cobra[-1], 'baixo')
        elif delta_y < 0:
            desenhar_olhos(lista_cobra[-1], 'cima')

        # Atualizar pontuação na tela
        texto = pygame.font.SysFont(None, 24).render(f'Pontuação: {pontuacao}', True, cor_cobra)
        janela.blit(texto, (10, 10))

        # Atualizar a tela
        pygame.display.update()

        # Controlar a velocidade do jogo
        pygame.time.Clock().tick(velocidade)

    pygame.quit()
    quit()

# Iniciar o jogo
jogo()
