import pygame
import json
import os
import sys
import math
import time
from typing import List, Tuple, Optional

# Pygame initialization
pygame.init()

# Constants
BOARD_SIZE = 8
CELL_SIZE = 80
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
SIDEBAR_WIDTH = 280
WINDOW_WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + 120
FPS = 60

# Vintage Color Palette
CREAM = (245, 238, 220)
LIGHT_SQUARE = (240, 230, 210)
DARK_SQUARE = (88, 70, 120)  # Purple matching knight
KNIGHT_PURPLE = (88, 70, 120)
PATH_COLOR = (180, 140, 200)
VISITED_COLOR = (150, 120, 180, 180)
CURRENT_HIGHLIGHT = (200, 160, 220)
VINTAGE_GOLD = (218, 165, 32)
DARK_TEXT = (60, 50, 70)
BUTTON_COLOR = (120, 100, 150)
BUTTON_HOVER = (140, 120, 170)
BORDER_COLOR = (70, 50, 90)

class Button:
    """Interactive button with vintage styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.is_clicked = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button events. Returns True if clicked."""
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
        """Draw vintage-styled button."""
        color = BUTTON_HOVER if self.is_hovered else BUTTON_COLOR
        if self.is_clicked:
            color = tuple(max(0, c - 20) for c in color)
        
        # Draw button with ornate border
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, VINTAGE_GOLD, self.rect, 3, border_radius=5)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 1, border_radius=5)
        
        # Draw text
        text_surface = self.font.render(self.text, True, CREAM)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class KnightTourGUI:
    """Vintage-styled GUI for Knight's Tour visualization."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("♞ Knight's Tour - Vintage Chess")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.load_fonts()
        
        # Load knight image
        self.knight_image = self.load_knight_image()
        
        # Animation state
        self.solution_data: Optional[dict] = None
        self.path: List[Tuple[int, int]] = []
        self.is_animating = False
        self.animation_index = 0
        self.animation_speed = 1.5
        self.last_move_time = 0
        self.knight_pos = (0, 0)
        self.target_pos = (0, 0)
        self.animation_progress = 1.0
        
        # Visual effects
        self.glow_intensity = 0
        self.glow_direction = 1
        
        # Buttons
        self.buttons = self._create_buttons()
        
        # Load solution
        self.load_solution()
    
    def load_fonts(self):
        """Load fonts with fallback to system fonts."""
        try:
            if os.path.exists("fonts/SuperCrawler.ttf"):
                self.title_font = pygame.font.Font("fonts/SuperCrawler.ttf", 48)
                self.font = pygame.font.Font("fonts/SuperCrawler.ttf", 22)
                self.small_font = pygame.font.Font("fonts/SuperCrawler.ttf", 16)
                self.large_font = pygame.font.Font("fonts/SuperCrawler.ttf", 36)
            else:
                # Fallback to system fonts with vintage feel
                self.title_font = pygame.font.SysFont('georgia', 48, bold=True)
                self.font = pygame.font.SysFont('georgia', 22)
                self.small_font = pygame.font.SysFont('georgia', 16)
                self.large_font = pygame.font.SysFont('georgia', 36, bold=True)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.font = pygame.font.Font(None, 22)
            self.small_font = pygame.font.Font(None, 16)
            self.large_font = pygame.font.Font(None, 36)
    
    def load_knight_image(self) -> Optional[pygame.Surface]:
        """Load and scale the knight image."""
        try:
            if os.path.exists("assets/knight.png"):
                image = pygame.image.load("assets/knight.png")
                # Scale to fit cell with some padding
                scaled_size = int(CELL_SIZE * 0.7)
                image = pygame.transform.scale(image, (scaled_size, scaled_size))
                return image
            else:
                print("Knight image not found. Using default representation.")
                return None
        except Exception as e:
            print(f"Error loading knight image: {e}")
            return None
    
    def _create_buttons(self) -> List[Button]:
        """Create control buttons."""
        buttons = []
        button_x = BOARD_WIDTH + 20
        button_width = SIDEBAR_WIDTH - 40
        button_height = 45
        start_y = 200
        spacing = 55
        
        button_labels = [
            "⟳ Load Solution",
            "▶ Start Animation",
            "⟲ Reset",
            "⊕ Speed Up",
            "⊖ Speed Down",
            "↻ Replay"
        ]
        
        for i, label in enumerate(button_labels):
            buttons.append(Button(
                button_x, 
                start_y + i * spacing, 
                button_width, 
                button_height, 
                label, 
                self.font
            ))
        
        return buttons
    
    def load_solution(self) -> bool:
        """Load solution from JSON file."""
        try:
            if os.path.exists("knight_solution.json"):
                with open("knight_solution.json", "r") as f:
                    self.solution_data = json.load(f)
                    self.path = self.solution_data["path"]
                    print(f"✓ Solution loaded: {len(self.path)} moves")
                    return True
            else:
                print("⚠ No solution file found.")
                return False
        except Exception as e:
            print(f"✗ Error loading solution: {e}")
            return False
    
    def start_animation(self):
        """Start the tour animation."""
        if self.path:
            self.is_animating = True
            self.animation_index = 0
            self.knight_pos = self.path[0]
            self.target_pos = self.path[0]
            self.animation_progress = 1.0
            self.last_move_time = time.time()
            print("▶ Animation started")
    
    def reset_animation(self):
        """Reset animation to beginning."""
        self.is_animating = False
        self.animation_index = 0
        if self.path:
            self.knight_pos = self.path[0]
            self.target_pos = self.path[0]
        self.animation_progress = 1.0
        print("⟲ Animation reset")
    
    def update_animation(self):
        """Update knight animation."""
        if not self.is_animating or not self.path:
            return
        
        current_time = time.time()
        time_per_move = 1.0 / self.animation_speed
        
        time_since_last_move = current_time - self.last_move_time
        self.animation_progress = min(1.0, time_since_last_move / time_per_move)
        
        if self.animation_progress >= 1.0:
            self.animation_index += 1
            
            if self.animation_index < len(self.path):
                self.knight_pos = self.target_pos
                self.target_pos = self.path[self.animation_index]
                self.animation_progress = 0.0
                self.last_move_time = current_time
            else:
                self.is_animating = False
                self.animation_progress = 1.0
                print("✓ Animation completed!")
        
        # Update glow effect
        self.glow_intensity += self.glow_direction * 2
        if self.glow_intensity >= 40 or self.glow_intensity <= 0:
            self.glow_direction *= -1
        self.glow_intensity = max(0, min(40, self.glow_intensity))
    
    def get_animated_knight_position(self) -> Tuple[float, float]:
        """Calculate interpolated knight position."""
        if self.animation_progress >= 1.0:
            return self.target_pos
        
        start_x, start_y = self.knight_pos
        target_x, target_y = self.target_pos
        
        # Smooth easing function
        t = self.animation_progress
        smooth_t = t * t * (3 - 2 * t)
        
        animated_x = start_x + (target_x - start_x) * smooth_t
        animated_y = start_y + (target_y - start_y) * smooth_t
        
        return (animated_x, animated_y)
    
    def draw_board(self):
        """Draw vintage chessboard with ornate border."""
        # Draw ornate border around board
        border_width = 10
        border_rect = pygame.Rect(-border_width, -border_width, 
                                  BOARD_WIDTH + 2*border_width, 
                                  BOARD_HEIGHT + 2*border_width)
        pygame.draw.rect(self.screen, BORDER_COLOR, border_rect)
        pygame.draw.rect(self.screen, VINTAGE_GOLD, border_rect, 4)
        
        # Draw squares
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE
                else:
                    color = DARK_SQUARE
                
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                
                # Draw subtle inner border
                pygame.draw.rect(self.screen, BORDER_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw coordinate labels
        for i in range(BOARD_SIZE):
            # Column labels (a-h)
            label = chr(97 + i)
            text = self.small_font.render(label, True, VINTAGE_GOLD)
            self.screen.blit(text, (i * CELL_SIZE + CELL_SIZE//2 - 5, BOARD_HEIGHT + 5))
            
            # Row labels (1-8)
            label = str(BOARD_SIZE - i)
            text = self.small_font.render(label, True, VINTAGE_GOLD)
            self.screen.blit(text, (BOARD_WIDTH + 5, i * CELL_SIZE + CELL_SIZE//2 - 8))
    
    def draw_path(self):
        """Draw the knight's path with vintage styling."""
        if not self.path:
            return
        
        visited_count = min(self.animation_index + 1, len(self.path)) if self.is_animating else len(self.path)
        
        # Draw visited squares with gradient effect
        for i in range(visited_count):
            x, y = self.path[i]
            screen_x = x * CELL_SIZE
            screen_y = y * CELL_SIZE
            
            # Create surface for transparency
            overlay = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
            
            # Fade effect based on position in path
            alpha = 100 + int(55 * (i / max(1, visited_count - 1)))
            color_with_alpha = (*PATH_COLOR, alpha)
            overlay.fill(color_with_alpha)
            
            self.screen.blit(overlay, (screen_x + 5, screen_y + 5))
            
            # Draw move number with ornate circle
            circle_center = (screen_x + CELL_SIZE // 2, screen_y + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, VINTAGE_GOLD, circle_center, 16)
            pygame.draw.circle(self.screen, DARK_SQUARE, circle_center, 14)
            
            text = self.small_font.render(str(i + 1), True, VINTAGE_GOLD)
            text_rect = text.get_rect(center=circle_center)
            self.screen.blit(text, text_rect)
        
        # Draw connecting path lines
        if visited_count > 1:
            points = []
            for i in range(visited_count):
                x, y = self.path[i]
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                points.append((center_x, center_y))
            
            if len(points) > 1:
                # Draw shadow line
                shadow_points = [(p[0]+2, p[1]+2) for p in points]
                pygame.draw.lines(self.screen, BORDER_COLOR, False, shadow_points, 4)
                # Draw main line
                pygame.draw.lines(self.screen, VINTAGE_GOLD, False, points, 3)
    
    def draw_knight(self):
        """Draw the knight piece."""
        if not self.path:
            return
        
        anim_x, anim_y = self.get_animated_knight_position()
        
        center_x = anim_x * CELL_SIZE + CELL_SIZE // 2
        center_y = anim_y * CELL_SIZE + CELL_SIZE // 2
        
        if self.knight_image:
            # Draw glow effect when animating
            if self.is_animating:
                glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                glow_color = (*CURRENT_HIGHLIGHT, self.glow_intensity)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (CELL_SIZE//2, CELL_SIZE//2), 
                                 int(CELL_SIZE * 0.4))
                glow_x = int(center_x - CELL_SIZE//2)
                glow_y = int(center_y - CELL_SIZE//2)
                self.screen.blit(glow_surface, (glow_x, glow_y))
            
            # Draw knight image
            img_rect = self.knight_image.get_rect(center=(int(center_x), int(center_y)))
            self.screen.blit(self.knight_image, img_rect)
        else:
            # Fallback: draw stylized knight symbol
            pygame.draw.circle(self.screen, KNIGHT_PURPLE, (int(center_x), int(center_y)), 28)
            pygame.draw.circle(self.screen, VINTAGE_GOLD, (int(center_x), int(center_y)), 28, 3)
            pygame.draw.circle(self.screen, BORDER_COLOR, (int(center_x), int(center_y)), 25)
            
            text = self.large_font.render("♞", True, CREAM)
            text_rect = text.get_rect(center=(int(center_x), int(center_y)))
            self.screen.blit(text, text_rect)
    
    def draw_sidebar(self):
        """Draw vintage-styled sidebar."""
        sidebar_rect = pygame.Rect(BOARD_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, CREAM, sidebar_rect)
        pygame.draw.rect(self.screen, VINTAGE_GOLD, (BOARD_WIDTH, 0, 4, WINDOW_HEIGHT))
        
        # Decorative header
        header_rect = pygame.Rect(BOARD_WIDTH, 0, SIDEBAR_WIDTH, 180)
        pygame.draw.rect(self.screen, DARK_SQUARE, header_rect)
        
        # Ornate title
        title_lines = ["Knight's", "Tour"]
        y_pos = 20
        for line in title_lines:
            title = self.title_font.render(line, True, VINTAGE_GOLD)
            title_shadow = self.title_font.render(line, True, BORDER_COLOR)
            x_center = BOARD_WIDTH + SIDEBAR_WIDTH // 2
            
            self.screen.blit(title_shadow, 
                           title_shadow.get_rect(center=(x_center + 2, y_pos + 2)))
            self.screen.blit(title, 
                           title.get_rect(center=(x_center, y_pos)))
            y_pos += 50
        
        # Vintage divider line
        div_y = 180
        pygame.draw.line(self.screen, VINTAGE_GOLD, 
                        (BOARD_WIDTH + 20, div_y), 
                        (BOARD_WIDTH + SIDEBAR_WIDTH - 20, div_y), 3)
        
        # Information panel
        if self.solution_data:
            info_y = 520
            info_texts = [
                ("Moves", f"{len(self.path)}/64"),
                ("Speed", f"{self.animation_speed:.1f}×"),
                ("Progress", f"{min(self.animation_index + 1, len(self.path)) if self.path else 0}")
            ]
            
            for label, value in info_texts:
                label_text = self.font.render(label + ":", True, DARK_TEXT)
                value_text = self.font.render(value, True, KNIGHT_PURPLE)
                
                self.screen.blit(label_text, (BOARD_WIDTH + 25, info_y))
                self.screen.blit(value_text, (BOARD_WIDTH + 180, info_y))
                info_y += 30
        
        # Status indicator
        status_y = 620
        if self.is_animating:
            status = "◉ Animating"
            color = (100, 180, 100)
        elif self.path:
            status = "◎ Ready"
            color = KNIGHT_PURPLE
        else:
            status = "○ No Solution"
            color = (180, 100, 100)
        
        status_surface = self.font.render(status, True, color)
        self.screen.blit(status_surface, (BOARD_WIDTH + 25, status_y))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
    
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            for i, button in enumerate(self.buttons):
                if button.handle_event(event):
                    self.handle_button_click(i)
            
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
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    self.animation_speed = min(5.0, self.animation_speed + 0.5)
                elif event.key == pygame.K_MINUS:
                    self.animation_speed = max(0.5, self.animation_speed - 0.5)
        
        return True
    
    def handle_button_click(self, button_index: int):
        """Handle button click actions."""
        actions = [
            lambda: self.load_solution(),
            lambda: self.start_animation() if not self.is_animating else None,
            lambda: self.reset_animation(),
            lambda: setattr(self, 'animation_speed', min(5.0, self.animation_speed + 0.5)),
            lambda: setattr(self, 'animation_speed', max(0.5, self.animation_speed - 0.5)),
            lambda: (self.reset_animation(), self.start_animation() if self.path else None)
        ]
        
        if button_index < len(actions):
            actions[button_index]()
    
    def run(self):
        """Main game loop."""
        print("╔══════════════════════════════════╗")
        print("║   Knight's Tour - Vintage GUI    ║")
        print("╚══════════════════════════════════╝")
        print("\n⌨ Controls:")
        print("  Space  : Start/Stop animation")
        print("  R      : Reset")
        print("  L      : Load solution")
        print("  +/-    : Adjust speed\n")
        
        running = True
        while running:
            running = self.handle_events()
            self.update_animation()
            
            # Render
            self.screen.fill(CREAM)
            self.draw_board()
            self.draw_path()
            self.draw_knight()
            self.draw_sidebar()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point."""
    try:
        gui = KnightTourGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\n✓ Program terminated by user")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()