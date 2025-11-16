"""
Script de démonstration des différentes interfaces du Tour du Cavalier
Demonstration script for different Knight's Tour interfaces
"""

import pygame
import sys
import os

def show_menu():
    """Affiche le menu de sélection des interfaces"""
    pygame.init()
    
    # Configuration de la fenêtre du menu
    MENU_WIDTH = 800
    MENU_HEIGHT = 600
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("🏰 Tour du Cavalier - Sélection Interface 🐎")
    clock = pygame.time.Clock()
    
    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    LIGHT_BLUE = (173, 216, 230)
    GOLD = (255, 215, 0)
    
    # Polices
    font_title = pygame.font.Font(None, 48)
    font_large = pygame.font.Font(None, 36)
    font_medium = pygame.font.Font(None, 24)
    
    # Boutons
    buttons = {
        'console': pygame.Rect(100, 200, 250, 80),
        'basic_gui': pygame.Rect(450, 200, 250, 80),
        'enhanced': pygame.Rect(275, 320, 250, 80),
        'quit': pygame.Rect(325, 450, 150, 50)
    }
    
    running = True
    selected = None
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                selected = 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for name, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            selected = name
                            running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = 'console'
                    running = False
                elif event.key == pygame.K_2:
                    selected = 'basic_gui'
                    running = False
                elif event.key == pygame.K_3:
                    selected = 'enhanced'
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    selected = 'quit'
                    running = False
        
        # Fond dégradé
        for y in range(MENU_HEIGHT):
            ratio = y / MENU_HEIGHT
            r = int(240 * (1 - ratio) + 200 * ratio)
            g = int(248 * (1 - ratio) + 220 * ratio)
            b = int(255 * (1 - ratio) + 240 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (MENU_WIDTH, y))
        
        # Titre
        title = font_title.render("🏰 Tour du Cavalier 🐎", True, BLACK)
        title_rect = title.get_rect(centerx=MENU_WIDTH // 2, y=50)
        screen.blit(title, title_rect)
        
        subtitle = font_medium.render("Choisissez votre interface préférée", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(centerx=MENU_WIDTH // 2, y=100)
        screen.blit(subtitle, subtitle_rect)
        
        # Dessiner les boutons
        button_info = {
            'console': {
                'text': "1. Console\nTexte simple",
                'color': (100, 150, 100),
                'hover': (120, 170, 120),
                'description': "Interface textuelle classique"
            },
            'basic_gui': {
                'text': "2. GUI Basique\nPygame simple", 
                'color': BLUE,
                'hover': (100, 160, 210),
                'description': "Interface graphique avec animations"
            },
            'enhanced': {
                'text': "3. GUI Avancée\nEffets visuels",
                'color': (180, 100, 180),
                'hover': (200, 120, 200),
                'description': "Interface complète avec particules"
            },
            'quit': {
                'text': "Quitter",
                'color': (150, 50, 50),
                'hover': (170, 70, 70),
                'description': "Fermer l'application"
            }
        }
        
        for name, rect in buttons.items():
            info = button_info[name]
            
            # Couleur selon survol
            if rect.collidepoint(mouse_pos):
                color = info['hover']
                # Effet de brillance
                highlight = pygame.Rect(rect.x, rect.y, rect.width, rect.height // 3)
                pygame.draw.rect(screen, (255, 255, 255, 100), highlight)
            else:
                color = info['color']
            
            # Dessiner le bouton
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            
            # Texte du bouton
            lines = info['text'].split('\n')
            total_height = len(lines) * 25
            start_y = rect.centery - total_height // 2
            
            for i, line in enumerate(lines):
                if i == 0:
                    text = font_large.render(line, True, WHITE)
                else:
                    text = font_medium.render(line, True, (220, 220, 220))
                text_rect = text.get_rect(centerx=rect.centerx, y=start_y + i * 25)
                screen.blit(text, text_rect)
            
            # Description en bas
            if rect.collidepoint(mouse_pos):
                desc = font_medium.render(info['description'], True, (50, 50, 50))
                desc_rect = desc.get_rect(centerx=MENU_WIDTH // 2, y=530)
                pygame.draw.rect(screen, WHITE, desc_rect.inflate(20, 10))
                pygame.draw.rect(screen, BLACK, desc_rect.inflate(20, 10), 1)
                screen.blit(desc, desc_rect)
        
        # Instructions
        instructions = font_medium.render("Cliquez sur un bouton ou utilisez les touches 1, 2, 3", True, (80, 80, 80))
        instructions_rect = instructions.get_rect(centerx=MENU_WIDTH // 2, y=570)
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return selected

def run_console():
    """Lance la version console"""
    print("Lancement de la version console...")
    os.system('python knights_tour_console.py')

def run_basic_gui():
    """Lance la version GUI basique"""
    print("Lancement de la version GUI basique...")
    os.system('python knights_tour_pygame.py')

def run_enhanced():
    """Lance la version GUI avancée"""
    print("Lancement de la version GUI avancée...")
    os.system('python knights_tour_enhanced.py')

def main():
    """Fonction principale du menu"""
    print("=" * 60)
    print("🏰 TOUR DU CAVALIER - MENU DE SÉLECTION 🐎")
    print("=" * 60)
    print("Dr. Meriem SEBAI, USTHB")
    print("Master 1, Visual Computing - 2025/2026")
    print("=" * 60)
    
    try:
        choice = show_menu()
        
        if choice == 'console':
            run_console()
        elif choice == 'basic_gui':
            run_basic_gui()
        elif choice == 'enhanced':
            run_enhanced()
        elif choice == 'quit' or choice is None:
            print("Au revoir ! 👋")
            return
            
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        print("Vérifiez que tous les fichiers sont présents dans le même dossier.")
    
    print("Fin du programme.")

if __name__ == "__main__":
    main()