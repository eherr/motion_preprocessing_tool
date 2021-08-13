'''
based on : http://www.technicaljar.com/?p=688
'''
from PySide2 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = []
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
     
    def init(self, num_sub_graphs=1):
        num_sub_graphs = int(num_sub_graphs)
        self.axes = []
        for i in range(num_sub_graphs):
            #m x n grid +  number of subgraph
            axis = self.fig.add_subplot(num_sub_graphs,1,i+1)
            self.axes.append(axis) 
            self.axes[i].axis("off")
        FigureCanvas.updateGeometry(self)
        
        
class CustomMatplotlibWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        
    def getSubPlot(self,axis = 0):
        return self.canvas.axes[axis]
        
    def getFigureId(self):
    	return self.canvas.fig