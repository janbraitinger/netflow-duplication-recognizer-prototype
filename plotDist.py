from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Visualize:

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def setTitel(self, _title):
        return self.fig .suptitle(_title, fontsize=20)

    def convertProtoTyp(self, proto):
        if proto == 6:
            return "TCP"
        if proto == 17:
            return "UDP"

    def getLabelInfo(self, element):
        result = str(self.convertProtoTyp(
            element["Proto"])) + ": " + str(element["DstPort"]) + " - " + str(element["SrcPort"])
        return result

    def generatePlot(self, netflows, color='r', _vectorFlag=False, _label="", _marker='o'):
        vectorList = []
        _flag = True
        for element in netflows:

            if _flag and not _vectorFlag:
                _label = self.getLabelInfo(element)
                _flag = False

            vectorList.append(
                (element["Bytes"], element["Packets"], element["TimeFlowEnd"]))

        xs = []
        ys = []
        zs = []

        n = len(vectorList)

        for element in vectorList:
            xs.append(int(element[0]))
            ys.append(int(element[1]))
            zs.append(int(element[2]))

        self.ax.scatter(xs, ys, zs, c=color,
                        marker=_marker, s=12**2, label=_label)

        for i in range(0, n):
            self.ax.text(xs[i], ys[i], zs[i], netflows[i]["loc"])
            #self.ax.text(xs[i], ys[i], zs[i], netflows[i]["loc"]+" [" + str(netflows[i]["id"])+"]")

            try:
                if _label != "noise":
                    x_values = [xs[0], xs[1]]
                    y_values = [ys[0], ys[1]]
                    z_values = [zs[0], zs[1]]
                    plt.plot(x_values, y_values, z_values,
                             color, linestyle="--")
            except:
                pass

        self.ax.set_xlabel('Bytes')
        self.ax.set_ylabel('Packets')
        self.ax.set_zlabel('FlowTimeEnd')
        self.ax.legend()
        self.fig.set_size_inches((20, 13))

    def display(self):
        print("[info] displaying plot")
        plt.show()
