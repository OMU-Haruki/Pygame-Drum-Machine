import pygame

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 350
BOTTOM_BOX_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT + BOTTOM_BOX_HEIGHT))
pygame.display.set_caption("Drum Machine")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
LIGHT_BLUE = (100, 100, 255)
BLUE = (200, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Drum settings
ROWS = 6
COLS = 16

sounds = [
    pygame.mixer.Sound('sounds/kick.wav'),
    pygame.mixer.Sound('sounds/snare.wav'),
    pygame.mixer.Sound('sounds/hihat.wav'),
    pygame.mixer.Sound('sounds/tom.wav'),
    pygame.mixer.Sound('sounds/clap.wav'),
    pygame.mixer.Sound('sounds/openhihat.wav')
]

sound_names = ["BD", "SD", "HH", "TM", "CL", "OH"]

# Sequencer grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# bpm and beats settings
bpm = 120
beats = 16

beat_interval = (60000 / bpm) / 4

# Main loop
running = True
paused = True
clock = pygame.time.Clock()
current_col = 0
last_beat_time = pygame.time.get_ticks()

# Font for text
font = pygame.font.Font(None, 36)

while running:
  screen.fill(WHITE)

  # Draw grid
  CELL_SIZE = WIDTH // (beats + 1)
  for row in range(ROWS):
    text = font.render(sound_names[row], True, DARK_GRAY)
    screen.blit(text, (5, row * (HEIGHT // ROWS) +
                (HEIGHT // ROWS - text.get_height()) // 2))

    for col in range(beats):
      if not paused and col == current_col:
        color = LIGHT_BLUE if grid[row][col] == 0 else BLUE
      else:
        if col % 4 == 0:
          color = DARK_GRAY if grid[row][col] == 0 else WHITE
        else:
          color = GRAY if grid[row][col] == 0 else WHITE
      pygame.draw.rect(screen, color, ((col + 1) * CELL_SIZE,
                       row * (HEIGHT // ROWS), CELL_SIZE, HEIGHT // ROWS))
      pygame.draw.rect(screen, DARK_GRAY, ((col + 1) * CELL_SIZE,
                       row * (HEIGHT // ROWS), CELL_SIZE, HEIGHT // ROWS), 1)

  # Draw bottom box
  pygame.draw.rect(screen, WHITE, (0, HEIGHT, WIDTH, BOTTOM_BOX_HEIGHT))

  # Draw play/pause button
  play_pause_text = "Play" if paused else "Pause"
  play_pause_button = pygame.draw.rect(
      screen, DARK_GRAY, (10, HEIGHT + 10, 90, 30))
  play_pause_label = font.render(play_pause_text, True, WHITE)
  screen.blit(play_pause_label, (20, HEIGHT + 15))

  # Draw BPM info and buttons
  bpm_label = font.render(f"BPM: {bpm}", True, DARK_GRAY)
  screen.blit(bpm_label, (110, HEIGHT + 15))
  bpm_increase_button = pygame.draw.rect(
      screen, DARK_GRAY, (270, HEIGHT + 10, 30, 30))
  bpm_decrease_button = pygame.draw.rect(
      screen, DARK_GRAY, (230, HEIGHT + 10, 30, 30))
  screen.blit(font.render("+", True, WHITE), (280, HEIGHT + 10))
  screen.blit(font.render("-", True, WHITE), (240, HEIGHT + 10))

  # Event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      x, y = event.pos
      if y < HEIGHT:
        col = (x - CELL_SIZE) // CELL_SIZE
        row = y // (HEIGHT // ROWS)
        if 0 <= col < beats and 0 <= row < ROWS:
          grid[row][col] = 1 - grid[row][col]
          if grid[row][col] == 1:
            sounds[row].play()
      else:
        if play_pause_button.collidepoint(x, y):
          paused = not paused
          if paused:
            current_col = 0
          else:
            current_col = -1
            last_beat_time = pygame.time.get_ticks()
        elif bpm_increase_button.collidepoint(x, y):
          bpm = min(bpm + 10, 1000)
          beat_interval = (60000 / bpm) / 4
        elif bpm_decrease_button.collidepoint(x, y):
          bpm = max(bpm - 10, 10)
          beat_interval = (60000 / bpm) / 4
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        bpm = min(bpm + 10, 1000)
        beat_interval = (60000 / bpm) / 4
      elif event.key == pygame.K_DOWN:
        bpm = max(bpm - 10, 10)
        beat_interval = (60000 / bpm) / 4
      elif event.key == pygame.K_RIGHT:
        beats = min(beats + 1, COLS)
      elif event.key == pygame.K_LEFT:
        beats = max(beats - 1, 1)
      elif event.key == pygame.K_SPACE:
        paused = not paused
        if paused:
          current_col = 0
        else:
          current_col = -1
          last_beat_time = pygame.time.get_ticks()
      elif event.key == pygame.K_r:
        grid = [[0 for _ in range(COLS)]
                for _ in range(ROWS)]  # Reset all cells
      elif pygame.K_1 <= event.key <= pygame.K_6:
        row = event.key - pygame.K_1
        sounds[row].play()
        if not paused:
          grid[row][current_col] = 1

  # Play sounds
  if not paused:
    current_time = pygame.time.get_ticks()
    if current_time - last_beat_time >= beat_interval:
      current_col = (current_col + 1) % beats
      for row in range(ROWS):
        if grid[row][current_col] == 1:
          sounds[row].play()
      last_beat_time = current_time

  pygame.display.flip()
  clock.tick(60)

pygame.quit()