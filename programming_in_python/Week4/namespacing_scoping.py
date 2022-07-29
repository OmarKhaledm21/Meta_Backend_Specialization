def d():
    animal = "elephant"
    def e():
        nonlocal animal
        animal = "giraffe"
        print("e ",animal)
    
    print("d before e ",animal)
    e()
    print("d after e ",animal)


animal = "camel"
d()
print("Global ",animal)
