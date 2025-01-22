from util import partitions, doesDominate, spechtDimension, kostka

def verifyInequality(mu):
    n = sum(mu)
    p = sorted(partitions(n), reverse=True)
    for ell in p:
        if ell == (n,) or ell == (n-1,1) or not doesDominate(ell, mu):
            continue
        K = kostka(ell, mu)
        dim = spechtDimension(ell)
        assert (n-1)*K <= (len(mu)-1)*dim
        print(ell, "&", K, "&", dim, "&", (n-1)*K, "&", (len(mu)-1)*dim, "\\\\")
    print()

verifyInequality((2,2,1))
verifyInequality((2,2,2))