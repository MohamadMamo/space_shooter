# entity.py


class Entity:
    """Base for everything drawn and moved on screen.

    Movement is accumulated in floats and only rounded into the integer rect,
    so slow sprites are not lost to truncation at high frame rates. The float
    position and the rect are kept in sync in one place: assign a position via
    set_center()/set_topleft() rather than touching .rect directly, or the next
    move() will snap the sprite back to where the floats still point.
    """

    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        self._x = float(self.rect.x)
        self._y = float(self.rect.y)

    def sync_from_rect(self):
        """Adopt the rect's current position as the float position."""
        self._x = float(self.rect.x)
        self._y = float(self.rect.y)

    def set_center(self, x, y):
        self.rect.center = (x, y)
        self.sync_from_rect()

    def set_topleft(self, x, y):
        self.rect.topleft = (x, y)
        self.sync_from_rect()

    def move_by(self, dx, dy):
        """Shift by a float offset, updating the rect."""
        self._x += dx
        self._y += dy
        self.rect.topleft = (round(self._x), round(self._y))

    def draw(self, win):
        win.blit(self.image, self.rect)
