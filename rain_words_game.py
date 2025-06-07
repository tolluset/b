import pygame
import sys
import random
import time
import os

# Initialize pygame
pygame.init()

# Define event constants
QUIT = pygame.QUIT
KEYDOWN = pygame.KEYDOWN
TEXTINPUT = pygame.TEXTINPUT
TEXTEDITING = pygame.TEXTEDITING
K_RETURN = pygame.K_RETURN
K_BACKSPACE = pygame.K_BACKSPACE
K_ESCAPE = pygame.K_ESCAPE
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("(雨)")

# Enable IME input
pygame.key.start_text_input()
pygame.key.set_text_input_rect(
    pygame.Rect(50, SCREEN_HEIGHT - 40, SCREEN_WIDTH - 100, 30)
)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

# Load custom fonts
jp_font_path = os.path.join(
    "assets", "fonts", "Noto_Sans_JP", "NotoSansJP-VariableFont_wght.ttf"
)
en_font_path = os.path.join(
    "assets", "fonts", "Noto_Sans", "NotoSans-VariableFont_wdth,wght.ttf"
)

# Load fonts in different sizes
jp_font_large = pygame.font.Font(jp_font_path, 36)
jp_font_medium = pygame.font.Font(jp_font_path, 28)
jp_font_small = pygame.font.Font(jp_font_path, 24)

en_font_large = pygame.font.Font(en_font_path, 36)
en_font_medium = pygame.font.Font(en_font_path, 28)
en_font_small = pygame.font.Font(en_font_path, 24)
print("Successfully loaded custom fonts")


# Game variables
lives = 5
score = 0
matched_words = []  # List to store matched word pairs
missed_words = []  # List to store missed word pairs
all_shown_words = set()  # Set to track all words that appeared in the game
matched_word_pairs = set()  # Set to track matched word pairs to avoid duplicates
game_active = True
start_time = 0
game_time = 0
input_text = ""
ime_text = ""  # Store IME composition text
current_page = 0  # Current page for game over screen


# Game variables
lives = 5
score = 0
matched_words = []  # List to store matched word pairs
missed_words = []  # List to store missed word pairs
all_shown_words = set()  # Set to track all words that appeared in the game
game_active = True
start_time = 0
game_time = 0
input_text = ""


# Word class for falling words
class Word:
    def __init__(self, english, japanese, x, speed):
        self.english = english
        self.japanese = japanese
        self.x = x
        self.y = 0
        self.speed = speed
        self.active = True
        self.matched = False  # Status flag for matched word animation
        self.match_time = 0  # Time when word was matched
        self.fade_out = 255  # Alpha value for fade out effect
        # Add the word to the set of all shown words
        all_shown_words.add((english, japanese))

    def update(self):
        if self.matched:
            # Fade out animation for matched words
            current_time = time.time()
            if current_time - self.match_time > 0.05:  # Update every 50ms
                self.fade_out -= 15  # Decrease alpha value
                self.match_time = current_time
            if self.fade_out <= 0:
                self.active = False
        else:
            # Normal words fall down
            self.y += self.speed

    def draw(self):
        if self.matched:
            # Matched words float upward with fade out effect
            self.y -= 1  # Move upward

            # Apply alpha value (fade out)
            eng_text = en_font_medium.render(self.english, True, WHITE)
            eng_text.set_alpha(self.fade_out)
            screen.blit(eng_text, (self.x, self.y))

            jpn_text = jp_font_small.render(
                self.japanese, True, GREEN
            )  # Green for matched words
            jpn_text.set_alpha(self.fade_out)
            screen.blit(jpn_text, (self.x, self.y + 30))
        else:
            # Display normal words
            eng_text = en_font_medium.render(self.english, True, WHITE)
            screen.blit(eng_text, (self.x, self.y))

            jpn_text = jp_font_small.render(self.japanese, True, YELLOW)
            screen.blit(jpn_text, (self.x, self.y + 30))

    def is_out_of_bounds(self):
        return (
            self.y > SCREEN_HEIGHT - 80
        )  # Adjusted to account for the katakana display


# Load word pairs from file
def load_word_pairs(filename):
    word_pairs = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        english, japanese = parts
                        word_pairs.append((english.strip(), japanese.strip()))
    except FileNotFoundError:
        # Default word pairs if file not found
        word_pairs = [
            ("hello", "ハロー"),
            ("computer", "コンピューター"),
            ("game", "ゲーム"),
            ("music", "ミュージック"),
            ("water", "ウォーター"),
        ]
    return word_pairs


