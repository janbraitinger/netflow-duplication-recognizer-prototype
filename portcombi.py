from genericpath import exists
import hashlib
import sys


class PortSelection:

    def __init__(self, netflows):
        self.dataset = netflows

    def iterateJsonDumps(self):
        portListObj = {}
        counter = 0
        for dump in self.dataset:
            if dump["Proto"] == 6 or dump["Proto"] == 17:
                portA = dump["SrcPort"]
                portB = dump["DstPort"]
                tmp = self.makeCombiList(portA, portB)
                
                if not self.makeCombiList(portA, portB) in portListObj:
                    portListObj[str(tmp)] = []
                    counter += 1
                
                portListObj[str(tmp)].append(dump)
        if len(portListObj.keys()) > 0:
            protocol = portListObj[next(iter(portListObj))][0]["Proto"]
            
            if protocol == 6:
                textProto = "TCP"
            if protocol == 17:
                textProto = "UDP"

            print("[info] found", len(portListObj.keys()),
                  "port combinations of", textProto), 

        return portListObj

    def makeCombiList(self, portA, portB):
        newPort = str(portA)+str(portB)
        len = self.getLength(newPort)
        #ck = self.checksum(newPort)
        return self.createHash(len, str(portA+portB))

    def createHash(self, len, ck):
        param = str(len)+str(ck)
        return hashlib.md5(param.encode()).hexdigest()

    def checksum(self, value):
        value = int(value)
        result = 0
        while value:
            result += value % 10
            value = int(value / 10)
        return result

    def getLength(self, param):
        return len(str(param))

    def returnPortList(self):
        return self.iterateJsonDumps()

