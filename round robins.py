import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (120,180,255)
RED = (255,0,0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("Helvetica", 30)
FONT20 = pygame.font.SysFont("Helvetica", 15)
DIAG_X, DIAG_Y, TILE_W = 100, 250, 30


def set_background():
    WIN.fill(WHITE)

procesos = ["x", "w", "z", "y"]
tis = [0, 2, 4, 5]
tcpus = [8, 6, 4, 2]
quantum = 1

n_procesos = len(procesos)
conj_cola_de_listos = []

def get_cpu(tis, tcpus, quantum):
    global conj_cola_de_listos
    tcpus_copy = tcpus.copy()
    t = 0
    q = 0
    cola_de_listos = []
    cpu = None
    cpu_lista = []
    while sum(tcpus_copy) > 0 and t < 1000:
        #Agregar nuevos procesos a la cola de listos
        grid_cola_de_listos = []
        if len(cola_de_listos) > 0:
            grid_cola_de_listos.append(procesos[cola_de_listos[0]])
        for i in range(n_procesos):
            if tis[i] == t:
                cola_de_listos.append(i)

        band = True
        if cpu is not None:
            if tcpus_copy[cpu] == 0:
                q = 0
                cpu = cola_de_listos.pop(0)
                band = False
        if q == 0 and band:
            if cpu is not None:
                cola_de_listos.append(cpu)
            cpu = cola_de_listos.pop(0)

        if cpu is not None:
            tcpus_copy[cpu] -= 1
        grid_cola_de_listos.extend(procesos[i] for i in cola_de_listos)
        conj_cola_de_listos.append(grid_cola_de_listos)
        cpu_lista.append(cpu)
        print(t, procesos[cpu], [procesos[i] for i in cola_de_listos], grid_cola_de_listos)
        if q + 1 < quantum and cpu is not None:
            q += 1
        else:
            q = 0
        t += 1
    return cpu_lista

cpu_lista = get_cpu(tis, tcpus, quantum)

def draw():

    #Dibujar rectangulos y textos

    for i, proc in enumerate(procesos):
        text_render = FONT.render(proc, True, BLACK)
        WIN.blit(text_render, (DIAG_X - 20 - text_render.get_width(), DIAG_Y + TILE_W*i + TILE_W/2 - text_render.get_height()/2))
    for i, num in enumerate(cpu_lista):
        #Escribir valores de tiempo
        text_render = FONT20.render(str(i), True, BLACK)
        WIN.blit(text_render, (DIAG_X + TILE_W*i - text_render.get_width()/2, DIAG_Y - 30))
        #Dibujar rectangulos azules
        pygame.draw.rect(WIN,BLUE, pygame.Rect(DIAG_X + TILE_W*i, DIAG_Y + TILE_W*num, TILE_W,TILE_W))
        #Dibujar texto lista cpu
        cpu_proc_render = FONT.render(procesos[num], True, BLACK)
        WIN.blit(cpu_proc_render, (DIAG_X + TILE_W/2 - cpu_proc_render.get_width()/2 + TILE_W*i, 80 - 10 - cpu_proc_render.get_height()))
        #Dibujar cola de listos
        for j in range(len(conj_cola_de_listos[i])):
            proc_cola_render = FONT.render(conj_cola_de_listos[i][j], True, BLACK)
            WIN.blit(proc_cola_render, (DIAG_X + TILE_W/2 - proc_cola_render.get_width()/2 + TILE_W*i, 80 + 25*j))
            pygame.draw.line(WIN, RED, (DIAG_X + TILE_W*i, 85 + 25), (DIAG_X + TILE_W*(i+1), 85),2)

    # dibujar lineas
    for i, proc in enumerate(procesos):
        if i == 0:
            pygame.draw.line(WIN, BLACK, (DIAG_X, DIAG_Y), (DIAG_X + len(cpu_lista)*TILE_W, DIAG_Y))
        pygame.draw.line(WIN, BLACK, (DIAG_X, DIAG_Y + TILE_W*(i+1)), (DIAG_X + len(cpu_lista) * TILE_W, DIAG_Y + TILE_W*(i+1)))

    for i, num in enumerate(cpu_lista):
        if i == 0:
            pygame.draw.line(WIN, BLACK, (DIAG_X, DIAG_Y), (DIAG_X, DIAG_Y + len(procesos)*TILE_W))
            pygame.draw.line(WIN, BLACK, (DIAG_X, 50), (DIAG_X, 50 + len(procesos) * TILE_W))
        pygame.draw.line(WIN, BLACK, (DIAG_X + (i+1) * TILE_W, DIAG_Y), (DIAG_X + (i+1) * TILE_W, DIAG_Y + len(procesos)*TILE_W))

        pygame.draw.line(WIN, BLACK, (DIAG_X + (i + 1) * TILE_W, 50), (DIAG_X + (i + 1) * TILE_W, 50 + len(procesos) * TILE_W))

    pygame.draw.line(WIN, BLACK, (20, 80), (DIAG_X + (len(cpu_lista) + 1)*TILE_W, 80))



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    set_background()
    draw()
    pygame.display.update()
pygame.quit()