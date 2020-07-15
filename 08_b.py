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

decodedImg = []
for y in range(HEIGHT):
    decodedImg.append([])
    decodedRow = decodedImg[-1]
    for x in range(WIDTH):
        for layer in imageLayers:
            value = int(layer[y][x])
            if value == 0:
                decodedRow.append(0)
                break
            elif value == 1:
                decodedRow.append(1)
                break
            else:
                assert value == 2
        else:
            # If no layer has a 1 or a 0, something is weird
            raise Exception("Position " + str(x) + " " + str(y) + " has no value")

# Display the img in a semi-legible manner
for row in decodedImg:
    print row

# I read it as 2YBLH
# but that's false so maybe it's Z
# -> It was

# for completeness, here it is in a more legible manner
for row in decodedImg:
    print "".join(['#' if c == 1 else ' ' for c in row])
