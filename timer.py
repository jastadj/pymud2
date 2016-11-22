import time

class timer(object):
    def __init__(self):
        self.starttime = time.time()
    
    def getelapsedsec(self):
        return int(time.time() - self.starttime)
        
    def getstarttime(self):
        return self.starttime
        
    def reset(self):
        self.starttime = time.time()


if __name__ == "__main__":
    
    mytimer = timer()
    
    sleepfor = 3
    
    print "Start Time:%f" %mytimer.getstarttime()
    
    print "Sleeping for %d seconds..." %sleepfor
    time.sleep(sleepfor)
    
    print "Elapsed Time : %d seconds" %mytimer.getelapsedsec()
    
    
    
