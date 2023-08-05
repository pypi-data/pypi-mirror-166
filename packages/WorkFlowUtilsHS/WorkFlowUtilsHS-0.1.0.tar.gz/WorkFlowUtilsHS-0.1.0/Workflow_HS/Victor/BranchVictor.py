from Edge.NormalEdge import NormalEdge
from Transfor.NodeTrans import TransVal
from Victor.BaseVictor import BaseVictor

class BranchVictor(BaseVictor):
    
    def __init__(self, id, name, desc=""):
        self.type_="branch"
        super().__init__(id, name, desc, self.type_)
        self.trans_params_ids=[] # 本节点需要依赖的上游节点的ids
        self.judge_param=None
        self.func_params = []

    def set_switch_func(self,func,*params):
        # 设置判断分支函数
        self.func = func
        self.desc_params = params
        for param in params:
            if type(param) == TransVal:
                self.trans_params_ids.append(param.get_key()) # 执行本节点需要依赖的上游节点的ids
        
    def execute_func(self):
        # 返回判断结果
        params=[]
        for param in self.func_params:
            if type(param) == TransVal:
                raise ValueError(f"在函数执行前，依赖值需要转化为具体变量，目前节点{self.id},变量{param},未进行转化")
            else:
                params.append(param)
        try:
            if len(params)==0:
                self.judge_param = self.func()
            else:
                self.judge_param = self.func(*params)
        except NameError:
            raise NameError(f"Branch {id} 没有设置函数，请设置后再执行")
        return self.judge_param

    def set_belong_to_workflow(self,wf):
        # 来自 workflow.create_node_val 的变量, 属于 NodeTransWorkFlow 下 生成类 child_node_trans_class
        self.belong_to_wf = wf
    
    def get_judge_val(self):
        return self.judge_param

    def get_trans_ids(self):
        return self.trans_params_ids
    
    def __or__(self,next_node):
        return NormalEdge(self,next_node[0],judge_param=next_node[1])
