import random
import networkx as nx
import matplotlib.pyplot as plt


class Vertices:
    def __init__(self, group_id) -> None:
        self.group_id = int(group_id)
        self.cost = [0, 0]


class UniformGraphPartition:
    def __init__(self, n) -> None:
        self.n = n
        self.maxStep = 1000000

    def GenerateData(self):
        self.edge = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    self.edge[i][j] = 0
                    continue
                self.edge[i][j] = random.random()
                self.edge[j][i] = self.edge[i][j]

        self.vertices = [Vertices(i/(self.n/2)) for i in range(self.n)]
        self.partVertices = [[], []]
        self.partVertices[0] = [i for i in range(self.n) if i < self.n/2]
        self.partVertices[1] = [i for i in range(self.n) if i >= self.n/2]
        self.CaluculateCost()

    def CaluculateCost(self):
        self.totalCost = 0
        for i in range(self.n):
            for j in range(self.n):
                self.vertices[i].cost[self.vertices[j].group_id] += self.edge[i][j]
                if self.vertices[i].group_id != self.vertices[j].group_id:
                    self.totalCost += self.edge[i][j]

    def step(self):
        bestCost = 10000
        v1Best = -1
        v2Best = -1
        for v1 in self.partVertices[0]:
            for v2 in self.partVertices[1]:
                dCost = self.vertices[v1].cost[0] + \
                    self.vertices[v2].cost[1] - \
                    self.vertices[v1].cost[1] - \
                    self.vertices[v2].cost[0] + self.edge[v1][v2] * 2
                if dCost < bestCost:
                    bestCost = dCost
                    v1Best = v1
                    v2Best = v2
        if bestCost < 0:
            self.partVertices[0].remove(v1Best)
            self.partVertices[1].remove(v2Best)
            self.partVertices[0].append(v2Best)
            self.partVertices[1].append(v1Best)
            self.vertices[v1Best].group_id = 1
            self.vertices[v2Best].group_id = 0
            for i in range(self.n):
                self.vertices[i].cost[0] += self.edge[i][v2Best] - \
                    self.edge[i][v1Best]
                self.vertices[i].cost[1] += self.edge[i][v1Best] - \
                    self.edge[i][v2Best]
            self.totalCost += bestCost
            print(
                f"Swap {v1Best} and {v2Best} with cost {bestCost}. Total cost: {self.totalCost}")
        return bestCost

    def partition(self):
        self.GenerateData()
        stepCount = 0
        cost_list = [self.totalCost]
        while stepCount < self.maxStep:
            dCost = self.step()
            cost_list.append(self.totalCost)
            stepCount += 1
            if dCost > 0:
                break
        return cost_list

    def plotCost(self, cost_list):
        plt.plot(range(len(cost_list)), cost_list)
        plt.xlabel('Step')
        plt.ylabel('Total Cost')
        plt.title(f'Total Cost vs Step (Vertex = {self.n})')
        plt.savefig(f"res/cost_{self.n}.png")

    def PlotResult(self):
        plt.cla()
        G = nx.Graph()
        for i in range(self.n):
            G.add_node(i)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.vertices[i].group_id == self.vertices[j].group_id:
                    G.add_edge(i, j)
        G.add_weighted_edges_from([(i, j, self.edge[i][j])
                                   for i in range(self.n) for j in range(i+1, self.n)])
        pos = {}
        color = []
        pos0 = 0
        pos1 = 0
        for i in range(self.n):
            if self.vertices[i].group_id == 0:
                pos[i] = (0, pos0)
                pos0 = pos0 + 1
                color.append('r')
            else:
                pos[i] = (1, pos1)
                pos1 = pos1 + 1
                color.append('b')
        nx.draw(G, pos, node_color=color, with_labels=True,
                node_size=500, font_size=10, font_weight='bold')
        edge_labels = {edge: f'{weight:.2f}' for edge,
                       weight in nx.get_edge_attributes(G, 'weight').items()}
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, label_pos=0.4)
        plt.savefig(f"res/UniformGraphPartition_{self.n}.png")


if __name__ == "__main__":
    graphPartition = UniformGraphPartition(100)
    costs = graphPartition.partition()
    graphPartition.plotCost(costs)
    graphPartition.PlotResult()
