import pygame
import numpy
from sys import exit

SCREEN_WIDTH = 605
SCREEN_HEIGHT = 705
GAME_SURF_HEIGHT = 605
GAME_SURF_WIDTH = 605


class Cursor(pygame.sprite.Sprite):
    def __init__(self, shape):
        super().__init__()
        if shape == 'cross':
            pygame.mouse.set_visible(False)
            self.image = pygame.image.load('cross_cursor.png').convert_alpha()
        elif shape == 'circle':
            pygame.mouse.set_visible(False)
            self.image = pygame.image.load('circle_cursor.png').convert_alpha()
        else:
            raise TypeError
        self.rect = self.image.get_rect()

    def move(self, new_pos, screen):
        self.rect.center = new_pos
        screen.blit(self.image, self.rect)


class GameBoard:
    def __init__(self):
        """
        This function creates a GameBoard object which contains a pygame Group of cells (see class 'Cell), a surface
        and a rectangle.
        """
        self.cells = pygame.sprite.Group()
        self.surf = pygame.Surface((GAME_SURF_WIDTH, GAME_SURF_HEIGHT))
        self.rect = self.surf.get_rect(bottomleft=(0, SCREEN_HEIGHT))
        for cell_num in range(9):
            self.cells.add(Cell(cell_num))

    def draw(self, display):
        display.blit(self.surf, self.rect)
        self.cells.draw(display)

    def update_cell(self, cell_num, shape):
        self.cells.sprites()[cell_num].set_shape(shape)


class Grid:
    def __init__(self, board_rect):

        # creating line surfaces
        self.vertical_line_surf = pygame.surface.Surface((1, board_rect.height))
        self.vertical_line_surf.fill('White')
        self.horizontal_line_surf = pygame.surface.Surface((board_rect.width, 1))
        self.horizontal_line_surf.fill('White')

        # runtime-reducing variables
        third_of_height = board_rect.height / 3
        third_of_width = board_rect.width / 3
        board_rect_top = board_rect.top
        board_rect_left = board_rect.left

        self.vertical_placement_1 = (board_rect_left + third_of_width, board_rect_top)
        self.vertical_placement_2 = (board_rect.right - third_of_width, board_rect_top)
        self.horizontal_placement_1 = (board_rect_left, board_rect_top + third_of_height)
        self.horizontal_placement_2 = (board_rect_left, board_rect.bottom - third_of_height)

    def draw(self, display):
        display.blit(self.vertical_line_surf, self.vertical_placement_1)
        display.blit(self.vertical_line_surf, self.vertical_placement_2)
        display.blit(self.horizontal_line_surf, self.horizontal_placement_1)
        display.blit(self.horizontal_line_surf, self.horizontal_placement_2)


