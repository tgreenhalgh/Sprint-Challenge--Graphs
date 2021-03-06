"""
Simple graph implementation compatible with BokehGraph class.
"""


class Vertex:
    def __init__(self, label, component=-1):
        self.label = str(label)
        self.component = component

    def __repr__(self):
        return 'Vertex: ' + self.label

    """Trying to make this Graph class work..."""


class Graph:
    def __init__(self):
        self.vertices = {}
        self.components = 0

    def add_vertex(self, vertex, edges=()):
        # check to make sure vertex doesn't already exist
        if vertex in self.vertices:
            raise Exception(
                'ERROR: The vertex {} already exists!'.format(vertex))
        # check to make sure the vertices for the edges do exist
        if not set(edges).issubset(self.vertices):
            raise Exception("ERROR: One or more vertices don't exist")
        self.vertices[vertex] = set(edges)

    def add_edge(self, start, end, bidirectional=True):
        # make sure vertices exist
        if start not in self.vertices or end not in self.vertices:
            raise Exception("ERROR: One or more vertices don't exist")
        # start should connect to end
        self.vertices[start].add(end)
        if bidirectional:
            # end should connect to start
            self.vertices[end].add(start)

    def dfs(self, start, target=None):
        # DSF wants a stack - LIFO
        stack = []
        stack.append(start)
        # keep track of visited verts in case there's a loop
        visited = set([start])

        # keep going as long as there are verts in the stack
        while stack:
            current_vert = stack.pop()
            if current_vert == target:
                break
            # remove the visted verts (appends the set subtraction)
            stack.extend(self.vertices[current_vert] - visited)
            # update visted (set union: visited U vertices[vert])
            visited.update(self.vertices[current_vert])

        return visited

# removed TARGET so will work with find_components method below
    # def graph_rec(self, start, target, visited=[], path=[]):
    def graph_rec(self, start, visited=[], path=[]):
        # update visited and path with the current vert
        visited.append(start)
        path.append(start)

        # check to see if we've hit the target
        # if start == target:
        #     return path

        for child_vert in self.vertices[start]:
            # only check verts not in visited
            if child_vert not in visited:
                new_path = self.graph_rec(child_vert, target, visited, path)
                #  when the recursion unrolls, see if we have a new_path
                if new_path:
                    return new_path
        return path

    def find_components(self):
        visited = set()
        current_component = 0

        for vertex in self.vertices:
            # check vertices NOT in visited
            if vertex not in visited:
                reachable = self.dfs(vertex)
                for other_vertex in reachable:
                    other_vertex.component = current_component
                current_component += 1
                visited.update(reachable)
        self.components = current_component
