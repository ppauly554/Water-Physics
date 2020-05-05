import traceback
import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f"""EXCEPTION IN ({str(line).strip()}, LINE {str(lineno).strip()} {line.strip()}): {str(exc_obj).strip()})""")
    
try:
    import pygame
    pygame.init()
    window = pygame.display.set_mode((800,800))
    screen = []
    box = pygame.Surface((8,8))
    for x in range(0,100):
        screen.append([])
        for y in range(0,100):
            screen[x].append(0)
            if y == 99:
                screen[x][y] = 9
    
    def load(x,y,num):
        global screen
        while x%8:x -= 1
        while y%8:y -= 1
        if num == 9:
            screen[int(x/8)][int(y/8)] = (9)
        else:
            screen[int(x/8)][int(y/8)] = (num)
    
    def physics():
        global screen
        for x in range(len(screen) -1, -1, -1):
            for y in range(len(screen) -1, -1, -1):
                if screen[x][y] in range(1,9):
                    if y < 99 and screen[x][y+1] not in (8,9):
                        screen[x][y+1] += 1
                        screen[x][y] -= 1
                    r = False
                    for i in range(y+1,100):
                        if screen[x][i] == 9:
                            r = True
                            break
                        if screen[x][i] == 0:
                            r = False
                            break
                    if x < 99 and screen[x+1][y] not in (8,9) and r:
                        screen[x+1][y] += 1
                        screen[x][y] -= 1
                    if x > 0 and screen[x-1][y] not in (8,9) and r:
                        screen[x-1][y] += 1
                        screen[x][y] -= 1
                        
    run = True
    while run:
        pygame.display.flip()
        
        for x in range(len(screen)):
            for y in range(len(screen[x])):
                if screen[x][y] == 0:
                    box.fill((0,0,0))
                elif screen[x][y] == 9:
                    box.fill((255,255,255))
                else:
                    box.fill((0,0,0))
                    box.fill((0,0,255), rect = [0,8-screen[x][y],8,screen[x][y]])
                window.blit(box, (x*8,y*8))
        
        pos = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed() == (1,0,0):
            load(pos[0],pos[1],9)
        elif pygame.mouse.get_pressed() == (0,0,1):
            load(pos[0],pos[1],8)
        
        physics()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
    pygame.quit()
except Exception as e:
    print(e)
    PrintException()
    track = traceback.format_exc()
    print(track)
    input('a')
