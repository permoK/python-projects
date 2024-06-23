class Node:
    def __init__(self, name):
        self.name = name
        self.outgoing = []
        self.incoming = []
        self.visited = False

class Arc:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.marked = False

class Graph:
    def __init__(self):
        self.nodes = {}
        self.arcs = []

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_arc(self, source, target):
        self.add_node(source)
        self.add_node(target)
        arc = Arc(source, target)
        self.arcs.append(arc)
        self.nodes[source].outgoing.append(arc)
        self.nodes[target].incoming.append(arc)

def detect_deadlock(graph):
    L = []
    for node_name in graph.nodes:
        node = graph.nodes[node_name]
        if not node.visited:
            if _detect_cycle(graph, node, L):
                return True, L
    return False, L

def _detect_cycle(graph, node, L):
    L.append(node.name)
    node.visited = True

    for arc in node.outgoing:
        if not arc.marked:
            arc.marked = True
            if arc.target.name in L:
                return True
            elif _detect_cycle(graph, arc.target, L):
                return True
            arc.marked = False

    L.pop()
    return False

def parse_input_file(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(' ')
                source = parts[0]
                target = parts[2][:-1]
                graph.add_arc(source, target)
    return graph

def print_graph(graph):
    for arc in graph.arcs:
        print(arc.source, '->', arc.target)

def main():
    filename = 'input.txt'
    graph = parse_input_file(filename)
    print("Input Graph:")
    print_graph(graph)
    deadlock, L = detect_deadlock(graph)
    if deadlock:
        print("\nDeadlock detected!")
        print("List L:", L)
    else:
        print("\nNo deadlock detected.")

if __name__ == "__main__":
    main()

