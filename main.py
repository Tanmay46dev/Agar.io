import random
import pygame
from entities import Blob, Player

pygame.init()

class Game:
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1200, 600
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.DISPLAY_SURFACE = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Agar.io")

        # Player
        self.player_start_pos = (200, 200)
        self.player = Player(self.player_start_pos, 20, "Red")

        # A list to store all the blobs
        self.blobs = []

        # Win screen attributes
        self.win_text_font = pygame.font.SysFont(None, 128)
        self.win_text_surface = self.win_text_font.render("You win!", True, "White")
        self.win_text_surface_pos = (self.WINDOW_WIDTH / 2 - self.win_text_surface.get_width() / 2, self.WINDOW_HEIGHT / 2 - self.win_text_surface.get_height() / 2)
        self.show_win_screen = False

        # Score
        self.score_font = pygame.font.SysFont(None, 32)
        self.score = 0

        # Restart Label
        self.restart_text_font = pygame.font.SysFont(None, 32)
        self.restart_text_surface = self.restart_text_font.render("Press 'R' to restart", True, "White")


        # Creating enemies
        self.no_of_enemies = 20
        self.create_enemies(self.no_of_enemies)

    def create_enemies(self, number_of_enemies):
        # Create all enemies
        for _ in range(number_of_enemies):
            radius = random.randint(5, 7)
            pos_x = random.randint(0, self.WINDOW_WIDTH - radius * 2)
            pos_y = random.randint(50, self.WINDOW_HEIGHT - radius * 2)
            color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.blobs.append(Blob((pos_x, pos_y), radius, color))

    def get_updated_score_surface(self, score):
        score_text_surface = self.score_font.render(f"Score: {score}", True, "White")
        return score_text_surface

    def handle_drawing(self):
        self.DISPLAY_SURFACE.fill("#212121")

        # Looping through all the blobs and drawing them on the display surface
        [blob.draw(self.DISPLAY_SURFACE) for blob in self.blobs]

        # Drawing the player
        self.player.draw(self.DISPLAY_SURFACE)

        # Display Score
        self.score_surface = self.get_updated_score_surface(self.score)
        self.DISPLAY_SURFACE.blit(self.score_surface, (20, 20))

        # Display restart text
        self.DISPLAY_SURFACE.blit(self.restart_text_surface, (self.WINDOW_WIDTH - 220, 20))

        pygame.draw.aaline(self.DISPLAY_SURFACE, (200, 200, 200), (0,50), (self.WINDOW_WIDTH, 50),2)

        # Display win text if no blobs are left
        if not self.blobs:
            self.show_win_screen = True

        if self.show_win_screen:
            self.DISPLAY_SURFACE.blit(self.win_text_surface, self.win_text_surface_pos)

        # Updating the display
        pygame.display.update()
    
    def reset_game(self):
        # Delete previous enemies
        self.blobs.clear()
        # Create all enemies again
        self.create_enemies(self.no_of_enemies)
        # hide win screen
        self.show_win_screen = False
        # set score to 0
        self.score = 0
        # Reset the player's position
        self.player.rect.center = self.player_start_pos

    def handle_player_movement(self, keys):
        # Player movement
        if keys[pygame.K_LEFT] and self.player.rect.left >= 0:
            self.player.move(-1)
        elif keys[pygame.K_RIGHT] and self.player.rect.right <= self.WINDOW_WIDTH:
            self.player.move(1)
        if keys[pygame.K_UP] and self.player.rect.top >= 57:
            self.player.move(-1, True)
        elif keys[pygame.K_DOWN] and self.player.rect.bottom <= self.WINDOW_HEIGHT:
            self.player.move(1, True)

    def run(self):
        # Main Game Loop
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

            # Drawing
            self.handle_drawing()
            
            # Player movement
            keys = pygame.key.get_pressed()
            self.handle_player_movement(keys)

            # Checking collisions
            for blob in self.blobs:
                if self.player.is_colliding(blob):
                    self.blobs.remove(blob)
                    self.score += 1

if __name__ == "__main__":
    Game().run()

