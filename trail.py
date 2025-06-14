import pygame
import sys
import math

# Nastavení okna
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (0, 0, 0)
FPS = 120

# Trail nastavení
TRAIL_LENGTH = 40  # Počet bodů v trailu

# Funkce pro interpolaci barvy (zelená -> oranžová -> červená)
def get_trail_color(speed, min_speed=0, max_speed=60):
    # speed: aktuální rychlost kurzoru
    # min_speed: rychlost pro zelenou
    # max_speed: rychlost pro červenou
    speed = max(min_speed, min(speed, max_speed))
    t = (speed - min_speed) / (max_speed - min_speed)
    if t < 0.5:
        # Zelená (0,255,0) -> Oranžová (255,165,0)
        t2 = t * 2
        r = int(0 + (255 - 0) * t2)
        g = int(255 - (255 - 165) * t2)
        b = 0
    else:
        # Oranžová (255,165,0) -> Červená (255,0,0)
        t2 = (t - 0.5) * 2
        r = 255
        g = int(165 - 165 * t2)
        b = 0
    return (r, g, b)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Osu Cursor Trail')
    clock = pygame.time.Clock()

    trail = []  # [(x, y), ...]
    prev_pos = pygame.mouse.get_pos()
    prev_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Získání pozice kurzoru
        pos = pygame.mouse.get_pos()
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
