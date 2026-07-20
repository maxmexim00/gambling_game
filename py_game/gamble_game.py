import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scratch-Style Coin Flip")
clock = pygame.time.Clock()

ASSET_DIR = "sprites"
SOUND_DIR = "sounds"
USE_CUSTOM_SPRITES = True
USE_CUSTOM_SOUNDS = True
DRAW_TEXT_ON_SPRITE_BUTTONS = True

MUSIC_VOLUME = 0.4
SFX_VOLUME = 0.7

SPRITE_CONFIG = {
    "background": {"file": "background.png", "size": (WIDTH, HEIGHT)},
    "panel": {"file": "panel.png", "size": (780, 320)},

    "heads": {"file": "heads.png", "size": (180, 180)},
    "tails": {"file": "tails.png", "size": (180, 180)},

    "heads_btn": {"file": "heads_button.png", "size": (150, 60)},
    "tails_btn": {"file": "tails_button.png", "size": (150, 60)},
    "minus_btn": {"file": "minus_button.png", "size": (60, 60)},
    "plus_btn": {"file": "plus_button.png", "size": (60, 60)},
    "flip_btn": {"file": "flip_button.png", "size": (270, 65)},
    "reset_btn": {"file": "reset_button.png", "size": (240, 60)},
}

EXTRA_SPRITE_CONFIG = [
    {"file": "mascot.png", "pos": (20, 360), "size": (140, 140)},
]

# Drop your own audio files into the "sounds" folder using these filenames
# (or change the filenames below to match whatever you have).
# Music: .ogg or .mp3 work well. Sound effects: .wav or .ogg recommended.
MUSIC_CONFIG = {
    "file": "03 funiculi holiday.mp3",
}

SOUND_CONFIG = {
    "click": {"file": "jump.wav"},
    "flip": {"file": "freesound_community-coin-flip-88793.wav"},
    "win": {"file": "point.wav"},
    "lose": {"file": "die.wav"},
    "game_over": {"file": "toby fox - UNDERTALE Soundtrack - 11 Determination.wav"},
}

SKY = (135, 206, 250)
GRASS = (120, 220, 120)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)

YELLOW = (255, 215, 0)
ORANGE = (255, 170, 50)
GREEN = (70, 210, 100)
RED = (255, 100, 120)
BLUE = (70, 170, 255)
PURPLE = (180, 120, 255)

title_font = pygame.font.SysFont("arial", 42, bold=True)
main_font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 22, bold=True)
coin_font = pygame.font.SysFont("arial", 30, bold=True)

balance = 100
bet = 10
choice = "Heads"
message = "Choose Heads or Tails, then click FLIP!"
anim_face = "Heads"
final_result = None
flip_timer = 0
FLIP_TIME = 40
game_over = False
music_on = True
sfx_on = True

heads_btn = pygame.Rect(120, 430, 150, 60)
tails_btn = pygame.Rect(290, 430, 150, 60)

minus_btn = pygame.Rect(520, 430, 60, 60)
plus_btn = pygame.Rect(730, 430, 60, 60)

flip_btn = pygame.Rect(520, 510, 270, 65)
reset_btn = pygame.Rect(330, 510, 240, 60)

music_btn = pygame.Rect(20, 20, 44, 44)
sfx_btn = pygame.Rect(74, 20, 44, 44)


def load_sprite(filename, size=None):
    if not USE_CUSTOM_SPRITES:
        return None

    path = os.path.join(ASSET_DIR, filename)
    if not os.path.exists(path):
        return None

    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error as e:
        print(f"Could not load {filename}: {e}")
        return None


def load_all_assets():
    loaded_sprites = {}

    for key, config in SPRITE_CONFIG.items():
        loaded_sprites[key] = load_sprite(config["file"], config.get("size"))

    loaded_extras = []
    for item in EXTRA_SPRITE_CONFIG:
        img = load_sprite(item["file"], item.get("size"))
        if img:
            loaded_extras.append({
                "image": img,
                "pos": item["pos"]
            })

    return loaded_sprites, loaded_extras


def load_sound_effect(filename):
    if not USE_CUSTOM_SOUNDS:
        return None

    path = os.path.join(SOUND_DIR, filename)
    if not os.path.exists(path):
        return None

    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(SFX_VOLUME)
        return sound
    except pygame.error as e:
        print(f"Could not load sound {filename}: {e}")
        return None


