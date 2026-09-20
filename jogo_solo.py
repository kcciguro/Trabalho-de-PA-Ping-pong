import pygame
import sys

# ==========================================
# CONFIGURAÇÕES DE TELA E CORES
# ==========================================
LARGURA = 800
ALTURA = 600
TAMANHO_RAQUETE = (15, 90)
RAIO_BOLA = 10

# Paleta de Cores (Estilo Neon/Arcade)
COR_FUNDO = (15, 18, 28)        # Azul escuro elegante
COR_LINHA = (40, 50, 75)        # Linha central
COR_P1 = (0, 210, 255)          # Azul Neon (Você)
COR_BOT = (255, 60, 100)        # Vermelho Neon (Bot)
COR_BOLA = (255, 220, 0)        # Amarelo Vibrante

def main():
    pygame.init()
    pygame.font.init()

    win = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ping Pong - Modo Solo vs Bot")
    relogio = pygame.time.Clock()
    fonte_placar = pygame.font.SysFont("Consolas", 60, bold=True)

    # Posições Iniciais
    y_p1 = ALTURA // 2 - TAMANHO_RAQUETE[1] // 2
    y_bot = ALTURA // 2 - TAMANHO_RAQUETE[1] // 2

    bola_x, bola_y = 400.0, 300.0
    vel_bola_x, vel_bola_y = 5.0, 5.0

    placar_p1, placar_bot = 0, 0
    velocidade_bot = 4.2  # Ajusta a inteligência/velocidade do Bot (menor que a bola para ser possível ganhar)

    rastro_bola = []
    rodando = True

    while rodando:
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
y_p1 = mouse_y - TAMANHO_RAQUETE[1] // 2  # Centraliza a raquete no ponteiro do mouse
y_p1 = max(10, min(ALTURA - TAMANHO_RAQUETE[1] - 10, y_p1))

        # --- INTELIGÊNCIA ARTIFICIAL DO BOT ---
        # O Bot tenta alinhar o centro da sua raquete com a altura da bola
        centro_bot = y_bot + TAMANHO_RAQUETE[1] // 2
        if centro_bot < bola_y - 10:
            y_bot += velocidade_bot
        elif centro_bot > bola_y + 10:
            y_bot -= velocidade_bot

        y_bot = max(10, min(ALTURA - TAMANHO_RAQUETE[1] - 10, y_bot))

        # --- MOVIMENTAÇÃO E FÍSICA DA BOLA ---
        bola_x += vel_bola_x
        bola_y += vel_bola_y

        # Colisão Topo e Fundo
        if bola_y <= 15 or bola_y >= ALTURA - 15:
            vel_bola_y *= -1

        # Colisão Raquete Jogador (Esquerda)
        if bola_x <= 42 and y_p1 <= bola_y <= y_p1 + TAMANHO_RAQUETE[1]:
            vel_bola_x = abs(vel_bola_x) * 1.05
            bola_x = 43

        # Colisão Raquete Bot (Direita)
        if bola_x >= LARGURA - 42 and y_bot <= bola_y <= y_bot + TAMANHO_RAQUETE[1]:
            vel_bola_x = -abs(vel_bola_x) * 1.05
            bola_x = LARGURA - 43

        # Ponto do Bot
        if bola_x < 0:
            placar_bot += 1
            bola_x, bola_y = 400.0, 300.0
            vel_bola_x, vel_bola_y = 5.0, 5.0

        # Ponto do Jogador
        elif bola_x > LARGURA:
            placar_p1 += 1
            bola_x, bola_y = 400.0, 300.0
            vel_bola_x, vel_bola_y = -5.0, 5.0

        # --- DESENHO NA TELA ---
        win.fill(COR_FUNDO)

        # Linha central tracejada
        for y in range(0, ALTURA, 25):
            if (y // 25) % 2 == 0:
                pygame.draw.rect(win, COR_LINHA, (LARGURA // 2 - 2, y, 4, 15))

        # Placar
        txt_p1 = fonte_placar.render(str(placar_p1), True, COR_P1)
        txt_bot = fonte_placar.render(str(placar_bot), True, COR_BOT)
        win.blit(txt_p1, (LARGURA // 4 - txt_p1.get_width() // 2, 30))
        win.blit(txt_bot, (3 * LARGURA // 4 - txt_bot.get_width() // 2, 30))

        # Rastro da bola
        rastro_bola.append((int(bola_x), int(bola_y)))
        if len(rastro_bola) > 5:
            rastro_bola.pop(0)

        for i, pos in enumerate(rastro_bola):
            raio_suave = int(RAIO_BOLA * (i + 1) / len(rastro_bola))
            pygame.draw.circle(win, (200, 200, 100), pos, max(2, raio_suave))

        # Raquetes e Bola
        pygame.draw.rect(win, COR_P1, (25, int(y_p1), TAMANHO_RAQUETE[0], TAMANHO_RAQUETE[1]), border_radius=4)
        pygame.draw.rect(win, COR_BOT, (LARGURA - 25 - TAMANHO_RAQUETE[0], int(y_bot), TAMANHO_RAQUETE[0], TAMANHO_RAQUETE[1]), border_radius=4)
        pygame.draw.circle(win, COR_BOLA, (int(bola_x), int(bola_y)), RAIO_BOLA)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
