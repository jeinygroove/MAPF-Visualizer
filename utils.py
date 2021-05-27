class Map:

    # Default constructor
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []

    # Initialization of map by string.
    def ReadFromString(self, cellStr, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                # TODO
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)


def ReadMapFromMovingAIFile(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        height = int(lines[1].split()[1])
        width = int(lines[2].split()[1])
        s = ''.join(lines[4:])

        def map_sym(c: str):
            if c.isspace():
                return c
            elif (c == '@') or (c == 'T'):
                return '#'
            else:
                return '.'

        m = Map()
        m.ReadFromString(''.join(map(map_sym, s)), width, height)
        return m

def ReadAgentsPathsFromFile(path):
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        paths = []

        curr_path = []
        for l in lines:
            digits = l.split(' ')
            if len(digits) == 1:
                paths.append(curr_path)
                curr_path = []
            elif len(digits) == 3:
                curr_path.append((int(digits[0]), int(digits[1]), int(digits[2])))
            else:
                raise Exception("Incorrect paths file")

        return paths[1:]
