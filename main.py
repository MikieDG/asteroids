import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot


def main():
    pygame.init()
    # Using SCALED makes F11 much smoother and keeps your coordinates consistent
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    
    while True:
        # 1. RESET GROUPS
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = updatable
        Shot.containers = (shots, updatable, drawable)
        Player.containers = (updatable, drawable)

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()

        dt = 0
        game_active = True
        
        # 2. GAME PLAY LOOP
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_active = False 
            
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        shot.kill()
                        asteroid.split()

            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000

        # 3. GAME OVER STATE
        waiting_for_input = True
        while waiting_for_input:
            text = font.render("GAME OVER - Press R to Restart", True, "white")
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_r:
                        waiting_for_input = False
if __name__ == "__main__":
    main()