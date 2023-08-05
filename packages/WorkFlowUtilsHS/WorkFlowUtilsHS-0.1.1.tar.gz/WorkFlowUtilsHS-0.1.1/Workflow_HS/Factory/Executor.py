from ..Edge.NormalEdge import NormalEdge
from ..Transfor.NodeTrans import NodeTransWorkFlow, TransVal
from ..Victor.BaseVictor import BaseVictor
from ..Victor.WorkflowVictor import WorkflowVictor


class Executor:
    def __init__(self,workflow:WorkflowVictor,father_trans_node_val=None):
        self.todu_queue=[]
        self.complete_queue=[]
        self.exec_edges=[]
        workflow.init()
        self.graph= workflow.graph.copy()
        self.params_quote = workflow.params_quote.copy()  #  格式{"key":["node1","node2"]} 
        self.workflow = workflow
        self.trans_node_val = NodeTransWorkFlow()  # 记录了此工作流下面所有节点所需要的参数
        if type(father_trans_node_val)==NodeTransWorkFlow:
            self.add_trans_vals(father_trans_node_val)

    def run(self):
        # 1. 获取待执行节点
        # 2. 执行每个节点
        # 3. 执行完成的节点，加入到执行完成列表中
        # 4. 对后续需要执行的参数进行更新去掉无需再用的参数
        # 5. 执行完成每个节点后更新待执行的图
        # 6. 获取下一个迭代待执行节点 --> 2
        # 6. 直到待执行没有获取值返回结果
        self.choise_todo_victor()
        while len(self.todu_queue)>0:
            for node in self.todu_queue:
                self.run_node(node)
                self.complete_queue.append(node)
                self.update_quote_param(node)
                self.update_graph(node)
            self.choise_todo_victor()
        # 返回 实际执行的节点列表 和 实际执行的路径
        return self.complete_queue,self.exec_edges
       
    # 选择待执行节点
    def choise_todo_victor(self):
        self.todu_queue=[]
        for victor_id,graph_node in self.graph.items():
            victor = graph_node.key_node
            if (graph_node.degree_in_num()==0):
                self.todu_queue.append(victor)

    # 更新图：根据上一个执行完成的节点，更新图。1. 找到下一个需要执行的节点；2. 删除已经完成的节点；3. 记录执行轨迹; 4. 传递参数
    def update_graph(self,victor:BaseVictor):
        next_nodes=[]
        if (victor.type_=="branch"):
            judge = victor.get_judge_val()
            for i,switch_elem in enumerate(self.graph[victor.id].judge_lis):
                if judge==switch_elem:
                    #找到下一个执行的node
                    next_node = self.graph[victor.id].degree_out[i]
                    next_nodes.append(next_node)
                    # 记录执行路径
                    exec_edge = NormalEdge(victor,self.graph[victor.id].degree_out[i],judge_param=judge)
                    self.exec_edges.append(exec_edge)
        elif(victor.type_ == "container"):
            try:
                next_nodes=self.graph[victor.id].degree_out
            except:
                pass
            for next_node in next_nodes:
                # 记录执行路径
                exec_edge = NormalEdge(victor,next_node)
                self.exec_edges.append(exec_edge)
        elif(victor.type_ in("start","end")):
            try:
                next_nodes=self.graph[victor.id].degree_out
            except:
                pass
            for next_node in next_nodes:
                # 记录执行路径
                exec_edge = NormalEdge(victor,next_node)
                self.exec_edges.append(exec_edge)
        elif(victor.type_ == "workflow"):
            try:
                next_nodes=self.graph[victor.id].degree_out
            except:
                pass
            for next_node in next_nodes:
                # 记录执行路径
                exec_edge = NormalEdge(victor,next_node)
                self.exec_edges.append(exec_edge)

        # 在图中，删除 victor对应key
        del(self.graph[victor.id])

        # 在其他节点 degree_in 中删除 此节点
        for node in next_nodes:
            self.graph[node.id].degree_in.remove(victor)
    
    # 具体执行对应节点，1. 转化具体执行参数；2. 执行函数方法 3. 子流程递归执行
    def run_node(self,victor:BaseVictor):
        if (victor.type_=="start"):
            pass
        elif (victor.type_=="end"):
            pass
        elif (victor.type_ in ("container","branch")):
            # 具体执行前，需要依赖节点变量，需要转化为具体参数后使用
            for param in victor.desc_params:
                if type(param) == TransVal:
                    victor.func_params.append(self.trans_node_val.get_val(param.get_key()))
                else:
                    victor.func_params.append(param)

            result = victor.execute_func()
            # 执行后，如果上传返回结果的子节点的id 需要被后续节点引用，则记录子节点结果数据，否则不记录 ，目前仅支持container and branch
            if victor.id in self.params_quote.keys():
                self.trans_node_val.add_val({victor.id:result})
        elif (victor.type_ =="workflow"):
            # workflow节点执行子节点内容
            complete_nodes,complete_edges = Executor(victor,self.trans_node_val).run()
            self.complete_queue.extend(complete_nodes)
            self.exec_edges.extend(complete_edges)
        else:
            raise TypeError(f"类型不对，需要传人类型 start,end,container,branch,workflow, 请检查，对应节点id为 {victor.id}")
        return victor

    # 节点执行完成后，更新后续节点依赖参数，如果参数不再使用则删除
    def update_quote_param(self,victor:BaseVictor):
        
        need_drop_keys=[]
        for quote_key, quote_lis in self.params_quote.items():
            if victor.id in quote_lis:
                quote_lis.remove(victor.id)
                if len(quote_lis)==0:
                    need_drop_keys.append(quote_key)

        # 在参数依赖关系中删除对应数据
        [self.params_quote.pop(x) for x in need_drop_keys]

        # 在参数列表中删除对应参数数据
        [self.trans_node_val.drop_val(x) for x in need_drop_keys]
    
    # 
    def add_trans_vals(self,vals:NodeTransWorkFlow):
        self.trans_node_val.add_val(vals.get_all())