from baduk.exceptions import ValidationError
from baduk.constants import ALPHA_KEY


class Point:
    def __init__(self, x=None, y=None, coordinate=None):
        if coordinate is not None and len(coordinate) != 2:
            raise ValidationError('Coordinate format is invalid')
        if coordinate:
            self.parse_coordinate(coordinate)
        elif x is not None and y is not None:
            self.parse_x_y(x, y)
        else:
            raise ValidationError('Needs to be passed a coordinate or x and y')

    def __repr__(self):
        return self.coordinate.upper()

    def parse_coordinate(self, coordinate):
        self.coordinate = coordinate
        alpha = coordinate[1]
        self.x = int(ALPHA_KEY.index(alpha))
        self.y = int(coordinate[0]) - 1

    def parse_x_y(self, x, y):
        self.coordinate = '%d%s' % (y + 1, ALPHA_KEY[x])
        self.x = x
        self.y = y

    def adjacent_points(self):
        return [
            {"x": self.x + 1, "y": self.y},
            {"x": self.x - 1, "y": self.y},
            {"x": self.x, "y": self.y + 1},
            {"x": self.x, "y": self.y - 1}
        ]

    def map_adjacent_links(self, callable, board):
        for adjacent_point in self.adjacent_points():
            if board.in_grid(adjacent_point):
                yield callable(board.get_point(**adjacent_point), board)

    def filter_adjacent_links(self, callable, board):
        for adjacent_point in self.adjacent_points():
            if board.in_grid(adjacent_point):
                link = board.get_point(**adjacent_point)
                if callable(link):
                    yield link