import json


class ListGenerator:

    def __init__(self, path):
        print("[info] analysing the file:", path)
        self.jsonList = []
        self.json_file = path
        with open(self.json_file, 'r') as self.json_file:
            for jsonObj in self.json_file:
                allJsonObjs = json.loads(jsonObj)
                self.jsonList.append(allJsonObjs)
        print("[info] found", len(self.jsonList)," netflow json dumps")
                

    def getList(self):
        return self.jsonList
