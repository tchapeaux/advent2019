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

def getPathFromComTo(node):
    path = []
    curNode = node
    while curNode != 'COM':
        parentNode = familyTree[curNode]
        # print parentNode, "is parent of", curNode
        curNode = parentNode
        path.append(curNode)
    return path

youPath = getPathFromComTo('YOU')
print "you", youPath

sanPath = getPathFromComTo('SAN')
print "san", sanPath

intersect = [n for n in youPath if n in sanPath]
print "inter", intersect
firstCommonNode = intersect[0]

print youPath.index(firstCommonNode) + sanPath.index(firstCommonNode)
