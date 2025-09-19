import time
import os

raw_map = [
    "XEXXXXXXXXX",
    "X.....X...X",
    "X.XXX.X.X.X",
    "X.X.X.X.X.X",
    "X.X.X.XXX.X",
    "X.X......@X",
    "XXXXXXXXXXX"
]

# Tempo entre movimentos (em segundos) - um pouco mais rápido para as viradas
SLEEP_TIME = 1.0

grid = [list(row) for row in raw_map]
rows, cols = len(grid), len(grid[0])

# Localiza inicio e objetivo
start = goal = None
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "E":
            start = (r, c)
        elif grid[r][c] == "@":
            goal = (r, c)

if not start or not goal:
    raise ValueError("Mapa precisa ter 'E' e '@'.")

# --- Estruturas de Dados para Direção ---
robot_chars = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
directions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
vector_to_direction = {v: k for k, v in directions.items()}

# --- NOVO: Dicionário para definir a rotação de 90 graus no sentido horário ---
clockwise_turns = {
    "UP": "RIGHT",
    "RIGHT": "DOWN",
    "DOWN": "LEFT",
    "LEFT": "UP"
}

# Estado inicial do robô
robot = {"pos": start, "direction": "DOWN"}

# Utilitários e Cores (sem alterações)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

BLUE, YELLOW, GREEN, RED, RESET = "\033[94m", "\033[93m", "\033[92m", "\033[91m", "\033[0m"

def print_grid_with_robot(grid, robot_state, path_azul=set(), path_amarelo=set()):
    gcopy = [row[:] for row in grid]
    r, c = robot_state["pos"]
    robot_char = robot_chars[robot_state["direction"]]
    clear_console()
    print(f"Movimentos: {movimentos}")
    for i, row in enumerate(gcopy):
        line = ""
        for j, ch in enumerate(row):
            if (i, j) == (r, c): line += GREEN + robot_char + RESET
            elif (i, j) == goal: line += RED + "@" + RESET
            elif (i, j) in path_amarelo and ch == ".": line += YELLOW + "." + RESET
            elif (i, j) in path_azul and ch == ".": line += BLUE + "." + RESET
            else: line += ch
        print(line)
    print()
    time.sleep(SLEEP_TIME)

# --- NOVA FUNÇÃO DE ROTAÇÃO ---
def turn_robot(target_direction):
    """Gira o robô 90 graus por vez até atingir a direção alvo."""
    global movimentos
    # Continua virando enquanto a direção atual não for a desejada
    while robot["direction"] != target_direction:
        # Pega a próxima direção na sequência horária
        robot["direction"] = clockwise_turns[robot["direction"]]
        movimentos += 1
        # Mostra a virada na tela
        print_grid_with_robot(grid, robot, ida_path, volta_path)

# --- Lógica de Exploração (DFS) Atualizada ---
movimentos = 0
visited = set()
found_goal = False
path_taken = []
goal_path = []
ida_path = set()
volta_path = set()

def explore(pos):
    global movimentos, found_goal, goal_path
    if found_goal: return

    visited.add(pos)
    path_taken.append(pos)
    ida_path.add(pos)
    
    print_grid_with_robot(grid, robot, ida_path, volta_path)

    if pos == goal:
        print("Objetivo encontrado!")
        found_goal = True
        goal_path = path_taken.copy()
        time.sleep(SLEEP_TIME * 3)
        return

    for target_direction, (dr, dc) in directions.items():
        nr, nc = pos[0] + dr, pos[1] + dc
        
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] in (".", "@"):
            # 1. VIRAR (usando a nova função)
            turn_robot(target_direction)
            
            # 2. MOVER PARA FRENTE
            movimentos += 1
            robot["pos"] = (nr, nc)
            
            explore((nr, nc))
            
            if found_goal: return
            
            # 3. VOLTAR (Backtracking)
            back_direction = vector_to_direction[(-dr, -dc)]
            turn_robot(back_direction) # Vira para a direção de volta

            movimentos += 1 # Conta o movimento de recuo
            robot["pos"] = pos
            print_grid_with_robot(grid, robot, ida_path, volta_path)

    path_taken.pop()

# Inicia a exploração
explore(start)

# Caminho de volta
if found_goal:
    print("\nRetornando ao início...\n")
    for i in range(len(goal_path) - 2, -1, -1):
        current_pos = robot["pos"]
        target_pos = goal_path[i]
        volta_path.add(current_pos)
        
        dr, dc = target_pos[0] - current_pos[0], target_pos[1] - current_pos[1]
        target_direction = vector_to_direction[(dr, dc)]

        # 1. VIRAR (usando a nova função)
        turn_robot(target_direction)
            
        # 2. MOVER
        movimentos += 1
        robot["pos"] = target_pos
        print_grid_with_robot(grid, robot, ida_path, volta_path)
    
    volta_path.add(start)
    print_grid_with_robot(grid, robot, ida_path, volta_path)

print(f"\nExploração concluída. Movimentos totais realizados: {movimentos}")