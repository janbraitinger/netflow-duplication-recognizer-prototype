from ast import arg
from dis import dis
import base64
from typing import final
from random import randrange
from pyparsing import col
from distance import Distance
from portcombi import *
from selectProtocol import *
from listGenerator import *
from plotDist import *
from distance import *
from preprocessing import *
import matplotlib.colors as colors
import socket
import sys
import argparse
import os

# ToDos:
# - Rework import style
# - Test it with multiple FlowCombinations
# - Implement click for choosing files etc.
# - Comments


class Main:
    colorSchema = list(colors._colors_full_map.values())
    finalecounter = 0
    duplicatedList = []

    def roundup(self, value):
        result = int(value)
        if result != value and value > 0:
            result += 1
        return result

    # convert the address fields in legible ip addresses
    def convert_ipv4(self, ip):
        try:
            if len(ip) > 8:
                adjustedIp = ip.split("/")
                return adjustedIp[len(adjustedIp)-1]
            return socket.inet_ntoa(base64.b64decode(ip))
        except:
            print(ip)

    # get length of an object/dic

    def getLength(self, mylist):
        counter = 0
        for kwy, element in mylist.items():
            for subelement in element:
                counter += 1
        return counter

    # dispaly all port combination of one protocol - no distance calculation
    def displayAll(self, portList, plot):
        i = 0
        colorSchema = ['r', 'g', 'b', 's']
        for key, x in portList.items():
            plot.generatePlot(x, colorSchema[i])
            i += 1

    # display one port combination
    def displayOne(self, portList, i, plot):
        tmp = list(portList.values())[i]
        plot.generatePlot(tmp, 'g')

    def getSingleListOfPorts(self, _list, i):
        return list(_list.values())[i]

    # get all processede IDs of tuples
    def getAllIdsOfTuples(self, tupleObj):
        idList = []
        for key, elements in tupleObj.items():
            for element in elements:
                if element[0] not in idList:
                    idList.append(element[0])
                if element[1] not in idList:
                    idList.append(element[1])
        return idList

    # get the min tuple of each list in the dic

    def getMinsOfDic(self, tupleObj):
        minList = []

        for key, values in tupleObj.items():
            tmpList = []
            for value in values:
                tmpList.append(value)
            if len(tmpList) > 0:
                minList.append(min(tmpList, key=lambda x: x[2]))
        return minList

    # return every id until the best one (so only noise)
    def getMaxsOfDic(self, tupleObj):
        maxList = []
        for key, values in tupleObj.items():
            tmpList = []
            for value in values:
                tmpList.append(value)
            if len(tmpList) > 0:
                maxListTmp = sorted(
                    tmpList, key=lambda x: float(x[2]), reverse=True)
                for entry in maxListTmp[:-1]:
                    # print(entry)
                    maxList.append(entry)

        return maxList

    # based on the ids of the similar flows, all others are noise
    # this method get the ids of them for later
    def noiseChecking(self, minTupleList, _flowIDs):
        flowIDs = _flowIDs
        noiseTuples = []
        doubletsListIds = []
        doubletsList = []
        doubleListIdsAdjusted = []

        for singleTuple in minTupleList:
            # print(singleTuple)
            idA = singleTuple[0]
            idB = singleTuple[1]

            if idA in flowIDs:
                flowIDs.remove(idA)
            if idB in flowIDs:
                flowIDs.remove(idB)
            else:  # get doublets
                if idA not in doubletsListIds:
                    doubletsListIds.append(idA)
                if idB not in doubletsListIds:
                    doubletsListIds.append(idB)

        # self.printList(doubletsListIds)

        for singleTuple in minTupleList:

            idA = singleTuple[0]
            idB = singleTuple[1]
            for doubleIds in doubletsListIds:
                if idA == doubleIds or idB == doubleIds:
                    doubletsList.append(singleTuple)

                    break

        idCounterList = []
        for singleDoubleTuple in doubletsList:
            idA = singleDoubleTuple[0]
            idB = singleDoubleTuple[1]
            idCounterList.append(idA)
            idCounterList.append(idB)

        doubletsIdListObj = {}
        doubletsIdSet = set(
            [x for x in idCounterList if idCounterList.count(x) > 1])
        noiseIds = []
        for values in doubletsIdSet:
            for singleDoubleTuple in doubletsList:
                idA = singleDoubleTuple[0]
                idB = singleDoubleTuple[1]
                if values not in doubletsIdListObj:
                    doubletsIdListObj[values] = []
                if idA == values or idB == values:
                    doubletsIdListObj[values].append(singleDoubleTuple)

        # nicht nur max streichen sondern alle bis auf kleinsten
        noiseTuples = self.getMaxsOfDic(doubletsIdListObj)

        return noiseTuples

    # loop through all portcombinations, calc the distances and display the similar ones
    def printList(self, list):
        for element in list:
            print(element)

    def printObj(self, obj):
        for key, values in obj.items():
            print(values)

    def removeNoise(self, totalList, noiseList):

        for noise in noiseList:
            totalList.remove(noise)
        # self.printList(totalList)
        return totalList

    def getIDsofList(self, _list):
        resultList = []
        for entry in _list:
            if entry[0] not in resultList:
                resultList.append(entry[0])
            if entry[1] not in resultList:
                resultList.append(entry[1])
        return resultList

    def getJSON(searchParameter, jsonList):
        for json in jsonList:
            if json[searchParameter] == searchParameter:
                return json[searchParameter]
        return "error"

    def analyse(self, data, proto, outputPath, visualize):
        breakUpCounter = 0
        # marker for plotting the flows
        markerList = ["D", "s", "o", "v"]
        markerCount = 0
        plot = Visualize()
        totalNoiseList = []

        # for each port combination of this dataObj
        for portcombi in range(0, len(data)):
            print("[info] analysing new portcombination ")
            distanceOfFlowsObj = Distance()
            flowList = self.getSingleListOfPorts(data, portcombi)
            distanceOfFlowsObj = distanceOfFlowsObj.euclidean(flowList)

            # if the system was not able to calc distances (please refer distance.py)
            if distanceOfFlowsObj != "error":

                idsdList = self.getAllIdsOfTuples(distanceOfFlowsObj)
                totalIDList = self.getAllIdsOfTuples(distanceOfFlowsObj)
                distanceList = self.getMinsOfDic(distanceOfFlowsObj)
                #print(distanceOfFlowsObj)
                # sys.exit(0)
                # toDo: check IPs here and not just befor plotting the points

                noiseList = self.noiseChecking(distanceList, idsdList)

                withoutNoise = self.removeNoise(distanceList, noiseList)
                difference = set(totalIDList).symmetric_difference(
                    set(self.getIDsofList(withoutNoise)))
                list_difference = list(difference)

                if markerCount >= len(markerList):
                    markerCount = 0

                ipNoiseList = self.visualizeTupleList(
                    withoutNoise, flowList, plot, markerList[markerCount], outputPath)

                for ipNoise in ipNoiseList:
                    noiseTupleA = ipNoise[0]
                    noiseTupleB = ipNoise[1]
                    totalNoiseList.append(noiseTupleA)
                    totalNoiseList.append(noiseTupleB)

                for singleDifference in list_difference:
                    totalNoiseList.append(singleDifference)

                breakUpCounter += 1

                # here you can set how much portcombinaitons of each protocol should be passed
                # if breakUpCounter == 1:
                #    break

            markerCount += 1

        # print("[info] noise: ",totalNoiseList)
        # plot noise - be carefull: a lot of data to plot
        # self.visualizeNoiseList(totalNoiseList, plot)
        plot.setTitel(proto)
        # print(self.finalecounter)
        if visualize == "True":
            plot.display()

    def visualizeNoiseList(self, ids, plot):
        _tmpList = []
        for flowId in ids:
            for json in self.jsonRawList:
                if json["id"] == flowId:
                    _tmpList.append(json)
        plot.generatePlot(_tmpList, "gray", True, "noise", "x")

    def compareIP(self, ipPair):
        ipDstA = self.convert_ipv4(ipPair[0])
        ipDstB = self.convert_ipv4(ipPair[2])
        ipSrcA = self.convert_ipv4(ipPair[1])
        ipSrcB = self.convert_ipv4(ipPair[3])
        if ipDstA == ipDstB or ipSrcA == ipSrcB or ipSrcA == ipDstB or ipSrcB == ipDstA:
            return True
        return False

    def visualizeTupleList(self, tupleList, jsonList, plot, marker, outputPath):
   
        resultList = []
        _tmpList = []
        ipFails = []
        for flowTuple in tupleList:
   
          
                color = randrange(len(self.colorSchema))
                _tmpList = []
                a = flowTuple[0]
                b = flowTuple[1]
                ipCheckList = []
                for json in jsonList:
                    # check if ip addresses are equal (todo: put it somewhere else...)
                    if json["id"] == a:
                        resultList.append(json)
                        _tmpList.append(json)
                        ipCheckList.append(json["DstAddr"])
                        ipCheckList.append(json["SrcAddr"])
                    if json["id"] == b:
                        ipCheckList.append(json["DstAddr"])
                        ipCheckList.append(json["SrcAddr"])
                        _tmpList.append(json)
                if self.compareIP(ipCheckList):
                    # print(flowTuple)
                    self.finalecounter += 1
                    self.duplicatedList.append(_tmpList[0])
                    self.duplicatedList.append(_tmpList[1])
                    print("[info] duplicate entry: ", flowTuple)
                    plot.generatePlot(
                        _tmpList, self.colorSchema[color], True, "Dist: " + str(self.roundup(flowTuple[2])), marker)
                else:
                    print("[warning] ip addresses missmatch on", flowTuple)
                    ipFails.append(flowTuple)
                    pass
    

        if outputPath != None:
            #print(outputPath)
            self.writeToFile(self.duplicatedList, outputPath)
        return ipFails

    def getDuplicates(self, flows):
        pass

    def writeToFile(self, data, path):
        with open(path, 'w') as f:
            counter = 0
            for item in data:
                counter += 1
                f.write(str(json.dumps(item))+'\n')
                if counter == 2:
                    f.write('\n')
                    counter = 0

    def __init__(self, fileList, protoFilter, outputPath, visualize):
        # self.fileLocation = fileLocation
        # listGenerator = ListGenerator(self.fileLocation)
        # self.jsonRawList = listGenerator.getList()

        adjustedNewList = []
        # for file in fileList:
        #    adjustedNewList.append(json.loads(file))
        #self.jsonRawList = adjustedNewList
        # generate dict
        flowProtoFilter = ProtoSelection(fileList)

        # protocol filter
        tcpFilter = flowProtoFilter.getTcpList()
        udpFilter = flowProtoFilter.getUdpList()

        # create dict with portcombinations and their flows
        tcpPort = PortSelection(tcpFilter)
        tcpPortList = tcpPort.returnPortList()
        udpPort = PortSelection(udpFilter)
        udpPortList = udpPort.returnPortList()

        # analyse all tcp port combination with euclidean distance
        if protoFilter == "tcp":
            self.analyse(tcpPortList, "TCP", outputPath, visualize)
        else:
            self.analyse(udpPortList, "UDP", outputPath, visualize)


# get input files by user
print("[info] starting process")
dir_path = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(
    description='netflow-duplication-recognizer')
# parser.add^_argument("-f", "--json_file",
#                    help="sourcefile of flows in json format")
parser.add_argument("-1", "--source_one",
                    help="sourcefile of flows in json format", required=True)
parser.add_argument("-2", "--source_two",
                    help="sourcefile of flows in json format", required=True)
parser.add_argument("-o", "--outputFile",
                    help="targetfile for duplicates flows in json format (if none -> no output data)")
parser.add_argument("-p", "--protocol",
                    help="filter for tcp/udp protocol", default="udp")
parser.add_argument("-v", "--visualize",
                    help="if you want to plot the results - True/False", default=True)

args = parser.parse_args()
protoFilter = ""
if not args.source_one or not args.source_two:
    parser.error(
        'Please select two json files from different locations with the flags -1 and -2')


file = []
preProcessing = PreProcessing()
file = preProcessing.handleInput(
    dir_path + '/' + args.source_one, dir_path + '/' + args.source_two)

Main(file, args.protocol, args.outputFile, args.visualize)
print("[info] done")
