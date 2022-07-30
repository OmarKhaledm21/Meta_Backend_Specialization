class P:
    pass

class C(P):
    pass

p = P()
c = C()
print(issubclass(C,P))