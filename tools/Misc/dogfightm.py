import pygame
import math
import random
import json

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Ultimate Dogfight Spectacle")
clock = pygame.time.Clock()
FPS = 60

# Constants
N = 24
SPEED = 3.2
TURN_SPEED = 3
BOOST_SPEED = 5.5
MISSILE_SPEED = 6.5
MISSILE_TURN = 4
MISSILE_RELOAD = 40
HIT_RADIUS = 14
MAX_HEALTH = 100
RESPAWN_TIME = 80
MAX_TOTAL_MISSILES = 60
EXPLOSION_DURATION = 20
TEAM_COUNT = 4
CLOUD_COUNT = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED_BAR = (255, 0, 0)
YELLOW = (255, 255, 0)
TEAM_COLORS = [(0,150,255), (255,50,50), (255,255,0), (0,255,100)]

font = pygame.font.SysFont("arial", 24)

# Camera variables
camera_x, camera_y = 0, 0
camera_target = None
camera_timer = 0
camera_duration = 0

def update_camera():
    global camera_x, camera_y, camera_target, camera_timer, camera_duration
    camera_timer -= 1
    if camera_timer <= 0 or camera_target is None or not camera_target.alive:
        alive_aircrafts = [a for a in aircrafts if a.alive]
        if alive_aircrafts:
            camera_target = random.choice(alive_aircrafts)
            camera_duration = camera_timer = random.randint(180, 360)
    if camera_target and camera_target.alive:
        target_x = camera_target.x - WIDTH // 2
        target_y = camera_target.y - HEIGHT // 2
        camera_x += (target_x - camera_x) * 0.05
        camera_y += (target_y - camera_y) * 0.05

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def rotate_point(cx, cy, angle_deg, px, py):
    angle = math.radians(angle_deg)
    s = math.sin(angle)
    c = math.cos(angle)
    px -= cx
    py -= cy
    xnew = px * c - py * s
    ynew = px * s + py * c
    return cx + xnew, cy + ynew

class Explosion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.timer = EXPLOSION_DURATION

    def update(self):
        self.timer -= 1

    def draw(self):
        r = 40 - 2 * (EXPLOSION_DURATION - self.timer)
        if r > 0:
            pygame.draw.circle(screen, (255, 100, 0), (int(self.x - camera_x), int(self.y - camera_y)), r)
            pygame.draw.circle(screen, (255, 255, 100), (int(self.x - camera_x), int(self.y - camera_y)), max(0, r - 6), 3)

