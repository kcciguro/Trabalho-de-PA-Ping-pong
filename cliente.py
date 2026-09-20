import socket
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
COR_FUNDO = (15, 18, 28)        # Azul escuro muito elegante
COR_LINHA = (40, 50, 75)        # Azul acinzentado para divisórias
COR_TEXTO = (240, 240, 245)      # Branco suave
COR_P1 = (0, 210, 255)          # Azul Neon (Jogador 1)
COR_P2 = (255, 60, 100)         # Vermelho Neon (Jogador 2)
COR_BOLA = (255, 220, 0)        # Amarelo Vibrante

class Cliente:
    """Gerencia a conexão socket com o servidor."""
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.id_jogador = self.conectar()

    def conectar(self):
        try:
            self.client.connect((self.host, self.port))
            return int(self.client.recv(2048).decode())
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
            return None

    def enviar(self, dados):
        try:
            self.client.send(str.encode(dados))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"[ERRO] Falha de comunicação: {e}")
            return None

def desenhar_campo(win, fonte, placar1, placar2):
    """Desenha o fundo, a rede central e o placar estilizado."""
    win.fill(COR_FUNDO)

    # Desenha a linha central tracejada
    for y in range(0, ALTURA, 25):
        if (y // 25) % 2 == 0:
            pygame.draw.rect(win, COR_LINHA, (LARGURA // 2 - 2, y, 4, 15))

    # Desenha o Placar
    txt_p1 = fonte.render(str(placar1), True, COR_P1)
    txt_p2 = fonte.render(str(placar2), True, COR_P2)
    win.blit(txt_p1, (LARGURA // 4 - txt_p1.get_width() // 2, 30))
    win.blit(txt_p2, (3 * LARGURA // 4 - txt_p2.get_width() // 2, 30))

def main():
    pygame.init()
    pygame.font.init()
    
    win = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ping Pong Online - Edição Especial")
    relogio = pygame.time.Clock()
    
    # Fontes do sistema
    fonte_placar = pygame.font.SysFont("Consolas", 60, bold=True)
    fonte_status = pygame.font.SysFont("Arial", 24)

    cliente = Cliente()

    # Tela de espera caso o servidor não esteja rodando
    if cliente.id_jogador is None:
        win.fill(COR_FUNDO)
        txt = fonte_status.render("Servidor não encontrado! Inicie o servidor.py primeiro.", True, (255, 100, 100))
        win.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    rodando = True
    pos_y = ALTURA // 2 - TAMANHO_RAQUETE[1] // 2
    rastro_bola = []

    while rodando:
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Controles do jogador (Setas ou W/S)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            pos_y -= 7
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            pos_y += 7

        # Limita o movimento da raquete dentro da janela
        pos_y = max(10, min(ALTURA - TAMANHO_RAQUETE[1] - 10, pos_y))

        # Envia a posição do jogador atual e recebe o estado atualizado do servidor
        resposta = cliente.enviar(str(pos_y))
        
        if resposta:
            try:
                # Formato recebido: "y_p1,y_p2,bola_x,bola_y,placar_p1,placar_p2"
                dados = [float(x) for x in resposta.split(",")]
                y_p1, y_p2, bola_x, bola_y, placar1, placar2 = dados
                placar1, placar2 = int(placar1), int(placar2)

                # Atualiza rastro da bola
                rastro_bola.append((int(bola_x), int(bola_y)))
                if len(rastro_bola) > 5:
                    rastro_bola.pop(0)

                # Desenha elementos
                desenhar_campo(win, fonte_placar, placar1, placar2)

                # Desenha o rastro da bola
                for i, pos in enumerate(rastro_bola):
                    alfa = int(255 * (i + 1) / len(rastro_bola))
                    raio_suave = int(RAIO_BOLA * (i + 1) / len(rastro_bola))
                    pygame.draw.circle(win, (200, 200, 100), pos, max(2, raio_suave))

                # Desenha as Raquetes
                # Raquete P1 (Esquerda)
                pygame.draw.rect(win, COR_P1, (25, int(y_p1), TAMANHO_RAQUETE[0], TAMANHO_RAQUETE[1]), border_radius=4)
                # Raquete P2 (Direita)
                pygame.draw.rect(win, COR_P2, (LARGURA - 25 - TAMANHO_RAQUETE[0], int(y_p2), TAMANHO_RAQUETE[0], TAMANHO_RAQUETE[1]), border_radius=4)

                # Desenha a Bola
                pygame.draw.circle(win, COR_BOLA, (int(bola_x), int(bola_y)), RAIO_BOLA)

                pygame.display.flip()
            except ValueError:
                pass

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
