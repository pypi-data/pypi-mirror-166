
from graphviz import Digraph
from Edge.BaseEdge import BaseEdge
from Victor.BaseVictor import BaseVictor

from Victor.WorkflowVictor import WorkflowVictor

class GraphTool:
    shape = {"branch":"diamond","container":"box","start":"ellipse","end":"ellipse"}
    def __init__(self):
        self.exec_nodes_id=[] #记录执行过程中实际执行的节点id
        self.exec_edges_id=[] #记录执行过程中实际执行的边Id
    def get_wf(self,wf:WorkflowVictor,format="svg"):
        
        self.graph = Digraph(wf.name,format=format)
        self.graph.attr(compound="true")
        # 画点：根据workflow画点，如果有实际执行结果，则实际执行节点突出显示
        wf.init()
        graph_map = wf.graph.copy()
        for victor_id,graph_node_value in graph_map.items():
            victor = graph_node_value.key_node
            if victor.type_=="workflow":
                sub_graph_tool = GraphTool()
                sub_graph_tool.update_graph(self.exec_nodes_id,self.exec_edges_id) 
                sub_graph_tool.get_wf(victor)
                sub_graph = sub_graph_tool.graph
                if victor_id in self.exec_nodes_id:
                    sub_graph.attr(style='filled', fillcolor='lightgrey')   # 突出显示执行子流程
                self.graph.subgraph(sub_graph)
            else:
                if victor_id in self.exec_nodes_id:
                    self.graph.node(victor_id,label=victor.name+":"+victor_id,shape=self.shape[victor.type_],style="filled",fillcolor="red") # 突出显示执行点
                else:
                    self.graph.node(victor_id,label=victor.name+":"+victor_id,shape=self.shape[victor.type_],style="filled",fillcolor="white")
        # 画边：根据workflow画边，如果有实际执行结果，则实际执行边突出显示
        for eg in wf.edge_g:
            if(eg.from_victor.type_=="workflow" and eg.to_victor.type_=="workflow"):
                self.graph.edge(eg.from_victor.id+"end",eg.to_victor.id+"start",ltail=eg.from_victor.name,lhead=eg.to_victor.name)
            elif (eg.from_victor.type_=="workflow"):
                self.graph.edge(eg.from_victor.id+"end",eg.to_victor.id,ltail=eg.from_victor.name)
            elif (eg.to_victor.type_=="workflow"):
                if(eg.type_ =="branch_out"):
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id+"start",lhead=eg.to_victor.name,label=str(eg.judge_param))
                else:
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id+"start",lhead=eg.to_victor.name)
            elif (eg.type_ =="branch_out"):
                if (eg.id in self.exec_edges_id):
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id,label=str(eg.judge_param),color="red")  # 突出显示执行边
                else:
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id,label=str(eg.judge_param))
            else:
                if (eg.id in self.exec_edges_id):
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id,color="red")  # 突出显示执行边
                else:
                    self.graph.edge(eg.from_victor.id,eg.to_victor.id)
        return self

    def update_graph(self,node_ids,edge_ids):
        '''
            记录：实际执行的节点及边 id
            node_ids:list<victor.id>
            edge_ids:list<edge.id>
        '''

        self.exec_nodes_id=[(id.id if isinstance(id,BaseVictor) else id) for id in node_ids]
        self.exec_edges_id=[(id.id if isinstance(id,BaseEdge) else id) for id in node_ids]

    def draw(self):
        self.graph.view()