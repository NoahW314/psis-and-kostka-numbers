from collections import Counter

from math import factorial, prod


# generate all partitions of d into j parts
# partition code was copied (with modification) from here: https://stackoverflow.com/a/44209393
def partitions(d, j=None):
    if j is None:
        j = d
    return [tuple(reversed(mu)) for mu in partitionsRec(d, j)]
def partitionsRec(d, j, I=1, depth=0):
    if depth >= j:
        return
    yield (d,)
    for i in range(I, d // 2 + 1):
        for p in partitionsRec(d-i, j, i, depth+1):
            yield (i,) + p

# get the metatype of a partition into n parts
def metatype(partition, n):
    exponents = Counter(partition)

    # to ensure that the returned partition is a partition of n, we
    #  append a value if needed (this corresponds to the number of zeros
    #  in the original partition)
    if sum(exponents.values()) != n:
        exponents[0] = (n-sum(exponents.values()))

    return sorted(exponents.values(), reverse=True)

# returns if the first argument dominates the second
def doesDominate(dPartition, partition):
    assert sum(partition) == sum(dPartition)
    partRS = 0
    dPartRS = 0
    for i in range(min(len(partition),len(dPartition))):
        partRS += partition[i]
        dPartRS += dPartition[i]
        if  partRS > dPartRS:
            return False
    return True

# compute the dimension of the Specht module associated with the given
#  partition by using the hook length formula
def spechtDimension(mu):
    # the diagram of mu
    tab = []
    for part in mu:
        row = [0] * part
        tab.append(row)

    hookLengths = []
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            rowLength = len(tab[i]) - j
            colLength = 1
            while i + colLength < len(tab) and len(tab[i + colLength]) > j:
                colLength += 1
            hookLength = rowLength + colLength - 1
            hookLengths.append(hookLength)
    return int(factorial(sum(mu)) / prod(hookLengths))


tabSet = set() # the set of tableaux that we have generated so far
# computes K_{lambda mu}, the number of semistandard tableaux with shape lambda and content mu
def kostka(ell, mu):
    global tabSet

    assert sum(ell) == sum(mu)

    # set up everything

    # 0 is empty
    blankTab = []
    # tells how many filled spots are next to each entry of tab. left and top edges count, but -1's don't
    initOpenings = []
    for index, part in enumerate(ell):
        row = [0]*part
        if index == 0:
            rowOpenings = [1]*part
        else:
            rowOpenings = [0]*part
        rowOpenings[0] += 1
        blankTab.append(row)
        initOpenings.append(rowOpenings)
    content = [i+1 for i, part in enumerate(mu) for j in range(part)]

    tabSet = set()
    # recursively create all possible semistandard tableaux with shape lambda and content mu
    #  we do this by placing the lowest value of content remaining in a "corner"
    #  where a corner is a node in the diagram whose left neighbor and above neighbor have
    #  both been filled already
    fill(blankTab, content, initOpenings, [(0, 0)])
    return len(tabSet)


# recursive filling of tab with content
def fill(tab, c, openings, corners):
    global tabSet
    # base case, no content is left
    if len(c) == 0:
        tTab = tuple(tuple(tRow) for tRow in tab)
        tabSet.add(tTab)
        return


    # note that the lowest number in c must be placed in a corner (a spot that has two openings)
    #  so placing it in all such corners
    iterCorners = corners.copy()
    for i, corner in enumerate(iterCorners):
        # check that this is legal
        if corner[0] != 0 and tab[corner[0]-1][corner[1]] >= c[0]:
            continue
        if corner[1] != 0 and tab[corner[0]][corner[1]-1] > c[0]:
            continue

        # place the content and remove the node from the list of corners
        tab[corner[0]][corner[1]] = c[0]
        corners.pop(i)
        openings[corner[0]][corner[1]] = -1

        # inform the neighbors that this node has been filled
        #  see if that produces any new corners
        if corner[0] + 1 != len(tab) and corner[1] < len(tab[corner[0]+1]):
            openings[corner[0] + 1][corner[1]] += 1
            if openings[corner[0] + 1][corner[1]] == 2:
                corners.append((corner[0] + 1, corner[1]))
        if corner[1] + 1 != len(tab[corner[0]]):
            openings[corner[0]][corner[1] + 1] += 1
            if openings[corner[0]][corner[1] + 1] == 2:
                corners.append((corner[0], corner[1] + 1))

        fill(tab, c[1:], openings, corners)

        # now undo all that so we can place the content in a different corner
        if corner[1] + 1 != len(tab[corner[0]]):
            if openings[corner[0]][corner[1] + 1] == 2:
                corners.pop()
            openings[corner[0]][corner[1] + 1] -= 1
        if corner[0] + 1 != len(tab) and corner[1] < len(tab[corner[0]+1]):
            if openings[corner[0] + 1][corner[1]] == 2:
                corners.pop()
            openings[corner[0] + 1][corner[1]] -= 1
        openings[corner[0]][corner[1]] = 2  # corners have 2 openings

        corners.insert(i, corner)
        tab[corner[0]][corner[1]] = 0