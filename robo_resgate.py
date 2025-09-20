import time
import os
import csv

# Labirinto (inalterado)
raw_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X...X.....X...........X...X.....X.......X",
    "X.X.XXX.X.X.XXXXX.XXX.XXX.X.XXX.X.XXX.XXX",
    "X.X...X.X.....X...X.X...X.X.X.X.....X...X",
    "X.XXX.XXXXXXXXX.XXX.XXX.X.X.X.XXXXXXXXX.X",
    "X.X.............X.....X.X.X.X.....X...X.X",
    "X.XXXXXXXXXXXXXXX.XXX.X.X.X.XXXXX.X.X.X.X",
    "X...........X.....X.X...X.......X.X.X...X",
    "X.XXXXXXXXX.XXXXX.X.XXXXXXXXXXX.X.X.XXX.X",
    "X.X.......X.....X.X.@...X...X.....X...X.X",
    "X.XXXXX.XXXXXXX.X.XXX.X.X.X.XXXXXXX.X.X.X",
    "X.......X.....X.X.....X.X.X...X...X.X.X.X",
    "X.XXXXX.X.XXX.X.XXXXXXX.X.XXX.X.X.XXX.X.X",
    "X.X...X.X.X...X.X.X...X...X...X.X.....X.X",
    "X.X.X.XXX.X.XXX.X.X.X.XXXXX.XXX.XXXXXXX.X",
    "X.X.X.....X.X...X.X.X.....X...X.......X.X",
    "X.X.XXXXXXX.X.XXX.X.X.XXXXXXX.XXXXXXX.X.X",
    "E.X...X...X.X.X.....X.X.....X...X.....X.X",
    "X.XXX.X.X.X.X.X.XXXXX.X.XXX.XXX.X.XXXXX.X",
    "X.....X.X.....X.....X.....X.......X.....X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

SLEEP_TIME = 0.05
LOG_FILENAME = "log_robo.csv"

grid = [list(row) for row in raw_map]
rows, cols = len(grid), len(grid[0])

# Localiza entrada e pessoa
start = goal = None
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "E":
            start = (r, c)
        elif grid[r][c] == "@":
            goal = (r, c)
if not start or not goal:
    raise ValueError("Mapa precisa ter 'E' e '@'.")

# --- INÍCIO DAS ADIÇÕES DE ALARMES ---
class RobotAlarm(Exception):
    pass
# --- FIM DAS ADIÇÕES DE ALARMES ---

# Direções e símbolos
robot_chars = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
directions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
vector_to_direction = {v: k for k, v in directions.items()}
clockwise_turns = {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}
counter_clockwise_turns = {"UP": "LEFT", "LEFT": "DOWN", "DOWN": "RIGHT", "RIGHT": "UP"}

robot = {"pos": start, "direction": "DOWN"}

# Cores ANSI
BLUE, YELLOW, GREEN, RED, RESET = "\033[94m", "\033[93m", "\033[92m", "\033[91m", "\033[0m"

# --- LÓGICA DE LOG ---
log_data = []
csv_headers = [
    "Comando enviado",
    "Leitura do sensor do lado esquerdo do robô após execução do comando",
    "Leitura do sensor do lado direito do robô após execução do comando",
    "Leitura do sensor do lado direito do robô após execução do comando",
    "Situação do compartimento de carga"
]
log_data.append(csv_headers)

def get_sensor_reading(pos, direction_key):
    dr, dc = directions[direction_key]
    nr, nc = pos[0] + dr, pos[1] + dc
    if not (0 <= nr < rows and 0 <= nc < cols): return "PAREDE"
    cell_content = grid[nr][nc]
    if cell_content == 'X': return "PAREDE"
    if cell_content == '@': return "HUMANO"
    if cell_content == 'E': return "BASE"
    return "VAZIO"

def log_state(command):
    current_dir = robot["direction"]
    left_dir = counter_clockwise_turns[current_dir]
    right_dir = clockwise_turns[current_dir]
    sensor_esquerdo = get_sensor_reading(robot['pos'], left_dir)
    sensor_direito = get_sensor_reading(robot['pos'], right_dir)
    carga = "COM HUMANO" if has_person else "SEM CARGA"
    log_data.append([command, sensor_esquerdo, sensor_direito, sensor_direito, carga])

# --- FUNÇÕES BÁSICAS ---
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            if (i, j) == (r, c): line += robot_color + robot_char + RESET
            elif not has_person and (i, j) == goal: line += RED + "@" + RESET
            elif (i, j) in path_amarelo and ch == ".": line += YELLOW + "." + RESET
            elif (i, j) in path_azul and ch == ".": line += BLUE + "." + RESET
            else: line += ch
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
        log_state("G"); log_state("G"); log_state("G")
    else:
        movimentos += 1
        robot["direction"] = clockwise_turns[current_direction]
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
        log_state("G")
        if robot["direction"] != target_direction:
            movimentos += 1
            robot["direction"] = clockwise_turns[robot["direction"]]
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
            log_state("G")

