
## decorator
import time

'''



def cheeseshop(kind, *arguments, **keywords):
    print "-- Do you have any", kind, "?"
    print "-- I'm sorry, we're all out of", kind
    for arg in arguments:
        print arg
    print "-" * 40
    keys = sorted(keywords.keys())
    for kw in keys:
        print kw, ":", keywords[kw]


cheeseshop("A",1,2,3,4,5, ssdf=3, abcd = 5)


class Verbose:
   def __init__(self, f):
      print "Initializing Verbose."
      self.func = f;

   def __call__(self, *args, **kwargs):
      print "Begin", self.func.__name__
      self.func(*args, **kwargs)
      print "End", self.func.__name__

@Verbose
def tttt():
    i = 5000000
    while i > 0 :
        i -= 1


v = Verbose(tttt)

##v()

class TIme_printer:

    def __init__(self, func):
        self.func = func

    def __call__(self, *a, **b):
        pre = time.time()
        self.func(*a, **b)
        print time.time() - pre

@TIme_printer
def time_consume(name):
    print name
    for a in xrange(10000):
        pass

time_consume("aa")
'''
def gen():
    for a in range(4):
        yield a
        print "zzazanzzan"

gene = gen()
print gene.next()
print gene.next()
##print gene.next()