def load_all_sounds():
    loaded_sounds = {}
    for key, config in SOUND_CONFIG.items():
        loaded_sounds[key] = load_sound_effect(config["file"])
    return loaded_sounds


def load_music_track():
    if not USE_CUSTOM_SOUNDS:
        return False

    path = os.path.join(SOUND_DIR, MUSIC_CONFIG["file"])
    if not os.path.exists(path):
        return False

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        return True
    except pygame.error as e:
        print(f"Could not load music {MUSIC_CONFIG['file']}: {e}")
        return False


sprites, extra_sprites = load_all_assets()
sounds = load_all_sounds()
music_loaded = load_music_track()

if music_loaded and music_on:
    pygame.mixer.music.play(loops=-1)


def play_sound(key):
    if sfx_on and sounds.get(key):
        sounds[key].play()


def reload_assets():
    global sprites, extra_sprites, sounds, music_loaded
    sprites, extra_sprites = load_all_assets()
    sounds = load_all_sounds()
    music_loaded = load_music_track()
    if music_loaded and music_on:
        pygame.mixer.music.play(loops=-1)


def toggle_music():
    global music_on
    music_on = not music_on
    if music_on and music_loaded:
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.stop()


def toggle_sfx():
    global sfx_on
    sfx_on = not sfx_on


def reset_game():
    global balance, bet, choice, message, anim_face, final_result, flip_timer, game_over
    balance = 100
    bet = 10
    choice = "Heads"
    message = "Choose Heads or Tails, then click FLIP!"
    anim_face = "Heads"
    final_result = None
    flip_timer = 0
    game_over = False


def brighten(color, amount=25):
    return tuple(min(c + amount, 255) for c in color)


def draw_button(rect, text, color, selected=False, sprite=None):
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)

    border_color = YELLOW if selected else BLACK
    border_width = 6 if hovered else 4

    if sprite:
        screen.blit(sprite, rect.topleft)
        pygame.draw.rect(screen, border_color, rect, border_width, border_radius=18)
    else:
        draw_color = brighten(color, 20) if hovered else color
        pygame.draw.rect(screen, draw_color, rect, border_radius=18)
        pygame.draw.rect(screen, border_color, rect, border_width, border_radius=18)

    if (not sprite) or DRAW_TEXT_ON_SPRITE_BUTTONS:
        label = main_font.render(text, True, BLACK)
        screen.blit(label, label.get_rect(center=rect.center))


def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 22)
    pygame.draw.circle(screen, WHITE, (x + 22, y - 10), 18)
    pygame.draw.circle(screen, WHITE, (x + 45, y), 22)
    pygame.draw.circle(screen, WHITE, (x + 20, y + 8), 18)


def draw_coin(cx, cy, face):
    pygame.draw.ellipse(screen, (180, 180, 180), (cx - 85, cy + 70, 170, 25))

    sprite = sprites["heads"] if face == "Heads" else sprites["tails"]

    if sprite:
        rect = sprite.get_rect(center=(cx, cy))
        screen.blit(sprite, rect)
    else:
        pygame.draw.circle(screen, YELLOW, (cx, cy), 90)
        pygame.draw.circle(screen, ORANGE, (cx, cy), 90, 6)
        text = coin_font.render(face, True, BLACK)
        screen.blit(text, text.get_rect(center=(cx, cy)))


def draw_background():
    if sprites["background"]:
        screen.blit(sprites["background"], (0, 0))
    else:
        screen.fill(SKY)
        draw_cloud(100, 80)
        draw_cloud(700, 100)
        draw_cloud(500, 60)
        pygame.draw.rect(screen, GRASS, (0, HEIGHT - 110, WIDTH, 110))


def draw_panel():
    panel_rect = pygame.Rect(60, 80, 780, 320)

    if sprites["panel"]:
        screen.blit(sprites["panel"], panel_rect.topleft)
    else:
        pygame.draw.rect(screen, WHITE, panel_rect, border_radius=25)
        pygame.draw.rect(screen, PURPLE, panel_rect, 5, border_radius=25)


def draw_extra_sprites():
    for item in extra_sprites:
        screen.blit(item["image"], item["pos"])


