from _lib import getRawForDay

data = getRawForDay(8).strip()

WIDTH = 25
HEIGHT = 6

# imageLayers is a three-level deep data structure:
# imageLayers is an array of Layers
# Each layer is an array of rows
# Each row is an array of letter (string of length 1 between '0' and '9')

imageLayers = [[[]]]
currentLayer = imageLayers[0]
currentRow = currentLayer[0]

for letter in data:
    currentRow.append(letter)
    if len(currentRow) == WIDTH:
        # We need to add a row before we add the next letter
        if len(currentLayer) == HEIGHT:
            # We need to add a layer before we add the next row
            imageLayers.append([])
            currentLayer = imageLayers[-1]
        currentLayer.append([])
        currentRow = currentLayer[-1]

# This implementation adds an empty layer at the end
# Rather than fixing this bug, we just remove it
if len(imageLayers[-1]) == 1 and len(imageLayers[-1][-1]) == 0:
    imageLayers.pop()

# Disclaimer:
# I have the flu and am half-conscious
# so i'm gonna do this step by step

# metadata is the number of each digit in layers
metadata = []
for layer in imageLayers:
    _m = {}
    for d in range(10):
        _m[d] = 0
        for row in layer:
            _m[d] += row.count(str(d))

    print _m
    metadata.append(_m)

bestLayerMetadata = None
bestValue = 1000000
for _m in metadata:
    if _m[0] < bestValue:
        bestLayerMetadata = _m
        bestValue = _m[0]

print bestLayerMetadata
print bestLayerMetadata[1] * bestLayerMetadata[2]


# past answers
# 2162 (too low)