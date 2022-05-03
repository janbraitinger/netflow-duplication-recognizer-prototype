import json
import hashlib
import sys


class PreProcessing:
    def handleInput(self, fileA, fileB):
        finalFlowList = []
        flowSources = ["krik", "spock"]
        baseId = 0
        json_files = [fileA, fileB]
        for i in range(0, len(json_files)):
            try:
                with open(json_files[i], 'r') as json_file:
                    for jsonObj in json_file:
                        try:
                            jsonObj = json.loads(jsonObj)
                            _hash = hashlib.md5(str(jsonObj).encode("utf-8")).hexdigest()
                            jsonObj["loc"] = flowSources[i]
                            #jsonObj["id"] = _hash
                            jsonObj["id"] = baseId
                            baseId += 1
                            jsonFinal = json.dumps(jsonObj)
                            finalFlowList.append(jsonObj)
                        except:
                            print("[error] please check your json files - it occurred a error")
            except:
                print("[error] files could not be opend")
                sys.exit(0)


        return finalFlowList


