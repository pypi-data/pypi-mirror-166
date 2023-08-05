from abc import ABCMeta,abstractmethod

from ..Victor.BaseVictor import BaseVictor
class BaseEdge(object,metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,id,name,from_victor:BaseVictor,to_victor:BaseVictor,type_):
        if not isinstance(from_victor,BaseVictor):
            raise TypeError(f"类型不对，from_victor需要传入 BaseVictor子类，实际传入的类型为 {type(from_victor)}")
        if not isinstance(to_victor,BaseVictor):
            raise TypeError(f"类型不对，to_victor需要传入 BaseVictor子类，实际传入的类型为 {type(to_victor)}")
        if type_ not in ("direct","branch_out","branch_in"):
            raise ValueError(f"边类型需要为1. direct 2. branch_out 3. branch_in 其中之一，实际传入类型为{type_}")
        self.from_victor = from_victor
        self.to_victor = to_victor
        self.type_ = type_ #1. direct 2. branch_out 3. branch_in
        self.id = id
        self.name = name
