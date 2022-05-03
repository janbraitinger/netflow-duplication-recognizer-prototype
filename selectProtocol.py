class ProtoSelection:

    # tcp 6
    # udp 17

    def __init__(self, jsonList):
        self.jsonList = jsonList

    def getTcpList(self):
        tcpList = self.filterForProto(6)
        return tcpList

    def getUdpList(self):
        tcpList = self.filterForProto(17)
        return tcpList

    def filterForProto(self, protocol):
        tmpList = []
        for singleFlow in self.jsonList:
            flowProto = singleFlow["Proto"]
            if flowProto == protocol:
                tmpList.append(singleFlow)
        if protocol == 6:
            textProto = "TCP"
        if protocol == 17:
            textProto = "UDP"
        print("[info] found ", len(tmpList), "flows of ", textProto)
        return tmpList
