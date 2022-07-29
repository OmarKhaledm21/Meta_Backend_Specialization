from distutils.log import info


a = 5
class A:
      a = 7
      pass

class B(A):
      pass

class C(B):
      pass

c = C()
print(help(c))