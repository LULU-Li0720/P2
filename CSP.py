from collections import defaultdict, deque


class GraphColoringCSP:
    def __init__(self, graph, colors):
        self.graph = graph
        self.colors = colors
        self.domain = defaultdict(lambda: list(colors))

    def constraint_satisfied(self, node, color, assignment):
        for neighbor in self.graph[node]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    #ac3
    def ac3(self, queue=None):
        if queue is None:
            queue = deque([(node, neighbor) for node in self.graph for neighbor in self.graph[node]])
        while queue:
            node1, node2 = queue.popleft()
            if self.revise(node1, node2):
                if not self.domain[node1]:
                    return False
                for neighbor in self.graph[node1]:
                    if neighbor != node2:
                        queue.append((neighbor, node1))
        return True

    def revise(self, node1, node2):
        revised = False
        for color1 in self.domain[node1]:
            if all(not self.constraint_satisfied(node1, color1, {node2: color2}) for color2 in self.domain[node2]):
                self.domain[node1].remove(color1)
                revised = True
        return revised

    # MRV
    def select_unassigned_variable(self, assignment):
        unassigned = [node for node in self.graph if node not in assignment]
        mrv_counts = [(node, len(self.domain[node])) for node in unassigned]
        min_count = min(count for node, count in mrv_counts)
        min_nodes = [node for node, count in mrv_counts if count == min_count]
        if len(min_nodes) == 1:
            return min_nodes[0]
        else:
            return max(min_nodes, key=lambda node: len(self.graph[node]))

    # LCV
    def order_domain_values(self, node, assignment):
        def count_conflicts(color):
            return sum(1 for neighbor in self.graph[node] if neighbor in assignment and assignment[neighbor] == color)
        return sorted(self.domain[node], key=count_conflicts)


    def backtracking_search(self, assignment={}):

        if len(assignment) == len(self.graph):
            return assignment
        # MRV
        node = self.select_unassigned_variable(assignment)
        # LCV
        for color in self.order_domain_values(node, assignment):
            if self.constraint_satisfied(node, color, assignment):
                assignment[node] = color
                self.domain[node] = [color]
                inferences = self.inference(node, assignment)
                if inferences:
                    result = self.backtracking_search(assignment)
                    if result is not None:
                        return result
                del assignment[node]
                self.restore_domain(node)

        return None

    def inference(self, node, assignment):
        self.domain[node] = [assignment[node]]
        queue = deque([(neighbor, node) for neighbor in self.graph[node] if neighbor not in assignment])
        if self.ac3(queue):
            return True
        else:
            self.restore_domain(node)
            return False

    def restore_domain(self, node):
        self.domain[node] = list(self.colors)

def read_graph(filename):
    graph = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if "colors" in line:
                    num_colors = int(line.split("=")[-1].strip())
                else:
                    v1, v2 = map(int, line.strip().split(','))
                    if v1 not in graph:
                        graph[v1] = set()
                    if v2 not in graph:
                        graph[v2] = set()
                    graph[v1].add(v2)
                    graph[v2].add(v1)
    return graph, num_colors