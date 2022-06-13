import time
from random import randint
from copy import deepcopy

class DriverWrapper:
    def __init__(self, driver_obj):
        self.driver = driver_obj
    
    def send_keys_delay(self, element, *values, delay_ms=200, random=True):
        for value in values:
            for key in value:
                element.send_keys(key)
                if random:
                    time.sleep(randint(0, delay_ms) / 1000)
                else:
                    time.sleep(delay_ms / 1000)

def return_append(origin, new):
    temp = deepcopy(origin)
    temp.append(new)
    return temp

def sum_dict(dicta, dictb):
    result = {}
    for key, value in dicta.items():
        if key in dictb:
            result[key] = value + dictb[key]
        else:
            result[key] = value
    for key, value in dictb.items():
        if key not in result:
            result[key] = value
    return result
    
def flatdict(target, parentpath:list=None) -> dict:
    if not parentpath:
        parentpath = []
    result = {}
    def addline(value, dictkeys:list):
        result['.'.join(dictkeys)] = value
    for key, value in target.items():
        if isinstance(value, dict):
            result = sum_dict(result, flatdict(value, return_append(parentpath, key)))
        else:
            print(key, value, parentpath)
            addline(value, return_append(parentpath, key))
    return result
