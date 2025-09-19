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

# Tempo entre movimentos (em segundos)
SLEEP_TIME = 0.4

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
clockwise_turns = {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}
counter_clockwise_turns = {"UP": "LEFT", "LEFT": "DOWN", "DOWN": "RIGHT", "RIGHT": "UP"}

# Estado inicial do robô
robot = {"pos": start, "direction": "DOWN"}

# --- Utilitários e Cores ---
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

BLUE, YELLOW, GREEN, RED, RESET = "\033[94m", "\033[93m", "\033[92m", "\033[91m", "\033[0m"

def print_grid_with_robot(grid, robot_state, has_person, path_azul=set(), path_amarelo=set()):
    gcopy = [row[:] for row in grid]
    r, c = robot_state["pos"]
    robot_char = robot_chars[robot_state["direction"]]
    robot_color = RED if has_person else GREEN

    clear_console()
    print(f"Movimentos: {movimentos}")
    for i, row in enumerate(gcopy):
        line = ""
        for j, ch in enumerate(row):
            if (i, j) == (r, c): 
                line += robot_color + robot_char + RESET
            ### MUDANÇA: Só desenha o @ se a pessoa NÃO foi resgatada ###
            elif not has_person and (i, j) == goal: 
                line += RED + "@" + RESET
            elif (i, j) in path_amarelo and ch == ".": 
                line += YELLOW + "." + RESET
            elif (i, j) in path_azul and ch == ".": 
                line += BLUE + "." + RESET
            else: 
                line += ch
        print(line)
    print()
    time.sleep(SLEEP_TIME)

def turn_robot(target_direction):
    global movimentos
    current_direction = robot["direction"]
    if current_direction == target_direction: return
    if counter_clockwise_turns[current_direction] == target_direction:
        movimentos += 1
        robot["direction"] = target_direction
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
    else:
        movimentos += 1
        robot["direction"] = clockwise_turns[current_direction]
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
        if robot["direction"] != target_direction:
            movimentos += 1
            robot["direction"] = clockwise_turns[robot["direction"]]
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)

# --- Variáveis de Estado da Missão ---
movimentos = 0
visited = set()
found_goal = False
has_person = False
path_taken = []
goal_path = []
ida_path = set()
volta_path = set()

def explore(pos):
    global movimentos, found_goal, goal_path, has_person
    if found_goal: return

    visited.add(pos)
    path_taken.append(pos)
    ida_path.add(pos)
    
    if movimentos == 0:
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)

    for target_direction, (dr, dc) in directions.items():
        nr, nc = pos[0] + dr, pos[1] + dc
        
        if (nr, nc) == goal:
            print("Objetivo localizado! Resgatando...")
            turn_robot(target_direction)
            found_goal = True
            has_person = True
            goal_path = path_taken.copy()

            ### MUDANÇA: Remove o '@' do mapa, substituindo por um caminho '.' ###
            goal_r, goal_c = goal
            grid[goal_r][goal_c] = '.'
            
            # Uma última exibição para mostrar o @ sumindo e o robô vermelho
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
            time.sleep(SLEEP_TIME * 2)
            return

        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == ".":
            turn_robot(target_direction)
            movimentos += 1
            robot["pos"] = (nr, nc)
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
            explore((nr, nc))
            if found_goal: return
            back_direction = vector_to_direction[(-dr, -dc)]
            turn_robot(back_direction)
            movimentos += 1
            robot["pos"] = pos
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)

    path_taken.pop()

# Inicia a exploração
explore(start)

# Caminho de volta
if found_goal:
    print("\nRetornando à base com a pessoa...\n")
    
    for i in range(len(goal_path) - 2, 0, -1):
        target_pos = goal_path[i]
        volta_path.add(robot["pos"])
        dr, dc = target_pos[0] - robot["pos"][0], target_pos[1] - robot["pos"][1]
        target_direction = vector_to_direction[(dr, dc)]
        turn_robot(target_direction)
        movimentos += 1
        robot["pos"] = target_pos
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
    
    volta_path.add(robot["pos"])
    print("Chegando ao ponto de entrega...")
    final_direction = vector_to_direction[(start[0] - robot["pos"][0], start[1] - robot["pos"][1])]
    turn_robot(final_direction)
    time.sleep(SLEEP_TIME * 2)
    print("\nPessoa entregue! Missão concluída.")

print(f"\nMovimentos totais realizados: {movimentos}")