from ..Edge.BaseEdge import BaseEdge
from ..Victor.BaseVictor import BaseVictor


class NormalEdge(BaseEdge):

    def __init__(self,from_victor:BaseVictor,to_victor:BaseVictor,name="",judge_param=""):
        try:
            id = (from_victor.id,to_victor.id)
        except:
            pass
        type_=""
        if (from_victor.type_=="branch"):
            if(to_victor.type_ in ("start","end","container","workflow")):
                type_="branch_out"  # 从分支节点到执行/流程节点
                if(judge_param==""):
                    raise ValueError(f"当输入节点为分支时，输出节点需要加上对应的判断条件参数，目前id={from_victor.id}的参数为空")
            elif(to_victor.type_=="branch"):
                raise TypeError("当输入节点为分支时，输出节点不能为分支节点，只能为container 或者 workflow")
        if(from_victor.type_ in ("start","end","container","workflow")):
            if(to_victor.type_ in ("start","end","container","workflow")):
                type_="direct" # 从执行/流程节点到执行/流程节点
            elif(to_victor.type_=="branch"):
                type_="branch_in" # 从执行/流程节点到分组节点
        self.judge_param=judge_param
        super().__init__(id,name,from_victor,to_victor,type_)