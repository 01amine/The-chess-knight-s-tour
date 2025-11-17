import pygame
import json
import os
import sys
import math
import time
from typing import List, Tuple, Optional

# Initialisation de Pygame
pygame.init()

# Constantes
BOARD_SIZE = 8
CELL_SIZE = 70
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + 100
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
KNIGHT_COLOR = (139, 69, 19)
PATH_COLOR = (0, 128, 255)
VISITED_COLOR = (144, 238, 144)
CURRENT_COLOR = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
TEXT_COLOR = (50, 50, 50)

class Button:
    """Classe pour créer des boutons interactifs."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.is_clicked = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère les événements du bouton. Retourne True si cliqué."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
        return False
    
    def draw(self, screen: pygame.Surface):
        """Dessine le bouton sur l'écran."""
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        if self.is_clicked:
            color = tuple(max(0, c - 30) for c in color)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class KnightTourGUI:
    """Interface graphique pour visualiser le parcours du cavalier."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Knight's Tour Visualization")
        self.clock = pygame.time.Clock()
        
        # Polices
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 32)
        
        # État de l'animation
        self.solution_data: Optional[dict] = None
        self.path: List[Tuple[int, int]] = []
        self.is_animating = False
        self.animation_index = 0
        self.animation_speed = 1.0  # Vitesse de l'animation
        self.last_move_time = 0
        self.knight_pos = (0, 0)  # Position actuelle du cavalier pour l'animation
        self.target_pos = (0, 0)  # Position cible pour l'animation fluide
        self.animation_progress = 1.0  # Progression de l'animation entre deux cases
        
        # Boutons
        self.buttons = self._create_buttons()
        
        # Charger la solution si elle existe
        self.load_solution()
    
    def _create_buttons(self) -> List[Button]:
        """Crée les boutons de contrôle."""
        buttons = []
        button_x = BOARD_WIDTH + 10
        button_width = SIDEBAR_WIDTH - 20
        button_height = 40
        
        buttons.append(Button(button_x, 50, button_width, button_height, "Load Solution", self.font))
        buttons.append(Button(button_x, 100, button_width, button_height, "Start Animation", self.font))
        buttons.append(Button(button_x, 150, button_width, button_height, "Reset", self.font))
        buttons.append(Button(button_x, 200, button_width, button_height, "Speed +", self.font))
        buttons.append(Button(button_x, 250, button_width, button_height, "Speed -", self.font))
        buttons.append(Button(button_x, 300, button_width, button_height, "Repeat", self.font))
        
        return buttons
    
    def load_solution(self) -> bool:
        """Charge la solution depuis le fichier JSON."""
        try:
            if os.path.exists("knight_solution.json"):
                with open("knight_solution.json", "r") as f:
                    self.solution_data = json.load(f)
                    self.path = self.solution_data["path"]
                    print(f"Solution loaded: {len(self.path)} moves")
                    return True
            else:
                print("No solution file found. Run the console program first.")
                return False
        except Exception as e:
            print(f"Error loading solution: {e}")
            return False
    
    def start_animation(self):
        """Démarre l'animation du parcours."""
        if self.path:
            self.is_animating = True
            self.animation_index = 0
            self.knight_pos = self.path[0]
            self.target_pos = self.path[0]
            self.animation_progress = 1.0
            self.last_move_time = time.time()
            print("Animation started")
    
    def reset_animation(self):
        """Remet l'animation à zéro."""
        self.is_animating = False
        self.animation_index = 0
        if self.path:
            self.knight_pos = self.path[0]
            self.target_pos = self.path[0]
        self.animation_progress = 1.0
        print("Animation reset")
    
    def update_animation(self):
        """Met à jour l'animation du cavalier."""
        if not self.is_animating or not self.path:
            return
        
        current_time = time.time()
        time_per_move = 1.0 / self.animation_speed  # Temps en secondes par mouvement
        
        # Calculer la progression de l'animation
        time_since_last_move = current_time - self.last_move_time
        self.animation_progress = min(1.0, time_since_last_move / time_per_move)
        
        # Si l'animation actuelle est terminée, passer au mouvement suivant
        if self.animation_progress >= 1.0:
            self.animation_index += 1
            
            if self.animation_index < len(self.path):
                # Définir la nouvelle cible
                self.knight_pos = self.target_pos
                self.target_pos = self.path[self.animation_index]
                self.animation_progress = 0.0
                self.last_move_time = current_time
            else:
                # Animation terminée
                self.is_animating = False
                self.animation_progress = 1.0
                print("Animation completed!")
    
    def get_animated_knight_position(self) -> Tuple[float, float]:
        """Calcule la position interpolée du cavalier pour une animation fluide."""
        if self.animation_progress >= 1.0:
            return self.target_pos
        
        # Interpolation linéaire entre la position actuelle et la cible
        start_x, start_y = self.knight_pos
        target_x, target_y = self.target_pos
        
        # Utiliser une courbe d'animation plus fluide (ease-in-out)
        t = self.animation_progress
        smooth_t = t * t * (3 - 2 * t)  # Fonction de lissage
        
        animated_x = start_x + (target_x - start_x) * smooth_t
        animated_y = start_y + (target_y - start_y) * smooth_t
        
        return (animated_x, animated_y)
    
    def draw_board(self):
        """Dessine l'échiquier."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                # Couleur de la case (alternance)
                if (row + col) % 2 == 0:
                    color = LIGHT_BROWN
                else:
                    color = DARK_BROWN
                
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    
    def draw_path(self):
        """Dessine le chemin parcouru par le cavalier."""
        if not self.path:
            return
        
        # Dessiner les cases visitées
        visited_count = min(self.animation_index + 1, len(self.path)) if self.is_animating else len(self.path)
        
        for i in range(visited_count):
            x, y = self.path[i]
            screen_x = x * CELL_SIZE
            screen_y = y * CELL_SIZE
            
            # Surligner la case visitée
            pygame.draw.rect(self.screen, VISITED_COLOR, 
                           (screen_x + 5, screen_y + 5, CELL_SIZE - 10, CELL_SIZE - 10))
            
            # Afficher le numéro du mouvement
            text = self.small_font.render(str(i + 1), True, TEXT_COLOR)
            text_rect = text.get_rect(center=(screen_x + CELL_SIZE // 2, screen_y + 15))
            self.screen.blit(text, text_rect)
        
        # Dessiner les lignes connectant le chemin
        if visited_count > 1:
            points = []
            for i in range(visited_count):
                x, y = self.path[i]
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                points.append((center_x, center_y))
            
            if len(points) > 1:
                pygame.draw.lines(self.screen, PATH_COLOR, False, points, 3)
    
    def draw_knight(self):
        """Dessine le cavalier à sa position actuelle."""
        if not self.path:
            return
        
        # Obtenir la position animée du cavalier
        anim_x, anim_y = self.get_animated_knight_position()
        
        # Convertir en coordonnées écran
        center_x = anim_x * CELL_SIZE + CELL_SIZE // 2
        center_y = anim_y * CELL_SIZE + CELL_SIZE // 2
        
        # Dessiner le cavalier (cercle simple)
        pygame.draw.circle(self.screen, KNIGHT_COLOR, (int(center_x), int(center_y)), 20)
        pygame.draw.circle(self.screen, BLACK, (int(center_x), int(center_y)), 20, 3)
        
        # Ajouter un "K" pour Knight
        text = self.font.render("K", True, WHITE)
        text_rect = text.get_rect(center=(int(center_x), int(center_y)))
        self.screen.blit(text, text_rect)
    
    def draw_sidebar(self):
        """Dessine la barre latérale avec les informations et contrôles."""
        # Fond de la barre latérale
        sidebar_rect = pygame.Rect(BOARD_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, sidebar_rect)
        pygame.draw.line(self.screen, BLACK, (BOARD_WIDTH, 0), (BOARD_WIDTH, WINDOW_HEIGHT), 2)
        
        # Titre
        title = self.large_font.render("Knight's Tour", True, TEXT_COLOR)
        self.screen.blit(title, (BOARD_WIDTH + 10, 10))
        
        # Informations sur la solution
        y_offset = 350
        if self.solution_data:
            info_texts = [
                f"Total Moves: {len(self.path)}",
                f"Fitness: {self.solution_data.get('fitness', 0)}/64",
                f"Speed: {self.animation_speed:.1f}x",
                f"Current Move: {min(self.animation_index + 1, len(self.path)) if self.path else 0}"
            ]
            
            for i, text in enumerate(info_texts):
                rendered_text = self.font.render(text, True, TEXT_COLOR)
                self.screen.blit(rendered_text, (BOARD_WIDTH + 10, y_offset + i * 25))
        
        # Status
        status_y = y_offset + 120
        if self.is_animating:
            status_text = "Status: Animating..."
            status_color = (0, 150, 0)
        elif self.path:
            status_text = "Status: Ready"
            status_color = (0, 100, 200)
        else:
            status_text = "Status: No Solution"
            status_color = (200, 0, 0)
        
        status_surface = self.font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (BOARD_WIDTH + 10, status_y))
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(self.screen)
    
    def handle_events(self):
        """Gère les événements de l'interface."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Gérer les événements des boutons
            for i, button in enumerate(self.buttons):
                if button.handle_event(event):
                    self.handle_button_click(i)
            
            # Contrôles clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.is_animating:
                        self.reset_animation()
                    else:
                        self.start_animation()
                elif event.key == pygame.K_r:
                    self.reset_animation()
                elif event.key == pygame.K_l:
                    self.load_solution()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.animation_speed = min(5.0, self.animation_speed + 0.5)
                elif event.key == pygame.K_MINUS:
                    self.animation_speed = max(0.5, self.animation_speed - 0.5)
        
        return True
    
    def handle_button_click(self, button_index: int):
        """Gère les clics sur les boutons."""
        if button_index == 0:  # Load Solution
            self.load_solution()
        elif button_index == 1:  # Start Animation
            if not self.is_animating:
                self.start_animation()
        elif button_index == 2:  # Reset
            self.reset_animation()
        elif button_index == 3:  # Speed +
            self.animation_speed = min(5.0, self.animation_speed + 0.5)
        elif button_index == 4:  # Speed -
            self.animation_speed = max(0.5, self.animation_speed - 0.5)
        elif button_index == 5:  # Repeat
            self.reset_animation()
            if self.path:
                self.start_animation()
    
    def run(self):
        """Boucle principale de l'interface."""
        print("Knight's Tour GUI started")
        print("Controls:")
        print("- Space: Start/Stop animation")
        print("- R: Reset animation")
        print("- L: Load solution")
        print("- +/-: Change animation speed")
        
        running = True
        while running:
            running = self.handle_events()
            
            # Mettre à jour l'animation
            self.update_animation()
            
            # Dessiner tout
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_path()
            self.draw_knight()
            self.draw_sidebar()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Point d'entrée principal."""
    try:
        gui = KnightTourGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()