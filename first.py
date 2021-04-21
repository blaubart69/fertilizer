import time,sched,threading

def doit():
    print("do it")
    threading.Timer(1, doit).run()

t = threading.Timer(1, doit)
t.start()

print("waiting for timer...")
time.sleep(5)

#milliseconds = int(time.time() * 1000)
#print("Time in milliseconds since epoch {}".format( milliseconds))

#a = [0]*1024
#for i in range(1,5):
#    print(i)

#print("i={}".format(i))
#print(a[1])