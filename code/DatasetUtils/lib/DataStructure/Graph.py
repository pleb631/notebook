# -*- coding: UTF-8 -*-
import abc
import numpy as np

from queue import Queue

'''
图（Vertex个顶点Edge条边）的存储方法有邻接矩阵、邻接表和链式前向星
邻接矩阵
    优点：对已确定的边进行增删操作，效率高时间复杂度为O(1)；易处理重边
    缺点：对于顶点数V，邻接矩阵存图的空间复杂度高达O(V^2)，顶点数上了一万可以不用考虑这种存图方式了；对于稀疏图(E远小于V^2)来说，邻接矩阵存图内存浪费太严重
邻接表
    优点：空间复杂度为O(V+E)。能较好处理稀疏图的存储
    缺点：判重比较麻烦，还要遍历已有的边，不能直接判断。一般情况下使用邻接表存图是会存储重边的，不会做重边的判断。
链式前向星（边集数组）
'''


class Graph(abc.ABC):
    '''图类

    Attributes:
        vertices_num: int, 顶点数量
        directed_flag: bool, 为True代表有向图Digraph；为False代表无向图Undigraph
    '''
    def __init__(self, vertices_num, directed_flag=False):
        self.vertices_num = vertices_num
        self.directed_flag = directed_flag

    @abc.abstractmethod
    def add_edge(self):
        '''添加边v1-v2
        '''
        pass

    @abc.abstractmethod
    def get_adjacent_vertices(self):
        '''获取顶点v的邻接顶点
        '''
        pass

    @abc.abstractmethod
    def get_indegree(self):
        '''获取顶点v的入度
        '''
        pass

    @abc.abstractmethod
    def get_edge_weight(self):
        '''获取边v1-v2的权重
        '''
        pass

    def display(self):
        '''绘制图
        '''
        for i in range(self.vertices_num):
            print("Adjacent to :", i, self.get_adjacent_vertices(i))

    def breadth_first_search(self, current):
        '''广度优先搜索，寻找当前顶点的连通节点

        Args: 
            current: int, 当前顶点的下标
        
        Returns:
            connected_vertices: list, 当前顶点的连通节点
        '''
        queue = Queue()
        connected_vertices = []
        visited = np.zeros(self.vertices_num)

        queue.put(current)
        while not queue.empty():
            vertex = queue.get()
            if visited[vertex] == 1:
                continue
            connected_vertices.append(vertex)
            visited[vertex] = 1

            for v in self.get_adjacent_vertices(vertex):
                if visited[v] != 1:
                    queue.put(v)
        
        return connected_vertices

    def depth_first_search_iterative(self, current):
        '''深度优先搜索-循环迭代法，寻找当前顶点的连通节点

        Args: 
            current: int, 当前顶点的下标
        
        Returns:
            connected_vertices: list, 当前顶点的连通节点
        '''
        visited = np.zeros(self.vertices_num)
        stack, connected_vertices = [], []

        # 维护一个栈，用于记录当前节点及下个邻接节点
        stack.append(current)
        visited[current] = 1
        connected_vertices.append(current)

        while stack:
            current = stack.pop()
            for next in self.get_adjacent_vertices(current):
                if visited[next] != 1:
                    stack.append(current)
                    stack.append(next)
                    visited[next] = 1
                    connected_vertices.append(next)
                    break

        return connected_vertices

    def depth_first_search_recursion(self, visited, current, connected_vertices):
        '''深度优先搜索-递归法，寻找当前顶点的连通节点

        Args: 
            graph: Graph, 图
            visited: list, 顶点是否被访问过的列表
            current: int, 当前顶点的下标
            connected_vertices: list, 当前顶点的连通节点
        '''
        if visited[current] == 1:
            return

        visited[current] = 1
        connected_vertices.append(current)

        for vertex in self.get_adjacent_vertices(current):
            self.depth_first_search_recursion(visited, vertex, connected_vertices)


    def get_connected_domain(self, mode='dfs_recur'):
        '''获取图的连通域。
        DFS内存开销小，但要多次遍历，搜索所有可能路径，深度很大的情况下效率不高
        BFS常用于搜索最短路径，时间复杂度为 O(V+E)，但内存开销大

        Args:
            mode: str, 若为'dfs_recur'，代表深度优先搜索-递归法；若为'dfs_iter'，代表深度优先搜索-循环迭代法；若为'bfs'，代表广度优先搜索

        Returns: 
            connected_domain: list, 图内所有的连通域
        '''
        connected_domain = []
        remaining_list = list(range(self.vertices_num))
        while remaining_list:
            if mode == 'dfs_recur':
                connected_vertices = []
                visited = np.zeros(self.vertices_num)
                self.depth_first_search_recursion(visited, remaining_list[0], connected_vertices)
            elif mode == 'dfs_iter':
                connected_vertices = self.depth_first_search_iterative(remaining_list[0])
            elif mode == 'bfs':
                connected_vertices = self.breadth_first_search(remaining_list[0])
            
            connected_domain.append(sorted(connected_vertices))

            for i in connected_vertices:
                remaining_list.remove(i)

        return connected_domain


class Node(abc.ABC):
    '''节点类

    Attributes:
        vertex_id: int, 节点下标
    '''
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id

    @abc.abstractmethod
    def add_edge(self):
        '''添加边
        '''
        pass

    @abc.abstractmethod
    def get_adjacent_vertices(self):
        '''获取邻接节点
        '''
        pass


