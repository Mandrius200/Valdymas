import Apjungtas as ap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys
import time
import threading
import numpy as np


class Worker(QRunnable):
     
    @pyqtSlot()
    def run(self):
        #try:
            for i in data_lines:
                i.clear()
            QApplication.processEvents()
            yg.clear()
            x.clear()
            y.clear()
            xmas = np.array([[]])
            ymas = np.array([[]])
            Ilimit = sroves_lim_spin.value()
            PrItampa = 0
            m = [0, 0]
            global outxmas
            #--------------------------------OUT1 KINTAMAS------------------------------------------------------
            if out1_check.isChecked()==True and out2_check.isChecked()==False:
                ap.output2()
                ap.set_voltage(voltage = pr_itampa02_spin.value())
                time.sleep(0.1)
                ap.output1()
                PrItampa = pr_itampa01_spin.value()
                Ustep = itampos1_step_spin.value()
                Ulim = itampos1_lim_spin.value()
                while m[0]<Ilimit and not event_stop.is_set():
                    m = ap.matavimas(Itampa=PrItampa)
                    print(m)
                    print(m[0])
                    print(m[1])
                    srove1_label.setText('Srovė: '+str(round(abs(m[0])*1000,3))+'mA')
                    itampa1_label.setText('Įtampa: '+str(round(abs(m[1]),3))+'V')
                    yg.append(abs(m[0]))
                    y.append(abs(m[0]*1000))
                    x.append(abs(m[1]))
                    data_lines[0].setData(x,yg)
                    QApplication.processEvents()
                    time.sleep(0.1)
                    PrItampa = PrItampa+Ustep
                
                    if PrItampa > Ulim:
                        ylaik = np.array(y)
                        xmas = np.append(xmas,x)
                        xmas = np.vstack((xmas,ylaik))
                        outxmas = xmas
                        ap.output1()
                        ap.nulinimas()
                        ap.output2()
                        ap.nulinimas()
                        status_label.setText('Būsena: Matavimas baigtas')
                        MainWindow.enable(self)
                        return
                ap.output1()
                ap.nulinimas()
                ap.output2()
                ap.nulinimas()
                event_stop.clear()
                MainWindow.enable(self)
                return
            
            #---------------------------------------OUT2 KINTAMAS----------------------------------------    
            elif out2_check.isChecked()==True and out1_check.isChecked()==False:
                ap.output1()
                ap.set_voltage(voltage = pr_itampa01_spin.value())
                ap.output2()
                PrItampa = pr_itampa02_spin.value()
                Ustep = itampos2_step_spin.value()
                Ulim = itampos2_lim_spin.value()
                
                while m[0]<Ilimit and not event_stop.is_set():
                    m = ap.matavimas(Itampa=PrItampa)
                    print(m)
                    print(m[0])
                    print(m[1])
                    srove2_label.setText('Srovė: '+str(round(abs(m[0])*1000,3))+'mA')
                    itampa2_label.setText('Įtampa: '+str(round(abs(m[1]),3))+'V')
                    yg.append(abs(m[0]))
                    y.append(abs(m[0]*1000))
                    x.append(abs(m[1]))
                    data_lines[0].setData(x,yg)
                    QApplication.processEvents()
                    PrItampa = PrItampa + Ustep
                    if PrItampa > Ulim:
                        ylaik = np.array(y)
                        xmas = np.append(xmas,x)
                        xmas = np.vstack((xmas,ylaik))
                        outxmas = xmas
                        ap.output1()
                        ap.nulinimas()
                        ap.output2()
                        ap.nulinimas()
                        status_label.setText('Būsena: Matavimas baigtas')
                        MainWindow.enable(self)
                        return
                ap.output1()
                ap.nulinimas()
                ap.output2()
                ap.nulinimas()
                event_stop.clear()
                MainWindow.enable(self)
                return
            
            #-----------------------------------ABUDU--------------------------------------
            elif out1_check.isChecked()==True and out2_check.isChecked()==True :
                PrItampa1 = pr_itampa01_spin.value()
                PrItampa2 = pr_itampa02_spin.value()
                Ustep1 = itampos1_step_spin.value()
                Ustep2 = itampos2_step_spin.value()
                Ulim1 = itampos1_lim_spin.value()
                Ulim2 = itampos2_lim_spin.value()
                index = 0
                cycle = 0
                while m[0]<Ilimit and not event_stop.is_set():
                    while PrItampa1<=Ulim1 and not event_stop.is_set():
                        ap.output1()
                        m = ap.matavimas(Itampa=PrItampa1)
                        PrItampa1 = PrItampa1 + Ustep1
                        LaikU = PrItampa2
                        print(m)
                        srove1_label.setText('Srovė: '+str(round(abs(m[0])*1000,3))+'mA')
                        itampa1_label.setText('Įtampa: '+str(round(abs(m[1]),3))+'V')
                        srove1_label.repaint()
                        itampa1_label.repaint()
                        while LaikU<=Ulim2 and index<6  and not event_stop.is_set():
                            ap.output2()
                            n = ap.rigol_matavimas(Itampa=LaikU)
                            print(m)
                            srove1_label.setText('Srovė: '+str(round(abs(m[0])*1000,3))+'mA')
                            itampa1_label.setText('Įtampa: '+str(round(abs(m[1]),3))+'V')
                            srove2_label.setText('Srovė: '+str(round(abs(n[0])*1000,3))+'mA')
                            itampa2_label.setText('Įtampa: '+str(round(abs(n[1]),3))+'V')                        
                            yg.append(abs(n[0]))
                            y.append(abs(n[0]*1000))
                            x.append(abs(n[1]))
                            data_lines[index].setData(x,yg)
                            #data_line2.setData(x2,yg2)
                            QApplication.processEvents()
                            #PrItampa1 = PrItampa1 + Ustep1
                            LaikU = LaikU + Ustep2
                            xlaik = np.array(x)
                            ylaik = np.array(y)
                        if cycle == 0:
                            xmas = np.append(xmas,x)
                            xmas = np.vstack((xmas,ylaik))
                        else:
                            xmas = np.vstack((xmas,xlaik))
                            xmas = np.vstack((xmas,ylaik))
                        cycle = cycle + 1    
                        print(xmas)
                        print(ymas)
                        index = index + 1
                        LaikU = 0
                        yg.clear()
                        x.clear()
                        y.clear()
                        if PrItampa1 > Ulim1:
                            outxmas = xmas
                            ap.output1()
                            ap.nulinimas()
                            ap.output2()
                            ap.nulinimas()
                            status_label.setText('Būsena: Matavimas baigtas')
                            MainWindow.enable(self)
                            return
                event_stop.clear()
                MainWindow.enable(self)
                ap.output1()
                ap.nulinimas()
                ap.output2()
                ap.nulinimas()
                return
            
            else:
                ap.output1()
                ap.set_voltage(voltage = pr_itampa01_spin.value())
                time.sleep(0.1)
                ap.output2()
                ap.set_voltage(voltage = pr_itampa02_spin.value())
                m = ap.matavimas(Itampa=PrItampa)
                print(m)
                print(m[0])
                print(m[1])
                srove1_label.setText('Srovė: '+str(round(abs(m[0])*1000,3))+'mA')
                itampa1_label.setText('Įtampa: '+str(round(abs(m[1]),3))+'V')
                srove1_label.repaint()
                itampa1_label.repaint()
                event_stop.clear()
                MainWindow.enable(self)
                return
            
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        global event_stop
        event_stop = threading.Event()
        self.setWindowTitle("Charakteristikų matavimas")
        self.setFixedSize(QSize(1280,720))
        self.threadpool = QThreadPool()

        
        #------------------------------COM LIST----------------------------------
        
        com1_list_label = QLabel("COM portas 1",self)
        com1_list_label.setGeometry(1020,450,200,30)
        com1_list_label.setFont(QFont('Arial',11))
        
        global com1_list
        com1_list = QComboBox(self)
        com1_list.setGeometry(1020,480,200,30)
        com1_list.setFont(QFont('Arial',11))
        
        global visa2_list
        visa2_list_label = QLabel("Visa 2",self)
        visa2_list_label.setGeometry(1020,510,200,30)
        visa2_list_label.setFont(QFont('Arial',11))
        
        visa2_list = QComboBox(self)
        visa2_list.setGeometry(1020,540,200,30)
        visa2_list.setFont(QFont('Arial',11))
        
        #---------------------------------VISA LIST---------------------------------
        
        visa1_list_label = QLabel("Visa 1",self)
        visa1_list_label.setGeometry(1020,570,200,30)
        visa1_list_label.setFont(QFont('Arial',11))
        
        global visa1_list
        visa1_list = QComboBox(self)
        visa1_list.setGeometry(1020,600,200,30)
        visa1_list.setFont(QFont('Arial',11))
        
        #-----------------RASTI---------------------
        
        global rasti_button
        rasti_button = QPushButton('Rasti',self)
        rasti_button.setGeometry(1080,650,90,30)
        rasti_button.pressed.connect(self.rasti)
        
        #---------------------------SROVES LIMITAS------------------------------------------------
        sroves_lim_label = QLabel("Srovės limitas, A",self)
        sroves_lim_label.setGeometry(780,50,200,30)
        sroves_lim_label.setFont(QFont('Arial',11))

        
        global sroves_lim_spin
        sroves_lim_spin=QDoubleSpinBox(self)
        sroves_lim_spin.setGeometry(780,80,100,30)
        sroves_lim_spin.setMinimum(0)
        sroves_lim_spin.setSingleStep(0.001)
        sroves_lim_spin.setMaximum(0.04)
        sroves_lim_spin.setFont(QFont('Arial',11))
        sroves_lim_spin.setDecimals(3)
        sroves_lim_spin.setValue(0.02)
        
        #-----------------------------------ITAMPOS1 LIMITAS----------------------
        itampos1_lim_label = QLabel('Įtampos limitas O1, V', self)
        itampos1_lim_label.setGeometry(780,110,200,30)
        itampos1_lim_label.setFont(QFont('Arial',11))
        
        global itampos1_lim_spin
        itampos1_lim_spin = QDoubleSpinBox(self)
        itampos1_lim_spin.setMinimum(0)
        itampos1_lim_spin.setMaximum(40)
        itampos1_lim_spin.setGeometry(780,140,150,30)
        itampos1_lim_spin.setFont(QFont('Arial',11))
        itampos1_lim_spin.setValue(10)
        
        #-----------------------------------ITAMPOS2 LIMITAS----------------------
        itampos2_lim_label = QLabel('Įtampos limitas O2, V', self)
        itampos2_lim_label.setGeometry(970,110,200,30)
        itampos2_lim_label.setFont(QFont('Arial',11))
        
        global itampos2_lim_spin
        itampos2_lim_spin = QDoubleSpinBox(self)
        itampos2_lim_spin.setMinimum(0)
        itampos2_lim_spin.setMaximum(40)
        itampos2_lim_spin.setGeometry(970,140,150,30)
        itampos2_lim_spin.setFont(QFont('Arial',11))
        itampos2_lim_spin.setValue(10)
               
        #---------------------------------PRADINE ITAMPAO1----------------------------
        pr_itampa01_label = QLabel('Pradinė įtampa O1, V',self)
        pr_itampa01_label.setGeometry(780,170,200,30)
        pr_itampa01_label.setFont(QFont('Arial',11))
        
        global pr_itampa01_spin
        pr_itampa01_spin=QDoubleSpinBox(self)
        pr_itampa01_spin.setMinimum(0)
        pr_itampa01_spin.setMaximum(10)
        pr_itampa01_spin.setGeometry(780,200,150,30)
        pr_itampa01_spin.setFont(QFont('Arial',11))
        pr_itampa01_spin.setValue(0)
        
        #------------------------------ITAMPOS1 STEP-------------------------------
        itampos1_step_label = QLabel('Įtampos žingsnis O1, V',self)
        itampos1_step_label.setGeometry(780,230,200,30)
        itampos1_step_label.setFont(QFont('Arial',11))
        
        global itampos1_step_spin
        itampos1_step_spin=QDoubleSpinBox(self)
        itampos1_step_spin.setMinimum(0)
        itampos1_step_spin.setMaximum(2)
        itampos1_step_spin.setGeometry(780,260,150,30)
        itampos1_step_spin.setFont(QFont('Arial',11))
        itampos1_step_spin.setValue(2)
        
        #--------------------------PRADINE ITAMPA O2-----------------------------------
        pr_itampa02_label = QLabel('Pradinė įtampa O2, V',self)
        pr_itampa02_label.setGeometry(970,170,200,30)
        pr_itampa02_label.setFont(QFont('Arial',11))
        
        global pr_itampa02_spin
        pr_itampa02_spin=QDoubleSpinBox(self)
        pr_itampa02_spin.setMinimum(0)
        pr_itampa02_spin.setMaximum(10)
        pr_itampa02_spin.setGeometry(970,200,150,30)
        pr_itampa02_spin.setFont(QFont('Arial',11))
        pr_itampa02_spin.setValue(0)
        
        #------------------------------ITAMPOS2 STEP-------------------------------
        itampos2_step_label = QLabel('Įtampos žingsnis O2, V',self)
        itampos2_step_label.setGeometry(970,230,200,30)
        itampos2_step_label.setFont(QFont('Arial',11))
        
        global itampos2_step_spin
        itampos2_step_spin=QDoubleSpinBox(self)
        itampos2_step_spin.setMinimum(0)
        itampos2_step_spin.setMaximum(2)
        itampos2_step_spin.setGeometry(970,260,150,30)
        itampos2_step_spin.setFont(QFont('Arial',11))
        itampos2_step_spin.setValue(0.5) 
        
        #------------------------------------BUSENA-----------------------------
        global status_label
        status_label = QLabel('Būsena:',self)
        status_label.setFont(QFont('Arial',10))
        status_label.setGeometry(780,410,300,30)
        
        #-------------------------------------ITAMPA/SROVE-------------------------------
        global itampa1_label
        itampa1_label = QLabel('Įtampa 1:',self)
        itampa1_label.setFont(QFont('Arial',11))
        itampa1_label.setGeometry(120,620,200,30)
        
        global srove1_label
        srove1_label = QLabel('Srovė 1:',self)
        srove1_label.setFont(QFont('Arial',11))
        srove1_label.setGeometry(300,620,200,30)
        
        global itampa2_label
        itampa2_label = QLabel('Įtampa 2:',self)
        itampa2_label.setFont(QFont('Arial',11))
        itampa2_label.setGeometry(120,640,200,30)
        
        global srove2_label
        srove2_label = QLabel('Srovė 2:',self)
        srove2_label.setFont(QFont('Arial',11))
        srove2_label.setGeometry(300,640,200,30)
        
        #----------------------------------MYGTUKAI----------------------------------         
        
        global ijungti_but
        ijungti_but = QPushButton("Įjungti",self)
        ijungti_but.setGeometry(790,490,90,30)
        ijungti_but.pressed.connect(self.turn_on)
        
        global matuoti_but
        matuoti_but = QPushButton("Matuoti",self)
        matuoti_but.pressed.connect(self.measure)
        matuoti_but.setGeometry(890,490,90,30)
        
        global saugoti_but
        saugoti_but = QPushButton("Saugoti",self)
        saugoti_but.pressed.connect(self.save)
        saugoti_but.setGeometry(890,540,90,30)
        
        global stabdyti_but
        self.worker = Worker()
        stabdyti_but = QPushButton("Stabdyti",self)
        stabdyti_but.pressed.connect(self.stop)
        stabdyti_but.setGeometry(790,540,90,30)
        
        global trinti_but
        trinti_but = QPushButton("Trinti grafiką",self)
        trinti_but.pressed.connect(self.reset)
        trinti_but.setGeometry(790,590,90,30)
        
        #-------------------------------CHECKBOX-------------------------------------------
        
        global out1_check
        out1_check = QCheckBox('OUT1 Kintamas',self)
        out1_check.setGeometry(780,300,150,30)
        out1_check.setFont(QFont('Arial 12'))
        global out2_check
        out2_check = QCheckBox('OUT2 Kintamas',self)
        out2_check.setGeometry(980,300,150,30)
        out2_check.setFont(QFont('Arial 12'))
        
        #-------------------------------GRAFIKAS-----------------------------------
        labelStyle = {'color':'#FFF','font-size':'18pt'}
        global graph
        graph=self.graphWidget = pg.PlotWidget(self)
       
        graph.setLabel('left',text='I', units='A',**labelStyle)
        graph.setLabel('bottom',text='U',units='V',**labelStyle)
        graph.move(50,50)
        graph.resize(700,550)
        global x, y, yg, xmas, ymas

        xmas = np.array([])
        ymas = np.array([])
        x = []
        y = []
        yg = []

        
        self.setGeometry
        self.show()
        data_line1 = graph.plot(x,
                                yg,
                                pen='g', 
                                symbol = 'o',
                                symbolPen='g',
                                name='green'
                                )
        data_line2 = graph.plot(x, 
                                yg,
                                prm = 'r',
                                symbol = 'o',
                                symbolPen='r',
                                name='red'
                                )                                
        data_line3 = graph.plot(x, 
                                yg,
                                prm = 'b',
                                symbol = 'o',
                                symbolPen='b',
                                name='blue'
                                )
        data_line4 = graph.plot(x, 
                                yg,
                                prm = 'y',
                                symbol = 'o',
                                symbolPen='y',
                                name='yellow'
                                )
        data_line5 = graph.plot(x, 
                                yg,
                                prm = 'k',
                                symbol = 'o',
                                symbolPen='k',
                                name='k'
                                )
        data_line6 = graph.plot(x, 
                                yg,
                                prm = 'c',
                                symbol = 'o',
                                symbolPen='c',
                                name='c'
                                )
        global data_lines
        data_lines = (data_line1,data_line2,data_line3,data_line4,data_line5, data_line6)
        legenda = graph.addLegend()
        legenda.addItem(item=data_line1, name='OUT1')
        legenda.addItem(item=data_line2, name='OUT2')
        legenda.addItem(item=data_line3, name='OUT3')
        legenda.addItem(item=data_line4, name='OUT4')
        legenda.addItem(item=data_line5, name='OUT5')
        legenda.addItem(item=data_line5, name='OUT6')
