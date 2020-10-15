class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'(X, Y): ({self.x}, {self.y})' + '\n'
