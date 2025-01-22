from util import partitions, metatype, spechtDimension, kostka

ell = (2,2)
f_ell = spechtDimension(ell)

kostkaSum = 0
dimSum = 0

for a in partitions(4):
    ma = metatype(a, 4)

    kostkaSum += 3*kostka(ell, ma)
    dimSum += (len(ma)-1)*f_ell

print(dimSum, kostkaSum)
assert dimSum >= kostkaSum