from pythonping import ping

from bagbag import *

class filelike():
    def __init__(self, c):
        self.c = c 

    def write(self, msg):
        msg = msg.strip()
        if msg != "":
            if 'timed out' in msg:
                self.c.Put("timeout")
            else:
                self.c.Put(Re.FindAll("Reply from .+?, .+? bytes in (.+)ms", msg)[0][0])

def Ping(host, timeout:int=1, count:int=15, interval:int=1):
    c = Tools.Chan(0)
    fd = filelike(c)
    def run():
        ping(host, timeout=timeout, count=count, interval=interval, verbose=True, out=fd)
        c.Close()
    Thread(run)
    return c

if __name__ == "__main__":
    for i in Ping("8.8.8.8"):
        print(i)