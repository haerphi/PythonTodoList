#!/usr/bin/env python
# coding: utf-8

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Task():
    def __init__(self, priority, task):
        self.priority = priority
        self.task = task

    def __eq__(self, other):
        if(self.task == other):
            return True
        else:
            return False

    def __lt__(self, other):
        if(self.priority == "Hight" and other.priority == "Hight"):
            return 0
        elif(self.priority == "Normal" and other.priority == "Normal"):
            return 0
        elif(self.priority == "Low" and other.priority == "Low"):
            return 0   
        elif(self.priority == "Hight" and other.priority == "Normal" or self.priority == "Hight" and other.priority == "Low"):
            return -1
        elif(self.priority == "Normal" and other.priority == "Low"):
            return -1

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Python3 - PyQt5: Todo List'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.spaceBeetweenInput = 50

        self.taskTab = []
        self.priorityList = ["Hight", "Normal", "Low"]

        self.initUI()
        
    def initUI(self):
        #window setup
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        
        #input
        height = 10
        #priority : label + box
        self.labelPriority = QLabel(self)
        self.labelPriority.setText('Task priority :')
        self.labelPriority.move(20, height)
        self.cbPriority = QComboBox(self)
        self.cbPriority.addItems(["Hight", "Normal", "Low"])
        self.cbPriority.move(self.labelPriority.width()+25, height)
        
        height += self.spaceBeetweenInput

        #task description
        self.labelTask = QLabel(self)
        self.labelTask.setText('Task name:')
        self.labelTask.move(20, height)
        self.textboxTask = QLineEdit(self)
        self.textboxTask.move(self.labelPriority.width()+25, height)
        self.textboxTask.resize(150, self.labelPriority.height())

        height += self.spaceBeetweenInput

        #submit button
        self.buttonSubmit = QPushButton('Submit', self)
        self.buttonSubmit.move(20,height)
        # connect button to function on_click
        self.buttonSubmit.clicked.connect(self.on_click_InsertRow)

        height += self.spaceBeetweenInput

        #table
        height
        self.createTable(height)

        #Delete task
        self.cbTask = QComboBox(self)
        self.cbTask.addItem("----------")
        self.cbTask.move((self.width/2)+20, 200)
        self.buttonSubmit = QPushButton('Delete task', self)
        self.buttonSubmit.move((self.width/2)+95, 200)
        # connect button to function on_click
        self.buttonSubmit.clicked.connect(self.on_click_DeleteTask)

        self.show()

    #table method
    def createTable(self, height):
        self.tableWidget = QTableWidget(0, 2, self)
        self.tableWidget.resize((self.width-40)/2, 300)
        self.tableWidget.move(20, height)
        
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Priority"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Task"))

    def insertRowPyQt(self, priority, task):
        print(self.tableWidget.rowCount())
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount()-1,0, QTableWidgetItem(priority))
        self.tableWidget.setItem(self.tableWidget.rowCount()-1,1, QTableWidgetItem(task))
        self.show()

    def insertRow(self, priority, task):
        if(len(task) < 12):
            self.taskTab.append(Task(priority, task))
            self.taskTab.sort()
            self.refreshTable()
            self.refreshDeleteComboBox()
        else:
            print("popup: Task name can't have more than 11 characters")
    
    def refreshTable(self):
        self.tableWidget.setRowCount(0)
        for i in self.taskTab:
            self.insertRowPyQt(i.priority, i.task)
    
    def refreshDeleteComboBox(self):
        self.cbTask.clear()
        self.cbTask.addItems(self.taskListToSimpleList())

        self.show


    #on_click methods
    def on_click_InsertRow(self):
        priority = self.cbPriority.currentText()
        task = self.textboxTask.text()
        #reset input
        self.textboxTask.setText("")
        self.insertRow(priority, task)
    
    def on_click_DeleteTask(self):
        if(self.cbTask.currentText() != "----------" and self.cbTask.count() > 0):
            if(self.validation(self.cbTask.currentText())):
                print("task deleted")
                print(self.cbTask.currentText())
                self.taskTab.remove(self.cbTask.currentText())
                self.taskTab.sort()
                self.refreshTable()
                self.refreshDeleteComboBox()


    #util
    def taskListToSimpleList(self):
        temp = []
        for i in self.taskTab:
            temp.append(i.task)
        return temp

    def validation(self, task):
        buttonReply = QMessageBox.question(self, 'Todo List - are you sure?', "Are you sure you want to delete " + task + " ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            return True
        else:
           return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())