# Game functions
def spawn_word(word_pairs):
    if not word_pairs:
        return None

    english, japanese = random.choice(word_pairs)
    x = random.randint(50, SCREEN_WIDTH - 100)
    # Reduced speed for slower falling
    speed = random.uniform(0.5, 1.5)
    return Word(english, japanese, x, speed)


def draw_lives():
    lives_text = en_font_small.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (20, 20))


def draw_score():
    score_text = en_font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))


def draw_input_box():
    pygame.draw.rect(screen, WHITE, (50, SCREEN_HEIGHT - 40, SCREEN_WIDTH - 100, 30), 2)

    # Display the input text with proper font for Japanese characters
    input_surface = jp_font_small.render(input_text, True, WHITE)
    screen.blit(input_surface, (55, SCREEN_HEIGHT - 35))

    # Display IME composition text if available
    if ime_text:
        ime_surface = jp_font_small.render(ime_text, True, YELLOW)
        screen.blit(
            ime_surface, (55 + input_surface.get_width() + 5, SCREEN_HEIGHT - 35)
        )

    # Display a prompt for input
    prompt_text = en_font_small.render("Type katakana here:", True, GRAY)
    screen.blit(prompt_text, (55, SCREEN_HEIGHT - 70))


def game_over_screen():
    global current_page

    screen.fill(BLACK)

    # Check if all words were matched
    all_matched = len(matched_words) == len(all_shown_words)

    # Display game over or game clear message
    if all_matched:
        game_over_text = en_font_large.render("Game Clear!", True, GREEN)
    else:
        game_over_text = en_font_large.render("Game Over!", True, RED)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, 30))

    # Display score and time
    score_text = en_font_medium.render(f"Score: {score} words", True, WHITE)
    time_text = en_font_medium.render(f"Time: {game_time} seconds", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 80))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 100, 110))

    # Display all word pairs that appeared in the game
    words_title = en_font_medium.render("Word Pairs:", True, WHITE)
    screen.blit(words_title, (SCREEN_WIDTH // 2 - 300, 160))

    # Create a list of all words that appeared
    all_words_list = list(all_shown_words)

    # Calculate total pages
    items_per_page = 20  # 10 items per column, 2 columns
    total_pages = max(1, (len(all_words_list) + items_per_page - 1) // items_per_page)

    # Ensure current_page is valid
    if current_page >= total_pages:
        current_page = total_pages - 1

    # Display page information
    page_info = en_font_small.render(
        f"Page {current_page + 1}/{total_pages}", True, WHITE
    )
    screen.blit(page_info, (SCREEN_WIDTH // 2 - 50, 160))

    # Create sets for easy lookup
    matched_set = set((word[0], word[1]) for word in matched_words)

    # Display word pairs with status indicators
    y_offset = 200
    max_pairs_per_column = 10
    column_width = 350

    # Calculate start and end indices for current page
    start_idx = current_page * items_per_page
    end_idx = min(start_idx + items_per_page, len(all_words_list))

    # Display only items for current page
    for i, idx in enumerate(range(start_idx, end_idx)):
        english, japanese = all_words_list[idx]

        # Determine which column to place this word pair
        column = i // max_pairs_per_column
        row = i % max_pairs_per_column

        x_pos = (SCREEN_WIDTH // 2 - 300) + (column * column_width)
        y_pos = y_offset + (row * 30)

        # Determine if this word was matched or missed
        if (english, japanese) in matched_set:
            status_color = GREEN
            status_icon = "O"  # Use O instead of check mark
        else:
            status_color = RED
            status_icon = "X"  # Use X instead of cross mark

        # Draw the status icon
        status_text = en_font_small.render(status_icon, True, status_color)
        screen.blit(status_text, (x_pos - 20, y_pos))

        # Draw the word pair
        word_text = en_font_small.render(f"{english} - ", True, WHITE)
        jp_text = jp_font_small.render(japanese, True, WHITE)

        # Blit English text first
        screen.blit(word_text, (x_pos, y_pos))
        # Then blit Japanese text right after it
        screen.blit(jp_text, (x_pos + word_text.get_width(), y_pos))

    # Navigation buttons (if more than one page)
    if total_pages > 1:
        # Previous page button
        if current_page > 0:
            pygame.draw.rect(
                screen, BLUE, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 80, 120, 50)
            )
            prev_text = en_font_medium.render("< Prev", True, WHITE)
            screen.blit(prev_text, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT - 70))

        # Next page button
        if current_page < total_pages - 1:
            pygame.draw.rect(
                screen, BLUE, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT - 80, 120, 50)
            )
            next_text = en_font_medium.render("Next >", True, WHITE)
            screen.blit(next_text, (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT - 70))

    # Restart button
    pygame.draw.rect(
        screen, GREEN, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
    )
    restart_text = en_font_medium.render("Restart", True, BLACK)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 70))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 70))


