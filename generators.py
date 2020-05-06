# MALACHI BUCHHEIT
from random import *

# O(1)
def main():
    sfc = gen_shell_fragile_connected([1, 2, 3, 4], [3, 5, 6, 9], m=3)
    print(sfc)
    file_out(sfc, 'out.txt', form='str')

# O()
# generates a shell-fragile connected set randomly or from/between sets
# root: initial element of the collection
# leaf: endpoint of the collection
# n: exclusive upper bound for elements of k-subsets
# m: num elements between the root and branch (trunk)
# sort: whether the sets should be sorted
def gen_shell_fragile_connected(root, leaf, n=10, m=0, sort=True):
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
    
    trunk = []
    for i in range(m):
        nks = out[i]
        while nks in out:
            nks = gen_next_ksub(k, n, out[len(out)-1], out, i_elems, leaf)
        out.append(nks)
        trunk.append(nks)
    
    branch = gen_branch(out, leaf)

    sort_sets(trunk)
    sort_sets(branch)
    
    print("Root:", root,\
          "\nTrunk:", trunk,\
          "\nBranch:", branch,\
          "\nLeaf:", leaf)
    
    for b in branch:
        out.append(b)
    
    out.append(leaf)
    
    if sort:
        sort_sets(out)

    print(i_elems, '***')
    for i in range(1, len(out)):
        print(intrs([out[0]]+[out[i]]))
    
    return out

# O()
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
        out[randrange(len(out)-1)] = e
    
    return out

# O()
# generates a vector which intersects a set
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: set to intersect
# num: number of intersections
def gen_i_ksub(k, n, s, num=-1):
    out = []

    if num == -1:
        num = k-1
    elif num > k:
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater than the cardinality ("+k+").")
    elif num > len(inters_elems):
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater "+\
              "than the possible intersections ("+len(inters_elems)+").")

    inters_elems = sample(s, k=num)
    #print(s, inters_elems)
    
    for i in range(k):
        if s[i] in inters_elems:
            out.append(s[i])
        else:
            out.append(gen_new_elem(n, s))
    
    return out

# O()
# returns the intersection of all sets in the collection
# c: a collection
def intrs(c):
    out = c[0]
    
    for i in range(1, len(c)):
        out = list(set(out) & set(c[i]))
    
    return out

# O()
# generates the next step of a fragile-connected chain
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: the previous set
# c: the collection thus far
# e: the intersecting elements
# leaf: the final set to reach overall
def gen_next_ksub(k, n, s, c, e, leaf):
    out = []+s
    c_inters = intrs(c)
    
    i = randrange(k)
    while out[i] in e:
        i = randrange(k)
    
    while s[i] == out[i]:
        out[i] = gen_new_elem(n, out+c[0]+leaf)
    
    return out

# O()
# returns an element which does not intersect the set
# n: exclusive upper bound for elements of k-subsets
# s: sets to avoid intersecting
def gen_new_elem(n, s):
    out = [*range(n)]

    for e in s:
        if e in out:
            out.remove(e)
    
    return choice(out)

# O()
# this function builds the connection from the trunk to the leaf
# col: the entire collection thus far
# leaf: the element to reach
def gen_branch(col, leaf):
    trunk = col[len(col)-1]
    out = []
    needed_elems = []
    needed_still = []
    c_inters = intrs([col[0]]+[leaf])
    
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
    for r in range(1, len(out)):
        out[r] = []+out[r-1]
    
        for c in range(len(out[r])):
            if out[r][c] not in needed_elems+c_inters:
                out[r][c] = choice(needed_still)
                needed_still.remove(out[r][c])
                
                # if the set is already in the collection, redo this set
                if out[r][c] in col:
                    r -= 1
                    
                    if out[r][c] in col and needed_still == 1:
                        raise ValueError("Cannot contruct branch."+\
                        "\n"+c+out+leaf) 
                break
    
    out.remove(trunk)
    
    return out

# O()
# sorts a collection's sets' internals
# c: collection
def sort_sets(c):
    for s in c:
        s.sort()

# prints the collection to a file
# c: collection to save
# name: name of the file
# form: format of the collection
def file_out(c, name, form=None):
    f = open(name, 'w')

    if form is None:
        for s in c:
            f.write(''.join(str(s)))
            f.write('\n')
            
    elif form is 'str':
        for s in c:
            for e in s:
                f.write(str(e))
            f.write('\n')

main()
