import time
from random import randint
from copy import deepcopy

class DriverWrapper:
    def __init__(self, driver_obj):
        self.driver = driver_obj

    def send_keys_delay(self, element, *values, delay_max=100, delay_min=50, random=True):
        for value in values:
            for key in value:
                element.send_keys(key)
                if random:
                    time.sleep(randint(delay_min, delay_max) * 1000)
                else:
                    time.sleep(delay_max * 1000)

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
            addline(value, return_append(parentpath, key))
    return result

def stylesplit(style):
    result = {}
    for line in style.split(';'):
        if ':' in line:
            key, value = line.split(':')
            result[key.strip()] = value.strip()
    return result
