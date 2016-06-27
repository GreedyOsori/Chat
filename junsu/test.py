p = [1,2,3]
l = [1,2,3]
class A:
    def __init__(self):

        pass
    def __del__(self):
        pass

a = A()
b = A()

print a
print b

a.__del__()
print a
print b
a.__init__()

l = []
print l

dic = {"a": (1,2)}
for x in dic:
    print x
