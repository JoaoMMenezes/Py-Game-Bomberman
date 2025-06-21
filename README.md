# Bomberman - Projeto de Programação Orientada a Objetos

Este projeto é uma implementação de um jogo estilo Bomberman, desenvolvido como parte da disciplina de **Análise, Projeto e Programação Orientada a Objetos (APPOO)** da Escola de Engenharia da UFMG.

O foco do projeto foi aplicar os conceitos de orientação a objetos, como encapsulamento, herança e polimorfismo, para criar um jogo funcional e bem estruturado para dois jogadores locais.

## Créditos

O desenvolvimento deste projeto foi inspirado e baseado na implementação de [forestf90/bomberman](https://github.com/forestf90/bomberman). As principais diferenças são a remoção da Inteligência Artificial para inimigos e a adaptação para um modo de 2 jogadores, além de uma estrutura de pastas e gerenciamento de estado customizados.

## Funcionalidades

- **Multiplayer Local para 2 Jogadores**: Dispute contra um amigo no mesmo teclado.
- **Jogabilidade Clássica**: Posicione bombas para destruir caixas, abrir caminho e derrotar seu oponente.
- **Power-ups**: Colete itens para aumentar o número de bombas que você pode plantar e o alcance das explosões.
- **Sistema de Menu Completo**: Navegue entre as telas de Jogo, Instruções e Ranking.
- **Ranking Persistente**: O jogo salva o histórico de vitórias de cada jogador, atualizando um ranking que pode ser visualizado no menu.

## Estrutura do Projeto

O código foi organizado em uma estrutura de pastas para separar as responsabilidades, seguindo os princípios de OOP:

- `classes/`: Contém as classes que representam os objetos do jogo (Player, Bomb, Wall, PowerUp, etc.).
- `manager/`: Contém as classes que gerenciam o fluxo do jogo (GameManager) e o acesso aos dados (DBManager).
- `db/`: Armazena o arquivo `history.json` com o ranking de vitórias.
- `main.py`: Ponto de entrada principal que inicializa e executa o jogo.

## Requisitos

- Python 3.x
- Bibliotecas listadas no arquivo `requirements.txt`.

## Instalação

1.  Clone ou faça o download deste repositório para a sua máquina.

2.  Navegue até a pasta raiz do projeto pelo terminal.

3.  Instale as dependências necessárias executando o seguinte comando:
    ```bash
    pip install -r requirements.txt
    ```

## Como Jogar

Para iniciar o jogo, execute o arquivo `main.py` a partir da pasta raiz do projeto:

```bash
python main.py
```

Isso abrirá o menu principal, onde você poderá iniciar uma partida, ver as instruções ou checar o ranking.

## Controles

- **Jogador 1 (Azul):**

  - **Movimento**: Setas do Teclado
  - **Plantar Bomba**: Barra de Espaço

- **Jogador 2 (Vermelho):**
  - **Movimento**: Teclas `W`, `A`, `S`, `D`
  - **Plantar Bomba**: Tecla `E`
