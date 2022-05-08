import copy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'''
            Point:
                x: {self.x}
                y: {self.y}
            '''

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def get_random_point():
        return Point(1, 1)

    def print(self):
        print('(' + str(self.x) + ', ' + str(self.y) + ')')

    def draw(self, ax):
        self.figure = ax.plot(self.x, self.y, 'go')

    def set_direction(self, vector):
        self.direction = vector[0]
        self.speed = vector[1]

    def move(self):
        self.x += self.direction.x
        self.y += self.direction.y

    def next(self):
        self.x += self.direction.x
        self.y += self.direction.y

    def stop(self):
        self.direction.x = 0
        self.direction.y = 0

    def get_next_state(self):
        next_state = copy.deepcopy(self)
        next_state.next()
        return next_state

    def reflect_direction(self):
        self.direction.x = -self.direction.x
        self.direction.y = -self.direction.y

    def copy(self):
        return Point(self.x, self.y)