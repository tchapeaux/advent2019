from _lib import getLinesForDay

myInput = getLinesForDay(6)

exampleInputs = [
    'COM)B',
    'B)C',
    'C)D',
    'D)E',
    'E)F',
    'B)G',
    'G)H',
    'D)I',
    'E)J',
    'J)K',
    'K)L',
]

# dict of node -> parent node
familyTree = {}
for descr in myInput:
    [parent, node] = descr.split(')')
    familyTree[node] = parent

def countOrbits(tree):
    count = 0
    for node in familyTree.keys():
        curNode = node
        while curNode != 'COM':
            parentNode = familyTree[curNode]
            print parentNode, "is parent of", curNode
            curNode = parentNode
            count += 1
    print count

countOrbits(familyTree)