# Trabalho-de-PA-Ping-pong

#  Ping Pong 3D

##  Integrantes da Equipa
* **João Carlos** - [Link do Perfil do GitHub]
* **Guilherme** - [Link do Perfil do GitHub]

##  Tema Escolhido
Jogo de Ping Pong em perspectiva de primeira pessoa (3D POV) desenvolvido em Python utilizando a biblioteca **Pygame**.

##  Objetivo do Sistema
Demonstrar a aplicação prática de conceitos de programação em Python, tais como:
* Estruturas de controle e laços de repetição em tempo real (*game loop*);
* Manipulação de eventos de entrada (mouse e teclado);
* Simulação de perspectiva 3D e física básica (gravidade, parábola de salto e rebatedura);
* Implementação de uma Inteligência Artificial simples (Bot) para o modo solo.

##  Descrição do Funcionamento
O jogo coloca o jogador em uma visão frontal (POV) de uma mesa de tênis de mesa:
1. **Seleção de Dificuldade:** O utilizador escolhe entre três níveis (Fácil, Médio, Impossível).
2. **Controlo da Raquete:** A raquete do jogador acompanha o movimento livre do rato (eixos X e Y na zona frontal da mesa).
3. **Física da Bola e Pingo:** A bola possui profundidade ($Z$) e altura ($Y$), simulando o salto real na mesa antes de ser rebatida.
4. **Regras e Pontuação:** Se a bola sair pelas laterais ou ultrapassar a linha da raquete sem colisão, o ponto é contabilizado automaticamente para o adversário e a jogada recomeça.
5. 
##  Atenção
Codigo para funcionar no Pycharm
1. python -m pip install --upgrade pip
2. pip install pygame-ce
3. Seja Feliz!
