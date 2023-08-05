

from Victor.BaseVictor import BaseVictor
from Edge.NormalEdge import NormalEdge

class GraphNode:
    def __init__(self,victor:BaseVictor):
        self.degree_in =[]
        self.degree_out=[]
        self.judge_lis=[]
        self.key_node=victor
        self.type_ = victor.type_
    
    def add_edge(self,edge:NormalEdge):
        if (edge.from_victor == self.key_node):
            if((self.key_node.type_ in ("container","workflow")) and len(self.degree_out)>=1):
                print(f"当前节点为 {self.key_node.type_},且已有出边{(self.key_node.id,self.degree_out[0].id)}，无法再增加出边{edge.id}")
            else:
                self.degree_out.append(edge.to_victor)
                if (self.type_=="branch"):
                    self.judge_lis.append(edge.judge_param)
        elif (edge.to_victor == self.key_node):
            if((self.key_node.type_ in ("container","workflow")) and len(self.degree_in)>=1):
                print(f"当前节点为 {self.key_node.type_},且已有入边{(self.degree_in[0].id,self.key_node.id)}，无法再增加入边{edge.id}")
            else:
                self.degree_in.append(edge.from_victor)
        else:
            print(f"添加的边 起点 终点 不满足此节点，当前节点id={self.key_node},插入的边为{edge.id}")
    def degree_in_num(self):
        return len(self.degree_in)
    
    def degree_out_num(self):
        return len(self.degree_out)