from genericpath import exists
from lib2to3.pytree import convert
import math
import numpy as np
from numpy import dot
from numpy.linalg import norm
from xml.dom.minidom import Element

import sys


class Distance:
    def __init__(self):
        pass

    # return vector (tuple)
    def convertToVector(self, netflow):
        return (netflow["id"], netflow["Bytes"],
                netflow["Packets"], netflow["TimeReceived"])

    # check all posible sources of the flows
    def prepare(self, netflowPortCombinations):
        locations = {}
        for netflow in netflowPortCombinations:
            singleLoc = str(netflow["loc"])
            if singleLoc not in locations:
                locations[singleLoc] = []

            # convert json flow in vector (tuple)
            netflowVector = self.convertToVector(netflow)
            locations[singleLoc].append(netflowVector)

        # if only one sources, it is not possible to calculate distances
        if len(locations) <= 1:
            print(
                "[info] found only one source for this set - not able to calc distances")
            return False
        else:
            print("[info] found", len(locations), "sources")
        return locations

    # seperate flowList in two lists based on location -> HARDCODED for two sources
    def seperateInLists(self, data):
        listA = []
        listB = []
        i = 0
        for key, loc in data.items():
            for vector in loc:
                if i == 0:
                    listA.append(vector)
                if i == 1:
                    listB.append(vector)
            i += 1
        if len(listA) >= len(listB):
            return listA, listB

        return listB, listA

    # check the length of each list
    def fieldCheck(self, listA, listB):
        lenList = [len(listB), len(listA)]
        if sum(lenList) % len(lenList) != 0:
            print("[info] 1:1 mapping")
        else:
            print("[warning]", len(listA), "to", len(listB), "mapping")

    # calc euclidean distance based on flows of one portcombination
    def euclidean(self, data):
        resultObj = {}
        #print("[info] euclidean distance")
        flows = self.prepare(data)

        # if only one location -> only one source of flows
        if flows == False:
            return "error"

        # seperate in lists (max 3 possible)
        listA, listB = self.seperateInLists(flows)
        self.fieldCheck(listA, listB)

        # calc euclidean distance
        for a in listA:
            for b in listB:
                x = int(b[1]) - int(a[1])
                y = int(b[2]) - int(a[2])
                z = int(b[3]) - int(a[3])
                dist = math.sqrt(x**2 + y**2 + z**2)
                newElement = a[0], b[0], dist

                # ListA >= ListB -> a is label
                label = a[0]
                if not label in resultObj:
                    resultObj[label] = []
                resultObj[label].append(newElement)

        #print("[info] calculated euclidean distances between the vectors")
        return resultObj

    def manhatten(self, data):
        resultObj = {}
        #print("[info] manhatten distance")
        flows = self.prepare(data)

        # if only one location -> only one source of flows
        if flows == False:
            return "error"

        # seperate in lists (max 3 possible)
        listA, listB = self.seperateInLists(flows)
        self.fieldCheck(listA, listB)

        for a in listA:
            tmpATuple = (int(a[1]), int(a[2]), int(a[3]))
            for b in listB:
                tmpBTuple = (int(b[1]), int(b[2]), int(b[3]))

                newElement = a[0], b[0], self.calcManhattan(
                    tmpATuple, tmpBTuple)
                # print(newElement)
                #print(tmpATuple, tmpBTuple, cos_sim)
                label = a[0]
                if not label in resultObj:
                    resultObj[label] = []
                resultObj[label].append(newElement)

        # sys.exit(0)
        #print("[info] calculated manhatten distances between the vectors")
        return resultObj

    def calcManhattan(self, a, b):
        return sum(abs(val1-val2) for val1, val2 in zip(a, b))

    def cosine(self, data):
        resultObj = {}
        print("[info] cosine distance")
        flows = self.prepare(data)

        # if only one location -> only one source of flows
        if flows == False:
            return "error"

        # seperate in lists (max 3 possible)
        listA, listB = self.seperateInLists(flows)
        self.fieldCheck(listA, listB)

        for a in listA:
            tmpATuple = (int(a[1]), int(a[2]), int(a[3]))
            for b in listB:
                tmpBTuple = (int(b[1]), int(b[2]), int(b[3]))
                cos_sim = dot(tmpATuple, tmpBTuple) / \
                    (norm(tmpATuple)*norm(tmpBTuple))
                newElement = a[0], b[0], cos_sim
                #print(tmpATuple, tmpBTuple, cos_sim)
                label = a[0]
                if not label in resultObj:
                    resultObj[label] = []
                resultObj[label].append(newElement)

        print("[info] calculated cosine distances between the vectors")
        return resultObj
