# from typing import  Optional
# # def dfs(node: Optional['int'] = 5):
# def dfs(node: int = 5):
#     print(node)


# dfs(None)    

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

#（1，2，4）
#（2，1，3）


#我先试一下遍历打印
from typing import Optional
class Solution:
    # node_global = None
    node_dict = {}
    # def dfs(self, nodes: Optional['list[Node]']):
    #     #现在给我一个节点，
    #     #填充val和list
    #     #（1，2，4）
    #     for node in nodes:

    #     if node.val not in self.node_dict:
    #         node_tmp = Node(node.val)


    def dfs(self, node: Optional['Node']):
        #打印过，就不打印了
        if node.val in self.node_dict:
            return
        #没打印过，打印
        if node.val not in self.node_dict:
            # print(node.val)
            
            neighbors_list = []
            self.node_dict[node.val] = []
            for tmp in node.neighbors:                                                
                self.dfs(tmp)
                neighbors_list.append(tmp.val)

            self.node_dict[node.val] = neighbors_list    

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:

        if node is None:
            return None

        
        self.node_dict = {}
        #做数字节点
        self.dfs(node)
        tmp_node = {}
        #初始化node
        for k,v in self.node_dict.items():
            if k not in tmp_node:
                tmp_node[k] = Node(k)
        print(tmp_node.items())    

        #赋值node邻居
        for first, second in zip(self.node_dict.items(), tmp_node.items()):
            print(f'first:{ first }')
            print(f'second:{ second }')
            for num in first[1]:
                second[1].neighbors.append(tmp_node[num])

        for tmp in tmp_node.items():
            print("-----------")
            print(tmp[1].val)
            for tmp2 in tmp[1].neighbors:
                print(tmp2.val)

        return tmp_node[node.val]


#我现在想让字典存储{"1": ["2", "4"]}
#现在把数字换成节点的地址

node1 = Node(1,[])
node2 = Node(2,[])
node3 = Node(3,[])
node4 = Node(4,[])

node1.neighbors.append(node2)
node1.neighbors.append(node4)
node2.neighbors.append(node1)
node2.neighbors.append(node3)
node3.neighbors.append(node2)
node3.neighbors.append(node4)
node4.neighbors.append(node1)
node4.neighbors.append(node3)

s1 = Solution()
s1.cloneGraph(node1)
s1.cloneGraph(None)

node_tmp = Node(666,[])
s1.cloneGraph(node_tmp)

for k,v in s1.node_dict.items():
    print(k,v)