def draw_sound_toggle(rect, is_on, icon_on, icon_off):
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)
    color = GREEN if is_on else RED
    draw_color = brighten(color, 20) if hovered else color

    pygame.draw.rect(screen, draw_color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 3, border_radius=12)

    label = small_font.render(icon_on if is_on else icon_off, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_l:
                reload_assets()
                message = "Sprites and sounds reloaded!"
            elif event.key == pygame.K_m:
                toggle_music()
            elif event.key == pygame.K_n:
                toggle_sfx()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if music_btn.collidepoint(mouse_pos):
                toggle_music()
            elif sfx_btn.collidepoint(mouse_pos):
                toggle_sfx()

            elif game_over:
                if reset_btn.collidepoint(mouse_pos):
                    play_sound("click")
                    reset_game()

            elif flip_timer == 0:
                if heads_btn.collidepoint(mouse_pos):
                    play_sound("click")
                    choice = "Heads"

                elif tails_btn.collidepoint(mouse_pos):
                    play_sound("click")
                    choice = "Tails"

                elif minus_btn.collidepoint(mouse_pos):
                    play_sound("click")
                    bet = max(10, bet - 10)

                elif plus_btn.collidepoint(mouse_pos):
                    play_sound("click")
                    bet = min(balance, bet + 10)

                elif flip_btn.collidepoint(mouse_pos) and balance >= bet:
                    play_sound("flip")
                    flip_timer = FLIP_TIME
                    final_result = random.choice(["Heads", "Tails"])
                    message = "Flipping..."

    if flip_timer > 0:
        if flip_timer % 4 == 0:
            anim_face = random.choice(["Heads", "Tails"])

        flip_timer -= 1

        if flip_timer == 0:
            anim_face = final_result

            if choice == final_result:
                balance += bet
                message = f"It was {final_result}! You won {bet} coins!"
                play_sound("win")
            else:
                balance -= bet
                message = f"It was {final_result}! You lost {bet} coins!"
                play_sound("lose")

            if balance <= 0:
                balance = 0
                game_over = True
                message = "Game Over! Click RESET to play again."
                play_sound("game_over")

            if balance > 0:
                bet = min(bet, balance)

    draw_background()
    draw_extra_sprites()

    title = title_font.render("Scratch-Style Coin Flip", True, BLACK)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 35)))

    draw_panel()

    balance_text = main_font.render(f"Balance: {balance} coins", True, BLACK)
    bet_text = main_font.render(f"Bet: {bet}", True, BLACK)

    screen.blit(balance_text, (100, 105))
    screen.blit(bet_text, (620, 105))

    draw_coin(WIDTH // 2, 245, anim_face)

    msg_box = pygame.Rect(120, 335, 660, 45)
    pygame.draw.rect(screen, GRAY, msg_box, border_radius=14)
    pygame.draw.rect(screen, DARK_GRAY, msg_box, 3, border_radius=14)

    msg_surface = small_font.render(message, True, BLACK)
    screen.blit(msg_surface, msg_surface.get_rect(center=msg_box.center))

    if not game_over:
        draw_button(heads_btn, "Heads", BLUE, selected=(choice == "Heads"), sprite=sprites["heads_btn"])
        draw_button(tails_btn, "Tails", RED, selected=(choice == "Tails"), sprite=sprites["tails_btn"])
        draw_button(minus_btn, "-", ORANGE, sprite=sprites["minus_btn"])
        draw_button(plus_btn, "+", GREEN, sprite=sprites["plus_btn"])
        draw_button(flip_btn, "FLIP!", YELLOW, sprite=sprites["flip_btn"])
    else:
        draw_button(reset_btn, "RESET", GREEN, sprite=sprites["reset_btn"])

    draw_sound_toggle(music_btn, music_on, "M", "M")
    draw_sound_toggle(sfx_btn, sfx_on, "S", "S")

    hint1 = small_font.render("Press R to reset", True, BLACK)
    hint2 = small_font.render("Press L to reload sprites/sounds", True, BLACK)
    hint3 = small_font.render("Press M: music, N: sound effects", True, BLACK)
    screen.blit(hint1, (20, HEIGHT - 90))
    screen.blit(hint2, (20, HEIGHT - 60))
    screen.blit(hint3, (20, HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
