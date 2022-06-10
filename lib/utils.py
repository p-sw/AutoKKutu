import time
from random import randint

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