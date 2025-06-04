from abc import ABC

class DatabaseClientInterface(ABC):
    def __init__(self,**args):
        pass
    
    def __construct_url(self):
        pass
    
    def __check_connection_valid(self):
        pass

    def insert(self,**args):
        pass
    