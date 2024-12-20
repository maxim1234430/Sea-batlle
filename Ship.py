class Ship:
    def __init__(self, length, orientation, start_x, start_y):
        self.length = length
        self.orientation = orientation  # 'horizontal' или 'vertical'
        self.coord_map = []
        self.status_map = []
        self.death = 0  # 0 - жив, 1 - убит

        for i in range(length):
            if self.orientation == 'horizontal':
                x = start_x + i
                y = start_y
            else:
                x = start_x
                y = start_y + i
            self.coord_map.append((x, y))
            self.status_map.append(0)

    def shoot(self, x, y):
        """
        Возвращает:
        0 - мимо,
        1 - попали, но ещё не убит,
        2 - убит корабль.
        """
        if (x, y) in self.coord_map:
            index = self.coord_map.index((x, y))
            self.status_map[index] = 1
            if all(s == 1 for s in self.status_map):
                self.death = 1
                return 2
            return 1
        return 0