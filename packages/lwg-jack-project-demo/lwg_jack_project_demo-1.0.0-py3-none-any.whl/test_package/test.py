import numpy

def pySum():
    a = list(range(10000))
    b = list(range(10000))
    c = []
    for i in range(len(a)):
        c.append(a[i] ** 2 + b[i] ** 2)

    return c


def npSum():
    a = numpy.arange(10000)
    b = numpy.arange(10000)
    c = a**2 + b**2
    return c

print(pySum())
print(npSum())