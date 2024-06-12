import math
import sys
from itertools import combinations


class EdgeColor:
    def __init__(self,vertex_num) -> None:
        self.vertex_num = vertex_num
        self.edge_colors = [[-1 for _ in range(self.vertex_num)]\
                                for _ in range(self.vertex_num)] # 
        
        
    def calculate(self):
        edges = list(combinations(range(self.vertex_num), 2))
        for vertex0, vertex1 in edges:
            k4_list = self.get_k4_edges(vertex0,vertex1)
            black_weight = 0
            white_weight = 0
            for edge_list in k4_list:
                black_num = 0
                white_num = 0
                for edge in edge_list:
                    if self.edge_colors[edge[0]][edge[1]] == 0:
                        black_num += 1
                    elif self.edge_colors[edge[0]][edge[1]] == 1:
                        white_num += 1
                black_weighti = self.calculate_weight(black_num+1, white_num)
                white_weighti = self.calculate_weight(black_num, white_num+1)
                black_weight += black_weighti
                white_weight += white_weighti

            if black_weight < white_weight:
                self.edge_colors[vertex0][vertex1] = 0
                self.edge_colors[vertex1][vertex0] = 0
            else:
                self.edge_colors[vertex0][vertex1] = 1
                self.edge_colors[vertex1][vertex0] = 1

        actual_k4_num = self.count_k4()
        expection_k4_num = math.comb(self.vertex_num, 4) * (2**-5)
        return actual_k4_num, expection_k4_num
    
    def get_k4_edges(self, vertex0, vertex1):
        k4_list = []
        vertexes_condinate = list(combinations(range(self.vertex_num), 2))
        for vertex2, vertex3 in vertexes_condinate:
            if  vertex2 == vertex0 or vertex2 == vertex1 \
            or vertex3 == vertex0 or vertex3 == vertex1: 
                continue
            vertexes = [vertex0, vertex1, vertex2, vertex3]
            edges = list(combinations(vertexes, 2))
            k4_list.append(edges)
        return k4_list

    def calculate_weight(self, black_num:int, white_num:int):
        colored_num = black_num + white_num
        if colored_num == 0:
            return 2**(-5) # case 1
        elif black_num != 0 and white_num != 0:
            return 0 # case 2
        else:
            return 2**(-(6-colored_num)) # case 3

    def plot_result(self):
        import matplotlib.pyplot as plt
        import networkx as nx
        G = nx.Graph()
        vertexes_condinate = list(combinations(range(self.vertex_num), 2))
        for vetex0, vetex1 in vertexes_condinate:
            if self.edge_colors[vetex0][vetex1] == 0:
                G.add_edge(vetex0, vetex1, color='red')
            else:
                G.add_edge(vetex0, vetex1, color='blue')
        pos = nx.spring_layout(G)
        edges = G.edges()
        colors = [G[u][v]['color'] for u,v in edges]
        nx.draw(G, pos, edge_color=colors)
        plt.title(f"vertex_num:{self.vertex_num}")
        plt.show()
        plt.savefig(f"result_{self.vertex_num}.png")

    def count_k4(self):
        k4_num = 0
        all_vertex_combination = list(combinations(range(self.vertex_num), 4))
        for vertexes in all_vertex_combination:
            edges = list(combinations(vertexes, 2))
            colors = [self.edge_colors[edge[0]][edge[1]] for edge in edges]
            if colors.count(0) == 6 or colors.count(1) == 6:
                k4_num += 1
        return k4_num

if __name__ == "__main__":
    vertex_num = 10
    if len(sys.argv) > 1:
        vertex_num = int(sys.argv[1])
    edge_color = EdgeColor(vertex_num)
    actual_k4_num, expection_k4_num = edge_color.calculate()
    print(f"actual_k4_num:{actual_k4_num}, expection_k4_num:{expection_k4_num}")
    edge_color.plot_result()