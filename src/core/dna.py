import time

class DNA(object):
    
    MG = 9999 # max valore x gene
    NG = 500  # num di geni
    
    def __init__(self):
        # 500 geni per le azioni
        self.genes = [0] * self.NG
        # tempo
        self.creation_date = int(time.time())
        self.cur_timestamp = self.creation_date
        self.decaying_time = int("9"*10)
    
    def set_timestamp(self):
        self.cur_timestamp = int(time.time())
    
    def set_dectime(self):
        self.decaying_time -= 1
    
    # timer per mutare i geni
    def timer(self):
        self.set_timestamp()
        self.set_dectime()