#-------------------------------BUTTON STATE------------------------------------
        ijungti_but.setEnabled(False)
        trinti_but.setEnabled(False)
        saugoti_but.setEnabled(False)
        stabdyti_but.setEnabled(False)
        matuoti_but.setEnabled(False)
        

    def turn_on(self):
        
            portas1 = com1_list.currentText()
            portas1 = portas1.split()
            print(portas1)

            visa1 = visa1_list.currentText()
            visa2 = visa2_list.currentText()
            
            ap.find(Port1=portas1[0], Visa1=visa1,Visa2=visa2)
            ap.ijungti()
            status_label.setText('Būsena: Ryšys susietas')
            #ap.matavimas(0)
            trinti_but.setEnabled(True)
            saugoti_but.setEnabled(True)
            stabdyti_but.setEnabled(True)
            matuoti_but.setEnabled(True)
            #self.error
    def measure(self):
        #try:
        #while not self.event_stop.is_set():
            self.dissable()
            self.worker = Worker()
            status_label.setText('Būsena: Matuojama')
            self.threadpool.start(self.worker)
            #ap.matavimas(0)
        #except:
            #self.error
    def save(self):
        #try:
            if out1_check.isChecked() == True and out2_check.isChecked() == False:
                outzmas = np.transpose(outxmas)
                np.savetxt('output_O1.txt',outzmas,fmt='%.5f',delimiter=' \t ',header='%12s\t%12s'%('Įtampa, V','Srovė, mA'), comments='')
            elif out2_check.isChecked() == True and out1_check.isChecked() == False:
               outzmas = np.transpose(outxmas)
               np.savetxt('output_O2.txt',outzmas,fmt='%.5f',delimiter=' \t ',header='%12s\t%12s'%('Įtampa, V','Srovė, mA'), comments='')
            elif out1_check.isChecked() == True and out2_check.isChecked() == True:
                print(outxmas)
                outzmas = np.transpose(outxmas)
                np.savetxt('output_both.txt', outzmas, fmt='%.5f', delimiter=' \t ',header='%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s\t%12s'%('Įtampa O1, V','Srovė O1, mA',
                                                                                                                                                                'Įtampa O2, V','Srovė O2, mA',
                                                                                                                                                                'Įtampa O3, V','Srovė O3, mA',
                                                                                                                                                                'Įtampa O4, V','Srovė O4, mA',
                                                                                                                                                                'Įtampa O5, V','Srovė O5, mA',
                                                                                                                                                                'Įtampa O6, V','Srovė O6, mA'),comments='')
                status_label.setText('Būsena: Išsaugota')
        #except:
            self.error
    def reset(self):
        for i in data_lines:
            i.clear()
        QApplication.processEvents()
    def error(self):
        status_label.setText("Būsena: Klaida")
    def stop(self):
        print('STOP')
        status_label.setText("Būsena: Matavimas nutrauktas")
        event_stop.set()
        self.enable()
    def dissable(self):
        trinti_but.setEnabled(False)
        saugoti_but.setEnabled(False)
        ijungti_but.setEnabled(False)
        matuoti_but.setEnabled(False)
    def enable(self):
        trinti_but.setEnabled(True)
        saugoti_but.setEnabled(True)
        ijungti_but.setEnabled(True)
        matuoti_but.setEnabled(True)
    def rasti(self):
        com1_list.clear()
        visa1_list.clear()
        visa2_list.clear()
        with open('Config/Check.txt','r') as z:
            line = z.readline()
            z.close()
        if line == 'False':
            portai = ap.find_com()
            print(type(portai))
            print(portai)
            visos = ap.find_visa()
            print(visos)
            for pr in portai:
                com1_list.addItem(str(pr))
            for i in visos:
                visa2_list.addItem(i)
            for i in visos:
                visa1_list.addItem(i)
            ijungti_but.setEnabled(True)
        if line == 'True':
            f = open('Config/com.txt','r')
            line = f.readline()
            com1_list.addItem(str(line))
            f.close()
            f = open('Config/visa1.txt','r')
            line = f.readline()
            visa1_list.addItem(str(line))
            f.close()
            f = open('Config/visa2.txt','r')
            line = f.readline()
            visa2_list.addItem(str(line))
            f.close()
            ijungti_but.setEnabled(True)
            
            

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()