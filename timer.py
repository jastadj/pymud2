import time

class Timer(object):
    def __init__(self):
        self.startTime = time.time()
    
    def getElapsedSec(self):
        return int(time.time() - self.startTime)
        
    def getStartTime(self):
        return self.startTime
        
    def reset(self):
        self.startTime = time.time()


if __name__ == "__main__":
    
    mytimer = Timer()
    
    sleepfor = 3
    
    print "Start Time:%f" %mytimer.getStartTime()
    
    print "Sleeping for %d seconds..." %sleepfor
    time.sleep(sleepfor)
    
    print "Elapsed Time : %d seconds" %mytimer.getElapsedSec()
    
    
    