class Missile:
    def __init__(self, x, y, angle, target):
        self.x, self.y = x, y
        self.angle = angle
        self.target = target
        self.alive = True
        self.trail = []

    def update(self):
        if not self.target.alive:
            self.alive = False
            return
        dx, dy = self.target.x - self.x, self.target.y - self.y
        desired_angle = math.degrees(math.atan2(dy, dx))
        delta = (desired_angle - self.angle + 360) % 360
        if delta > 180:
            delta -= 360
        self.angle += max(-MISSILE_TURN, min(MISSILE_TURN, delta))
        self.angle %= 360
        rad = math.radians(self.angle)
        self.x += MISSILE_SPEED * math.cos(rad)
        self.y += MISSILE_SPEED * math.sin(rad)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        if math.hypot(self.target.x - self.x, self.target.y - self.y) < HIT_RADIUS:
            self.target.hit(20)
            self.alive = False

    def draw(self):
        for i, (tx, ty) in enumerate(self.trail):
            pygame.draw.circle(screen, (255, 220, 0), (int(tx - camera_x), int(ty - camera_y)), max(1, 5 - i // 2))
        pygame.draw.circle(screen, YELLOW, (int(self.x - camera_x), int(self.y - camera_y)), 4)

class Aircraft:
    def __init__(self, x, y, color, model_name, team):
        self.x, self.y = x, y
        self.color = color
        self.team = team
        self.angle = random.uniform(0, 360)
        self.health = MAX_HEALTH
        self.missiles = []
        self.reload_timer = 0
        self.respawn_timer = 0
        self.alive = True
        self.model = models.get(model_name, {})
        self.model_name = model_name

    def hit(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.explode()

    def explode(self):
        self.alive = False
        self.respawn_timer = RESPAWN_TIME
        explosions.append(Explosion(self.x, self.y))

    def update(self, aircraft_list):
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.respawn()
            return

        margin = 50
        if self.x < margin and 90 < self.angle < 270:
            self.angle += TURN_SPEED
        elif self.x > WIDTH - margin and (self.angle < 90 or self.angle > 270):
            self.angle += TURN_SPEED
        if self.y < margin and 0 < self.angle < 180:
            self.angle += TURN_SPEED
        elif self.y > HEIGHT - margin and 180 < self.angle < 360:
            self.angle += TURN_SPEED

        enemies = [a for a in aircraft_list if a is not self and a.alive and a.team != self.team]
        if not enemies:
            return
        enemy = min(enemies, key=lambda a: math.hypot(a.x - self.x, a.y - self.y))
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        target_angle = math.degrees(math.atan2(dy, dx))
        diff = (target_angle - self.angle + 360) % 360
        if diff > 180:
            diff -= 360
        self.angle += max(-TURN_SPEED, min(TURN_SPEED, diff))
        self.angle %= 360
        speed = BOOST_SPEED if abs(diff) < 20 else SPEED
        rad = math.radians(self.angle)
        self.x += speed * math.cos(rad)
        self.y += speed * math.sin(rad)

        if self.reload_timer > 0:
            self.reload_timer -= 1
        if (math.hypot(dx, dy) < 300 and self.reload_timer <= 0 and
                len(self.missiles) < 3 and sum(len(a.missiles) for a in aircraft_list) < MAX_TOTAL_MISSILES):
            self.missiles.append(Missile(self.x, self.y, self.angle, enemy))
            self.reload_timer = MISSILE_RELOAD

        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def respawn(self):
        self.health = MAX_HEALTH
        self.alive = True
        self.x, self.y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        self.angle = random.uniform(0, 360)
        self.missiles = []

    def draw(self):
        if not self.alive:
            return
        for part_name, points in self.model.items():
            if not points or part_name == "colors":
                continue
            rotated = [rotate_point(self.x - camera_x, self.y - camera_y, self.angle,
                                    self.x - camera_x + p[0], self.y - camera_y + p[1]) for p in points]
            pygame.draw.polygon(screen, self.color, rotated, 0)
        pygame.draw.rect(screen, RED_BAR, (self.x - 22 - camera_x, self.y + 24 - camera_y, 44, 6))
        pygame.draw.rect(screen, GREEN, (self.x - 22 - camera_x, self.y + 24 - camera_y, 44 * self.health / MAX_HEALTH, 6))
        for m in self.missiles:
            m.draw()

class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(60, 180)
        self.color = (220, 220, 220)
        self.speed = random.uniform(0.15, 0.35)

    def update(self):
        self.x -= self.speed
        if self.x < -self.size:
            self.x = WIDTH + self.size
            self.y = random.randint(0, HEIGHT)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x - camera_x, self.y - camera_y, self.size, self.size//2))

# Load aircraft models once
with open("2dfight.json") as f:
    models = json.load(f)
model_names = list(models.keys())

# Initialize objects
clouds = [Cloud() for _ in range(CLOUD_COUNT)]
aircrafts = [
    Aircraft(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100),
             TEAM_COLORS[i % TEAM_COUNT], random.choice(model_names), i % TEAM_COUNT)
    for i in range(N)
]
explosions = []

# Main game loop
running = True
while running:
    screen.fill((10, 10, 20))
    update_camera()

    for cloud in clouds:
        cloud.update()
        cloud.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    for a in aircrafts:
        a.update(aircrafts)
    for a in aircrafts:
        a.draw()
    for e in explosions:
        e.update()
        e.draw()
    explosions = [e for e in explosions if e.timer > 0]

    draw_text(f"Alive: {sum(1 for a in aircrafts if a.alive)} / {N}", 10, 10)
    draw_text(f"Missiles: {sum(len(a.missiles) for a in aircrafts)}", 10, 34)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()