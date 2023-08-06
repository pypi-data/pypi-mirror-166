import random
try:
    import pygame
except ModuleNotFoundError:
    raise ModuleNotFoundError("Pygame is required for the use of Pygrille. Please install it for Pygrille to work correctly.")


class Pixel:
    def __init__(self, x_pos: int, y_pos: int, colour: tuple, extras: list = None, image: pygame.Surface = None):
        if extras is None:
            extras = []
        self.colour = colour
        self.extras = dict.fromkeys(extras)
        self.label = (x_pos, y_pos)
        self.pos = (x_pos, y_pos)
        self.image = image

    def __repr__(self):
        return str(self.label)


class Grid:
    def __init__(self, screen: pygame.Surface, size: list, pixel_size: int, default_colour: tuple, framerate: int, border_width: int, border_colour: tuple, default_image: pygame.Surface, extras: list):
        if extras is None:
            extras = []
        if default_colour is None:
            default_colour = (0, 0, 0)
        self.screen = screen
        self.size = size
        self.default_colour = default_colour
        self.pixel_size = pixel_size
        self.extra_list = extras
        self.framerate = framerate
        self.lastclick = None
        self.newclick = False
        self.lastkey = None
        self.newkey = False
        self.border_width = border_width
        self.border_colour = border_colour
        self.default_image = default_image
        self.grid = list(zip(*[[Pixel(i, j, default_colour, extras, default_image) for i in range(size[1])] for j in range(size[0])]))
        self.clock = pygame.time.Clock()
        self.draw()

    def __repr__(self):
        return "\n".join([str(row) for row in self.grid])

    def __getitem__(self, key):
        return self.grid[key]

    def draw_borders(self):
        for i in range(len(self.grid)):
            pass

    def draw(self):
        self.screen.fill(self.border_colour)
        for i, node_row in enumerate(self.grid):
            for j, node in enumerate(node_row):
                pygame.draw.rect(self.screen, node.colour, pygame.Rect(self.border_width + i*self.pixel_size + i*self.border_width, self.border_width + j*self.pixel_size + + j*self.border_width, self.pixel_size, self.pixel_size))
                if node.image is not None:
                    rect = node.image.get_rect()
                    rect.x = self.border_width + i * self.pixel_size + i * self.border_width
                    rect.y = self.border_width + j * self.pixel_size + + j * self.border_width
                    self.screen.blit(node.image, rect)
        pygame.display.flip()

    def update(self, coords: tuple, *, colour: tuple = None, label: str = None, draw: bool = None, border_colour: tuple = None, **kwargs):
        if draw is None:
            draw = False
        if colour is not None:
            self.grid[coords[0]][coords[1]].colour = colour
        if label is not None:
            self.grid[coords[0]][coords[1]].label = label
        if border_colour is not None:
            self.border_colour = border_colour
        for item in kwargs:
            if item in self.extra_list:
                self.grid[coords[0]][coords[1]].extras[item] = kwargs[item]
            else:
                raise KeyError(f"\"{item}\" does not exist in the possible extras for this pixel")
        if draw:
            self.draw()

    def tick(self):
        self.clock.tick(self.framerate)

    def check_open(self):
        self.newclick = False
        self.newkey = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (pos[0]-self.border_width) % (self.pixel_size+self.border_width) <= self.pixel_size and (pos[1]-self.border_width) % (self.pixel_size+self.border_width) <= self.pixel_size:
                    self.lastclick = (pos[0]//(self.pixel_size+self.border_width), pos[1]//(self.pixel_size+self.border_width))
                    self.newclick = True
            elif event.type == pygame.KEYDOWN:
                self.lastkey = pygame.key.name(event.key)
                self.newkey = True
        return True

    def set_image(self, pos, image_path):
        self.grid[pos[0]][pos[1]].image = load_image(image_path, self.pixel_size)


def random_colour():
    return [random.randint(0, 255) for i in range(3)]


def load_image(image_path, pixel_size):
    return pygame.transform.scale(pygame.image.load(image_path), (pixel_size, pixel_size))


def quit():
    pygame.quit()


def init(pixel_size: int, grid_dimensions: tuple, *, window_name: str = None, default_colour: tuple = None, extras: list = None, framerate: int = None, border_width: int = None, border_colour: tuple = None, default_image: str = None):
    if window_name is None:
        window_name = "pygrille window"
    if framerate is None:
        framerate = 60
    if border_width is None:
        border_width = 0
    if border_colour is None:
        border_colour = (100, 100, 100)
    if default_image is not None:
        default_image = load_image(default_image, pixel_size)
    grid_dimensions = (grid_dimensions[1], grid_dimensions[0])
    pygame.init()
    pygame.display.set_caption(window_name)
    screensize = [2 * border_width + i * pixel_size + (i-1) * border_width for i in grid_dimensions]
    screen = pygame.display.set_mode((screensize[1], screensize[0]))
    grid = Grid(screen, grid_dimensions, pixel_size, default_colour, framerate, border_width, border_colour, default_image, extras)
    return grid
