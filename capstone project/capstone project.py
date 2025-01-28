import pygame
import random

pygame.init()




WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE




WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("square fights")

clock = pygame.time.Clock()


enemy_killed_sound = pygame.mixer.Sound("enemy_death.mp3")
health_item_pickup_sound = pygame.mixer.Sound("health_item_pickup.mp3")


pygame.mixer.music.load("game_music.mp3")   
pygame.mixer.music.play(-1)


class Player:
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.hp = 100

    
    
    def move(self, dx, dy, game_map):
        
        if 0 <= self.x + dx < GRID_WIDTH and 0 <= self.y + dy < GRID_HEIGHT:
            if game_map[self.y + dy][self.x + dx] == 0:
                self.x += dx
                self.y += dy

    
    
    def attack(self, enemies, score):
        
        for enemy in enemies:
            if (self.x == enemy.x and abs(self.y - enemy.y) == 1) or (self.y == enemy.y and abs(self.x - enemy.x) == 1):
                enemies.remove(enemy)
                enemy_killed_sound.play()
                print("enemy defeated")
                score += 1  
                break
        return score

    
    
    def draw(self):
        
        pygame.draw.rect(screen, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Enemy:
    
    
    def __init__(self, x, y, level=1):
        
        self.x = x
        self.y = y
        self.hp = 3 * level  
        self.attack_power = 1 * level  

    
    
    def move_towards_player(self, player, game_map):
        
        dx = player.x - self.x
        dy = player.y - self.y
        if abs(dx) > abs(dy):
            step_x = 1 if dx > 0 else -1
            if game_map[self.y][self.x + step_x] == 0 and not (self.x + step_x == player.x and self.y == player.y):
                self.x += step_x
        else:
            step_y = 1 if dy > 0 else -1
            if game_map[self.y + step_y][self.x] == 0 and not (self.x == player.x and self.y + step_y == player.y):
                self.y += step_y

    
    
    def attack(self, player):
        
        if (self.x == player.x and abs(self.y - player.y) == 1) or (self.y == player.y and abs(self.x - player.x) == 1):
            player.hp -= self.attack_power
            print(f"enemy attacked the player for {self.attack_power} damage")

    
    
    def draw(self):
        
        pygame.draw.rect(screen, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class HealthItem:
    
    def __init__(self, x, y, amount):
        
        self.x = x
        self.y = y
        self.amount = amount

    
    def draw(self):
        
        pygame.draw.rect(screen, GREEN, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))




def generate_map():
    
    game_map = [[0 if random.random() > 0.2 else 1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return game_map




def generate_enemies():
    
    num_enemies = random.randint(3, 10)
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        enemies.append(Enemy(x, y))
    return enemies




def generate_health_items():
    
    num_items = random.randint(1, 5)
    items = []
    for _ in range(num_items):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        amount = random.randint(1, 10)
        items.append(HealthItem(x, y, amount))
    return items



def draw_map(game_map):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BLACK if game_map[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))




def check_collisions(player, enemies):
    for enemy in enemies:
        if player.x == enemy.x and player.y == enemy.y:
            return True
    return False




def check_health_item_pickup(player, health_items):
    for item in health_items:
        if player.x == item.x and player.y == item.y:
            player.hp += item.amount
            health_items.remove(item)
            health_item_pickup_sound.play()
            print(f"player picked up a health item (+{item.amount} hp)")



def display_health(player):
    font = pygame.font.Font(None, 36)
    health_text = font.render(f'health: {player.hp}', True, YELLOW)
    screen.blit(health_text, (10, 10))




def display_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'score: {score}', True, YELLOW)
    screen.blit(score_text, (WIDTH - 150, 10))



def increase_enemy_strength(enemies, score):
    level = score // 10 
    for enemy in enemies:
        enemy.hp = 3 * (level + 1) 
        enemy.attack_power = 1 * (level + 1)  



def main():
    running = True
    player = Player(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    enemies = generate_enemies()
    health_items = generate_health_items()
    game_map = generate_map()

    player_turn = True
    score = 0  

    while running:
        screen.fill(WHITE)
        draw_map(game_map)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player_turn:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.move(0, -1, game_map)
                player_turn = False
            elif keys[pygame.K_DOWN]:
                player.move(0, 1, game_map)
                player_turn = False
            elif keys[pygame.K_LEFT]:
                player.move(-1, 0, game_map)
                player_turn = False
            elif keys[pygame.K_RIGHT]:
                player.move(1, 0, game_map)
                player_turn = False
            elif keys[pygame.K_SPACE]:
                score = player.attack(enemies, score)

        else:
            for enemy in enemies:
                enemy.move_towards_player(player, game_map)
                enemy.attack(player)
            player_turn = True

        check_health_item_pickup(player, health_items)

        player.draw()
        for enemy in enemies:
            enemy.draw()
        for item in health_items:
            item.draw()

        if check_collisions(player, enemies):
            
            player.hp -= 1

        display_health(player)
        display_score(score)  

        
        increase_enemy_strength(enemies, score)

        if player.hp <= 0:
            print("game over")
            running = False

        if not enemies:
            
            game_map = generate_map()
            enemies = generate_enemies()
            health_items = generate_health_items()

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
