from unittest import result
from Victor.BranchVictor import BranchVictor
from Victor.ContainerVictor import ContainerVictor
from Victor.WorkflowVictor import WorkflowVictor


class GlobalId:
    """生成全局唯一

    Returns:
        String: 全局唯一ID
    """
    id=-1
    def get_id():
        GlobalId.id=GlobalId.id+1
        return str(GlobalId.id)

class VictorFactory:
    @staticmethod
    def containers(*params):
        result =[]
        for param in params:
            if type(param)==str:
                result.append(ContainerVictor(param,param))
            elif type(param) ==tuple and len(param)==2:
                result.append(ContainerVictor(param[0],param[1]))
            elif type(param) == tuple and len(param)==3:
                result.append(ContainerVictor(param[0],param[1],param[2]))
            else:
                raise ValueError(f"输入错误，支持的输入参数有 str ,(str,str),(str,str,str),实际输入的参数为{param}")
        if len(result)==1:
            return result[0]
        else:
            return result
    @staticmethod
    def branches(*params):
        result =[]
        for param in params:
            if type(param)==str:
                result.append(BranchVictor(param,param)) 
            elif type(param) ==tuple and len(param)==2:
                result.append(BranchVictor(param[0],param[1]))
            elif type(param) == tuple and len(param)==3:
                result.append(BranchVictor(param[0],param[1],param[2]))
            else:
                raise ValueError(f"输入错误，支持的输入参数有 str ,(str,str),(str,str,str),实际输入的参数为{param}")
        if len(result)==1:
            return result[0]
        else:
            return result
    @staticmethod
    def workflows(*params):
        result =[]
        for param in params:
            if type(param)==str:
                result.append(WorkflowVictor(param,param)) 
            elif type(param) ==tuple and len(param)==2:
                result.append(WorkflowVictor(param[0],param[1]))
            elif type(param) == tuple and len(param)==3:
                result.append(WorkflowVictor(param[0],param[1],param[2]))
            else:
                raise ValueError(f"输入错误，支持的输入参数有 str ,(str,str),(str,str,str),实际输入的参数为{param}")
        if len(result)==1:
            return result[0]
        else:
            return result