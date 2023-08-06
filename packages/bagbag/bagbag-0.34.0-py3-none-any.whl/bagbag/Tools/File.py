

class File():
    def __init__(self, path:str):
        self.path = path 
    
    def Append(self, data:str):
        fd = open(self.path, "a")
        fd.write(data)
        fd.close()