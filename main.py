import pygame
import sys
import random
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLUE = (100, 150, 255)
GRAY = (128, 128, 128)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Music RPG Attack Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.show_title = True
        self.title_start_time = pygame.time.get_ticks()
        # Target date: January 16, 2026 at 3:50 (assuming 3:50 AM)
        self.target_date = datetime(2026, 1, 16, 3, 50, 0)
        self.show_time_up_message = False
        self.time_up_message_start = None
        # Achievements screen
        self.show_achievements = False
        # Track achievements
        self.achievements = {
            "win": {"name": "Win", "description": "Win a game", "unlocked": False},
            "pay_taxes": {"name": "Now you have to pay your taxes", "description": "Lose a game", "unlocked": False},
            "why": {"name": "Why", "description": "Win as the character", "unlocked": False},
            "tune_i_love": {"name": "That the tune i love", "description": "Win as Saxophone with under 50% health", "unlocked": False},
            "bird_plane": {"name": "It bird it a plane what nooooooo", "description": "Win without using super moves", "unlocked": False},
        }
        self.blocks_used = 0
        self.super_moves_used_this_battle = 0
        self.won_with_character = None
        # Character select screen
        self.show_character_select = False
        self.selected_character_index = 0
        self.characters = [
            # Flute: Fastest speed, lowest weight (low HP, low damage)
            {"name": "Flute", "color": WHITE, "image": None, "speed": 10, "weight": 1, "base_hp": 70, "base_damage": 6},
            # Clarinet: Fast speed, low weight (low-medium HP, low-medium damage)
            {"name": "Clarinet", "color": GOLD, "image": "yamaha-CSG-A-clarinet-hamilton_184d3b00-c2f5-49a5-8878-546cc1516648.webp", "speed": 8, "weight": 2, "base_hp": 80, "base_damage": 7},
            # Saxophone: Medium speed, medium weight (medium HP, medium damage)
            {"name": "Saxophone", "color": BLUE, "image": "61Sax-cOyBL._AC_UF894,1000_QL80_.jpg", "speed": 6, "weight": 4, "base_hp": 90, "base_damage": 8},
            # Trombone: Slow speed, high weight (high HP, high damage)
            {"name": "Trombone", "color": GOLD, "image": None, "speed": 4, "weight": 6, "base_hp": 110, "base_damage": 10},
            # Baritone: Very slow speed, very high weight (very high HP, very high damage)
            {"name": "Baritone", "color": WHITE, "image": "BR12LBaritonefront_1445x.webp", "speed": 3, "weight": 8, "base_hp": 120, "base_damage": 11},
            # Tuba: Slowest speed, highest weight (highest HP, highest damage)
            {"name": "Tuba", "color": BLUE, "image": None, "speed": 2, "weight": 10, "base_hp": 130, "base_damage": 12},
            # Mafeoso: Unlocked character (high HP and damage, mysterious character)
            {"name": "Mafeoso", "color": GOLD, "image": None, "speed": 7, "weight": 5, "base_hp": 200, "base_damage": 14, "unlocked": False},
        ]
        self.selected_character = None
        # Try to load character images
        self.character_images = {}
        self.load_character_images()
        # NPC selection
        self.show_npc_select = False
        self.selected_npc_index = 0
        self.selected_npc = None
        # Difficulty selection
        self.show_difficulty_select = False
        self.selected_difficulty_index = 0
        self.difficulties = ["Easy", "Medium", "Hard", "Expert", "Teacher Mode"]
        self.selected_difficulty = None
        # Teacher Mode - NPC learning system
        self.teacher_mode = False
        self.teacher_battle_count = 0
        self.teacher_max_battles = 3
        self.learned_player_patterns = {
            "preferred_moves": {"attack": 0, "block": 0, "super": 0},
            "move_sequences": [],  # Track sequences of moves
            "health_thresholds": {"low": [], "medium": [], "high": []},  # What player does at different health levels
            "block_usage": 0,  # How often player blocks
            "super_usage": 0,  # How often player uses super
        }
        self.current_battle_moves = []  # Track moves in current battle
        # Battle state
        self.in_battle = False
        self.player_health = 100
        self.npc_health = 100
        self.player_turn = True
        self.battle_message = ""
        self.battle_message_timer = 0
        self.npc_thinking_time = 0
        self.npc_last_action_time = 0
        self.npc_next_reaction_time = 0
        self.show_move_selection = False
        self.selected_move_index = 0
        # Define 3 moves available to all characters
        self.moves = [
            {"name": "Normal Attack", "type": "attack", "damage_multiplier": 1.0, "description": "Standard attack"},
            {"name": "Block", "type": "block", "damage_multiplier": 0.0, "description": "Defend against next attack"},
            {"name": "Super", "type": "super", "damage_multiplier": 2.0, "description": "Answer music question for big damage"},
        ]
        # Multi-hit system for lighter instruments
        self.attack_hits = []  # List of hits to process
        self.current_hit_index = 0
        # NPC move system
        self.npc_move_selection = None
        self.npc_question_answer = ""
        self.npc_blocking = False
        # Music question system
        self.show_question = False
        self.current_question = None
        self.question_answer = ""
        self.question_correct = False
        # Block state
        self.player_blocking = False
        # Win/Lose state
        self.battle_over = False
        self.battle_result = None  # "win" or "lose"
        # Music notes for questions
        self.music_notes = ["C", "D", "E", "F", "G", "A", "B"]
        self.music_notes_sharp = ["C#", "D#", "F#", "G#", "A#"]
        self.all_notes = self.music_notes + self.music_notes_sharp
    
    def load_character_images(self):
        """Load character images if available"""
        for character in self.characters:
            if character["image"]:
                try:
                    img = pygame.image.load(character["image"])
                    # Scale image to fit character box
                    img = pygame.transform.scale(img, (120, 120))
                    self.character_images[character["name"]] = img
                except:
                    self.character_images[character["name"]] = None
            else:
                self.character_images[character["name"]] = None
    
    def draw_character_sprite(self, surface, x, y, width, height, character_name):
        """Draw a detailed sprite of a white person holding the instrument"""
        # Draw person (white figure)
        person_color = WHITE
        center_x = x + width // 2
        
        # Head (circle with better proportions)
        head_radius = 12
        head_y = y + 8
        pygame.draw.circle(surface, person_color, (center_x, head_y), head_radius)
        pygame.draw.circle(surface, BLACK, (center_x, head_y), head_radius, 1)
        
        # Body (trapezoid shape for better look)
        body_width_top = 25
        body_width_bottom = 30
        body_height = 35
        body_y = head_y + head_radius + 3
        body_top_x = center_x - body_width_top // 2
        body_bottom_x = center_x - body_width_bottom // 2
        # Draw body as polygon
        body_points = [
            (body_top_x, body_y),
            (body_top_x + body_width_top, body_y),
            (body_bottom_x + body_width_bottom, body_y + body_height),
            (body_bottom_x, body_y + body_height)
        ]
        pygame.draw.polygon(surface, person_color, body_points)
        pygame.draw.polygon(surface, BLACK, body_points, 1)
        
        # Arms (more natural position)
        arm_width = 6
        arm_length = 22
        arm_y = body_y + 8
        
        # Left arm (holding instrument)
        left_arm_x = body_top_x - arm_length + 5
        pygame.draw.rect(surface, person_color, (left_arm_x, arm_y, arm_length, arm_width))
        pygame.draw.rect(surface, BLACK, (left_arm_x, arm_y, arm_length, arm_width), 1)
        
        # Right arm
        right_arm_x = body_top_x + body_width_top - 5
        pygame.draw.rect(surface, person_color, (right_arm_x, arm_y, arm_length, arm_width))
        pygame.draw.rect(surface, BLACK, (right_arm_x, arm_y, arm_length, arm_width), 1)
        
        # Legs
        leg_width = 8
        leg_height = 25
        leg_y = body_y + body_height
        # Left leg
        left_leg_x = body_bottom_x + 6
        pygame.draw.rect(surface, person_color, (left_leg_x, leg_y, leg_width, leg_height))
        pygame.draw.rect(surface, BLACK, (left_leg_x, leg_y, leg_width, leg_height), 1)
        # Right leg
        right_leg_x = body_bottom_x + body_width_bottom - leg_width - 6
        pygame.draw.rect(surface, person_color, (right_leg_x, leg_y, leg_width, leg_height))
        pygame.draw.rect(surface, BLACK, (right_leg_x, leg_y, leg_width, leg_height), 1)
        
        # Draw detailed instrument based on character
        instrument_color = GOLD
        instrument_dark = (200, 150, 0)  # Darker gold for shading
        
        if character_name == "Clarinet":
            # Clarinet - long vertical tube with keys
            clarinet_x = center_x
            clarinet_y_start = arm_y + 3
            clarinet_y_end = y + height - 5
            clarinet_length = clarinet_y_end - clarinet_y_start
            
            # Main body (thick line)
            pygame.draw.line(surface, instrument_color, 
                           (clarinet_x, clarinet_y_start), 
                           (clarinet_x, clarinet_y_end), 5)
            # Keys (small circles along the body)
            for i in range(5):
                key_y = clarinet_y_start + (i * clarinet_length // 5) + 8
                pygame.draw.circle(surface, instrument_dark, (clarinet_x, key_y), 3)
            # Bell at bottom
            pygame.draw.circle(surface, instrument_color, (clarinet_x, clarinet_y_end), 6)
            pygame.draw.circle(surface, BLACK, (clarinet_x, clarinet_y_end), 6, 1)
            
        elif character_name == "Saxophone":
            # Saxophone - curved body with bell
            sax_x = center_x - 15
            sax_y = arm_y + 5
            
            # Curved body (using arc and lines)
            bell_x = sax_x + 25
            bell_y = sax_y + 35
            # Main tube
            pygame.draw.line(surface, instrument_color, (sax_x, sax_y), (bell_x, bell_y), 6)
            # Curved section
            pygame.draw.arc(surface, instrument_color, 
                          (sax_x - 5, sax_y + 15, 30, 25), 0.5, 2.5, 6)
            # Bell (flared)
            pygame.draw.ellipse(surface, instrument_color,
                              (bell_x - 8, bell_y - 5, 16, 10))
            pygame.draw.ellipse(surface, BLACK,
                              (bell_x - 8, bell_y - 5, 16, 10), 2)
            # Keys
            for i in range(4):
                key_x = sax_x + (i * 6)
                key_y = sax_y + 10 + (i * 4)
                pygame.draw.circle(surface, instrument_dark, (key_x, key_y), 2)
                
        elif character_name == "Flute":
            # Flute - horizontal tube with keys
            flute_y = arm_y + 3
            flute_x_start = left_arm_x + 5
            flute_x_end = right_arm_x + arm_length - 5
            flute_length = flute_x_end - flute_x_start
            
            # Main body
            pygame.draw.line(surface, instrument_color,
                           (flute_x_start, flute_y),
                           (flute_x_end, flute_y), 4)
            # Keys along the body
            for i in range(6):
                key_x = flute_x_start + (i * flute_length // 6) + 5
                pygame.draw.circle(surface, instrument_dark, (key_x, flute_y), 2)
            # Mouthpiece
            pygame.draw.circle(surface, instrument_color, (flute_x_start, flute_y), 5)
            pygame.draw.circle(surface, BLACK, (flute_x_start, flute_y), 5, 1)
            
        elif character_name == "Trombone":
            # Trombone - slide with bell
            trombone_x = center_x
            trombone_y_start = arm_y + 5
            trombone_y_end = y + height - 8
            
            # Slide section (two parallel lines)
            slide_width = 8
            pygame.draw.line(surface, instrument_color,
                           (trombone_x - slide_width//2, trombone_y_start),
                           (trombone_x - slide_width//2, trombone_y_end - 15), 3)
            pygame.draw.line(surface, instrument_color,
                           (trombone_x + slide_width//2, trombone_y_start),
                           (trombone_x + slide_width//2, trombone_y_end - 15), 3)
            # Bell
            bell_y = trombone_y_end - 15
            pygame.draw.ellipse(surface, instrument_color,
                              (trombone_x - 12, bell_y - 8, 24, 16))
            pygame.draw.ellipse(surface, BLACK,
                              (trombone_x - 12, bell_y - 8, 24, 16), 2)
            # Mouthpiece
            pygame.draw.circle(surface, instrument_dark, (trombone_x, trombone_y_start), 4)
            
        elif character_name == "Baritone":
            # Baritone - large brass with valves
            baritone_x = center_x
            baritone_y = arm_y + 8
            
            # Main body (large tube)
            body_start_y = baritone_y
            body_end_y = y + height - 10
            pygame.draw.line(surface, instrument_color,
                           (baritone_x, body_start_y),
                           (baritone_x, body_end_y - 20), 8)
            # Bell (large and flared)
            bell_y = body_end_y - 20
            pygame.draw.ellipse(surface, instrument_color,
                              (baritone_x - 18, bell_y - 12, 36, 24))
            pygame.draw.ellipse(surface, BLACK,
                              (baritone_x - 18, bell_y - 12, 36, 24), 2)
            # Valves (three circles)
            for i in range(3):
                valve_x = baritone_x - 8 + (i * 8)
                valve_y = body_start_y + 15
                pygame.draw.circle(surface, instrument_dark, (valve_x, valve_y), 4)
                pygame.draw.circle(surface, BLACK, (valve_x, valve_y), 4, 1)
            # Mouthpiece
            pygame.draw.circle(surface, instrument_dark, (baritone_x, body_start_y), 5)
            
        elif character_name == "Tuba":
            # Tuba - largest, bell pointing up
            tuba_x = center_x
            tuba_y = arm_y - 5
            
            # Large bell at top (pointing up)
            bell_y = tuba_y
            pygame.draw.ellipse(surface, instrument_color,
                              (tuba_x - 22, bell_y - 15, 44, 30))
            pygame.draw.ellipse(surface, BLACK,
                              (tuba_x - 22, bell_y - 15, 44, 30), 2)
            # Main body (very thick)
            body_start_y = bell_y + 10
            body_end_y = y + height - 8
            pygame.draw.line(surface, instrument_color,
                           (tuba_x, body_start_y),
                           (tuba_x, body_end_y - 25), 10)
            # Large bell at bottom
            bottom_bell_y = body_end_y - 25
            pygame.draw.ellipse(surface, instrument_color,
                              (tuba_x - 20, bottom_bell_y - 10, 40, 20))
            pygame.draw.ellipse(surface, BLACK,
                              (tuba_x - 20, bottom_bell_y - 10, 40, 20), 2)
            # Valves (four circles, larger)
            for i in range(4):
                valve_x = tuba_x - 12 + (i * 8)
                valve_y = body_start_y + 20
                pygame.draw.circle(surface, instrument_dark, (valve_x, valve_y), 5)
                pygame.draw.circle(surface, BLACK, (valve_x, valve_y), 5, 1)
            # Mouthpiece
            pygame.draw.circle(surface, instrument_dark, (tuba_x, body_start_y), 6)
        elif character_name == "Mafeoso":
            # Mafeoso - mysterious character with fedora and golden saxophone
            # Draw fedora (black hat)
            fedora_x = center_x
            fedora_y = head_y - 5
            # Fedora brim
            pygame.draw.ellipse(surface, BLACK,
                              (fedora_x - 18, fedora_y - 3, 36, 8))
            # Fedora crown
            pygame.draw.ellipse(surface, BLACK,
                              (fedora_x - 12, fedora_y - 8, 24, 10))
            # Fedora top
            pygame.draw.ellipse(surface, (30, 30, 30),
                              (fedora_x - 10, fedora_y - 10, 20, 6))
            
            # Draw suit (black suit with tie) - shorter, more proportional
            # Suit jacket (stops at waist, doesn't go all the way down)
            suit_top_y = head_y + 15
            # Calculate where body ends (before legs start) - use approximate position
            # Legs typically start around 70% down the sprite height
            suit_bottom_y = y + int(height * 0.7)  # Stop around waist/hip level
            # Left side of suit jacket
            pygame.draw.rect(surface, BLACK,
                           (center_x - 25, suit_top_y, 20, suit_bottom_y - suit_top_y))
            # Right side of suit jacket
            pygame.draw.rect(surface, BLACK,
                           (center_x + 5, suit_top_y, 20, suit_bottom_y - suit_top_y))
            # Tie (vertical line, shorter)
            pygame.draw.line(surface, BLACK,
                           (center_x, suit_top_y + 5),
                           (center_x, suit_top_y + 20), 3)
            
            # Draw golden saxophone (held on the right side)
            sax_x = center_x + 20
            sax_y = arm_y + 5
            
            # Golden color for the instrument
            golden_color = (255, 215, 0)  # Gold
            golden_dark = (184, 134, 11)  # Dark goldenrod
            
            # Main curved body
            bell_x = sax_x + 20
            bell_y = sax_y + 30
            # Curved tube
            pygame.draw.line(surface, golden_color, (sax_x, sax_y), (bell_x, bell_y), 7)
            # Curved section (more pronounced)
            pygame.draw.arc(surface, golden_color, 
                          (sax_x - 8, sax_y + 12, 35, 28), 0.4, 2.6, 7)
            # Bell (flared, golden)
            pygame.draw.ellipse(surface, golden_color,
                              (bell_x - 10, bell_y - 6, 20, 12))
            pygame.draw.ellipse(surface, BLACK,
                              (bell_x - 10, bell_y - 6, 20, 12), 2)
            # Mouthpiece (golden)
            pygame.draw.circle(surface, golden_dark, (sax_x, sax_y), 5)
            pygame.draw.circle(surface, BLACK, (sax_x, sax_y), 5, 1)
            # Keys (golden highlights)
            for i in range(4):
                key_x = sax_x + (i * 6)
                key_y = sax_y + 8 + (i * 4)
                pygame.draw.circle(surface, golden_dark, (key_x, key_y), 3)
                pygame.draw.circle(surface, BLACK, (key_x, key_y), 3, 1)
        
    def get_countdown_text(self):
        """Calculate and format the countdown timer"""
        now = datetime.now()
        time_remaining = self.target_date - now
        
        if time_remaining.total_seconds() <= 0:
            # Time is up - trigger the message display
            if not self.show_time_up_message:
                self.show_time_up_message = True
                self.time_up_message_start = pygame.time.get_ticks()
            return "Time's up!"
        
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"
    
    def show_title_screen(self):
        """Display the title screen"""
        self.screen.fill(BLACK)
        
        # Check if we should show the "time's up" message
        if self.show_time_up_message:
            # Show the message for 5 minutes (300000 milliseconds)
            message_elapsed = pygame.time.get_ticks() - self.time_up_message_start
            if message_elapsed < 300000:  # 5 minutes = 300000 ms
                # Display the time's up message (split into two lines)
                message_line1 = "holy fuck it the end of the 1st"
                message_line2 = "half of school"
                message_display1 = self.font_large.render(message_line1, True, GOLD)
                message_display2 = self.font_large.render(message_line2, True, GOLD)
                message_rect1 = message_display1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
                message_rect2 = message_display2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                self.screen.blit(message_display1, message_rect1)
                self.screen.blit(message_display2, message_rect2)
                pygame.display.flip()
                return
            else:
                # 5 minutes have passed, allow game to continue
                self.show_time_up_message = False
        
        # Title text
        title_text = self.font_large.render("Music RPG Attack Game", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Countdown timer
        countdown_text = self.get_countdown_text()
        timer_display = self.font_medium.render(countdown_text, True, WHITE)
        timer_rect = timer_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(timer_display, timer_rect)
        
        # Target date display
        target_text = self.font_small.render("Target: 1/16/2026 3:50", True, WHITE)
        target_rect = target_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(target_text, target_rect)
        
        # Start button and Achievements button (appears after 1 second)
        elapsed = pygame.time.get_ticks() - self.title_start_time
        if elapsed > 1000:
            # Start button
            start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 40)
            pygame.draw.rect(self.screen, (50, 50, 50), start_button)
            pygame.draw.rect(self.screen, GOLD, start_button, 2)
            start_text = self.font_medium.render("Start", True, GOLD)
            start_text_rect = start_text.get_rect(center=start_button.center)
            self.screen.blit(start_text, start_text_rect)
            
            # Achievements button
            achievements_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 40)
            pygame.draw.rect(self.screen, (50, 50, 50), achievements_button)
            pygame.draw.rect(self.screen, GOLD, achievements_button, 2)
            achievements_text = self.font_medium.render("Achievements", True, GOLD)
            achievements_text_rect = achievements_text.get_rect(center=achievements_button.center)
            self.screen.blit(achievements_text, achievements_text_rect)
        
        pygame.display.flip()
    
    def handle_title_input(self, event):
        """Handle input on title screen"""
        # Don't allow skipping if the time's up message is showing
        if self.show_time_up_message:
            return
        
        elapsed = pygame.time.get_ticks() - self.title_start_time
        if elapsed > 1000:  # Only allow input after 1 second
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if start button was clicked
                start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 40)
                if start_button.collidepoint(mouse_x, mouse_y):
                    self.show_title = False
                    self.show_character_select = True
                # Check if achievements button was clicked
                achievements_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 40)
                elif achievements_button.collidepoint(mouse_x, mouse_y):
                    # Click achievements button to open
                    self.show_achievements = True
                    self.show_title = False
    
    def show_character_select_screen(self):
        """Display the character select screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("Select Character", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Display characters in a grid (2 rows, 3 columns)
        char_width = 180
        char_height = 200
        chars_per_row = 3
        spacing_x = 20
        spacing_y = 20
        start_x = (SCREEN_WIDTH - (chars_per_row * char_width + (chars_per_row - 1) * spacing_x)) // 2
        start_y = 120
        
        for i, character in enumerate(self.characters):
            # Check if character is unlocked (Mafeoso starts locked)
            if character.get("unlocked", True) == False:
                # Show locked character (grayed out)
                row = i // chars_per_row
                col = i % chars_per_row
                x = start_x + col * (char_width + spacing_x)
                y = start_y + row * (char_height + spacing_y)
                
                # Locked character box
                pygame.draw.rect(self.screen, (20, 20, 20), 
                               (x, y, char_width, char_height + 50))
                pygame.draw.rect(self.screen, GRAY, 
                               (x, y, char_width, char_height + 50), 2)
                
                # Draw character sprite (grayed out)
                self.draw_character_sprite(self.screen, x + 10, y + 10, 
                                           char_width - 20, char_height - 30, 
                                           character["name"])
                
                # Draw dark overlay to gray out the character
                overlay = pygame.Surface((char_width - 20, char_height - 30))
                overlay.set_alpha(150)  # Semi-transparent dark overlay
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (x + 10, y + 10))
                
                # Draw lock overlay
                # Lock icon/text
                lock_text = self.font_medium.render("LOCKED", True, WHITE)
                lock_rect = lock_text.get_rect(center=(x + char_width // 2, y + char_height // 2))
                self.screen.blit(lock_text, lock_rect)
                
                # Draw a simple lock symbol on top
                # Lock body
                pygame.draw.rect(self.screen, WHITE, (x + char_width // 2 - 12, y + char_height // 2 + 15, 24, 20), 2)
                # Lock shackle (arc)
                pygame.draw.arc(self.screen, WHITE, (x + char_width // 2 - 12, y + char_height // 2 + 5, 24, 18), 0, 3.14, 2)
                
                # Character name (grayed)
                name_text = self.font_medium.render(character["name"], True, GRAY)
                name_rect = name_text.get_rect(center=(x + char_width // 2, y + char_height + 15))
                self.screen.blit(name_text, name_rect)
                
                locked_text = self.font_small.render("LOCKED", True, GRAY)
                locked_rect = locked_text.get_rect(center=(x + char_width // 2, y + char_height + 35))
                self.screen.blit(locked_text, locked_rect)
                continue
            
            row = i // chars_per_row
            col = i % chars_per_row
            x = start_x + col * (char_width + spacing_x)
            y = start_y + row * (char_height + spacing_y)
            
            # Highlight selected character
            if i == self.selected_character_index:
                # Draw selection border
                pygame.draw.rect(self.screen, GOLD, 
                               (x - 5, y - 5, char_width, char_height + 50), 4)
                bg_color = (50, 50, 50)
            else:
                bg_color = (30, 30, 30)
            
            # Character box background (taller to fit stats)
            pygame.draw.rect(self.screen, bg_color, 
                           (x, y, char_width, char_height + 50))
            
            # Draw character sprite (white person holding instrument)
            sprite_area = pygame.Rect(x + 10, y + 10, char_width - 20, char_height - 30)
            self.draw_character_sprite(self.screen, x + 10, y + 10, 
                                       char_width - 20, char_height - 30, 
                                       character["name"])
            
            # Character name
            name_text = self.font_medium.render(character["name"], True, character["color"])
            name_rect = name_text.get_rect(center=(x + char_width // 2, y + char_height + 15))
            self.screen.blit(name_text, name_rect)
            
            # Stats display
            stats_text = self.font_small.render(
                f"Spd:{character['speed']} Wgt:{character['weight']} HP:{character['base_hp']} DMG:{character['base_damage']}", 
                True, GRAY
            )
            stats_rect = stats_text.get_rect(center=(x + char_width // 2, y + char_height + 35))
            self.screen.blit(stats_text, stats_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Arrow Keys: Navigate | Enter: Select", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def show_achievements_screen(self):
        """Display the achievements screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("Achievements", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Display achievements
        y_offset = 120
        spacing = 60
        
        for i, (key, achievement) in enumerate(self.achievements.items()):
            achievement_y = y_offset + (i * spacing)
            
            # Achievement name and status
            if achievement["unlocked"]:
                status_text = "✓ UNLOCKED"
                status_color = GOLD
                name_color = WHITE
            else:
                status_text = "LOCKED"
                status_color = GRAY
                name_color = GRAY
            
            # Achievement name
            name_display = self.font_medium.render(achievement["name"], True, name_color)
            name_rect = name_display.get_rect(left=100, top=achievement_y)
            self.screen.blit(name_display, name_rect)
            
            # Status
            status_display = self.font_small.render(status_text, True, status_color)
            status_rect = status_display.get_rect(right=SCREEN_WIDTH - 100, top=achievement_y + 5)
            self.screen.blit(status_display, status_rect)
            
            # Description
            desc_display = self.font_small.render(achievement["description"], True, GRAY)
            desc_rect = desc_display.get_rect(left=100, top=achievement_y + 30)
            self.screen.blit(desc_display, desc_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Press ESC or click to return to title", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def handle_achievements_input(self, event):
        """Handle input on achievements screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_achievements = False
                self.show_title = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click anywhere to return
            self.show_achievements = False
            self.show_title = True
    
    def handle_character_select_input(self, event):
        """Handle input on character select screen"""
        if event.type == pygame.KEYDOWN:
            chars_per_row = 3
            if event.key == pygame.K_LEFT:
                # Skip locked characters when moving left
                new_index = (self.selected_character_index - 1) % len(self.characters)
                while new_index != self.selected_character_index and self.characters[new_index].get("unlocked", True) == False:
                    new_index = (new_index - 1) % len(self.characters)
                self.selected_character_index = new_index
            elif event.key == pygame.K_RIGHT:
                # Skip locked characters when moving right
                new_index = (self.selected_character_index + 1) % len(self.characters)
                while new_index != self.selected_character_index and self.characters[new_index].get("unlocked", True) == False:
                    new_index = (new_index + 1) % len(self.characters)
                self.selected_character_index = new_index
            elif event.key == pygame.K_UP:
                # Move up one row
                new_index = self.selected_character_index - chars_per_row
                if new_index >= 0:
                    # Skip locked characters
                    while new_index >= 0 and self.characters[new_index].get("unlocked", True) == False:
                        new_index -= 1
                    if new_index >= 0:
                        self.selected_character_index = new_index
            elif event.key == pygame.K_DOWN:
                # Move down one row
                new_index = self.selected_character_index + chars_per_row
                if new_index < len(self.characters):
                    # Skip locked characters
                    while new_index < len(self.characters) and self.characters[new_index].get("unlocked", True) == False:
                        new_index += 1
                    if new_index < len(self.characters):
                        self.selected_character_index = new_index
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Character selected, check if unlocked
                if self.characters[self.selected_character_index].get("unlocked", True) != False:
                    self.selected_character = self.characters[self.selected_character_index]
                    self.show_character_select = False
                    self.show_npc_select = True
                    self.selected_npc_index = 0
    
    def show_npc_select_screen(self):
        """Display the NPC character select screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("Select NPC Character", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Display characters in a grid (2 rows, 3 columns)
        char_width = 180
        char_height = 200
        chars_per_row = 3
        spacing_x = 20
        spacing_y = 20
        start_x = (SCREEN_WIDTH - (chars_per_row * char_width + (chars_per_row - 1) * spacing_x)) // 2
        start_y = 120
        
        for i, character in enumerate(self.characters):
            row = i // chars_per_row
            col = i % chars_per_row
            x = start_x + col * (char_width + spacing_x)
            y = start_y + row * (char_height + spacing_y)
            
            # Highlight selected character
            if i == self.selected_npc_index:
                # Draw selection border
                pygame.draw.rect(self.screen, GOLD, 
                               (x - 5, y - 5, char_width, char_height + 50), 4)
                bg_color = (50, 50, 50)
            else:
                bg_color = (30, 30, 30)
            
            # Character box background (taller to fit stats)
            pygame.draw.rect(self.screen, bg_color, 
                           (x, y, char_width, char_height + 50))
            
            # Draw character sprite (white person holding instrument)
            self.draw_character_sprite(self.screen, x + 10, y + 10, 
                                       char_width - 20, char_height - 30, 
                                       character["name"])
            
            # Character name
            name_text = self.font_medium.render(character["name"], True, character["color"])
            name_rect = name_text.get_rect(center=(x + char_width // 2, y + char_height + 15))
            self.screen.blit(name_text, name_rect)
            
            # Stats display
            stats_text = self.font_small.render(
                f"Spd:{character['speed']} Wgt:{character['weight']} HP:{character['base_hp']} DMG:{character['base_damage']}", 
                True, GRAY
            )
            stats_rect = stats_text.get_rect(center=(x + char_width // 2, y + char_height + 35))
            self.screen.blit(stats_text, stats_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Arrow Keys: Navigate | Enter: Select", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def handle_npc_select_input(self, event):
        """Handle input on NPC select screen"""
        if event.type == pygame.KEYDOWN:
            chars_per_row = 3
            if event.key == pygame.K_LEFT:
                self.selected_npc_index = (self.selected_npc_index - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_npc_index = (self.selected_npc_index + 1) % len(self.characters)
            elif event.key == pygame.K_UP:
                new_index = self.selected_npc_index - chars_per_row
                if new_index >= 0:
                    self.selected_npc_index = new_index
            elif event.key == pygame.K_DOWN:
                new_index = self.selected_npc_index + chars_per_row
                if new_index < len(self.characters):
                    self.selected_npc_index = new_index
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # NPC selected, move to difficulty selection
                self.selected_npc = self.characters[self.selected_npc_index]
                self.show_npc_select = False
                self.show_difficulty_select = True
                self.selected_difficulty_index = 0
    
    def show_difficulty_select_screen(self):
        """Display the difficulty selection screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("Select Difficulty", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Display difficulty options
        option_height = 60
        start_y = 250
        spacing = 20
        
        for i, difficulty in enumerate(self.difficulties):
            y = start_y + i * (option_height + spacing)
            
            # Highlight selected difficulty
            if i == self.selected_difficulty_index:
                pygame.draw.rect(self.screen, GOLD, 
                               (SCREEN_WIDTH // 2 - 150, y - 5, 300, option_height), 4)
                bg_color = (50, 50, 50)
            else:
                bg_color = (30, 30, 30)
            
            # Difficulty box background
            pygame.draw.rect(self.screen, bg_color, 
                           (SCREEN_WIDTH // 2 - 150, y, 300, option_height))
            
            # Difficulty name
            diff_text = self.font_medium.render(difficulty, True, WHITE)
            diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, y + option_height // 2))
            self.screen.blit(diff_text, diff_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Arrow Keys: Navigate | Enter: Select", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def handle_difficulty_select_input(self, event):
        """Handle input on difficulty select screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_difficulty_index = (self.selected_difficulty_index - 1) % len(self.difficulties)
            elif event.key == pygame.K_DOWN:
                self.selected_difficulty_index = (self.selected_difficulty_index + 1) % len(self.difficulties)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Difficulty selected, start battle
                self.selected_difficulty = self.difficulties[self.selected_difficulty_index]
                self.teacher_mode = (self.selected_difficulty_index == 4)  # Teacher Mode is index 4
                if self.teacher_mode:
                    # Initialize teacher mode
                    self.teacher_battle_count = 0
                    self.learned_player_patterns = {
                        "preferred_moves": {"attack": 0, "block": 0, "super": 0},
                        "move_sequences": [],
                        "health_thresholds": {"low": [], "medium": [], "high": []},
                        "block_usage": 0,
                        "super_usage": 0,
                    }
                self.show_difficulty_select = False
                self.in_battle = True
                # Set health based on character stats
                self.player_health = self.selected_character["base_hp"]
                self.player_max_health = self.selected_character["base_hp"]
                self.npc_health = self.selected_npc["base_hp"]
                self.npc_max_health = self.selected_npc["base_hp"]
                # Determine turn order based on speed (higher speed goes first)
                if self.selected_character["speed"] >= self.selected_npc["speed"]:
                    self.player_turn = True
                else:
                    self.player_turn = False
                if self.teacher_mode:
                    self.battle_message = f"Teacher Mode: Battle 1/3 - NPC is learning..."
                else:
                    self.battle_message = "Battle Start!"
                self.battle_message_timer = pygame.time.get_ticks()
                self.npc_last_action_time = pygame.time.get_ticks()
                self.npc_next_reaction_time = 0
                self.current_battle_moves = []
                self.npc_blocking = False
    
    def show_battle_screen(self):
        """Display the battle screen with green map"""
        # Green background (battle map)
        self.screen.fill(GREEN)
        
        # Draw some grass pattern/texture
        for x in range(0, SCREEN_WIDTH, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.circle(self.screen, DARK_GREEN, (x, y), 2)
        
        # Player character on left side
        player_x = 150
        player_y = SCREEN_HEIGHT // 2
        self.draw_character_sprite(self.screen, player_x - 50, player_y - 100, 100, 200, 
                                   self.selected_character["name"])
        
        # Player health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 50
        health_bar_y = 50
        # Background
        pygame.draw.rect(self.screen, BLACK, 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        # Health
        health_width = int((self.player_health / self.player_max_health) * health_bar_width)
        pygame.draw.rect(self.screen, RED, 
                        (health_bar_x, health_bar_y, health_width, health_bar_height))
        # Border
        pygame.draw.rect(self.screen, WHITE, 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        # Health text
        health_text = self.font_small.render(f"Player: {self.player_health}/{self.player_max_health}", True, WHITE)
        self.screen.blit(health_text, (health_bar_x, health_bar_y - 25))
        # Speed and weight info
        stats_text = self.font_small.render(f"Speed: {self.selected_character['speed']} | Weight: {self.selected_character['weight']}", True, WHITE)
        self.screen.blit(stats_text, (health_bar_x, health_bar_y - 50))
        
        # NPC character on right side
        npc_x = SCREEN_WIDTH - 150
        npc_y = SCREEN_HEIGHT // 2
        self.draw_character_sprite(self.screen, npc_x - 50, npc_y - 100, 100, 200, 
                                   self.selected_npc["name"])
        
        # NPC health bar
        npc_health_bar_x = SCREEN_WIDTH - 250
        npc_health_bar_y = 50
        # Background
        pygame.draw.rect(self.screen, BLACK, 
                        (npc_health_bar_x, npc_health_bar_y, health_bar_width, health_bar_height))
        # Health
        npc_health_width = int((self.npc_health / self.npc_max_health) * health_bar_width)
        pygame.draw.rect(self.screen, RED, 
                        (npc_health_bar_x, npc_health_bar_y, npc_health_width, health_bar_height))
        # Border
        pygame.draw.rect(self.screen, WHITE, 
                        (npc_health_bar_x, npc_health_bar_y, health_bar_width, health_bar_height), 2)
        # Health text
        npc_health_text = self.font_small.render(f"NPC: {self.npc_health}/{self.npc_max_health}", True, WHITE)
        self.screen.blit(npc_health_text, (npc_health_bar_x, npc_health_bar_y - 25))
        # Speed and weight info
        npc_stats_text = self.font_small.render(f"Speed: {self.selected_npc['speed']} | Weight: {self.selected_npc['weight']}", True, WHITE)
        self.screen.blit(npc_stats_text, (npc_health_bar_x, npc_health_bar_y - 50))
        
        # Show win/lose screen
        if self.battle_over:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.battle_result == "win":
                result_text = self.font_large.render("YOU WIN!", True, GOLD)
            else:
                result_text = self.font_large.render("YOU LOSE!", True, RED)
            
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(result_text, result_rect)
            
            # Teacher mode progress
            if self.teacher_mode:
                progress_text = self.font_medium.render(
                    f"Teacher Mode: Battle {self.teacher_battle_count + 1}/{self.teacher_max_battles}",
                    True, WHITE
                )
                progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(progress_text, progress_rect)
                
                if self.teacher_battle_count < self.teacher_max_battles - 1:
                    restart_text = self.font_medium.render("Press Enter to continue learning...", True, WHITE)
                else:
                    restart_text = self.font_medium.render("Press Enter to finish learning", True, WHITE)
            else:
                restart_text = self.font_medium.render("Press Enter to return to character select", True, WHITE)
            
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
            pygame.display.flip()
            return
        
        # Show music question screen
        if self.show_question and self.current_question:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Question box (larger to fit staff)
            question_box = pygame.Rect(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 200, 700, 400)
            pygame.draw.rect(self.screen, (30, 30, 30), question_box)
            pygame.draw.rect(self.screen, GOLD, question_box, 4)
            
            # Question text
            question_title = self.font_medium.render("SUPER MOVE - Music Question", True, GOLD)
            title_rect = question_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170))
            self.screen.blit(question_title, title_rect)
            
            question_text = self.font_medium.render(self.current_question["question"], True, WHITE)
            q_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
            self.screen.blit(question_text, q_rect)
            
            # Draw musical staff
            staff_y = SCREEN_HEIGHT // 2 - 60
            staff_x_start = SCREEN_WIDTH // 2 - 250
            staff_x_end = SCREEN_WIDTH // 2 + 250
            staff_width = staff_x_end - staff_x_start
            line_spacing = 12
            
            # Draw 5 staff lines
            for i in range(5):
                line_y = staff_y + (i * line_spacing)
                pygame.draw.line(self.screen, WHITE, 
                               (staff_x_start, line_y), 
                               (staff_x_end, line_y), 2)
            
            # Draw clef symbol (text representation)
            clef_x = staff_x_start + 30
            clef_label = "Treble" if self.current_question["clef"] == "treble" else "Bass"
            clef_display = self.font_small.render(clef_label, True, WHITE)
            self.screen.blit(clef_display, (clef_x - 15, staff_y - 20))
            
            # Draw notes on staff
            if "notes" in self.current_question:
                note_spacing = staff_width // (len(self.current_question["notes"]) + 2)
                note_start_x = staff_x_start + 100
                
                for i, note in enumerate(self.current_question["notes"]):
                    note_x = note_start_x + (i * note_spacing)
                    position = self.get_note_position_on_staff(note, self.current_question["clef"])
                    
                    # Calculate note Y position (0 = top line, higher = lower on staff)
                    note_y = staff_y + (position * (line_spacing // 2))
                    
                    # Draw note (circle)
                    note_radius = 8
                    pygame.draw.circle(self.screen, WHITE, (note_x, note_y), note_radius)
                    pygame.draw.circle(self.screen, BLACK, (note_x, note_y), note_radius, 2)
                    
                    # Draw note stem
                    stem_length = 25
                    if position < 4:  # Notes above middle line, stem down
                        pygame.draw.line(self.screen, WHITE, 
                                       (note_x + note_radius, note_y), 
                                       (note_x + note_radius, note_y + stem_length), 2)
                    else:  # Notes below middle line, stem up
                        pygame.draw.line(self.screen, WHITE, 
                                       (note_x + note_radius, note_y), 
                                       (note_x + note_radius, note_y - stem_length), 2)
                    
                    # Circle the target note (no letter labels - all whited out)
                    if i == self.current_question["circled_index"]:
                        circle_radius = note_radius + 15
                        pygame.draw.circle(self.screen, GOLD, (note_x, note_y), circle_radius, 3)
            
            # Answer input
            answer_label = self.font_small.render("Your answer:", True, WHITE)
            answer_label_rect = answer_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(answer_label, answer_label_rect)
            
            answer_display = self.font_medium.render(self.question_answer + "_", True, GOLD)
            answer_rect = answer_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
            self.screen.blit(answer_display, answer_rect)
            
            instruction_text = self.font_small.render("Type your answer (e.g., C, D, E) and press Enter", True, GRAY)
            inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            self.screen.blit(instruction_text, inst_rect)
            
            pygame.display.flip()
            return
        
        # Battle message
        if self.battle_message:
            message_text = self.font_medium.render(self.battle_message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            # Background for message
            pygame.draw.rect(self.screen, BLACK, 
                           (message_rect.x - 10, message_rect.y - 5, 
                            message_rect.width + 20, message_rect.height + 10))
            self.screen.blit(message_text, message_rect)
        
        # Teacher mode progress indicator
        if self.teacher_mode:
            teacher_text = self.font_small.render(
                f"Teacher Mode: Battle {self.teacher_battle_count + 1}/{self.teacher_max_battles} - NPC Learning...",
                True, BLUE
            )
            teacher_rect = teacher_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            self.screen.blit(teacher_text, teacher_rect)
        
        # Turn indicator or move selection
        if self.player_turn:
            if self.show_move_selection:
                # Show move selection menu
                move_menu_y = SCREEN_HEIGHT - 200
                menu_bg = pygame.Rect(SCREEN_WIDTH // 2 - 200, move_menu_y - 10, 400, 180)
                pygame.draw.rect(self.screen, (20, 20, 20), menu_bg)
                pygame.draw.rect(self.screen, GOLD, menu_bg, 3)
                
                move_title = self.font_medium.render("Select Move:", True, GOLD)
                title_rect = move_title.get_rect(center=(SCREEN_WIDTH // 2, move_menu_y))
                self.screen.blit(move_title, title_rect)
                
                for i, move in enumerate(self.moves):
                    move_y = move_menu_y + 30 + (i * 40)
                    if i == self.selected_move_index:
                        # Highlight selected move
                        highlight_rect = pygame.Rect(SCREEN_WIDTH // 2 - 190, move_y - 5, 380, 35)
                        pygame.draw.rect(self.screen, (50, 50, 50), highlight_rect)
                        pygame.draw.rect(self.screen, GOLD, highlight_rect, 2)
                        move_color = GOLD
                    else:
                        move_color = WHITE
                    
                    move_text = self.font_small.render(
                        f"{i+1}. {move['name']} - {move['description']}", True, move_color
                    )
                    move_rect = move_text.get_rect(center=(SCREEN_WIDTH // 2, move_y + 10))
                    self.screen.blit(move_text, move_rect)
                
                instruction_text = self.font_small.render("1/2/3 or Arrow Keys + Enter | ESC to cancel", True, WHITE)
                inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, move_menu_y + 150))
                self.screen.blit(instruction_text, inst_rect)
            else:
                turn_text = self.font_medium.render("Your Turn - Press SPACE to Select Move!", True, GOLD)
                turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                self.screen.blit(turn_text, turn_rect)
        else:
            turn_text = self.font_medium.render("NPC Turn...", True, BLUE)
            turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(turn_text, turn_rect)
        
        pygame.display.flip()
    
    def handle_battle_input(self, event):
        """Handle input during battle"""
        if event.type == pygame.KEYDOWN:
            # Handle win/lose screen
            if self.battle_over:
                if event.key == pygame.K_RETURN:
                    # Handle teacher mode
                    if self.teacher_mode:
                        self.teacher_battle_count += 1
                        # Save move sequence from this battle
                        if len(self.current_battle_moves) > 0:
                            self.learned_player_patterns["move_sequences"].append(self.current_battle_moves.copy())
                        
                        if self.teacher_battle_count < self.teacher_max_battles:
                            # Continue to next battle in teacher mode
                            self.in_battle = True
                            self.player_health = self.player_max_health
                            self.npc_health = self.npc_max_health
                            self.battle_over = False
                            self.battle_result = None
                            self.player_turn = True
                            self.player_blocking = False
                            self.npc_blocking = False
                            self.battle_message = f"Teacher Mode: Battle {self.teacher_battle_count + 1}/3 - Learning in progress..."
                            self.battle_message_timer = pygame.time.get_ticks()
                            self.npc_last_action_time = pygame.time.get_ticks()
                            self.npc_next_reaction_time = 0
                            self.current_battle_moves = []
                            return
                        else:
                            # All 3 battles done, NPC has learned
                            self.battle_message = "Teacher Mode Complete! NPC has learned your strategies!"
                            self.battle_message_timer = pygame.time.get_ticks()
                    
                    # Go back to character select screen
                    self.in_battle = False
                    self.battle_over = False
                    self.battle_result = None
                    self.show_character_select = True
                    self.selected_character_index = 0
                    self.selected_character = None
                    self.selected_npc = None
                    self.selected_difficulty = None
                    self.show_move_selection = False
                    self.show_question = False
                    self.player_blocking = False
                    self.teacher_mode = False
                    self.teacher_battle_count = 0
                return
            
            # Handle music question
            if self.show_question:
                if event.key == pygame.K_RETURN:
                    # Check answer
                    user_answer = self.question_answer.strip().upper()
                    correct_answer = self.current_question["answer"].upper()
                    
                    if user_answer == correct_answer:
                        self.question_correct = True
                        # Deal super damage
                        base_damage = self.selected_character["base_damage"]
                        damage = int(base_damage * self.moves[2]["damage_multiplier"])
                        self.npc_health = max(0, self.npc_health - damage)
                        self.battle_message = f"Correct! Super move deals {damage} damage!"
                        
                        # Check if NPC is defeated
                        if self.npc_health <= 0:
                            self.battle_over = True
                            self.battle_result = "win"
                            self.battle_message = "You Win!"
                            self.battle_message_timer = pygame.time.get_ticks()
                            self.check_win_achievements()
                    else:
                        self.question_correct = False
                        self.battle_message = f"Wrong! The answer was {correct_answer}. No damage dealt."
                    
                    self.show_question = False
                    self.current_question = None
                    self.question_answer = ""
                    self.battle_message_timer = pygame.time.get_ticks()
                    self.player_turn = False
                    self.npc_last_action_time = pygame.time.get_ticks()
                    self.npc_next_reaction_time = 0
                elif event.key == pygame.K_BACKSPACE:
                    # Delete last character
                    self.question_answer = self.question_answer[:-1]
                else:
                    # Add character to answer
                    if event.unicode.isalnum() or event.unicode == '#':
                        self.question_answer += event.unicode
                return
            
            # Normal battle input
            if self.player_turn:
                if not self.show_move_selection:
                    # Show move selection when player presses space
                    if event.key == pygame.K_SPACE:
                        self.show_move_selection = True
                        self.selected_move_index = 0
                else:
                    # Move selection is active
                    if event.key == pygame.K_UP:
                        self.selected_move_index = (self.selected_move_index - 1) % len(self.moves)
                    elif event.key == pygame.K_DOWN:
                        self.selected_move_index = (self.selected_move_index + 1) % len(self.moves)
                    elif event.key == pygame.K_1:
                        self.selected_move_index = 0
                        self.execute_player_move()
                    elif event.key == pygame.K_2:
                        self.selected_move_index = 1
                        self.execute_player_move()
                    elif event.key == pygame.K_3:
                        self.selected_move_index = 2
                        self.execute_player_move()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Execute selected move
                        self.execute_player_move()
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel move selection
                        self.show_move_selection = False
    
    def get_clef_for_instrument(self, instrument_name):
        """Get the appropriate clef for the instrument"""
        # Treble clef for higher instruments
        if instrument_name in ["Flute", "Clarinet", "Saxophone"]:
            return "treble"
        # Bass clef for lower instruments
        elif instrument_name in ["Tuba", "Baritone", "Trombone"]:
            return "bass"
        # Default to treble
        return "treble"
    
    def get_note_position_on_staff(self, note, clef):
        """Get the vertical position of a note on the staff (0-8 for lines/spaces)"""
        # Note positions: C, D, E, F, G, A, B, C (next octave)
        note_positions = {
            "C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6,
            "C#": 0, "D#": 1, "F#": 3, "G#": 4, "A#": 5
        }
        
        base_note = note.replace("#", "")
        position = note_positions.get(note, note_positions.get(base_note, 0))
        
        # Adjust for clef (bass clef starts lower)
        if clef == "bass":
            position += 2  # Shift down for bass clef
        
        return position
    
    def generate_music_question(self):
        """Generate a music question showing a staff with a circled note"""
        # Get clef based on player's instrument
        clef = self.get_clef_for_instrument(self.selected_character["name"])
        
        # Choose a random note
        note = random.choice(self.music_notes)  # Use basic notes for simplicity
        
        # Generate 3-5 notes on the staff, with the target note circled
        num_notes = random.randint(3, 5)
        all_notes = random.sample(self.music_notes, min(num_notes, len(self.music_notes)))
        
        # Make sure our target note is in the list
        if note not in all_notes:
            all_notes[random.randint(0, len(all_notes) - 1)] = note
        
        # Find which position has the target note
        circled_index = all_notes.index(note)
        
        return {
            "type": "staff_note",
            "question": "What note is circled?",
            "notes": all_notes,
            "circled_index": circled_index,
            "answer": note.upper(),
            "clef": clef,
            "instrument": self.selected_character["name"]
        }
    
    def record_player_move(self, move_type):
        """Record player move for teacher mode learning and achievements"""
        # Track super moves for achievement
        if move_type == "super":
            self.super_moves_used_this_battle += 1
        
        if self.teacher_mode:
            self.current_battle_moves.append(move_type)
            self.learned_player_patterns["preferred_moves"][move_type] += 1
            
            # Record health level when move was used
            health_percent = self.player_health / self.player_max_health
            if health_percent < 0.33:
                health_level = "low"
            elif health_percent < 0.67:
                health_level = "medium"
            else:
                health_level = "high"
            
            self.learned_player_patterns["health_thresholds"][health_level].append(move_type)
            
            if move_type == "block":
                self.learned_player_patterns["block_usage"] += 1
            elif move_type == "super":
                self.learned_player_patterns["super_usage"] += 1
    
    def execute_player_move(self):
        """Execute the player's selected move"""
        selected_move = self.moves[self.selected_move_index]
        
        # Record move for teacher mode
        self.record_player_move(selected_move["type"])
        
        if selected_move["type"] == "block":
            # Block - defend against next attack
            self.player_blocking = True
            self.battle_message = "You prepare to block the next attack!"
            self.battle_message_timer = pygame.time.get_ticks()
            self.show_move_selection = False
            self.player_turn = False
            self.npc_last_action_time = pygame.time.get_ticks()
            self.npc_next_reaction_time = 0
        elif selected_move["type"] == "super":
            # Super - show music question
            self.show_move_selection = False
            self.show_question = True
            self.current_question = self.generate_music_question()
            self.question_answer = ""
            self.question_correct = False
        else:
            # Normal attack - calculate multi-hits for lighter instruments
            base_damage = self.selected_character["base_damage"]
            weight = self.selected_character["weight"]
            
            # Lighter instruments have chance for multiple hits
            # Weight 1-2: 2-3 hits possible
            # Weight 3-4: 1-2 hits possible  
            # Weight 5+: 1 hit (single strong attack)
            if weight <= 2:
                # Very light - 2-3 hits
                num_hits = random.randint(2, 3)
            elif weight <= 4:
                # Medium - 1-2 hits
                num_hits = random.randint(1, 2)
            else:
                # Heavy - 1 hit
                num_hits = 1
            
            # Calculate damage per hit (slightly reduced for multi-hits)
            damage_per_hit = int(base_damage * selected_move["damage_multiplier"])
            if num_hits > 1:
                # Multi-hits do slightly less damage per hit but more total
                damage_per_hit = int(damage_per_hit * 0.9)
            
            # Create list of hits to process
            self.attack_hits = []
            for i in range(num_hits):
                self.attack_hits.append({
                    "damage": damage_per_hit,
                    "hit_number": i + 1,
                    "total_hits": num_hits
                })
            
            self.current_hit_index = 0
            self.process_next_hit()
    
    def process_next_hit(self):
        """Process the next hit in a multi-hit attack (player)"""
        if self.current_hit_index < len(self.attack_hits):
            hit = self.attack_hits[self.current_hit_index]
            
            # Check if NPC is blocking
            if self.npc_blocking:
                damage = max(1, int(hit["damage"] * 0.3))  # Block reduces to 30%
                if hit["total_hits"] > 1:
                    self.battle_message = f"Hit {hit['hit_number']}/{hit['total_hits']}! NPC blocks and takes {damage} damage!"
                else:
                    self.battle_message = f"You attack! NPC blocks and takes {damage} damage!"
                self.npc_blocking = False
            else:
                damage = hit["damage"]
                if hit["total_hits"] > 1:
                    self.battle_message = f"Hit {hit['hit_number']}/{hit['total_hits']}: {damage} damage!"
                else:
                    self.battle_message = f"You use Normal Attack and deal {damage} damage!"
            
            self.npc_health = max(0, self.npc_health - damage)
            self.battle_message_timer = pygame.time.get_ticks()
            self.current_hit_index += 1
            
            # If more hits to process, wait a bit then continue
            if self.current_hit_index < len(self.attack_hits):
                # Will continue in update_battle
                pass
            else:
                # All hits done
                self.show_move_selection = False
                self.player_turn = False
                self.npc_last_action_time = pygame.time.get_ticks()
                self.npc_next_reaction_time = 0
                self.attack_hits = []
                self.current_hit_index = 0
                
                # Check if NPC is defeated
                if self.npc_health <= 0:
                    self.battle_over = True
                    self.battle_result = "win"
                    self.battle_message = "You Win!"
                    self.battle_message_timer = pygame.time.get_ticks()
                    self.check_win_achievements()
    
    def check_win_achievements(self):
        """Check and unlock win-related achievements"""
        # Achievement 1: Win
        if not self.achievements["win"]["unlocked"]:
            self.achievements["win"]["unlocked"] = True
        
        # Achievement 3: Why - Win as the character (any character)
        if not self.achievements["why"]["unlocked"]:
            self.achievements["why"]["unlocked"] = True
            self.won_with_character = self.selected_character["name"]
        
        # Achievement 4: That the tune i love - Win as Saxophone with under 50% health
        if not self.achievements["tune_i_love"]["unlocked"]:
            if self.selected_character["name"] == "Saxophone":
                health_percent = self.player_health / self.player_max_health
                if health_percent < 0.5:  # Under 50% health
                    self.achievements["tune_i_love"]["unlocked"] = True
                    # Unlock Mafeoso character
                    for char in self.characters:
                        if char["name"] == "Mafeoso":
                            char["unlocked"] = True
        
        # Achievement 5: It bird it a plane what nooooooo - Win without using super moves
        if not self.achievements["bird_plane"]["unlocked"]:
            if self.super_moves_used_this_battle == 0:
                self.achievements["bird_plane"]["unlocked"] = True
    
    def check_lose_achievements(self):
        """Check and unlock lose-related achievements"""
        # Achievement 2: Now you have to pay your taxes - Lose a game
        if not self.achievements["pay_taxes"]["unlocked"]:
            self.achievements["pay_taxes"]["unlocked"] = True
    
    def npc_choose_move(self):
        """NPC AI chooses a move based on difficulty and situation"""
        # Teacher Mode: Use learned patterns to counter player
        if self.teacher_mode:
            self.npc_choose_move_teacher_mode()
            return
        
        difficulty = self.selected_difficulty_index
        
        # Calculate probabilities based on difficulty
        # Easy: More likely to attack, less likely to use super
        # Expert: More strategic, uses all moves effectively
        if difficulty == 0:  # Easy
            # 70% attack, 20% block, 10% super
            move_weights = [0.7, 0.2, 0.1]
        elif difficulty == 1:  # Medium
            # 60% attack, 25% block, 15% super
            move_weights = [0.6, 0.25, 0.15]
        elif difficulty == 2:  # Hard
            # 50% attack, 30% block, 20% super
            move_weights = [0.5, 0.3, 0.2]
        else:  # Expert
            # Strategic: Use block if low health, super if good opportunity
            if self.npc_health < self.npc_max_health * 0.3:
                # Low health - more defensive
                move_weights = [0.4, 0.4, 0.2]
            elif self.npc_health > self.npc_max_health * 0.7:
                # High health - more aggressive
                move_weights = [0.4, 0.2, 0.4]
            else:
                # Medium health - balanced
                move_weights = [0.45, 0.3, 0.25]
        
        # Choose move based on weights
        rand = random.random()
        if rand < move_weights[0]:
            self.npc_move_selection = "attack"
        elif rand < move_weights[0] + move_weights[1]:
            self.npc_move_selection = "block"
        else:
            self.npc_move_selection = "super"
    
    def npc_choose_move_teacher_mode(self):
        """NPC uses learned patterns to counter player strategy"""
        # If still learning (first 3 battles), use adaptive learning
        if self.teacher_battle_count < self.teacher_max_battles:
            # During learning phase, adapt based on what we've seen so far
            total_moves = sum(self.learned_player_patterns["preferred_moves"].values())
            if total_moves > 0:
                # Counter player's most common move
                player_most_common = max(self.learned_player_patterns["preferred_moves"], 
                                       key=self.learned_player_patterns["preferred_moves"].get)
                
                # Counter strategy: If player attacks a lot, block more. If player blocks, attack more.
                if player_most_common == "attack":
                    move_weights = [0.3, 0.5, 0.2]  # More blocking
                elif player_most_common == "block":
                    move_weights = [0.6, 0.2, 0.2]  # More attacking
                else:  # super
                    move_weights = [0.4, 0.3, 0.3]  # Balanced with more super
            else:
                # No data yet, use balanced
                move_weights = [0.4, 0.3, 0.3]
        else:
            # After learning, use optimal counter-strategy
            total_moves = sum(self.learned_player_patterns["preferred_moves"].values())
            if total_moves == 0:
                move_weights = [0.4, 0.3, 0.3]
            else:
                # Analyze player patterns
                attack_pct = self.learned_player_patterns["preferred_moves"]["attack"] / total_moves
                block_pct = self.learned_player_patterns["preferred_moves"]["block"] / total_moves
                super_pct = self.learned_player_patterns["preferred_moves"]["super"] / total_moves
                
                # Counter-strategy: Adapt to player's style
                if attack_pct > 0.5:
                    # Player attacks a lot - counter with blocks and strategic attacks
                    move_weights = [0.3, 0.5, 0.2]
                elif block_pct > 0.4:
                    # Player blocks a lot - counter with more attacks
                    move_weights = [0.6, 0.2, 0.2]
                elif super_pct > 0.3:
                    # Player uses super a lot - counter with blocks and supers
                    move_weights = [0.3, 0.4, 0.3]
                else:
                    # Balanced player - use strategic mix
                    move_weights = [0.4, 0.3, 0.3]
                
                # Adjust based on health
                health_percent = self.npc_health / self.npc_max_health
                if health_percent < 0.3:
                    # Low health - check what player does at low health
                    low_health_moves = self.learned_player_patterns["health_thresholds"]["low"]
                    if len(low_health_moves) > 0:
                        most_common_low = max(set(low_health_moves), key=low_health_moves.count)
                        if most_common_low == "attack":
                            move_weights = [0.2, 0.6, 0.2]  # Block more when low
                        else:
                            move_weights = [0.4, 0.4, 0.2]
        
        # Choose move based on learned weights
        rand = random.random()
        if rand < move_weights[0]:
            self.npc_move_selection = "attack"
        elif rand < move_weights[0] + move_weights[1]:
            self.npc_move_selection = "block"
        else:
            self.npc_move_selection = "super"
    
    def npc_execute_attack(self):
        """NPC executes normal attack with multi-hits"""
        base_damage = self.selected_npc["base_damage"]
        weight = self.selected_npc["weight"]
        
        # Calculate multi-hits for lighter NPC instruments
        if weight <= 2:
            num_hits = random.randint(2, 3)
        elif weight <= 4:
            num_hits = random.randint(1, 2)
        else:
            num_hits = 1
        
        damage_per_hit = base_damage
        if num_hits > 1:
            damage_per_hit = int(damage_per_hit * 0.9)
        
        # Check accuracy
        if not self.check_npc_accuracy():
            self.battle_message = "NPC attacks but misses!"
            self.battle_message_timer = pygame.time.get_ticks()
            self.player_turn = True
            self.npc_last_action_time = pygame.time.get_ticks()
            self.npc_next_reaction_time = 0
            self.npc_move_selection = None
            return
        
        # Create hits list
        self.attack_hits = []
        for i in range(num_hits):
            self.attack_hits.append({
                "damage": damage_per_hit,
                "hit_number": i + 1,
                "total_hits": num_hits,
                "is_npc": True
            })
        
        self.current_hit_index = 0
        self.process_npc_hit()
    
    def process_npc_hit(self):
        """Process the next hit in NPC's multi-hit attack"""
        if self.current_hit_index < len(self.attack_hits):
            hit = self.attack_hits[self.current_hit_index]
            
            # Check if player is blocking
            if self.player_blocking:
                damage = max(1, int(hit["damage"] * 0.3))  # Block reduces to 30%
                if hit["total_hits"] > 1:
                    self.battle_message = f"NPC Hit {hit['hit_number']}/{hit['total_hits']}! You block and take {damage} damage!"
                else:
                    self.battle_message = f"NPC attacks! You block and take {damage} damage!"
                self.player_blocking = False
            else:
                damage = hit["damage"]
                if hit["total_hits"] > 1:
                    self.battle_message = f"NPC Hit {hit['hit_number']}/{hit['total_hits']}: {damage} damage!"
                else:
                    self.battle_message = f"NPC deals {damage} damage!"
            
            self.player_health = max(0, self.player_health - damage)
            self.battle_message_timer = pygame.time.get_ticks()
            self.current_hit_index += 1
            
            if self.current_hit_index < len(self.attack_hits):
                # More hits to process
                pass
            else:
                # All hits done
                self.player_turn = True
                self.npc_last_action_time = pygame.time.get_ticks()
                self.npc_next_reaction_time = 0
                self.attack_hits = []
                self.current_hit_index = 0
                self.npc_move_selection = None
                
                # Check if player is defeated
                if self.player_health <= 0:
                    self.battle_over = True
                    self.battle_result = "lose"
                    self.battle_message = "You Lose!"
                    self.battle_message_timer = pygame.time.get_ticks()
                    # Check achievements
                    self.check_lose_achievements()
    
    def npc_execute_block(self):
        """NPC uses block"""
        self.npc_blocking = True
        self.battle_message = "NPC prepares to block the next attack!"
        self.battle_message_timer = pygame.time.get_ticks()
        self.player_turn = True
        self.npc_last_action_time = pygame.time.get_ticks()
        self.npc_next_reaction_time = 0
        self.npc_move_selection = None
    
    def npc_execute_super(self):
        """NPC uses super move (answers music question automatically)"""
        # NPC generates and answers question
        clef = self.get_clef_for_instrument(self.selected_npc["name"])
        note = random.choice(self.music_notes)
        num_notes = random.randint(3, 5)
        all_notes = random.sample(self.music_notes, min(num_notes, len(self.music_notes)))
        if note not in all_notes:
            all_notes[random.randint(0, len(all_notes) - 1)] = note
        circled_index = all_notes.index(note)
        
        # NPC "answers" the question (based on difficulty - smarter NPCs more likely correct)
        accuracy_rates = [0.5, 0.65, 0.8, 0.95]  # Easy to Expert
        npc_accuracy = accuracy_rates[self.selected_difficulty_index]
        is_correct = random.random() < npc_accuracy
        
        if is_correct:
            # NPC answers correctly
            base_damage = self.selected_npc["base_damage"]
            damage = int(base_damage * self.moves[2]["damage_multiplier"])
            self.player_health = max(0, self.player_health - damage)
            self.battle_message = f"NPC uses Super! Correct answer! Deals {damage} damage!"
        else:
            self.battle_message = f"NPC uses Super! Wrong answer! No damage dealt."
        
        self.battle_message_timer = pygame.time.get_ticks()
        self.player_turn = True
        self.npc_last_action_time = pygame.time.get_ticks()
        self.npc_next_reaction_time = 0
        self.npc_move_selection = None
        
        # Check if player is defeated
        if self.player_health <= 0:
            self.battle_over = True
            self.battle_result = "lose"
            self.battle_message = "You Lose!"
            self.battle_message_timer = pygame.time.get_ticks()
            self.check_lose_achievements()
    
    def calculate_npc_reaction_time(self):
        """Calculate NPC reaction time based on difficulty and speed (smarter = faster, faster instrument = faster)"""
        # Base reaction time based on difficulty (smarter = faster)
        # Easy: 2-3 seconds (slow, sometimes hesitates)
        # Medium: 1.5-2 seconds (normal)
        # Hard: 1-1.5 seconds (fast)
        # Expert: 0.5-1 second (very fast)
        base_times = [2500, 1750, 1250, 750]  # milliseconds
        variation = [500, 250, 250, 250]  # random variation
        base = base_times[self.selected_difficulty_index]
        var = random.randint(-variation[self.selected_difficulty_index], variation[self.selected_difficulty_index])
        
        # Adjust based on NPC speed (faster instruments react faster)
        # Speed 2 (Tuba) = +500ms, Speed 10 (Flute) = -500ms
        speed_modifier = (10 - self.selected_npc["speed"]) * 50  # Each speed point = 50ms difference
        return max(300, base + var - speed_modifier)  # Minimum 300ms
    
    def check_npc_accuracy(self):
        """Check if NPC hits based on difficulty (smarter = more accurate)"""
        # Easy: 60% hit rate
        # Medium: 75% hit rate
        # Hard: 90% hit rate
        # Expert: 100% hit rate
        accuracy_rates = [0.6, 0.75, 0.9, 1.0]
        return random.random() < accuracy_rates[self.selected_difficulty_index]
    
    def update_battle(self):
        """Update battle state (NPC turn, etc.)"""
        # Don't update if battle is over or question is showing
        if self.battle_over or self.show_question:
            return
        
        # Process multi-hit attacks (player or NPC)
        if self.attack_hits and self.current_hit_index < len(self.attack_hits):
            current_time = pygame.time.get_ticks()
            # Wait 500ms between hits
            if current_time - self.battle_message_timer > 500:
                if self.player_turn:
                    self.process_next_hit()
                else:
                    self.process_npc_hit()
            return
            
        if not self.player_turn and self.npc_health > 0 and self.player_health > 0:
            current_time = pygame.time.get_ticks()
            time_since_turn = current_time - self.npc_last_action_time
            
            # Set reaction time when turn starts
            if self.npc_next_reaction_time == 0:
                self.npc_next_reaction_time = self.calculate_npc_reaction_time()
            
            if time_since_turn >= self.npc_next_reaction_time:
                # NPC chooses a move based on difficulty and situation
                if self.npc_move_selection is None:
                    self.npc_choose_move()
                
                # Execute NPC move
                if self.npc_move_selection == "attack":
                    self.npc_execute_attack()
                elif self.npc_move_selection == "block":
                    self.npc_execute_block()
                elif self.npc_move_selection == "super":
                    self.npc_execute_super()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.show_title:
                    self.handle_title_input(event)
                elif self.show_achievements:
                    self.handle_achievements_input(event)
                elif self.show_character_select:
                    self.handle_character_select_input(event)
                elif self.show_npc_select:
                    self.handle_npc_select_input(event)
                elif self.show_difficulty_select:
                    self.handle_difficulty_select_input(event)
                elif self.in_battle:
                    self.handle_battle_input(event)
            
            if self.show_title:
                self.show_title_screen()
            elif self.show_achievements:
                self.show_achievements_screen()
            elif self.show_character_select:
                self.show_character_select_screen()
            elif self.show_npc_select:
                self.show_npc_select_screen()
            elif self.show_difficulty_select:
                self.show_difficulty_select_screen()
            elif self.in_battle:
                self.update_battle()
                self.show_battle_screen()
            else:
                # Game main screen (placeholder for now)
                self.screen.fill(BLACK)
                if self.selected_character:
                    game_text = self.font_medium.render(
                        f"Game Started! Selected: {self.selected_character['name']}", 
                        True, WHITE
                    )
                else:
                    game_text = self.font_medium.render("Game Started!", True, WHITE)
                game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(game_text, game_rect)
                pygame.display.flip()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
