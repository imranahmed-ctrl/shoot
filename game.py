import pygame, sys, random
from database import init_db, get_player_id, update_score, read_players

pygame.init()


class Player:
    def __init__(self, x, y, width=50, height=50, speed=7):
        
        self.image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self, screen, color=(0, 255, 0)):
        screen.blit(self.image, self.rect)


class Enemy:
    def __init__(self, screen_width, y=-40, width=40, height=40, speed=3):
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(
            topleft=(random.randint(0, screen_width - width), y)
        )
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen, color=(255, 0, 0)):
        screen.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y, width=10, height=20, speed=-7):
        self.image = pygame.image.load("assets/bullet.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen, color=(255, 255, 255)):
        screen.blit(self.image, self.rect)


class Score:
    def __init__(self, player_name, font_size=24):
        self.value = 0
        self.font = pygame.font.SysFont("Arial", font_size)
        self.player_name = player_name
        get_player_id(player_name)  

    def increase(self, points=10):
        self.value += points

    def save(self):
        update_score(self.player_name, self.value)

    def draw(self, screen, color=(255, 255, 255)):
        text = self.font.render(f"Score: {self.value}", True, color)
        screen.blit(text, (10, 10))

    @staticmethod
    def get_last_scores(limit=6):
        scores = read_players()
        return scores[:limit] if scores else []



def get_player_name(screen):
    font = pygame.font.SysFont("Arial", 36)
    input_box = pygame.Rect(250, 250, 300, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    active = False
    text = ""
    clock = pygame.time.Clock()

    while True:
        background = pygame.image.load("assets/background.jpg")
        screen.blit(background, (0, 0))
        msg = font.render("Enter Your Name:", True, (255, 255, 255))
        screen.blit(msg, (250, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text.strip():
                        return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def show_game_over(screen, score_obj):
    font = pygame.font.SysFont("Arial", 36)
    small_font = pygame.font.SysFont("Arial", 24)

    score_obj.save()
    last_scores = score_obj.get_last_scores(6)

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        msg = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(msg, (300, 100))

        score_text = font.render(f"Your Score: {score_obj.value}", True, (255, 255, 255))
        screen.blit(score_text, (280, 160))

        y = 220
        screen.blit(small_font.render("Last 6 Scores:", True, (0, 255, 0)), (300, y))
        y += 40
        for name, sc in last_scores:
            line = small_font.render(f"{name}: {sc}", True, (255, 255, 255))
            screen.blit(line, (300, y))
            y += 30

        msg2 = small_font.render("Press ENTER to play again or ESC to quit", True, (200, 200, 200))
        screen.blit(msg2, (180, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()



def main():
    init_db()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter with CRUD & Scores")
    clock = pygame.time.Clock()

    while True:
        player_name = get_player_name(screen)

        player = Player(WIDTH//2 - 25, HEIGHT - 60)
        bullets, enemies = [], []
        score = Score(player_name)

        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 1000)

        running = True
        while running:
            background = pygame.image.load("assets/background.jpg")
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.rect.centerx-5, player.rect.y))
                if event.type == SPAWN_EVENT:
                    enemies.append(Enemy(WIDTH))

            keys = pygame.key.get_pressed()
            player.move(keys, WIDTH)

            for bullet in bullets[:]:
                bullet.move()
                if bullet.rect.y < 0:
                    bullets.remove(bullet)

            for enemy in enemies[:]:
                enemy.move()
                if enemy.rect.y > HEIGHT:
                    enemies.remove(enemy)

            # Collisions
            for enemy in enemies[:]:
                if player.rect.colliderect(enemy.rect):
                    running = False
                for bullet in bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score.increase(10)

            # Draw
            player.draw(screen)
            for bullet in bullets: bullet.draw(screen)
            for enemy in enemies: enemy.draw(screen)
            score.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        restart = show_game_over(screen, score)
        if not restart:
            break


if __name__ == "__main__":
    main()