class ListNode(Node):
    '''链表节点类
    '''
    pass


class SetNode(Node):
    '''集合节点类

    Attributes:
        vertex_id: int, 顶点下标
        adjacency_set: set, 使用集合表示邻接顶点
    '''
    def __init__(self, vertex_id):
        super().__init__(vertex_id)
        self.adjacency_set = set()

    def add_edge(self, v):
        '''添加邻接顶点v，作为一条新的边

        Args: 
            v: int, 邻接顶点的下标v
        '''
        if self.vertex_id == v:
            raise ValueError("The vertex %d cannot be adjacent to itself" %v)

        self.adjacency_set.add(v)

    def get_adjacent_vertices(self):
        '''获取邻接顶点；排序只是为了方便没有特殊意义

        Returns: 
            adjacent_vertices: list, 邻接顶点列表
        '''
        return sorted(self.adjacency_set)


class AdjacencySet(Graph):
    '''图的邻接集合类

    Attributes:
        vertices_num: int, 顶点下标
        directed_flag: bool, 为True代表有向图Digraph；为False代表无向图Undigraph
        vertex_list: set, 使用集合表示邻接节点
    '''
    def __init__(self, vertices_num, directed_flag=False):
        super().__init__(vertices_num, directed_flag)
        self.vertex_list = []
        for i in range(vertices_num):
            self.vertex_list.append(SetNode(i))

    def add_edge(self, v1, v2, weight=1):
        '''添加边v1-v2，目前只支持无权图
        TODO: 添加有权图

        Args: 
            v1: int, 起始点的下标
            v2: int, 终点的下标
            weight: float, 边的权重
        '''
        if v1 >= self.vertices_num or v2 >= self.vertices_num or v1 < 0 or v2 < 0:
            raise ValueError("Vertices %d and %d are out of bounds" %(v1,v2))

        if weight != 1:
            raise ValueError("An adjacency set cannot represent edge weight >1")

        self.vertex_list[v1].add_edge(v2)

        if not self.directed_flag:
            self.vertex_list[v2].add_edge(v1)

    def get_adjacent_vertices(self, v):
        '''获取顶点v的邻接顶点

        Args: 
            v: int, 顶点下标

        Returns: 
            adjacent_vertices: list, 顶点v邻接顶点列表
        '''
        if v < 0 or v >= self.vertices_num:
            raise ValueError("Cannot access vertex %d" %v)

        return self.vertex_list[v].get_adjacent_vertices()

    def get_indegree(self, v):
        '''获取顶点v的入度

        Args: 
            v: int, 顶点下标

        Returns: 
            indegree: int, 顶点v的入度
        '''
        if v < 0 or v >= self.vertices_num:
            raise ValueError("Cannot access vertex %d" % v )

        indegree = 0
        for i in range(self.vertices_num):
            if v in self.get_adjacent_vertices(i):
                indegree +=1
        
        return indegree

    def get_edge_weight(self, v1, v2):
        '''获取边v1-v2的权重
        '''
        return 1


class AdjacencyMatrix(Graph):
    '''图的邻接矩阵类

    Attributes:
        vertices_num: int, 顶点下标
        directed_flag: bool, 为True代表有向图Digraph；为False代表无向图Undigraph
        adjacency_matrix: np.array, 使用邻接矩阵表示图
    '''
    def __init__(self, vertices_num, directed_flag = False):
        super().__init__(vertices_num, directed_flag)
        self.adjacency_matrix = np.zeros((vertices_num, vertices_num))

    def add_edge(self, v1, v2, weight=1):
        '''添加边v1-v2

        Args: 
            v1: int, 起始点的下标
            v2: int, 终点的下标
            weight: float, 边的权重
        '''
        if v1 >= self.vertices_num or v2 >= self.vertices_num or v1 < 0 or v2 < 0:
            raise ValueError("Vertices %d and %d are out of bounds" %(v1,v2))

        if weight < 1:
            raise ValueError("An edge cannot have weight less than 1")

        self.adjacency_matrix[v1][v2] = weight

        if not self.directed_flag:
            self.adjacency_matrix[v2][v1] = weight

    def get_adjacent_vertices(self, v):
        '''获取顶点v的邻接顶点

        Args: 
            v: int, 顶点下标

        Returns: 
            adjacent_vertices: list, 顶点v邻接顶点列表
        '''
        if v < 0 or v >= self.vertices_num :
            raise ValueError("Cannot access vertex %d" %v)

        adjacent_vertices=[]
        for i in range(self.vertices_num):
            if self.adjacency_matrix[v][i] > 0:
                adjacent_vertices.append(i)
        
        return adjacent_vertices

    def get_indegree(self, v):
        '''获取顶点v的入度

        Args: 
            v: int, 顶点下标

        Returns: 
            indegree: int, 顶点v的入度
        '''
        if v < 0 or v >= self.vertices_num :
            raise ValueError("Cannot access vertex %d" % v)

        indegree = 0
        for i in range(self.vertices_num):
            if self.adjacency_matrix[i][v] >0:
                indegree +=1
        
        return indegree

    def get_edge_weight(self, v1, v2):
        '''获取边v1-v2的权重

        Args: 
            v1: int, 起始点的下标
            v2: int, 终点的下标

        Returns: 
            edge_weight: float, 边v1-v2的权重
        '''
        return self.adjacency_matrix[v1][v2]

