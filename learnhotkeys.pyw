#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
import sys, os, random

from ui_mainwindow import Ui_MainWindow
from defdialog import DefWindow
from cheatsheet import CSWindow

class MainWindow ( QMainWindow , Ui_MainWindow):

	#var initialization
	key = []
	hotkeys_path = "./hotkeys"
	hotkeys_folder = hotkeys_path+'/'
	settings = QSettings()
	settings.setFallbacksEnabled(False)

	def __init__ ( self, parent = None ):
		QMainWindow.__init__( self, parent )
		self.ui = Ui_MainWindow()
		self.ui.setupUi( self )
		#disabled new question button on load
		self.ui.newQuestionButton.setEnabled(False)
		#add signal on the widget
		self.ui.radioButton.pressed.connect(lambda who=self.ui.radioButton: self.checkAnswer(who))
		self.ui.radioButton_2.pressed.connect(lambda who=self.ui.radioButton_2: self.checkAnswer(who))
		self.ui.radioButton_3.pressed.connect(lambda who=self.ui.radioButton_3: self.checkAnswer(who))
		self.ui.newQuestionButton.clicked.connect(self.new_question)
		self.ui.openDef.clicked.connect(self.openDefDialog)
		self.ui.openCS.clicked.connect(self.openCSDialog)
		#load hotkeys file
		self.loadHotkeys()
		self.show()

	def loadHotkeys(self):
		#check if hotkeys was choosen
		if self.settings.value('file_name_default') != "":
			if sys.version_info < (3, 0):
				fname = self.hotkeys_folder+self.settings.value('file_name_default').toString()
			else:
				fname = self.hotkeys_folder+self.settings.value('file_name_default')
		else:
			fname = self.hotkeys_folder+'Bash.xml'
		#load xml file
		dom = QDomDocument()
		error = None
		fh = None
		try:
			fh = QFile(fname)
			if not fh.open(QIODevice.ReadOnly):
				print(IOError, unicode(fh.errorString()))
			if not dom.setContent(fh):
				print(ValueError, "could not parse XML")
		except (IOError, OSError, ValueError) as e:
			error = "Failed to import: {0}".format(e)
		finally:
			if fh is not None:
				fh.close()
			if error is not None:
				return False, error
		root = dom.documentElement()
		#check version of syntax
		if not root.hasAttribute('fileversion'):
			QMessageBox.information(self.window(), "LearnHotkeys","The file %s is not an LearnHotkeys definition file." % self.settings.value('file_name_default').toString())
			return False
		self.ui.hotkeys_program.setText('<font style="font-weight:bold">%s - %s<font>' % (root.attribute('software'),root.attribute('softwareversion')))
		#load hotkeys in a list
		child = root.firstChildElement('hotkey')
		while not child.isNull():
			self.key.append([child.firstChildElement('question').text(),child.firstChildElement('key').text()])
			child = child.nextSiblingElement('hotkey')
		#load new question
		self.new_question()

	def openDefDialog(self):
		#i need to explain this??
		window = QDialog()
		ui = DefWindow()
		ui.setupUi(window)
		if ui.exec_() == 1:
			self.loadHotkeys()

	def openCSDialog(self):
		window = QDialog()
		ui = CSWindow()
		ui.setupUi(window)
		ui.exec_()

	def checkAnswer(self, who):
		#check the answer
		if who.text() == self.key[self.question_chosen][1]:
			self.ui.result.setText('Correct answer <b>'+self.key[self.question_chosen][1]+'</b> !')
		else:
			self.ui.result.setText('<font color="#ff0000" style="font-weight:bold">The correct answer are %s</font>' % self.key[self.question_chosen][1])
		self.ui.newQuestionButton.setEnabled(True)
		self.ui.radioButton.setEnabled(False)
		self.ui.radioButton_2.setEnabled(False)
		self.ui.radioButton_3.setEnabled(False)

	def new_question(self):
		self.question_chosen = self.key.index(random.choice(self.key))
		self.ui.question.setText(self.key[self.question_chosen][0].replace(".",".<br>"))
		radiolist = [self.ui.radioButton,self.ui.radioButton_2,self.ui.radioButton_3]
		#Set the correct key
		radiorandom = radiolist.index(random.choice(radiolist))
		radiolist[radiorandom].setText(self.key[self.question_chosen][1])
		radiolist.pop(radiorandom)
		#Set the other key
		key_temp = list(self.key)
		index_temp = key_temp.index(random.choice(self.key))
		radiorandom = radiolist.index(random.choice(radiolist))
		radiolist[radiorandom].setText(key_temp[index_temp][1])
		key_temp.pop(index_temp)
		radiolist.pop(radiorandom)
		index_temp = key_temp.index(random.choice(self.key))
		radiorandom = radiolist.index(random.choice(radiolist))
		radiolist[radiorandom].setText(key_temp[index_temp][1])
		key_temp.pop(index_temp)
		radiolist.pop(radiorandom)
		self.ui.radioButton.setEnabled(True)
		self.ui.radioButton_2.setEnabled(True)
		self.ui.radioButton_3.setEnabled(True)
		self.ui.newQuestionButton.setEnabled(False)
		self.ui.result.setText('')

def main():
    app = QApplication(sys.argv)
    MainWindow_ = QMainWindow()
    ui = MainWindow()
    ui.setupUi(MainWindow_)
    sys.exit(app.exec_())

main()
