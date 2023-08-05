class NodeTransWorkFlow:
    '''
        在 workflow中记录了前面节点产生的，其下节点所需要引用的变量值
    '''
    def __init__(self):
        self.val={}
        
    def add_val(self,params:dict):
        self.val.update(params)

    def get_all(self):
        return self.val

    def get_val(self,key):
        return self.val[key]
    
    def drop_val(self,key):
        if (key in self.val.keys()):
            del(self.val[key])

    
class TransVal:
    '''
        标记每一个node，需要引入前面节点产生的变量的结果来源，记录对应节点的id
    '''
    def __init__(self,key_):
        self.key_ = key_

    def get_key(self):
        return self.key_
    