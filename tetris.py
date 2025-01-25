#
#                                           $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  $$$$$$\  $$$$$$\  
#                                           \__$$  __|$$  _____|\__$$  __|$$  __$$\ \_$$  _|$$  __$$\ 
#                                              $$ |   $$ |         $$ |   $$ |  $$ |  $$ |  $$ /  \__|
#                                              $$ |   $$$$$\       $$ |   $$$$$$$  |  $$ |  \$$$$$$\  
#                                              $$ |   $$  __|      $$ |   $$  __$$<   $$ |   \____$$\ 
#                                              $$ |   $$ |         $$ |   $$ |  $$ |  $$ |  $$\   $$ |
#                                              $$ |   $$$$$$$$\    $$ |   $$ |  $$ |$$$$$$\ \$$$$$$  |
#                                              \__|   \________|   \__|   \__|  \__|\______| \______/ 
#                                                                    by z4nk                                    
#
#        Bienvenido a mi versión de Tetris, creado por Z4nk. En el archivo SECURITY.md encontrarás los términos y condiciones que aceptas al usar este código.
#        Sé que puede sonar ridículo incluir términos y condiciones en un repositorio de GitHub, considerando que al subir un repositorio ya estás aceptando los términos y condiciones de GitHub. Sin embargo, lo hago por seguridad. 
#        Me veo obligado a tomar esta medida, aunque parezca exagerado, porque en proyectos anteriores algunas personas han utilizado mis repositorios para ventas ilegales o se han hecho pasar por mí con fines maliciosos. Por eso considero necesario incluir esta aclaración.
#
#
#        Así que, si usas este código sin leer el archivo "SECURITY.md", no me hago responsable de las acciones que cometas ni de los problemas que causes o enfrentes.
#        Además, quiero dejar en claro que este código no puede ser vendido ni compartido a cambio de dinero o cualquier actividad que implique fines lucrativos. Lo he compartido de manera gratuita.
#        Si deseas compartir este código con fines comerciales, estarías incurriendo en un acto ilegal. No obstante, podríamos colaborar en algún otro proyecto si estás interesado en desarrollar algo que sí podamos vender de forma legítima.
#
#                            Discord: https://discord.gg/rc3gZSf2g9       GitHub: https://github.com/z44nkkk


import pygame
import random

pygame.init()


print("TETRIS HECHO Y DESARROLLADO POR: Z4NK")
print("GitHub: https://github.com/z44nkkk")
print("Discord: https://discord.gg/rc3gZSf2g9")


# Constantes del juego Tetris

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colores
BLACK = (0, 0, 0) # Negro para el fondo
WHITE = (255, 255, 255) # Blanco para el texto
CYAN = (0, 255, 255) # Pieza I
BLUE = (0, 0, 255) # Pieza J
ORANGE = (255, 165, 0) # Pieza L
YELLOW = (255, 255, 0) # Pieza O
GREEN = (0, 255, 0) # Pieza S
PURPLE = (128, 0, 128) # Pieza T
RED = (255, 0, 0) # Pieza Z
GRAY = (128, 128, 128) # Líneas de la cuadrícula

# Formas de las figuras
SHAPES = [
    [[1, 1, 1, 1]], # Forma I
    [[1, 0, 0], [1, 1, 1]], # Forma J
    [[0, 0, 1], [1, 1, 1]], # Forma L
    [[1, 1], [1, 1]], # Forma O
    [[0, 1, 1], [1, 1, 0]], # Forma S
    [[0, 1, 0], [1, 1, 1]], # Forma T
    [[1, 1, 0], [0, 1, 1]] # Forma Z
]

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

# Empezamos con las clases

class Tetromino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_idx]]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape) - 1, -1, -1)] for x in range (len(self.shape[0]))]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.font = pygame.font.Font(None, 36)
    
    def valid_move(self, piece, x, y):
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or (y +i >= 0 and self.grid[y + i][x + j] != BLACK)):
                        return False
        return True
    
    def lock_place(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    if self.current_piece.y + i <= 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

        if not self.game_over:
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()

            # Verificar si la nueva pieza puede entrar en el tablero
            for i in range(len(self.current_piece.shape)):
                for j in range(len(self.current_piece.shape[i])):
                    if (self.current_piece.shape[i][j] and self.grid[self.current_piece.y + i][self.current_piece.x + j] != BLACK):
                        self.game_over = True
                        return
    
    def clear_lines(self):
        lines_cleared = 0
        for i in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            if lines_cleared:
                self.score += (100 * lines_cleared)
    
    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, GRAY, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    pygame.draw.rect(self.screen, self.current_piece.color, ((self.current_piece.x + j) * BLOCK_SIZE, (self.current_piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        next_piece_text = self.font.render('Siguiente', True, WHITE)
        self.screen.blit(next_piece_text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[i])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(self.screen, self.next_piece.color, (GRID_WIDTH * BLOCK_SIZE + 20 + j * BLOCK_SIZE, 80 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        score_text = self.font.render(f'Puntuaje: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 200))

    def run(self):
        while not self.game_over:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece.x -1, self.current_piece.y):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        original_shape = [row[:] for row in self.current_piece.shape]
                        self.current_piece.rotate()
                        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                            self.current_piece.shape = original_shape
            if self.fall_time >= self.fall_speed:
                if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.lock_place()
                self.fall_time = 0
            self.screen.fill(BLACK)
            self.draw_grid()
            pygame.display.flip()

        game_over = True

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
            
            # Oscurecer el fondo
            dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surface.fill(BLACK)
            dark_surface.set_alpha(128)
            self.screen.blit(dark_surface, (0, 0))

            # Mostrar mensaje de Game Over
            game_over_text = self.font.render('¡Game Over¡!', True, WHITE)
            score_text = self.font.render(f'Puntuaje: {self.score}', True, WHITE)
            continue_text = self.font.render('Presiona X para salir', True, WHITE)

            # Posicionar textos
            text_y = SCREEN_HEIGHT // 2 - 60
            for text in [game_over_text, score_text, continue_text]:
                text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
                self.screen.blit(text, (text_x, text_y))
                text_y += 40

            pygame.display.flip()

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
    pygame.quit()