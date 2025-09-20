# 🤖 Robô Resgate em Labirinto

Simulação de um robô que percorre um labirinto, localiza uma pessoa (`@`), resgata-a e a leva até a entrada (`E`), exibindo o processo passo a passo no terminal.

---

## 📦 Estrutura do Labirinto

O labirinto é definido como uma matriz de caracteres (`raw_map`) com os seguintes símbolos:

| Símbolo | Significado                |
|---------|-----------------------------|
| `X`     | Parede (obstáculo)         |
| `.`     | Caminho livre              |
| `E`     | Entrada (início e entrega) |
| `@`     | Pessoa a ser resgatada     |

---

## 🤖 Comportamento do Robô

- Inicia na posição `E` com direção inicial válida (buscada dinamicamente).
- Explora o labirinto usando **busca em profundidade (DFS)**.
- Antes de avançar, gira para se alinhar na direção correta.
- Ao chegar ao lado da pessoa (`@`):
  - Considera que ela foi resgatada.
  - Muda de cor para **vermelho**.
  - Remove o `@` do mapa.
- Retorna pelo mesmo caminho até a **entrada (`E`)**.
- Libera a pessoa e volta à cor **verde**.

---

## 🎨 Visualização no Terminal

A cada movimento, o labirinto é exibido com cores ANSI:

| Cor       | Significado       |
|-----------|-------------------|
| 🟢 Verde   | Robô sem pessoa   |
| 🔴 Vermelho| Robô com pessoa   |
| 🔵 Azul    | Caminho de ida    |
| 🟡 Amarelo | Caminho de volta  |

---

## ⚙️ Configurações

- `SLEEP_TIME = 0.5` → controla a velocidade da animação (em segundos).  
- O labirinto pode ser modificado editando a matriz `raw_map`.  
- As ações e leituras dos sensores são salvas no arquivo **`log_robo.csv`**.  

---

## 🖥️ Como Executar no VS Code

### 1. Instalar o Python
- Baixe em [python.org](https://www.python.org/downloads/)  
- Verifique no terminal:
  ```bash
  python --version


## 🖥️ Como Executar no VS Code

### 2. Instalar o VS Code
- Baixe em [code.visualstudio.com](https://code.visualstudio.com)

### 3. Criar o Projeto
- Abra o VS Code
- Crie uma pasta chamada `labirinto`
- Dentro dela, crie um arquivo chamado `resgate.py`
- Cole o código completo no arquivo

### 4. Executar o Código
- Clique com o botão direito no arquivo e selecione **"Run Python File in Terminal"**
- Ou abra o terminal integrado (`Ctrl + \``) e digite:

```bash
python resgate.py
