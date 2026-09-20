import socket
import time
from _thread import *

# ==========================================
# CONFIGURAÇÕES DO SERVIDOR
# ==========================================
HOST = ''          # Aceita conexões de qualquer IP na rede local
PORTA = 5555       # Porta padrão para comunicação dos sockets

# Inicializa o socket do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    servidor.bind((HOST, PORTA))
except socket.error as e:
    print(f"[ERRO CRÍTICO] Não foi possível vincular a porta {PORTA}: {e}")

servidor.listen(2)

print("=" * 50)
print("   SERVIDOR PING PONG ONLINE - PRONTO")
print(f"   Aguardando jogadores na porta {PORTA}...")
print("=" * 50)

# Estado global do jogo:
# [y_p1, y_p2, bola_x, bola_y, vel_x, vel_y, placar_p1, placar_p2]
estado_jogo = [255.0, 255.0, 400.0, 300.0, 5.0, 5.0, 0, 0]

# Configurações de Física
VELOCIDADE_INICIAL = 5.0
VELOCIDADE_MAXIMA = 12.0
FATOR_ACELERACAO = 1.05  # Aumenta 5% da velocidade a cada rebate

def resetar_bola(vencedor_ponto):
    """Reseta a bola no centro e ajusta a direção para o jogador que levou o ponto."""
    global estado_jogo
    estado_jogo[2] = 400.0  # X central
    estado_jogo[3] = 300.0  # Y central
    
    # Se o Jogador 1 fez ponto, lança a bola para o Jogador 2, e vice-versa
    direcao_x = 1.0 if vencedor_ponto == 1 else -1.0
    
    estado_jogo[4] = VELOCIDADE_INICIAL * direcao_x
    estado_jogo[5] = VELOCIDADE_INICIAL if estado_jogo[5] > 0 else -VELOCIDADE_INICIAL

def atualizar_bola():
    """Calcula a movimentação da bola, colisões e pontuação."""
    global estado_jogo
    
    # Atualiza posição x e y da bola
    estado_jogo[2] += estado_jogo[4]
    estado_jogo[3] += estado_jogo[5]

    # Colisão com o Topo e Fundo do campo (Altura = 600px)
    if estado_jogo[3] <= 15 or estado_jogo[3] >= 585:
        estado_jogo[5] *= -1

    # Colisão com Raquete 1 (Esquerda - X: 25 a 40px)
    if estado_jogo[2] <= 42 and estado_jogo[0] <= estado_jogo[3] <= estado_jogo[0] + 90:
        # Garante rebate para a direita com aceleração gradual
        nova_vel = min(abs(estado_jogo[4]) * FATOR_ACELERACAO, VELOCIDADE_MAXIMA)
        estado_jogo[4] = nova_vel
        estado_jogo[2] = 43  # Previne travamento dentro do retângulo da raquete

    # Colisão com Raquete 2 (Direita - X: 745 a 760px)
    if estado_jogo[2] >= 758 and estado_jogo[1] <= estado_jogo[3] <= estado_jogo[1] + 90:
        # Garante rebate para a esquerda com aceleração gradual
        nova_vel = min(abs(estado_jogo[4]) * FATOR_ACELERACAO, VELOCIDADE_MAXIMA)
        estado_jogo[4] = -nova_vel
        estado_jogo[2] = 757  # Previne travamento dentro do retângulo da raquete

    # Ponto do Jogador 2 (Bola passou pelo lado esquerdo)
    if estado_jogo[2] < 0:
        estado_jogo[7] += 1
        print(f"[PLACAR] Ponto do Jogador 2! ({estado_jogo[6]} x {estado_jogo[7]})")
        resetar_bola(vencedor_ponto=2)

    # Ponto do Jogador 1 (Bola passou pelo lado direito)
    elif estado_jogo[2] > 800:
        estado_jogo[6] += 1
        print(f"[PLACAR] Ponto do Jogador 1! ({estado_jogo[6]} x {estado_jogo[7]})")
        resetar_bola(vencedor_ponto=1)

def thread_cliente(conexao, id_jogador):
    """Gerencia a comunicação em tempo real com cada jogador conectado."""
    global estado_jogo
    
    # Envia o ID numérico do jogador no momento da conexão (0 ou 1)
    conexao.send(str.encode(str(id_jogador)))

    while True:
        try:
            dados = conexao.recv(2048).decode()
            if not dados:
                print(f"[DESCONEXÃO] Jogador {id_jogador + 1} saiu do jogo.")
                break

            # Recebe a posição Y da raquete enviada pelo cliente
            pos_y = float(dados)
            estado_jogo[id_jogador] = pos_y

            # Somente o Jogador 1 calcula a física da bola para evitar duplicação de processamento
            if id_jogador == 0:
                atualizar_bola()

            # Formata resposta com todo o estado da partida
            # Formato enviado: "y_p1,y_p2,bola_x,bola_y,placar_p1,placar_p2"
            resposta = f"{estado_jogo[0]},{estado_jogo[1]},{estado_jogo[2]},{estado_jogo[3]},{estado_jogo[6]},{estado_jogo[7]}"
            conexao.sendall(str.encode(resposta))

        except Exception as e:
            print(f"[ERRO] Falha na conexão com Jogador {id_jogador + 1}: {e}")
            break

    conexao.close()

# Loop principal do servidor para aceitar os 2 jogadores
jogador_atual = 0
while True:
    conn, ender = servidor.accept()
    print(f"[CONECTADO] Jogador {jogador_atual + 1} entrou a partir de {ender}")

    # Abre uma thread para processar o jogador sem travar os demais
    start_new_thread(thread_cliente, (conn, jogador_atual))
    jogador_atual += 1