# --- LÓGICA PRINCIPAL ---
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
    if movimentos == 0: print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)

    current_dir = robot["direction"]
    sensor_dirs = [clockwise_turns[current_dir], current_dir, counter_clockwise_turns[current_dir]]

    for target_direction in sensor_dirs:
        dr, dc = directions[target_direction]
        nr, nc = pos[0] + dr, pos[1] + dc
        if (nr, nc) == goal:
            print("Objetivo localizado! Resgatando...")
            turn_robot(target_direction)
            if get_sensor_reading(robot['pos'], robot['direction']) != "HUMANO":
                raise RobotAlarm("ALARM: Tentativa de coleta sem humano à frente do robô!")
            found_goal = True
            has_person = True
            log_state("P")
            goal_path = path_taken.copy()
            goal_path.append(goal)
            grid[goal[0]][goal[1]] = "."
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
            time.sleep(SLEEP_TIME * 2)
            return

    for target_direction in sensor_dirs:
        dr, dc = directions[target_direction]
        nr, nc = pos[0] + dr, pos[1] + dc
        cell_content = grid[nr][nc]
        if cell_content == 'X': continue
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and cell_content in (".", "E"):
            turn_robot(target_direction)
            movimentos += 1
            robot["pos"] = (nr, nc)
            log_state("A")
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
            explore((nr, nc))
            if found_goal: return
            
            # Calculate back direction safely
            back_vec = (-dr, -dc)
            if back_vec not in vector_to_direction:
                raise RobotAlarm(f"ALARM: Direção de retorno inválida: {back_vec}")
            back_direction = vector_to_direction[back_vec]
            turn_robot(back_direction)
            movimentos += 1
            robot["pos"] = pos
            log_state("A")
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
    path_taken.pop()

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
try:
    log_state("LIGAR")
    explore(start)
    if found_goal:
        # ALARME: Caminho de volta precisa de ao menos 2 pontos: a base 'E' e a casa adjacente.
        if not goal_path or len(goal_path) < 2:
            raise RobotAlarm("ALARM: Caminho de retorno inválido ou curto demais para entrega.")

        print("\nRetornando para o ponto de entrega...\n")

        # O robô NÃO deve entrar na casa 'E' (start). Ele para na casa ao lado.
        delivery_spot = start  # Coordenada da casa 'E'
        final_robot_pos = goal_path[1] # A casa adjacente, primeiro passo do robô

        # Loop de retorno até a posição final (adjacente a 'E')
        for i in range(len(goal_path) - 2, 0, -1):
            target_pos = goal_path[i]
            volta_path.add(robot["pos"])
            dr, dc = target_pos[0] - robot["pos"][0], target_pos[1] - robot["pos"][1]
            
            # Skip if no movement needed (already at target position)
            if (dr, dc) == (0, 0):
                continue
                
            if (dr, dc) not in vector_to_direction:
                raise RobotAlarm(f"ALARM: Movimento inválido detectado: ({dr}, {dc})")
                
            target_direction = vector_to_direction[(dr, dc)]
            turn_robot(target_direction)

            if get_sensor_reading(robot['pos'], robot['direction']) == 'PAREDE':
                raise RobotAlarm("ALARM: Tentativa de colisão com parede durante o retorno!")

            movimentos += 1
            robot["pos"] = target_pos
            log_state("A")
            print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)

            # ALARME: Garante que o robô não entre na base 'E' por acidente.
            if robot['pos'] == delivery_spot:
                raise RobotAlarm("ALARM: Falha na lógica de retorno! Robô entrou na base.")

        volta_path.add(robot["pos"])
        print("Chegando ao ponto de entrega...")
        
        # Manobra final: Virar-se para a base 'E' para fazer a entrega.
        dr, dc = delivery_spot[0] - robot['pos'][0], delivery_spot[1] - robot['pos'][1]
        final_direction = vector_to_direction.get((dr, dc))
        
        if not final_direction:
             raise RobotAlarm("ALARM: Não foi possível determinar a direção final para a entrega.")
        
        turn_robot(final_direction)
        print_grid_with_robot(grid, robot, has_person, ida_path, volta_path)
        time.sleep(SLEEP_TIME * 2)

        if not has_person:
            raise RobotAlarm("ALARM: Tentativa de ejeção sem humano presente!")

        print("\nPessoa entregue! Missão concluída.")
        log_state("E")
    else:
        print("Missão falhou: Humano não encontrado.")

except RobotAlarm as e:
    print(f"\n!!! MISSÃO INTERROMPida POR ALARME DE SEGURANÇA !!!")
    print(f"MOTIVO: {e}")

finally:
    print(f"\nMovimentos totais realizados: {movimentos}")
    try:
        with open(LOG_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(log_data)
        print(f"\nArquivo de log '{LOG_FILENAME}' gerado com sucesso.")
    except IOError:
        print(f"\nErro ao tentar escrever o arquivo de log '{LOG_FILENAME}'.")