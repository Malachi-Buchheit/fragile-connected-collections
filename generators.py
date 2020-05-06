# MALACHI BUCHHEIT
from random import *

# O(1)
def main():
    sfc = gen_shell_fragile_connected(root=[0, 1, 2, 3, 4],\
                                      leaf=[3, 4, 5, 6, 7],\
                                      m=3)
##    sfc = gen_shell_fragile_connected(m=3)
    print(sfc)
    file_out(sfc, 'out.txt', form='str')

# O(nlogk + nlog(num) + k + |c|k + m(|e| + |s|n) + m + k + |e| + k|e|^2 + |e|)
# generates a shell-fragile connected set randomly or from/between sets
# root: initial element of the collection
# leaf: endpoint of the collection
# n: exclusive upper bound for elements of k-subsets
# m: num elements between the root and branch (trunk)
# sort: whether the sets should be sorted
def gen_shell_fragile_connected(root=None, leaf=None, n=10, m=0, sort=True):
    if root is None:
        # O(nlogk)
        root = gen_rand_ksub(choice([*range(3, 6)]), n)
    
    if leaf is None:
        # O(nlog(num) + k)
        leaf = gen_i_ksub(len(root), n, root, num=randrange(1, len(root)))
    # O(|c|k)
    elif intrs([leaf]+[root]) is None:
        raise ValueError("Root and leaf share no elements.")

    if len(root) != len(leaf):
        raise ValueError("Root and leaf do not match size.")

    # root
    root.sort()
    out = [root]

    # trunk
    # O(|c|k + m(|e| + |s|n))
    trunk = gen_trunk(root, leaf, m, n)
    sort_sets(trunk)

    # O(m)
    for t in trunk:
        out.append(t)

    # branch
    # O(k + |e| + k|e|^2)
    branch = gen_branch(out, leaf)
    sort_sets(branch)

    # O(|e|)
    for b in branch:
        out.append(b)

    # leaf
    leaf.sort()
    out.append(leaf)

    
    print("Root:", root,\
          "\nTrunk:", trunk,\
          "\nBranch:", branch,\
          "\nLeaf:", leaf)

    print(intrs([root]+[leaf]), '***')
    for i in range(1, len(out)):
        print(intrs([out[0]]+[out[i]]))
    
    return out

# O(nlogk)
# generates a random set
# k: cardinality of the set
# n: exclusive upper bound for elements of k-subsets
def gen_rand_ksub(k, n):
    # O(nlogk)
    return sample([*range(n)], k=k)

# O(nlog(num) + k)
# generates a vector which intersects a set
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: set to intersect
# num: number of intersections
def gen_i_ksub(k, n, s, num=-1):
    if num == -1:
        num = k-1

    # O(nlog(num))
    inters_elems = sample(s, k=num)
        
    if num > k:
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater than the cardinality ("+k+").")
    elif num > len(inters_elems):
        raise ValueError("The number of intersections requested ("+num+")"+\
              "is greater "+\
              "than the possible intersections ("+len(inters_elems)+").")

    out = []

    # O(k)
    for i in range(k):
        if s[i] in inters_elems:
            out.append(s[i])
        else:
            out.append(gen_new_elem(n, s))
    
    return out

# O(|c|k)
# returns the intersection of all sets in the collection
# c: a collection
def intrs(c):
    out = c[0]

    # O(|c|)
    for i in range(1, len(c)):
        # O(k+k)
        out = list(set(out) & set(c[i]))
    
    return out

# O(|c|k + m(|e| + |s|n))
# generates the trunk
# root: the initial set
# leaf: the final set
# m: the number of sets to generate
# n: exclusive upper bound for elements of k-subsets
def gen_trunk(root, leaf, m, n):
    out = [root]
    # O(|c|k)
    i_elems = intrs([root]+[leaf])

    # O(m)
    for i in range(m):
        nks = out[i]

        while nks in out:
            # O(|e| + |s|n)
            nks = gen_next_ksub(len(root), n, out[len(out)-1], out, i_elems, leaf)

        out.append(nks)

    out.remove(root)
    
    return out
        
# O(|e| + |s|n)
# generates the next step of a fragile-connected chain
# k: cardinality of the sets
# n: exclusive upper bound for elements of k-subsets
# s: the previous set
# c: the collection thus far
# e: the intersecting elements
# leaf: the final set to reach overall
def gen_next_ksub(k, n, s, c, e, leaf):
    out = []+s

    # O(|e|)
    i = randrange(k)
    while out[i] in e:
        i = randrange(k)

    while s[i] == out[i]:
        # O(|s|n)
        out[i] = gen_new_elem(n, out+c[0]) # +leaf
    
    return out

# O(|s|n)
# returns an element which does not intersect the set
# n: exclusive upper bound for elements of k-subsets
# s: sets to avoid intersecting
def gen_new_elem(n, s):
    out = [*range(n)]

    # O(|s|)
    for e in s:
        if e in out:
            # O(n)
            out.remove(e)
    
    return choice(out)

# O(k + |e| + k|e|^2)
# this function builds the connection from the trunk to the leaf
# c: the entire collection thus far
# leaf: the element to reach
def gen_branch(c, leaf):
    trunk = c[len(c)-1]
    out = []
    needed_elems = []
    needed_still = []
    c_inters = intrs([c[0]]+[leaf])
    
    # identify all needed elements
    # O(k)
    for a in leaf:
        if a not in trunk:
            needed_elems.append(a)        
    #print("Needed Elems:", needed_elems)
    
    needed_still = []+needed_elems
    
    # set the first element to the trunk
    out.append(trunk)
    
    # create a set for each missing element - 1
    # O(|e|)
    for i in range(len(needed_elems)-1):
        out.append([])
    
    # starting from the second index, go through the remaining empty sets
    # O(|e|)
    for x in range(1, len(out)):
        out[x] = []+out[x-1]

        # O(k)
        for y in range(len(out[r])):
            # O(|e|)
            if out[x][y] not in needed_elems+c_inters:
                # O(|e|)
                out[x][y] = choice(needed_still)
                # O(|e|)
                needed_still.remove(out[x][y])
                
                # if the set is already in the collection, redo this set
                if out[x][y] in c:
                    r -= 1

                    # O(|e|)
                    if out[x][y] in c and needed_still == 1:
                        raise ValueError("Cannot contruct branch."+\
                        "\n"+y+out+leaf) 
                break

    # O(|e|)
    out.remove(trunk)
    
    return out

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
