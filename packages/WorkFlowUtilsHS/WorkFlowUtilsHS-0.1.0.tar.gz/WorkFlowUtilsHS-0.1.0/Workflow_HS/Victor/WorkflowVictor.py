
from Edge.NormalEdge import NormalEdge
from Transfor.NodeTrans import NodeTransWorkFlow
from Victor.BaseVictor import BaseVictor
from Edge.BaseEdge import BaseEdge
from Victor.StartVictor import StartVictor
from Victor.EndVictor import EndVictor
from Transfor.GraphNode import GraphNode

class WorkflowVictor(BaseVictor):
    
    def __init__(self, id, name, desc=""):
        self.type_="workflow"
        super().__init__(id, name, desc, self.type_)
        self.edge_g=set()  # 记录了此工作流下面所有的边
        self.isinit=False  # 初始化后

    def add_edge(self,edge:BaseEdge):
        if not isinstance(edge,BaseEdge):
            raise TypeError(f"类型错误，需要传入BaseEdge子类，实际传入的类型为{type(edge)}")
        self.edge_g.add(edge)
        return self
    
    def add_edges(self,*edges):
        for edge in edges:
            self.add_edge(edge)
    
    def init(self):
        # 初始化执行后不再重复执行
        if (not self.isinit):
            self.exec_init()
            self.isinit=True
        
    def exec_init(self):
        # 初始便利每一个边获取所属节点
        self.params_quote ={}
        # 记录了工作流下面所有参数的引用关系，格式{"key":["node1","node2"]} "key":所提供的参数的node_id,node1,node2 所需要参数的node id
        self.graph ={}

        for edge in self.edge_g:
            if(edge.from_victor.id not in self.graph.keys()):
                self.__register_child_node(edge.from_victor)
                self.graph[edge.from_victor.id].add_edge(edge)
            else:
                self.graph[edge.from_victor.id].add_edge(edge)
            if(edge.to_victor.id not in self.graph.keys()):
                self.__register_child_node(edge.to_victor)
                self.graph[edge.to_victor.id].add_edge(edge)
            else:
                self.graph[edge.to_victor.id].add_edge(edge)

        # 补充 每个node的开始/结束节点

        start_victor = StartVictor(self.id+"start","start")
        end_victor = EndVictor(self.id+"end","end")
        start_victor_lis=[]
        end_victor_lis=[]
        for victor_id,graph_node_value in self.graph.items():
            victor = graph_node_value.key_node
            if ((start_victor.id not in self.graph.keys()) and self.graph[victor_id].degree_in_num()==0):
                edge = NormalEdge(start_victor,victor)
                self.edge_g.add(edge)
                self.graph[victor_id].add_edge(edge)
                start_victor_lis.append(edge)
            elif((end_victor.id not in self.graph.keys()) and self.graph[victor_id].degree_out_num()==0):
                edge = NormalEdge(victor,end_victor)
                self.edge_g.add(edge)
                self.graph[victor_id].add_edge(edge)
                end_victor_lis.append(edge)

        # 补充开始/结束节点 对应的边
        if (start_victor.id not in self.graph.keys()):
            self.graph[start_victor.id] = GraphNode(start_victor)
            for start in start_victor_lis:
                self.graph[start_victor.id].add_edge(start)
        if (end_victor.id not in self.graph.keys()):
            self.graph[end_victor.id] = GraphNode(end_victor)
            for end in end_victor_lis:
                self.graph[end_victor.id].add_edge(end)
       

    def set_belong_to_workflow(self,wf):
        # 来自 workflow.create_node_val 的变量, 属于 NodeTransWorkFlow 下 生成类 child_node_trans_class
        self.belong_to_wf = wf

    def __or__(self,next_node):
        return NormalEdge(self,next_node)
    
    def __register_child_node(self,node):
        self.graph[node.id] = GraphNode(node)
        if node.type_ in ("branch","container"):
            trans_params_ids = node.get_trans_ids()
            for trans_id in trans_params_ids:
                if trans_id in self.params_quote.keys():
                    self.params_quote[trans_id].append(node.id)
                else:
                    self.params_quote[trans_id] = [node.id]
        elif node.type_ == "workflow":
            node.set_belong_to_workflow(self)
            node.init()
            # 子节点初始化后，把子流程需要的参数注册给父流程
            for key in node.params_quote.keys():
                if key in self.params_quote.keys():
                    self.params_quote[key].append(self.id)
                else:
                    self.params_quote[key]=[self.id]


        