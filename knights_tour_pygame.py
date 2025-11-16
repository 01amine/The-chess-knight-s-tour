"""
Knight's Tour Problem Solver with Pygame GUI and Animations
Interface graphique avec animations pour le problème du Tour du Cavalier
Author: Dr. Meriem SEBAI, USTHB
"""

import pygame
import sys
import random
import time
from knights_tour_console import Chromosome, Knight, Population

# Configuration pygame
pygame.init()

# Constantes pour l'affichage
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
BOARD_X = 50
BOARD_Y = 100

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
KNIGHT_COLOR = (139, 69, 19)
PATH_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 255, 0)
CURRENT_COLOR = (0, 0, 255)
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER = (150, 200, 250)
TEXT_COLOR = (50, 50, 50)

# Police
font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)

class KnightTourGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tour du Cavalier - Algorithme Génétique")
        self.clock = pygame.time.Clock()
        
        # État de l'application
        self.running = True
        self.algorithm_running = False
        self.animation_running = False
        self.population = None
        self.best_knight = None
        self.current_generation = 0
        self.best_fitness = 0
        self.animation_step = 0
        self.animation_speed = 5  # FPS pour l'animation
        
        # Paramètres de l'algorithme
        self.population_size = 50
        self.max_generations = 100
        
        # Boutons
        self.buttons = {
            'start': pygame.Rect(1000, 150, 150, 40),
            'stop': pygame.Rect(1000, 200, 150, 40),
            'animate': pygame.Rect(1000, 250, 150, 40),
            'reset': pygame.Rect(1000, 300, 150, 40),
            'speed_up': pygame.Rect(1000, 400, 70, 30),
            'speed_down': pygame.Rect(1080, 450, 70, 30)
        }
        
        self.mouse_pos = (0, 0)
        
    def draw_chessboard(self):
        """Dessine l'échiquier"""
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(
                    BOARD_X + col * SQUARE_SIZE,
                    BOARD_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                
                # Bordure
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Coordonnées
                coord_text = font_small.render(f"({col},{row})", True, TEXT_COLOR)
                text_rect = coord_text.get_rect()
                text_rect.topleft = (rect.x + 5, rect.y + 5)
                self.screen.blit(coord_text, text_rect)
    
    def draw_knight_path(self, knight, animate_up_to=None):
        """Dessine le chemin du cavalier avec animations"""
        if not knight or not knight.path:
            return
            
        path = knight.path
        if animate_up_to is not None:
            path = knight.path[:animate_up_to + 1]
        
        # Dessiner les lignes du chemin
        if len(path) > 1:
            points = []
            for pos in path:
                x = BOARD_X + pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2
                y = BOARD_Y + pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(self.screen, PATH_COLOR, False, points, 3)
        
        # Dessiner les positions visitées
        for i, pos in enumerate(path):
            x = BOARD_X + pos[0] * SQUARE_SIZE
            y = BOARD_Y + pos[1] * SQUARE_SIZE
            
            # Cercle pour la position visitée
            center_x = x + SQUARE_SIZE // 2
            center_y = y + SQUARE_SIZE // 2
            
            if i == 0:
                # Position de départ (vert)
                pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 15)
                text = font_small.render("START", True, WHITE)
            elif i == len(path) - 1 and animate_up_to is None:
                # Position finale (rouge)
                pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 15)
                text = font_small.render("END", True, WHITE)
            elif animate_up_to is not None and i == animate_up_to:
                # Position actuelle dans l'animation (bleu)
                pygame.draw.circle(self.screen, CURRENT_COLOR, (center_x, center_y), 20)
                text = font_medium.render(str(i + 1), True, WHITE)
            else:
                # Positions intermédiaires
                pygame.draw.circle(self.screen, VISITED_COLOR, (center_x, center_y), 12)
                text = font_small.render(str(i + 1), True, BLACK)
            
            # Numéro de l'étape
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)
    
    def draw_knight(self, pos, color=KNIGHT_COLOR):
        """Dessine le cavalier à une position donnée"""
        x = BOARD_X + pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        y = BOARD_Y + pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Forme du cavalier (triangle stylisé)
        points = [
            (x, y - 20),
            (x - 15, y + 15),
            (x + 15, y + 15)
        ]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, BLACK, points, 2)
        
        # Œil du cavalier
        pygame.draw.circle(self.screen, WHITE, (x - 5, y - 5), 3)
        pygame.draw.circle(self.screen, BLACK, (x - 5, y - 5), 1)
    
    def draw_button(self, name, rect, text, enabled=True):
        """Dessine un bouton"""
        color = BUTTON_COLOR if enabled else (150, 150, 150)
        
        # Effet de survol
        if enabled and rect.collidepoint(self.mouse_pos):
            color = BUTTON_HOVER
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        
        # Texte du bouton
        text_color = TEXT_COLOR if enabled else (100, 100, 100)
        button_text = font_medium.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)
    
    def draw_ui(self):
        """Dessine l'interface utilisateur"""
        # Titre
        title = font_large.render("Tour du Cavalier - Algorithme Génétique", True, TEXT_COLOR)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, y=20)
        self.screen.blit(title, title_rect)
        
        # Statistiques
        stats_y = 150
        if self.population:
            stats = [
                f"Génération: {self.current_generation}",
                f"Meilleur fitness: {self.best_fitness}/64",
                f"Taille population: {self.population_size}",
                f"Pourcentage: {(self.best_fitness/64)*100:.1f}%"
            ]
        else:
            stats = [
                "Cliquez sur 'Démarrer' pour commencer",
                f"Taille population: {self.population_size}",
                "Vitesse animation: " + str(self.animation_speed) + " FPS",
                ""
            ]
        
        for i, stat in enumerate(stats):
            text = font_medium.render(stat, True, TEXT_COLOR)
            self.screen.blit(text, (700, stats_y + i * 30))
        
        # Boutons
        self.draw_button('start', self.buttons['start'], "Démarrer", not self.algorithm_running)
        self.draw_button('stop', self.buttons['stop'], "Arrêter", self.algorithm_running)
        self.draw_button('animate', self.buttons['animate'], "Animer", self.best_knight is not None and not self.animation_running)
        self.draw_button('reset', self.buttons['reset'], "Reset", not self.algorithm_running and not self.animation_running)
        
        # Contrôles de vitesse
        speed_text = font_small.render("Vitesse animation:", True, TEXT_COLOR)
        self.screen.blit(speed_text, (700, 370))
        self.draw_button('speed_down', self.buttons['speed_down'], "-", True)
        speed_display = font_small.render(f"{self.animation_speed}", True, TEXT_COLOR)
        self.screen.blit(speed_display, (730, 410))
        self.draw_button('speed_up', self.buttons['speed_up'], "+", True)
        
        # Instructions
        instructions = [
            "Instructions:",
            "• Démarrer: Lance l'algorithme génétique",
            "• Animer: Montre le chemin étape par étape",
            "• +/-: Ajuste la vitesse d'animation",
            "",
            "L'algorithme cherche à visiter les 64 cases",
            "de l'échiquier avec un cavalier."
        ]
        
        for i, instruction in enumerate(instructions):
            color = TEXT_COLOR if instruction != "Instructions:" else BLACK
            weight = font_medium if instruction != "Instructions:" else font_large
            text = weight.render(instruction, True, color)
            self.screen.blit(text, (700, 500 + i * 25))
    
    def handle_button_click(self, pos):
        """Gère les clics sur les boutons"""
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == 'start' and not self.algorithm_running:
                    self.start_algorithm()
                elif name == 'stop' and self.algorithm_running:
                    self.stop_algorithm()
                elif name == 'animate' and self.best_knight and not self.animation_running:
                    self.start_animation()
                elif name == 'reset' and not self.algorithm_running and not self.animation_running:
                    self.reset()
                elif name == 'speed_up':
                    self.animation_speed = min(30, self.animation_speed + 1)
                elif name == 'speed_down':
                    self.animation_speed = max(1, self.animation_speed - 1)
    
    def start_algorithm(self):
        """Démarre l'algorithme génétique"""
        self.algorithm_running = True
        self.population = Population(self.population_size)
        self.current_generation = 0
        self.best_fitness = 0
        
    def stop_algorithm(self):
        """Arrête l'algorithme génétique"""
        self.algorithm_running = False
    
    def start_animation(self):
        """Démarre l'animation du chemin"""
        self.animation_running = True
        self.animation_step = 0
    
    def reset(self):
        """Remet à zéro l'application"""
        self.population = None
        self.best_knight = None
        self.current_generation = 0
        self.best_fitness = 0
        self.animation_running = False
        self.animation_step = 0
    
    def update_algorithm(self):
        """Met à jour une étape de l'algorithme génétique"""
        if not self.algorithm_running or not self.population:
            return
        
        # Vérifier la validité de la population
        self.population.check_population()
        
        # Évaluer la génération actuelle
        max_fit, best_solution = self.population.evaluate()
        
        if max_fit > self.best_fitness:
            self.best_fitness = max_fit
            self.best_knight = best_solution
        
        self.current_generation = self.population.generation
        
        # Vérifier les conditions d'arrêt
        if max_fit == 64:
            self.algorithm_running = False
            return
        
        if self.current_generation >= self.max_generations:
            self.algorithm_running = False
            return
        
        # Créer la nouvelle génération
        self.population.create_new_generation()
    
    def update_animation(self):
        """Met à jour l'animation du chemin"""
        if not self.animation_running or not self.best_knight:
            return
        
        # Avancer dans l'animation
        self.animation_step += 1
        
        if self.animation_step >= len(self.best_knight.path):
            self.animation_running = False
            self.animation_step = 0
    
    def run(self):
        """Boucle principale de l'application"""
        frame_count = 0
        
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_button_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.best_knight:
                        if not self.animation_running:
                            self.start_animation()
                        else:
                            self.animation_running = False
                    elif event.key == pygame.K_ESCAPE:
                        if self.algorithm_running:
                            self.stop_algorithm()
                        elif self.animation_running:
                            self.animation_running = False
            
            # Mise à jour de la logique
            frame_count += 1
            
            # Algorithme génétique (toutes les 10 frames pour la visibilité)
            if self.algorithm_running and frame_count % 10 == 0:
                self.update_algorithm()
            
            # Animation (selon la vitesse définie)
            if self.animation_running and frame_count % max(1, 60 // self.animation_speed) == 0:
                self.update_animation()
            
            # Rendu
            self.screen.fill(WHITE)
            self.draw_chessboard()
            
            # Dessiner le chemin du meilleur cavalier
            if self.best_knight:
                if self.animation_running:
                    self.draw_knight_path(self.best_knight, self.animation_step)
                    if self.animation_step < len(self.best_knight.path):
                        self.draw_knight(self.best_knight.path[self.animation_step], CURRENT_COLOR)
                else:
                    self.draw_knight_path(self.best_knight)
                    if self.best_knight.path:
                        self.draw_knight(self.best_knight.path[-1])
            
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """Fonction principale"""
    app = KnightTourGUI()
    app.run()

if __name__ == "__main__":
    main()