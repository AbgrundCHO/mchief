from graph.utils import link2neo4j

class MainGraph:
    def __init__(self):
        self.graph = link2neo4j()


if __name__ == '__main__':
    a = MainGraph()
    print(a.graph)
