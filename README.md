# 🤖 Robô Resgate em Labirinto

Simulação de um robô que percorre um labirinto, localiza uma pessoa (`@`), resgata-a e a leva até a entrada (`E`), exibindo o processo passo a passo no terminal.

---

## 📦 Estrutura do Labirinto

O labirinto é definido como uma matriz de caracteres (`raw_map`) com os seguintes símbolos:

| Símbolo | Significado               |
|---------|---------------------------|
| `X`     | Parede (obstáculo)        |
| `.`     | Caminho livre             |
| `E`     | Entrada (início e entrega)|
| `@`     | Pessoa a ser resgatada    |

---

## 🤖 Comportamento do Robô

- Inicia na posição `E` com direção para baixo.
- Explora o labirinto usando busca em profundidade (DFS).
- Gira para se alinhar antes de cada movimento.
- Ao chegar ao lado da pessoa (`@`), considera que ela foi resgatada.
- Muda de cor para vermelho e remove o `@` do mapa.
- Retorna pelo mesmo caminho até ficar ao lado da entrada.
- Libera a pessoa e volta à cor verde.

---

## 🎨 Visualização no Terminal

O labirinto é exibido a cada movimento com cores ANSI:

| Cor      | Significado              |
|----------|--------------------------|
| 🟢 Verde   | Robô sem pessoa          |
| 🔴 Vermelho| Robô com pessoa          |
| 🔵 Azul    | Caminho de ida           |
| 🟡 Amarelo | Caminho de volta         |

---

## ⚙️ Configurações

- `SLEEP_TIME = 0.4`: controla a velocidade da animação (em segundos).
- O labirinto pode ser alterado modificando os valores dentro de `raw_map`.

---

## 🖥️ Como Executar no VS Code

### 1. Instalar o Python
- Baixe em [python.org](https://www.python.org/downloads/)
- Verifique no terminal:
  ```bash
  python --version
