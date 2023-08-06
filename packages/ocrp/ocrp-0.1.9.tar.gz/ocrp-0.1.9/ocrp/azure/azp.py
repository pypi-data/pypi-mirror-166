# -*- coding: utf-8 -*-



import json


class Struct(object):
    def __init__(self, obj):
        for name, value in obj.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)): 
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value
        
    # def __repr__(self):
    #     return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.items()))
    
    def __repr__(self): 
        return ("{ " + str(", ".join([f"'{k}': {v}" for k, v in [(k, repr(v)) for (k, v) in self.__dict__.items()]])) + " }")
        


class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)


def main(filen):
    with open ( filen,'r') as f:
        data = json.loads(f.read())
        
    s = Struct(data)
    
    
    o = dict2obj(data)
    
    b = obj(data)
    
    return s,o,b
    
if __name__ == "__main__":
    

                                  

    
