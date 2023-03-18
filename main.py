from CSP import GraphColoringCSP


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


if __name__ == '__main__':

    graph, num_colors = read_graph("test6.txt")
    colors = list(range(num_colors))
    csp = GraphColoringCSP(graph, colors)
    solution = csp.backtracking_search()
    print("Solution(node,color):{0} ".format(solution))