def main():
    global lives, score, game_active, start_time, input_text, matched_words, missed_words, all_shown_words, game_time, ime_text, current_page, matched_word_pairs

    # Load word pairs
    word_pairs = load_word_pairs("word_pairs.txt")

    # Game variables
    falling_words = []
    last_spawn_time = 0
    spawn_interval = 5.0  # seconds - increased for slower gameplay

    # Reset game state
    lives = 5
    score = 0
    matched_words = []
    missed_words = []
    all_shown_words = set()
    matched_word_pairs = set()
    game_active = True
    start_time = time.time()
    game_time = 0
    input_text = ""
    ime_text = ""
    current_page = 0

    # Game loop
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        # Don't respond to Enter key during IME composition
                        if not ime_text:  # Only process when not in IME mode
                            # Only process when there's input
                            if input_text.strip():  # Only process if input is not empty
                                for word in falling_words[:]:
                                    if input_text == word.japanese:
                                        # Set animation for matched word
                                        word.matched = True
                                        word.match_time = time.time()

                                        score += 1
                                        matched_words.append(
                                            (word.english, word.japanese)
                                        )
                                        matched_word_pairs.add(
                                            (word.english, word.japanese)
                                        )
                                        input_text = ""
                                        break
                                # Clear input even if no match
                                input_text = ""
                    elif event.key == K_BACKSPACE:
                        if ime_text:
                            # If there's IME text, let the IME handle backspace
                            pass
                        else:
                            input_text = input_text[:-1]
                    elif event.key == K_ESCAPE:
                        input_text = ""
                        ime_text = ""
                # Handle IME text input events
                elif event.type == TEXTINPUT:
                    input_text += event.text
                    ime_text = ""
                # Handle IME text editing events (composition)
                elif event.type == TEXTEDITING:
                    ime_text = event.text
            else:
                if event.type == MOUSEBUTTONDOWN:
                    # Check if restart button is clicked
                    mouse_pos = pygame.mouse.get_pos()
                    restart_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50
                    )
                    if restart_rect.collidepoint(mouse_pos):
                        # Reset game
                        main()  # Restart the game by calling main again
                        return  # Exit the current game loop

                    # Check if previous page button is clicked
                    if current_page > 0:
                        prev_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 80, 120, 50
                        )
                        if prev_rect.collidepoint(mouse_pos):
                            current_page -= 1

                    # Check if next page button is clicked
                    total_pages = max(1, (len(all_shown_words) + 19) // 20)
                    if current_page < total_pages - 1:
                        next_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT - 80, 120, 50
                        )
                        if next_rect.collidepoint(mouse_pos):
                            current_page += 1

        if game_active:
            # Update game time
            game_time = int(time.time() - start_time)

            # Spawn new words
            current_time = time.time()
            if current_time - last_spawn_time > spawn_interval:
                # Exclude already matched words when selecting new words
                available_pairs = [
                    (eng, jpn)
                    for eng, jpn in word_pairs
                    if (eng, jpn) not in matched_word_pairs
                ]

                # Check if all words have been matched
                if not available_pairs:
                    # End game if all words are matched
                    game_active = False
                    game_time = int(time.time() - start_time)
                else:
                    # Generate new word
                    english, japanese = random.choice(available_pairs)
                    x = random.randint(50, SCREEN_WIDTH - 100)

                    # Increase speed based on time and score
                    base_speed = (
                        0.5 + (game_time / 60) * 0.5
                    )  # Increase speed by 0.5 every minute
                    score_boost = min(
                        score / 10, 1.0
                    )  # Increase speed up to 1.0 based on score (every 10 points)
                    speed = random.uniform(base_speed, base_speed + 1.0 + score_boost)

                    falling_words.append(Word(english, japanese, x, speed))
                    last_spawn_time = current_time

                    # Decrease spawn interval based on score and time (increase difficulty)
                    spawn_interval = max(1.5, 5.0 - (game_time / 60) - (score / 20))

            # Update falling words
            for word in falling_words[:]:
                word.update()
                if not word.active:  # Remove words when animation is complete
                    falling_words.remove(word)
                elif word.is_out_of_bounds() and not word.matched:
                    # Add to missed words list
                    missed_words.append((word.english, word.japanese))
                    falling_words.remove(word)
                    lives -= 1
                    if lives <= 0:
                        # Game over - record the final game time
                        game_active = False
                        game_time = int(time.time() - start_time)

            # Draw everything
            screen.fill(BLACK)
            for word in falling_words:
                word.draw()

            draw_lives()
            draw_score()
            draw_input_box()

        else:
            game_over_screen()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
