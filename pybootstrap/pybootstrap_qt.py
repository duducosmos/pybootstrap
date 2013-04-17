#!/usr/bin/env python
__title__ = "bootstrap_qt.py"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "12/04/2013"
__versio__ = "0.1"
"""
Bootstrap resample with replacement as described by
Wherens et al. 2000

Wherens, R. et al., 2000. Chemometrics and Inteligent Laboratory System, 54, 35


This file is part of PyBootstrap.
    copyright : Eduardo dos Santos Pereira
    15 april 2013

    PyBootstrap is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyBootstrap is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from PyQt4 import QtCore, QtGui
from pybootstrapUI import Ui_MainWindow

from pybootstrap import *
from fishermatrix import *
import numpy
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(DesignerMainWindow,self).__init__(parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.pushButton,\
                               QtCore.SIGNAL("clicked()"),\
                               self.bootstrp)
        QtCore.QObject.connect(self.pushButton_2,\
                               QtCore.SIGNAL("clicked()"),\
                               self.plot)
        QtCore.QObject.connect(self.pushButton_3,\
                               QtCore.SIGNAL("clicked()"),\
                               self.open)
                               
        QtCore.QObject.connect(self.pushButton_4,\
                               QtCore.SIGNAL("clicked()"),\
                               self.plotOrigianl)
                               
        self.sample = None
        self.Parameters = None
        self.toolbar = NavigationToolbar(self.mplwidget.canvas, self.mplwidget)
        
    def bootstrp(self):
        if(self.sample == None):
            self.open()
        self.mplwidget.canvas.ax.clear()
        B = self.spinBox.value()
        func = r'lambda p,x:'+unicode(self.lineEdit.text())
        func = eval(func)
        self.textBrowser.setHtml('Start bootstrap')
        myBootstrap = bootstrap(self.sample, B, func =func)  
        bpar = myBootstrap.resample()
        p0 = eval(unicode(self.lineEdit_2.text()))
        bpar = myBootstrap.parameter(p0)
        self.Parameters = myBootstrap.bootstrapparameters()
        bias = myBootstrap.bias()
        std = myBootstrap.sdt()
        confidence= myBootstrap.confidence(0.25)
        text = '''Bootstrap Finishe
        <br>
        The best fit parameters are:
        <br>
        %s
        <br>
        <br>
        The bootstrap bias are : 
        <br>
        <br>
        %s
        <br>
        <br>
        The bootstrap standard error are :
       <br>
       %s
       <br>
       <br>
        The 95 percent of confidence interval are:
       <br>
       %s
       <br>
       <br>
        '''%(' , '.join([str(i) for i in bpar]) ,\
                ' , '.join([str(i) for i in bias]) ,\
                ' , '.join([str(i) for i in std]),\
                ' , '.join([str(i) for i in confidence]) )
        
        self.textBrowser.setHtml(text)
            
        
    
    def open(self):
        nameLoc = QtGui.QFileDialog.getOpenFileName(self, 'Open File','Open File',  self.tr('csv - Comman Separetor  Value(*.csv)'))
        if(nameLoc != ''):
            arq = open(unicode(nameLoc))
            self.sample  = numpy.loadtxt(arq, delimiter=",")
            
    def plot(self):
        if(self.Parameters != None):
            i = self.spinBox_2.value()
            if(i >= self.Parameters.shape[1]):
                pass
            else:
                self.mplwidget.canvas.ax.clear()
                self.mplwidget.canvas.ax.set_ylabel(r'Frequency')
                self.mplwidget.canvas.ax.set_xlabel(unicode(self.lineEdit_3.text()))
                self.mplwidget.canvas.ax.hist(self.Parameters[:, i], self.spinBox_3.value())
                self.mplwidget.canvas.setMinimumSize(self.mplwidget.canvas.size())
                self.mplwidget.canvas.draw()
                
    def plotOrigianl(self):
        if(self.sample != None):
            func = r'lambda p,x:'+unicode(self.lineEdit.text())
            func = eval(func)
            p0 = eval(unicode(self.lineEdit_2.text()))
            bpar = optimizer(p0, self.sample, func)
            Y = [func(bpar, xi) for xi in self.sample[:, 0]]
            self.mplwidget.canvas.ax.clear()
            self.mplwidget.canvas.ax.clear()
            self.mplwidget.canvas.ax.set_ylabel(r'y')
            self.mplwidget.canvas.ax.set_xlabel(r'x')
            self.mplwidget.canvas.ax.plot(self.sample[:, 0], self.sample[:, 1], '.', label='Sample')
            self.mplwidget.canvas.ax.plot(self.sample[:, 0], Y, label='Fit')
            self.mplwidget.canvas.ax.legend(loc=4)
            self.mplwidget.canvas.setMinimumSize(self.mplwidget.canvas.size())
            self.mplwidget.canvas.draw()
        
    
def main():    
    app = QtGui.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
    
