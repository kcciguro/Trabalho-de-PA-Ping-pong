import pygame
import sys
import random

# =========================================================
# CONFIGURAÇÕES E ESTILO 3D (POV)
# =========================================================
LARGURA = 800
ALTURA = 600

COR_FUNDO = (10, 12, 24)
COR_MESA = (20, 35, 75)
COR_MESA_BORDA = (0, 255, 255)
COR_REDE = (180, 200, 255)
COR_P1 = (0, 210, 255)       # Cyan (Você)
COR_BOT = (255, 60, 100)     # Vermelho (Bot)
COR_BOLA = (255, 220, 0)     # Amarelo
COR_SOMBRA = (10, 20, 45)    # Sombra da bola
COR_CABO = (120, 70, 30)     # Cabo da raquete

def main():
    pygame.init()
    pygame.font.init()

    win = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ping Pong 3D - Regras Reais de Mesa")
    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.SysFont("Consolas", 40, bold=True)
    fonte_menu = pygame.font.SysFont("Consolas", 22, bold=True)
    fonte_placar = pygame.font.SysFont("Consolas", 45, bold=True)
    fonte_hud = pygame.font.SysFont("Consolas", 16, bold=True)

    DIFICULDADES = {
        "FACIL": {"nome": "Fácil", "vel": 4.0},
        "MEDIO": {"nome": "Médio", "vel": 6.0},
        "DIFICIL": {"nome": "Impossível", "vel": 8.5}
    }

    dificuldade_atual = None

    # --- TELA DE SELEÇÃO DE DIFICULDADE ---
    no_menu = True
    while no_menu:
        win.fill(COR_FUNDO)

        p_fundo_esq = (200, 210)
        p_fundo_dir = (600, 210)
        p_frente_dir = (750, 540)
        p_frente_esq = (50, 540)
        pygame.draw.polygon(win, COR_MESA, [p_fundo_esq, p_fundo_dir, p_frente_dir, p_frente_esq])
        pygame.draw.polygon(win, COR_MESA_BORDA, [p_fundo_esq, p_fundo_dir, p_frente_dir, p_frente_esq], 3)

        txt_tit = fonte_titulo.render("PING PONG 3D - POV", True, COR_MESA_BORDA)
        win.blit(txt_tit, (LARGURA // 2 - txt_tit.get_width() // 2, 80))

        txt_1 = fonte_menu.render("[1] - Fácil", True, (0, 255, 150))
        txt_2 = fonte_menu.render("[2] - Médio", True, (255, 200, 0))
        txt_3 = fonte_menu.render("[3] - Impossível (3D IA)", True, COR_BOT)

        win.blit(txt_1, (LARGURA // 2 - 140, 240))
        win.blit(txt_2, (LARGURA // 2 - 140, 290))
        win.blit(txt_3, (LARGURA // 2 - 140, 340))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_1, pygame.K_KP1):
                    dificuldade_atual = DIFICULDADES["FACIL"]
                    no_menu = False
                elif evento.key in (pygame.K_2, pygame.K_KP2):
                    dificuldade_atual = DIFICULDADES["MEDIO"]
                    no_menu = False
                elif evento.key in (pygame.K_3, pygame.K_KP3):
                    dificuldade_atual = DIFICULDADES["DIFICIL"]
                    no_menu = False

    def reset_bola(quem_saca):
        # Reset da bola
        # quem_saca: 'p1' ou 'bot'
        x = LARGURA // 2
        z = 0.5
        alt = 40.0
        v_alt = 2.0
        v_z = 0.014 if quem_saca == 'p1' else -0.014
        v_x = random.choice([-2.5, 2.5])
        return x, z, alt, v_alt, v_x, v_z

    bola_x, bola_z, bola_altura, vel_altura, vel_x, vel_z = reset_bola('p1')

    p1_x = LARGURA // 2
    p1_y = 480
    bot_x = LARGURA // 2

    placar_p1 = 0
    placar_bot = 0

    rodando = True
    while rodando:
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # CONTROLE DO JOGADOR (Limitado à borda da mesa frontal)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        p1_x = max(50, min(750, mouse_x))
        p1_y = max(420, min(520, mouse_y))

        # --- MOVIMENTO DA BOLA ---
        bola_z += vel_z
        bola_x += vel_x

        # Gravidade/Pingo
        bola_altura += vel_altura
        vel_altura -= 0.25

        # Mapeamento do chão da mesa no ecrã conforme Z
        chao_y = 540 - (bola_z * 330)

        # Calculo das bordas exatas da mesa na profundidade Z atual
        limite_esq = 50 + (bola_z * 150)
        limite_dir = 750 - (bola_z * 150)

        # EFEITO DE PINGO NA MESA / VERIFICAÇÃO SE CAIU FORA
        if bola_altura <= 0:
            # Se a bola bate no nível da mesa
            if limite_esq <= bola_x <= limite_dir and 0.0 <= bola_z <= 1.0:
                # Pingou dentro da mesa!
                bola_altura = 0
                vel_altura = 5.5
            else:
                # Bateu FORA da mesa -> Ponto de quem não jogou a bola para fora
                if vel_z > 0:
                    # Tu atiraste a bola para fora -> Ponto do Bot
                    placar_bot += 1
                    bola_x, bola_z, bola_altura, vel_altura, vel_x, vel_z = reset_bola('bot')
                else:
                    # Bot atirou a bola para fora -> Teu Ponto
                    placar_p1 += 1
                    bola_x, bola_z, bola_altura, vel_altura, vel_x, vel_z = reset_bola('p1')
                continue

        # CONTROLE DA IA DO BOT (Limitado estritamente à largura do fundo da mesa: 200 a 600)
        if vel_z > 0 and bola_z <= 0.92:
            alvo_x = max(200, min(600, bola_x))
            if bot_x < alvo_x - 5:
                bot_x += dificuldade_atual["vel"]
            elif bot_x > alvo_x + 5:
                bot_x -= dificuldade_atual["vel"]
        bot_x = max(200, min(600, bot_x))

        # --- REBATIDA DA RAQUETE DO JOGADOR (Frente) ---
        if -0.05 <= bola_z <= 0.08 and vel_z < 0:
            pos_bola_y = chao_y - bola_altura
            if abs(bola_x - p1_x) < 65 and abs(pos_bola_y - p1_y) < 55:
                vel_z = abs(vel_z)
                vel_x = (bola_x - p1_x) * 0.10
                vel_altura = 5.5

        # --- REBATIDA DA RAQUETE DO BOT (Fundo) ---
        if 0.90 <= bola_z <= 1.0 and vel_z > 0:
            if abs(bola_x - bot_x) < 50:
                vel_z = -abs(vel_z)
                vel_x = (bola_x - bot_x) * 0.08
                vel_altura = 5.0

        # --- PONTUAÇÃO QUANDO A BOLA PASSA DIRETO PELAS RAQUETES ---
        # Passou do Jogador sem tocar na raquete -> Ponto Bot
        if bola_z < -0.10:
            placar_bot += 1
            bola_x, bola_z, bola_altura, vel_altura, vel_x, vel_z = reset_bola('bot')

        # Passou do Bot sem tocar na raquete -> Ponto Jogador
        if bola_z > 1.10:
            placar_p1 += 1
            bola_x, bola_z, bola_altura, vel_altura, vel_x, vel_z = reset_bola('p1')

        # --- DESENHO NA TELA ---
        win.fill(COR_FUNDO)

        # 1. Mesa em Perspectiva
        p_fundo_esq = (200, 210)
        p_fundo_dir = (600, 210)
        p_frente_dir = (750, 540)
        p_frente_esq = (50, 540)

        pygame.draw.polygon(win, COR_MESA, [p_fundo_esq, p_fundo_dir, p_frente_dir, p_frente_esq])
        pygame.draw.polygon(win, COR_MESA_BORDA, [p_fundo_esq, p_fundo_dir, p_frente_dir, p_frente_esq], 3)
        pygame.draw.line(win, (40, 60, 110), (400, 210), (400, 540), 2)

        # 2. Rede
        pygame.draw.line(win, COR_REDE, (125, 375), (675, 375), 3)
        pygame.draw.line(win, COR_REDE, (125, 355), (675, 355), 2)
        for rx in range(125, 680, 20):
            pygame.draw.line(win, (100, 120, 180), (rx, 355), (rx, 375), 1)

        # 3. Raquete do Bot (Fundo - Presa na Mesa)
        tam_bot_w, tam_bot_h = 45, 30
        pygame.draw.rect(win, COR_BOT, (bot_x - tam_bot_w // 2, 210 - tam_bot_h, tam_bot_w, tam_bot_h), border_radius=4)

        # 4. Sombra da Bola
        raio_sombra = max(3, int((18 * (1.1 - bola_z * 0.7)) * 0.8))
        pygame.draw.ellipse(win, COR_SOMBRA, (int(bola_x - raio_sombra), int(chao_y - raio_sombra // 2), raio_sombra * 2, raio_sombra))

        # 5. Bola 3D
        raio_bola = max(5, int(22 * (1.1 - bola_z * 0.7)))
        pos_real_y = int(chao_y - bola_altura)
        pygame.draw.circle(win, COR_BOLA, (int(bola_x), pos_real_y), raio_bola)

        # 6. Raquete POV do Jogador
        cabo_rect = pygame.Rect(p1_x - 8, p1_y + 35, 16, 45)
        pygame.draw.rect(win, COR_CABO, cabo_rect, border_radius=3)
        pygame.draw.ellipse(win, COR_P1, (p1_x - 50, p1_y - 25, 100, 65))
        pygame.draw.ellipse(win, (255, 255, 255), (p1_x - 50, p1_y - 25, 100, 65), 3)

        # HUD / Placar
        txt_p1 = fonte_placar.render(str(placar_p1), True, COR_P1)
        txt_bot = fonte_placar.render(str(placar_bot), True, COR_BOT)
        win.blit(txt_p1, (100, 30))
        win.blit(txt_bot, (LARGURA - 130, 30))

        txt_dif = fonte_hud.render(f"Modo: {dificuldade_atual['nome']}", True, COR_MESA_BORDA)
        win.blit(txt_dif, (LARGURA // 2 - txt_dif.get_width() // 2, 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