class Cell(pygame.sprite.Sprite):
    def __init__(self, cell_pos: int):
        """
        The 'Cell' object is used to describe a TicTacToe cell by giving it a position, the cell's displayed shape may
        be changed using the set_shape() function
        :param cell_pos: the cell's position on the board - between 0 - 8
        :type cell_pos: int
        """
        super().__init__()
        self.is_previewed = False
        self.cell_number = cell_pos
        self.coordinates = get_cell_coordinates(self.cell_number)
        self.contents = 'empty'
        self.image = pygame.image.load('empty.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.coordinates)

    def set_shape(self, shape):
        if not self.is_previewed:
            self.contents = shape
        self.image = pygame.image.load(f'{shape}.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.coordinates)

    def get_contents(self) -> str:
        """
        This function gets the contents of the cell
        :return: the cell's contents ('empty' | 'cross' | 'circle')
        """
        return self.contents

    def start_preview(self, shape):
        """
        This function starts a shape preview on the cell
        :param shape: the chosen shape
        :type shape: str
        :return: None
        :rtype: NoneType
        """
        self.is_previewed = True
        self.set_shape(f'transparent_{shape}')

    def end_preview(self):
        """
        This function starts the preview on the cell
        :return: None
        :rtype: NoneType
        """
        self.is_previewed = False
        self.set_shape('empty')

    def is_empty(self):
        """
        This function checks for cell emptiness
        :return: is the cell empty
        :rtype: bool
        """
        return self.contents == 'empty'


def get_cell_coordinates(cell_number) -> tuple:
    """
    This function returns the coordinates of the cells center
    :return: the cell's center coordinates
    :rtype: tuple
    """
    return ((cell_number % 3)*2 + 1)*SCREEN_WIDTH/6, (numpy.floor(cell_number/3)*2 + 1)*(SCREEN_HEIGHT-100)/6 + 100


def easy_ai_place_shape(board, shape):
    """
    This function places the enemy's shape at a random position
    :param board: the game board
    :type board: GameBoard
    :param shape: the shape to place
    :type shape: str
    :return: None
    :rtype: NoneType
    """
    cell_num = numpy.random.randint(0, 9)
    while not board.cells.sprites()[cell_num].is_empty():
        cell_num = numpy.random.randint(0, 9)
    board.update_cell(cell_num, shape)


def medium_ai_place_shape(board, shape):
    # TODO
    pass


def hard_ai_place_shape(board, shape):
    # TODO
    pass


def change_cursor(chosen_shape, screen, mouse_pos):
    """
    This function changes the cursor image into the shape that the player has chosen
    :param mouse_pos: the current position of the mouse
    :type mouse_pos: tuple
    :param screen: the display screen
    :type screen: pygame display
    :param chosen_shape: the shape that the player has chosen
    :type chosen_shape: str ('X' or 'O')
    :return: the new cursor rectangle
    :rtype: pygame rectangle
    """
    pygame.mouse.set_visible(False)
    cursor = Cursor(chosen_shape)
    cursor.move(mouse_pos, screen)
    return cursor


def start_game_animation(screen):
    """
    This function shows a cool startup animation for the game
    :param screen: the display screen
    :type screen: pygame surface
    :return: None
    :rtype: NoneType
    """
    pass  # TODO learn to make animations


def print_shapes(screen):
    """
    This function prints the shape option to the user
    :param screen: the display screen
    :type screen: pygame display
    :return: the rectangle oof the printed shapes (for easier collision detection later)
    :rtype: tuple[pygame rectangle]
    """
    text_surf = pygame.font.SysFont('Comic sans', 40).render('Chose your shape:', True, 'deeppink')
    text_rect = text_surf.get_rect(midtop=(SCREEN_WIDTH / 2, 50))

    circle_surf = pygame.image.load('circle.png').convert_alpha()
    circle_rect = circle_surf.get_rect(center=(SCREEN_WIDTH/3, SCREEN_HEIGHT*2/3))
    cross_surf = pygame.image.load('cross.png').convert_alpha()
    cross_rect = cross_surf.get_rect(center=(SCREEN_WIDTH*2/3, SCREEN_HEIGHT*2/3))

    screen.blit(cross_surf, circle_rect)
    screen.blit(circle_surf, cross_rect)
    screen.blit(text_surf, text_rect)

    return cross_rect, circle_rect


def chose_shape(circle_rect: pygame.rect.RectType, cross_rect: pygame.rect.RectType, mouse_pos):
    """
    This functions return the clicked shape (if a shape was clicked)
    :param mouse_pos: the current cursor coordinates
    :type mouse_pos: tuple
    :param circle_rect: the circle rectangle
    :type circle_rect: pygame rectangle
    :param cross_rect: the cross rectangle
    :type cross_rect: pygame rectangle
    :return: the chosen shape (or None)
    :rtype: str
    """
    if circle_rect.collidepoint(mouse_pos):
        return 'circle'
    if cross_rect.collidepoint(mouse_pos):
        return 'cross'
    # else: return None


def cls(screen):
    """
    This function clears the display screen
    :param screen: the display screen
    :type screen: pygame display
    :return: None
    :rtype: NoneType
    """
    screen.fill('Black')
    pygame.display.update() # #


def place_shape(board, mouse_pos, shape):
    """
    This function places the chosen shape on the selected cell
    :param board: the game board
    :type board: GameBoard
    :param mouse_pos: the current cursor coordinates
    :type mouse_pos: tuple
    :param shape: the shape chosen by the player ('cross' | 'circle')
    :type shape: str
    :return: was a shape placed
    :rtype: bool
    """
    for cell in board.cells:
        if cell.is_empty() and cell.rect.collidepoint(mouse_pos):
            cell.is_previewed = False
            cell.set_shape(shape)
            return True
    return False


def show_preview(board, mouse_pos, shape):
    """
    This function shows a preview of the shape on the current hovered cell
    :param board: the game board
    :type board: GameBoard
    :param mouse_pos: the current cursor coordinates
    :type mouse_pos: tuple
    :param shape: the player's shape
    :type shape: str ('circle | 'cross')
    :return: None
    :rtype: NoneType
    """
    for cell in board.cells:
        if cell.is_empty() and cell.rect.collidepoint(mouse_pos):
            if not cell.is_previewed:
                cell.start_preview(shape)
        elif cell.is_previewed and not cell.rect.collidepoint(mouse_pos):
            cell.end_preview()


def check_for_win(board):
    for shape in ('circle', 'cross'):



def main():
    # initializing pygame
    pygame.init()

    # creating clock and display objects
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # defining game state keepers
    game_active = False
    game_choosing_shape = False  # the game is started by choosing the shape TODO change

    # opening game screen
    start_game_animation(screen)

    # letting player chose desired shape (X | O)
    game_choosing_shape = True
    shapes = print_shapes(screen)

    # creating the game board and gridlines
    board = GameBoard()
    grid = Grid(board.rect)

    while True:
        for event in pygame.event.get():
            # if game window has been closed
            if event.type == pygame.QUIT:
                pygame.quit()
                print('Thanks for playing tic tac toe!\n'
                      'Goodbye!')
                exit()

            # if mouse has been clicked
            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if board.rect.collidepoint(mouse_pos):
                        was_placed = place_shape(board, mouse_pos, chosen_shape)
                        winner = check_for_win(board)
                        if winner:
                            game_active = False
                            if winner == chosen_shape:
                                pass  # TODO
                            else:
                                pass  # TODO
                        elif was_placed:
                            easy_ai_place_shape(board, enemy_shape)
                    else:
                        pass  # TODO 'change_settings(params)'
            elif game_choosing_shape:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chosen_shape = chose_shape(*shapes, mouse_pos)
                    if chosen_shape:
                        cursor = Cursor(chosen_shape)
                        game_choosing_shape = False
                        game_active = True

                        if chosen_shape == 'circle':
                            enemy_shape = 'cross'
                        else:
                            enemy_shape = 'circle'

        mouse_pos = pygame.mouse.get_pos()
        if game_active:
            show_preview(board, mouse_pos, chosen_shape)
            board.draw(screen)
            grid.draw(screen)
            cursor.move(mouse_pos, screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
