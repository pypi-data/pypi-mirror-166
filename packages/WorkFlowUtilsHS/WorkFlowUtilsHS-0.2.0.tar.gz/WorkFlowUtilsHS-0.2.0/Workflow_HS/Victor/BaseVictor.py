from abc import ABCMeta,abstractmethod

class BaseVictor(object,metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,id,name,desc,type_):
        if not isinstance(id,str):
            raise TypeError(f"类型错误，需要传入字符串类型，实际传入的类型为{type(id)}")
        self.id = id
        self.name = name
        self.desc = desc
        self.type_ = type_ # 1. 开始节点 start 2. 结束节点 end 3. 执行容器 container 4. 分支 branch 5. 工作流 workflow

    

    