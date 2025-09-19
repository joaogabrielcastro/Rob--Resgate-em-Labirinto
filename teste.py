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

# tempo entre movimentos (em segundos)
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

# utilitários
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# ANSI cores
BLUE = "\033[94m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def print_grid_with_robot(grid, robot_pos, path_azul=set(), path_amarelo=set()):
    gcopy = [row[:] for row in grid]
    r, c = robot_pos
    gcopy[r][c] = "R"
    for i, row in enumerate(gcopy):
        line = ""
        for j, ch in enumerate(row):
            if (i, j) == robot_pos:  # robô em verde
                line += GREEN + "R" + RESET
            elif (i, j) == goal:  # objetivo em vermelho
                line += RED + "@" + RESET
            elif (i, j) in path_amarelo and ch == ".":   # amarelo na volta
                line += YELLOW + "." + RESET
            elif (i, j) in path_azul and ch == ".":  # azul na ida
                line += BLUE + "." + RESET
            else:
                line += ch
        print(line)
    print()

# DFS exploratória
movimentos = 0
visited = set()
found_goal = False
path_taken = []   # caminho até o objetivo
goal_path = []    # caminho definitivo até o objetivo
ida_path = set()  # posições visitadas na ida
volta_path = set()  # posições visitadas na volta

def explore(pos):
    global movimentos, found_goal, goal_path
    if found_goal:
        return
    r, c = pos
    visited.add(pos)
    path_taken.append(pos)
    ida_path.add(pos)

    clear_console()
    print_grid_with_robot(grid, pos, ida_path, volta_path)
    time.sleep(SLEEP_TIME)

    if pos == goal:
        print("Objetivo encontrado em", pos)
        found_goal = True
        goal_path = path_taken.copy()
        return

    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if (nr, nc) not in visited and grid[nr][nc] in (".", "@"):
                movimentos += 1
                explore((nr, nc))
                if found_goal:
                    return
                # voltar
                back = path_taken.pop()
                movimentos += 1
                ida_path.add(back)
                clear_console()
                print_grid_with_robot(grid, back, ida_path, volta_path)
                time.sleep(SLEEP_TIME)

# Inicia exploração até o objetivo
explore(start)

# Agora faz o caminho inverso até o início
if found_goal:
    print("\nRetornando ao início...\n")
    for pos in reversed(goal_path[:-1]):  # ignora o último pq já está no objetivo
        movimentos += 1
        volta_path.add(pos)  # marca como caminho de volta
        clear_console()
        print_grid_with_robot(grid, pos, ida_path, volta_path)
        time.sleep(SLEEP_TIME)

print(f"\nExploração concluída. Movimentos realizados: {movimentos}")
