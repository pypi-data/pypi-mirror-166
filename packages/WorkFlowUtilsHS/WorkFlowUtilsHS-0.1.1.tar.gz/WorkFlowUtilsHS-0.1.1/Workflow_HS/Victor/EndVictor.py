from ..Victor.BaseVictor import BaseVictor

class EndVictor(BaseVictor):

    def __init__(self, id, name, desc=""):
        self.type_="end"
        super().__init__(id, name, desc, self.type_)
        
    def set_belong_to_workflow(self,wf):
        # 来自 workflow.create_node_val 的变量, 属于 NodeTransWorkFlow 下 生成类 child_node_trans_class
        self.belong_to_wf = wf
        self.trans_node_val = wf.create_node_val()