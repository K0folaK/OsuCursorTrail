import pygame
import sys
import math
try:
    from screeninfo import get_monitors
except ImportError:
    print("Please install screeninfo: pip install screeninfo")
    sys.exit(1)
import tkinter as tk
from tkinter import ttk
import ctypes

# Nastavení okna
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (0, 0, 0)
FPS = 120

# Trail nastavení
TRAIL_LENGTH = 15# Počet bodů v trailu (rychlejší mizení)

# Funkce pro interpolaci barvy (zelená -> oranžová -> červená)
def get_trail_color(speed, green_thr=1000, orange_thr=3000):
    # Zelená (0,255,0), Oranžová (255,165,0), Červená (255,0,0)
    if speed <= green_thr:
        return (0, 255, 0)
    elif speed <= orange_thr:
        # Interpolace zelená -> oranžová
        t = (speed - green_thr) / (orange_thr - green_thr)
        r = int(0 + (255 - 0) * t)
        g = int(255 - (255 - 165) * t)
        b = 0
        return (r, g, b)
    else:
        # Interpolace oranžová -> červená (rychlosti nad orange_thr)
        t = min((speed - orange_thr) / 100, 1.0)  # 100 px/s pro plnou červenou
        r = 255
        g = int(165 - 165 * t)
        b = 0
        return (r, g, b)

def select_monitor_gui(monitors):
    selected = {'idx': 0}
    def on_select():
        selected['idx'] = combo.current()
        root.destroy()
    root = tk.Tk()
    root.title('Select Monitor for Cursor Tracking')
    tk.Label(root, text='Select monitor to track cursor:').pack(padx=10, pady=10)
    combo = ttk.Combobox(root, state='readonly', width=40)
    combo['values'] = [f"{i}: {m.name} ({m.width}x{m.height}) at ({m.x},{m.y})" for i, m in enumerate(monitors)]
    combo.current(0)
    combo.pack(padx=10, pady=5)
    tk.Button(root, text='OK', command=on_select).pack(pady=10)
    root.mainloop()
    return selected['idx']

def get_cursor_pos():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def main():
    # Výběr monitoru
    monitors = get_monitors()
    idx = select_monitor_gui(monitors)
    monitor = monitors[idx]
    # Výpočet pozice pro střed okna na vybraném monitoru
    win_x = monitor.x + (monitor.width - WIDTH) // 2
    win_y = monitor.y + (monitor.height - HEIGHT) // 2
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{win_x},{win_y}"
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Osu Cursor Trail')
    clock = pygame.time.Clock()

    trail = []  # [(x, y), ...]
    prev_pos = get_cursor_pos()
    prev_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Získání globální pozice kurzoru
        global_pos = get_cursor_pos()
        # Přepočet na relativní pozici v rámci vybraného monitoru
        rel_x = global_pos[0] - monitor.x
        rel_y = global_pos[1] - monitor.y
        # Přepočet na okno 1280x720
        pos_x = int(rel_x * WIDTH / monitor.width)
        pos_y = int(rel_y * HEIGHT / monitor.height)
        pos = (pos_x, pos_y)

        now = pygame.time.get_ticks()
        dt = (now - prev_time) / 1000.0  # v sekundách
        dx = pos[0] - prev_pos[0]
        dy = pos[1] - prev_pos[1]
        dist = math.hypot(dx, dy)
        speed = dist / dt if dt > 0 else 0
        prev_pos = pos
        prev_time = now

        # Přidání pozice do trailu
        trail.append(pos)
        if len(trail) > TRAIL_LENGTH:
            trail.pop(0)

        # Vykreslení
        screen.fill(BG_COLOR)
        if len(trail) > 1:
            color = get_trail_color(speed)
            pygame.draw.lines(screen, color, False, trail, 6)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
