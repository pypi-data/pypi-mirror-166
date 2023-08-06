# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 07:07:03 2022

@author: HEDI
"""
json_schema = {"rho":["T","x"]}
class __prop_obj__:
    def __init__(self,):
        pass

def unzip_args(prop,args_=[],**args):
    res = []
    if not len(args_):
        args_ =args.items()
    print(args_)
    for k in sorted(args_):
        if k in json_schema[prop]:
            res.append(args[k])
    return res
        