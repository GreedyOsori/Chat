class Test:
    def __init__(self, l):
        self.l = l

l1 = [1,2,3,4]
l2 = [3,4,5,6,]
l3 = [99,55,56]

a = Test(l1)
b = Test(l2)
c = Test(l3)

print a.l
print b.l
print c.l

l1.remove(1)

print a.l
