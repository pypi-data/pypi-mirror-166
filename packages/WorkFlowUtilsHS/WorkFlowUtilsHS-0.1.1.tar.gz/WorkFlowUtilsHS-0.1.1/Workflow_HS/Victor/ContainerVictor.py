from ..Edge.NormalEdge import NormalEdge
from ..Transfor.NodeTrans import TransVal
from ..Victor.BaseVictor import BaseVictor
from ..Victor.WorkflowVictor import WorkflowVictor

class ContainerVictor(BaseVictor):

    def __init__(self, id, name, desc=""):
        self.type_="container"
        super().__init__(id, name, desc, self.type_)
        self.trans_params_ids=[] # 本节点需要依赖的上游节点的ids
        self.func_params = []

    def set_work_func(self,func,*params):
        # 执行外部函数
        self.func = func
        self.desc_params = params # 名义变量，外边变量直接转化为执行参数，需要依赖节点变量，需要转化后使用，转化在具体执行前完成
        for param in params:
            if type(param) == TransVal:
                self.trans_params_ids.append(param.get_key()) # 记录本节点需要依赖的上游节点的ids

    def execute_func(self):
        # 执行完成后，执行结果记录到trans变量中，以此节点id为索引向下传递
        params=[]
        for param in self.func_params:
            if type(param) == TransVal:
                raise ValueError(f"在函数执行前，依赖值需要转化为具体变量，目前节点{self.id},变量{param},未进行转化")
            else:
                params.append(param)
        try:
            if len(params)==0:
                result = self.func()
            else:
                result = self.func(*params)
        except NameError:
            raise NameError(f"Container {id} 没有设置函数，请设置后再执行")
            # print(f"Container {id} 没有设置函数，请设置后再执行")
        return result
    
    def set_belong_to_workflow(self,wf:WorkflowVictor):
        # 来自 workflow.create_node_val 的变量, 属于 NodeTransWorkFlow 下 生成类 child_node_trans_class
        self.belong_to_wf = wf

    def get_trans_ids(self):
        return self.trans_params_ids

    def __or__(self,next_node):
        return NormalEdge(self,next_node)