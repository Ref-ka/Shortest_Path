class Info:

    def __init__(self):
        self.connections = []
        self.vertexes = {}
        self.src = None

    def get_connections(self) -> list:
        return self.connections

    def get_vertexes_count(self) -> int:
        return len(self.vertexes)

    def get_vertexes(self) -> dict:
        return self.vertexes

    def get_src(self) -> int:
        return self.src

    def insert_connection(self, line):
        self.connections.append(line)
        for i in range(2):
            if line[i] not in self.vertexes:  # Counter of vertexes
                self.vertexes[line[i]] = 1
            else:
                self.vertexes[line[i]] += 1

    def delete_connection(self, line):
        self.connections.remove(line)
        for i in range(2):
            if self.vertexes[line[i]] > 1:  # Change vertex counter when delete some connection
                self.vertexes[line[i]] -= 1
            else:
                self.vertexes.pop(line[i])  # If amount of vertex equals 1 we delete this vertex from dict

    def insert_src(self, src):
        self.src = src

    def connection_check(self, line) -> tuple:
        for connection in self.connections:
            if line[:2] == connection[:2]:  # Check if inserting line already was inserted but with another weight
                if line[2] == connection[2]:
                    return True, False  # Same connection already exist
                else:
                    return True, True  # Connection already exist but with another weight
        return False, False  # Connection doesn't exist

    def clear(self):
        self.connections = []
        self.vertexes = {}
        self.src = None
