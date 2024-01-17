from archicad import ACConnection
from typing import List, Tuple, Iterable
from itertools import cycle

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

################################ CONFIGURATION #################################
propertyId = acu.GetBuiltInPropertyId('General_ElementID')
propertyValueStringPrefix = 'P '
classificationItem = acu.FindClassificationItemInSystem(
    'ARCHICAD Classification', 'Parking Space')
elements = acc.GetElementsByClassification(
    classificationItem.classificationItemId)

ROW_GROUPING_LIMIT = 0.25
STORY_GROUPING_LIMIT = 1

def GeneratePropertyValueString(storyIndex: int, elemIndex: int) -> str:
    return f"{propertyValueStringPrefix}{storyIndex:1d}{elemIndex:02d}"
################################################################################


def generatePropertyValue(storyIndex: int, elemIndex: int) -> act.NormalStringPropertyValue:
    return act.NormalStringPropertyValue(GeneratePropertyValueString(storyIndex, elemIndex))


def createClusters(positions: Iterable[float], limit: float) -> List[Tuple[float, float]]:
    positions = sorted(positions)
    if len(positions) == 0:
        return []

    clusters = []
    posIter = iter(positions)
    firstPos = lastPos = next(posIter)

    for pos in posIter:
        if pos - lastPos <= limit:
            lastPos = pos
        else:
            clusters.append((firstPos, lastPos))
            firstPos = lastPos = pos

    clusters.append((firstPos, lastPos))
    return clusters


boundingBoxes = acc.Get3DBoundingBoxes(elements)
elementBoundingBoxes = list(zip(elements, boundingBoxes))
zClusters = createClusters((bb.boundingBox3D.zMin for bb in boundingBoxes), STORY_GROUPING_LIMIT)

storyIndex = 0
elemPropertyValues = []
for (zMin, zMax) in zClusters:
    elemIndex = 1
    elemsOnStory = [e for e in elementBoundingBoxes if zMin <= e[1].boundingBox3D.zMin <= zMax]
    yClusters = createClusters((e[1].boundingBox3D.yMin for e in elemsOnStory), ROW_GROUPING_LIMIT)

    for ((yMin, yMax), reverseOrder) in zip(yClusters, cycle([False, True])):
        elemsInRow = [e for e in elemsOnStory
                        if yMin <= e[1].boundingBox3D.yMin <= yMax]

        for (elem, bb) in sorted(elemsInRow, key=lambda e: e[1].boundingBox3D.xMin, reverse=reverseOrder):
            elemPropertyValues.append(act.ElementPropertyValue(
                elem.elementId, propertyId, generatePropertyValue(storyIndex, elemIndex)))
            elemIndex += 1
    storyIndex += 1

acc.SetPropertyValuesOfElements(elemPropertyValues)

# Print the result
newValues = acc.GetPropertyValuesOfElements(elements, [propertyId])
elemAndValuePairs = [(elements[i].elementId.guid, v.propertyValue.value) for i in range(len(newValues)) for v in newValues[i].propertyValues]
for elemAndValuePair in sorted(elemAndValuePairs, key=lambda p: p[1]):
    print(elemAndValuePair)
