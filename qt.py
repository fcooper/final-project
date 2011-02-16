import numpy
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import os




class MyDialog(QMainWindow):

    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.windowSize = (800,600)
        self.orig = None


        self.words = "Save"

        browseAction = QAction( '&Browse', self)        
        browseAction.setShortcut('Ctrl+Q')
        browseAction.setStatusTip('Browse application')
        browseAction.triggered.connect(self.selectFile)


        exitAction = QAction( '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        self.mouseDown = False


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(browseAction)
        fileMenu.addAction(exitAction)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.zoomOffset = [0,0]

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Ken Burn's Effect Creator")    
        self.show()
        self.origTran = None
        self.values = []
        self.nothing = 1.5
        for z in range(0,13):
            self.values.append(1300-z*100)


        for z in range(0,9):
            self.values.append(90-z*10)

        print self.values

        self.values.append(5)
        self.values.append(2.5)
        self.values.append(1)                

        self.currentValue = [12,12]


        self.table = []

        for x in range(1,10):
            self.table.append(x/(x+1.0))
        for x in range(1,10):
            self.table.append(x/(x+1.0))            

        print self.table

        #exit()
        self.statusBar.showMessage("Load Image by using File->Browse")
        self.mouseOffset = (0,0)

    def selectFile(temp,temp1):
        self = temp

        test = QFileDialog.getOpenFileName()

        self.orig = cv2.imread(str(test))

        self.translate = []
        self.translate.append([400,300])
        self.translate.append([400,300])

        self.startMouse = []
        self.startMouse.append([0,0])
        self.startMouse.append([0,0])


        self.index = 0
        
        self.updateStatusBar()


    def mousePressEvent(self, QMouseEvent):
        if self.orig is None:
            return

        self.mouseDown = True

        self.mouseOffset = (0,0)
        self.startMouse[self.index][0] = QMouseEvent.pos().x()
        self.startMouse[self.index][1] = QMouseEvent.pos().y() 


    def mouseMoveEvent(self, QMouseEvent):
        if self.orig is None:
            return

        endX , endY = QMouseEvent.pos().x(),QMouseEvent.pos().y()
        startX , startY = self.startMouse[self.index]

        self.mouseOffset = (endX-startX,endY-startY)
        print "Mouse",self.mouseOffset
        print "Original Translate",self.translate[self.index]
        self.repaint()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.orig is None:
            return

        self.translate[self.index][1] = self.translate[self.index][1] + self.mouseOffset[1]/self.getZoom()
        self.translate[self.index][0] = self.translate[self.index][0] + self.mouseOffset[0]/self.getZoom()
        
        self.mouseOffset = (0,0)

        self.repaint()
        self.mouseDown = False

    def updateStatusBar(self):
        text = "Editing "
        if self.index == 0:
            text = text + "First "
        else:
            text = text + "Second "

        text = text + "Frame    Zoom at "+str(self.values[self.currentValue[self.index]]) + "%"
        self.statusBar.showMessage(text)

    def increaseZoom(self):

        self.currentValue[self.index] = self.currentValue[self.index] - 1

        if self.currentValue[self.index] < 0:
            self.currentValue[self.index] = 0
    def decreaseZoom(self):

        self.currentValue[self.index] = self.currentValue[self.index] + 1

        if self.currentValue[self.index] >= len(self.values):
            self.currentValue[self.index] = len(self.values)-1    


    def getZoom(self):
        return self.values[self.currentValue[self.index]]/100.0

    def mouseDoubleClickEvent(self,QMouseEvent):

        if self.orig is None:
            return

        origZoom = self.getZoom()
        print self.getZoom()

        left = False
        if QMouseEvent.button() == 1:

            self.increaseZoom()
        else:

            self.decreaseZoom()


        self.updateStatusBar()

        mouseX , mouseY = QMouseEvent.pos().x(),QMouseEvent.pos().y()



        self.translate[self.index][0] = self.translate[self.index][0] 
        self.translate[self.index][1] = self.translate[self.index][1]


        self.repaint()


    def getImage(self,xTranslate,yTranslate,zoom):

        windowWidth , windowHeight = self.windowSize

        xTranslate = int(xTranslate)
        yTranslate = int(yTranslate)

        self.cvImage = numpy.copy(self.orig)


        imgHeight , imgWidth , chan = self.cvImage.shape

        self.cvImage = cv2.resize(self.cvImage,(int(imgWidth*zoom),int(imgHeight*zoom)))

        startX = xTranslate - windowWidth/2       
        startY = yTranslate - windowHeight/2

        if startX < 0:
            self.cvImage = cv2.copyMakeBorder(self.cvImage,0,0,abs(startX),0,cv2.BORDER_CONSTANT,value=[0,0,0])
            startX = 0

        if startY < 0:
            self.cvImage = cv2.copyMakeBorder(self.cvImage,abs(startY),0,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
            startY = 0

        endX = startX + windowWidth
        endY = startY + windowHeight


        imgHeight , imgWidth , chan = self.cvImage.shape

        if imgWidth < endX:
            self.cvImage = cv2.copyMakeBorder(self.cvImage,0,0,0,endX-imgWidth,cv2.BORDER_CONSTANT,value=[0,0,0])

        if imgHeight < endY:
            self.cvImage = cv2.copyMakeBorder(self.cvImage,0,endY-imgHeight,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])

    

        return self.cvImage[startY:endY,startX:endX]




    def paintEvent(self, QPaintEvent):
        windowWidth , windowHeight = self.windowSize

        if self.orig is not None:

            zoom = self.getZoom()

            xTranslate = self.mouseOffset[0] + self.translate[self.index][0]*zoom
            yTranslate = self.mouseOffset[1] + self.translate[self.index][1]*zoom

            print "Mouse Offset",self.mouseOffset
            print "Translate:",(xTranslate,yTranslate)

            self.cvImage = self.getImage(xTranslate,yTranslate,zoom)

            height, width, byteValue = self.cvImage.shape
            byteValue = byteValue * width

            cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

            self.mQImage = QImage(numpy.copy(self.cvImage), width, height, byteValue, QImage.Format_RGB888)
        else:
            self.mQImage = QImage(windowWidth, windowHeight,QImage.Format_RGB888)
            
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.setBrush(QBrush(QColor(255,0,0)))
        painter.drawEllipse(windowWidth/2,windowHeight/2,10,10)
        painter.end()

        print "-----------------"

    def createMovie(self):


        duration = 2
        frame_per_sec = 30
        frame = duration * frame_per_sec

        filelist = [ f for f in os.listdir("save") if f.endswith(".jpeg") ]
        for f in filelist:
            os.remove("save/"+f)

        xdeltatemp = self.translate[1][0] - self.translate[0][0]
        ydeltatemp = self.translate[1][1] - self.translate[0][1]


        xrate = xdeltatemp / frame
        yrate = ydeltatemp / frame


        zoomStart = self.values[self.currentValue[0]]/100.0
        zoomEnd = self.values[self.currentValue[1]]/100.0

        print "zoomStart", zoomStart , "zoomEnd",zoomEnd

        zoom = abs(zoomEnd - zoomStart)
        zoomrate = zoom / frame


        windowWidth , windowHeight = self.windowSize

        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, frame_per_sec, (w.windowSize[0], w.windowSize[1]))

        for z in range(int(frame+1)):




            if zoomStart > zoomEnd:
                zoomdelta = zoomStart - zoomrate * z
            else:
                zoomdelta = zoomStart + zoomrate * z


            xdelta = int(self.translate[0][0]*zoomdelta + z*xrate)
            ydelta = int(self.translate[0][1]*zoomdelta + z*yrate)


            print "Movie XY",(xdelta,ydelta),"Zoom Delta: ",zoomdelta,"Zoom Rate",zoomrate


            self.cvImage = self.getImage(xdelta,ydelta,zoomdelta)
            out.write(self.cvImage)

            if z == 0 or z == int(frame):
                for x in range(0,frame_per_sec):
                    out.write(self.cvImage)                   

        out.release()


    def keyPressEvent(self, QKeyEvent):
        super(MyDialog, self).keyPressEvent(QKeyEvent)
        if 'n' == QKeyEvent.text() and self.orig is not None:

            if self.mouseDown == False:

                if self.index == 0:
                    self.index = 1
                else:
                    self.index = 0

                self.updateStatusBar()

                self.repaint()

        elif 's' == QKeyEvent.text() and self.orig is not None:
            self.createMovie()

        elif 'r' == QKeyEvent.text() and self.orig is not None:
            self.translate[self.index] = [0,0]
            self.zoomOffset = [0,0]
            self.currentValue[self.index] = 12

            self.updateStatusBar()

            self.repaint()

        elif 'q' == QKeyEvent.text():
            app.exit(1)


if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    w = MyDialog()
    w.resize(w.windowSize[0], w.windowSize[1])
    w.setFixedSize(w.windowSize[0], w.windowSize[1])
    w.show()
    app.exec_()