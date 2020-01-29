# MALACHI BUCHHEIT
from random import *

def main():
    sfc = gen_shell_fragile_connected([1, 2, 3, 4], [4, 5, 6, 7])
    print(sfc)
        
# returns the intersection of all sets in the list of sets
# s: a list of sets
def intrs(s):
    out = s[0]
    
    for i in range(1, len(s)):
        out = list(set(out) & set(s[i]))
    
    return out

# returns an element which does not intersect the set
# n: exclusive upper bound for elements of k-subsets
# s: sets to avoid intersecting
def gen_new_elem(n, s):
    out = [*range(n)]
    
    for e in s:
        if e in out:
            out.remove(e)
    
    return choice(out)

# generates a random vector
# k: cardinality of the set
# n: exclusive upper bound for elements of k-subsets
# e: element to include
def gen_rand_ksub(k, n, e=None):
    out = []
    # out = [randrange(n) for i in range(k)]
    for i in range(k):
        out.append(randrange(n))
    
    if e is not None:
        out[randrange(len(out))] = e
    
    return out

# generates a vector which intersects a set
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: set to intersect
# num: number of intersections to try
def gen_i_ksub(k, n, s, num=1):
    out = []
    inters_elems = intrs(s)
        
    if num > k:
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater than the cardinality ("+k+").")
    elif num > len(inters_elems):
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater "+\
              "than the possible intersections ("+len(inters_elems)+").")
    
    # choose a random element in the intersection of all sets
    inters_elem = choice(inters_elems)
    
    for i in range(k):
        if i == inters_elem:
            out.append(i)
        else:
            out.append(randrange(n))
    
    return out
    
# generates the next step of a fragile-connected chain
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: the previous set
# e: the intersecting elements
# leaf: the final set to reach overall
def gen_next_ksub(k, n, s, e, leaf):
    out = []+s
    
    ic = randrange(len(out))
    while out[ic] in e:
        ic = randrange(len(out))
    
    while s[ic] == out[ic]:
        out[ic] = gen_new_elem(k, n, out+leaf)
    
    return out

# this function builds the connection from the trunk to the leaf
# col: the entire collection thus far
# leaf: the element to reach
def gen_branch(col, leaf):
    trunk = col[len(col)-1]
    out = []
    needed_elems = []
    needed_still = []
    
    # identify all needed elements
    for a in leaf:
        if a not in trunk:
            needed_elems.append(a)        
    #print("Needed Elems:", needed_elems)
    
    needed_still = []+needed_elems
    
    # set the first element to the trunk
    out.append(trunk)
    
    # create a set for each missing element - 1
    for i in range(len(needed_elems)-1):
        out.append([])
    
    # starting from the second index, go through the remaining empty sets
    r = 1
    while r < len(out):
        out[r] = []+out[r-1]
    
        for c in range(len(out[r])):
            if out[r][c] not in needed_elems:
                out[r][c] = choice(needed_still)
                needed_still.remove(out[r][c])
                
                # if the set is already in the collection, redo this set
                if out[r][c] in col:
                    r -= 1
                    
                    if out[r][c] in col and needed_still == 1:
                        raise ValueError("Cannot contruct branch."+\
                        "\n"+c+out+leaf) 
                break
        r += 1
    
    out.remove(trunk)
    
    return out
                
# generates a shell-fragile connected set randomly or from/between sets
# root: initial element of the collection
# leaf: endpoint of the collection
# n: exclusive upper bound for elements of k-subsets
# m: num elements between the root and leaf
def gen_shell_fragile_connected(root, leaf, n=10, m=0):
    k = len(root)
    
    if len(root) != len(leaf):
        raise ValueError("Root and leaf do not match size.")
    
    if root is None:
        root = gen_rand_ksub(k, n)
    elif len(root) != k:
        raise ValueError("Root "+root+" is not the right cardinality.")
    
    if leaf is None:
        leaf = gen_i_ksub(k, n, [root])
    elif len(leaf) != k:
        raise ValueError("Root "+root+" is not the right cardinality.")
    elif intrs([leaf]+[root]) is None:
        raise ValueError("Root and leaf share no elements.")
    
    out = [root]
    
    i_elems = intrs([leaf]+[root])
    
    for i in range(m):
        nks = out[0]
        while nks in out:
            nks = gen_next_ksub(k, n, out[len(out)-1], i_elems, leaf)
        out.append(nks)
    
    branch = gen_branch(out, leaf)
    
    #print("Root+Trunk:", out, "\nBranch:", branch, "\nLeaf:", leaf)
    
    for b in branch:
        out.append(b)
    
    out.append(leaf)
    
    sort_sets(out)
    
    return out

# sorts a collection's sets' internals
# c: collection
def sort_sets(c):
    for s in c:
        s.sort()

main()

