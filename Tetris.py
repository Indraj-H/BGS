"""
Single-file Tetris implementation using Pygame.
Save as `tetris.py` and open in PyCharm (or run with `python tetris.py`).

Controls:
  - Left / Right arrows: move piece
  - Down arrow: soft drop
  - Up arrow: rotate
  - Space: hard drop
  - P: pause
  - R: restart after game over

Dependencies:
  pip install pygame

This implementation is intentionally straightforward and commented so you can
customize shapes, colors, sounds, or UI later.
"""

import pygame
import random

# ---------- Configuration ----------
CELL_SIZE = 30
COLS, ROWS = 10, 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

# Tetromino shapes (each shape is a list of rotations using a 4x4 grid representation)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [
    (0, 255, 0),    # S - green
    (255, 0, 0),    # Z - red
    (0, 255, 255),  # I - cyan
    (255, 255, 0),  # O - yellow
    (255, 165, 0),  # J - orange
    (0, 0, 255),    # L - blue
    (128, 0, 128)   # T - purple
]

# ---------- Helper classes & functions ----------
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

    for r in range(ROWS):
        for c in range(COLS):
            if (c, r) in locked_positions:
                grid[r][c] = locked_positions[(c, r)]
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions


def valid_space(piece, grid):
    accepted_positions = [(c, r) for r in range(ROWS) for c in range(COLS) if grid[r][c] == BLACK]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos[1] >= 0:
            if pos not in accepted_positions:
                return False
    return True


def check_lost(locked_positions):
    for pos in locked_positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(COLS // 2 - 2, 0, random.choice(SHAPES))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (WIDTH // 2 - (label.get_width() // 2), HEIGHT // 2 - label.get_height() // 2))


def clear_rows(grid, locked):
    # Need to see if row is clear then shift every row above down
    inc = 0
    for i in range(ROWS - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            # add positions to remove from locked
            for j in range(COLS):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # shift rows down
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            color = locked.pop(key)
            new_key = (x, y + inc)
            locked[new_key] = color
    return inc


def draw_grid(surface, grid):
    for r in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, r * CELL_SIZE), (WIDTH, r * CELL_SIZE))
    for c in range(COLS):
        pygame.draw.line(surface, GRAY, (c * CELL_SIZE, 0), (c * CELL_SIZE, HEIGHT))


def draw_window(surface, grid, score=0):
    surface.fill(BLACK)

    # Title
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('TETRIS', True, WHITE)
    surface.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))

    # Score
    score_font = pygame.font.SysFont('comicsans', 24)
    score_label = score_font.render(f'Score: {score}', True, WHITE)
    surface.blit(score_label, (10, 10))

    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(surface, grid[r][c], (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, WHITE, (0, 0, WIDTH, HEIGHT), 2)


def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 24)
    label = font.render('Next:', True, WHITE)

    sx = WIDTH + 20
    sy = 50
    surface.blit(label, (sx + 10, sy - 30))

    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (sx + j * CELL_SIZE, sy + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)


# ---------- Main game loop ----------

def main():
    pygame.init()
    win_width = WIDTH + 200  # extra vertical space for next-piece/score if desired
    win = pygame.display.set_mode((win_width, HEIGHT))
    pygame.display.set_caption('Tetris - PyGame')

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # seconds per cell fall initially
    level_time = 0
    score = 0

    paused = False

    while run:
        grid = create_grid(locked_positions)
        dt = clock.tick(FPS) / 1000.0
        fall_time += dt
        level_time += dt

        if level_time > 10:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.02

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                if paused:
                    continue

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    # hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        if paused:
            draw_window(win, grid, score)
            draw_text_middle(win, "PAUSED", 60, WHITE)
            pygame.display.update()
            continue

        if fall_time >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for pos in shape_pos:
            x, y = pos
            if y >= 0:
                grid[y][x] = current_piece.color

        # if piece hit the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # clear rows and update score
            cleared = clear_rows(grid, locked_positions)
            if cleared > 0:
                score += (cleared ** 2) * 100

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_window(win, grid, score)
            draw_text_middle(win, "GAME OVER", 60, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)

            # wait for R to restart or quit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                            return
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            return


if __name__ == '__main__':
    main()
