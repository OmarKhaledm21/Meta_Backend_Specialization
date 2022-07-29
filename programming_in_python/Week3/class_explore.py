from abc import ABC, abstractmethod
from mimetypes import init

class Animal(ABC):
    @abstractmethod
    def addAnimal(self):
        pass


class X:
    def __init__(self) -> None:
        self.a = 10
        pass
    
class Y():
    def __init__(self) -> None:
        self.a=11

class Z(X,Y):
    def out(self):
        print(self.a)

z= Z()
z.out()

class A:
    def __init__(self, c):
        print("---------Inside class A----------")
        self.c = c
    print("Print inside A.")

    def alpha(self):
        c = self.c + 1
        return c


print(dir(A))
print("Instantiating A..")
a = A(1)
print(a.alpha())


class B:
    def __init__(self, a):
        print("---------Inside class B----------")
        self.a = a

    print(a.alpha())
    d = 5
    print(d)
    print(a)


print("Instantiating B..")
b = B(a)
print(a)
