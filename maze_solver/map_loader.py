import json

class Checkpoint:

    def __init__(self,value,coordinates):
        self.value = value
        self.coordinates = coordinates

    def __lt__(self,other):
        return self.value < other.value

class Map:

    DEFAULT_SETTINGS = '{"wall_char": "#", "passable_char": "."}'

    def __init__(self,walls=None,checkpoints=None,settings=None):
        if walls == None:
            self.walls = [[]]
        else:
            self.walls = walls

        if checkpoints == None:
            self.checkpoints = []
        else:
            self.checkpoints = checkpoints

        if settings == None:
            self.settings = json.loads(Map.DEFAULT_SETTINGS)
        else:
            self.settings = json.loads(settings)

    def __str__(self):
        map_str_arr = []

        for i in range(0,len(self.walls)):
            row_arr = [ self.settings['wall_char'] if x else self.settings['passable_char'] \
                    for x in self.walls[i] ]
            map_str_arr.append(row_arr)

        for checkpoint in self.checkpoints:
            i, j = checkpoint.coordinates
            map_str_arr[i][j] = str(checkpoint.value)

        for i, line in enumerate(map_str_arr):
            map_str_arr[i] = ''.join(x for x in line)
            
        return '\n'.join(x for x in map_str_arr)

    @staticmethod
    def load_map_from_file(file_name,settings=None):
        map_file = open(file_name,'r')

        # Settings is in JSON format
        # See DEFAULT_SETTINGS for required data
        if settings == None:
            settings_data = json.loads(Map.DEFAULT_SETTINGS)
        else:
            settings_data = json.loads(settings)

        cur_line = map_file.readline()

        cols = len(cur_line) - 1
        rows = 0

        # Rewind file
        map_file.seek(0)

        walls = []
        checkpoints = []

        # Get the unppassable parts of the maps and the checkpoints
        for i, line in enumerate(map_file):

            # Check number of columns
            if len(cur_line) - 1 != cols:
                raise MapLoadingError("Expected {} columns, got {}".format(cols,len(cur_line)), i)

            row_walls = [False] * cols

            for j in range(0,cols):
                row_walls[j] = line[j] == settings_data["wall_char"]

                if line[j].isdigit():
                    checkpoint = Checkpoint(int(line[j]),(i,j))
                    checkpoints.append(checkpoint)

            walls.append(row_walls)
            checkpoints = sorted(checkpoints)

        map_file.close()

        return Map(walls,checkpoints,settings)

class MapError(Exception):
    pass

class MapLoadingError(MapError):

    def __init__(self, message, line):
        self.message = message
        self.line = line
