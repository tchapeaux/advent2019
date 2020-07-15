a = 3

def foo():
    global a
    a = 2

foo()

print a