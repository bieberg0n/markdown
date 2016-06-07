#!/usr/bin/env python3
#coding:utf-8
import sys
import os
# reload(sys)
# sys.setdefaultencoding('utf-8')
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QGridLayout, QMainWindow
# from PyQt5.QtWebKitWidgets import QWebView
# from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtCore import *
import re
import markdown
import time
import threading
from bs4 import BeautifulSoup

class Thread(QThread):
	trigger = pyqtSignal(int)

	def __init__(self, parent=None):
		super(Thread,self).__init__(parent)

	def run(self):
		while 1:
			time.sleep(1)
			self.trigger.emit(1)


class Md(QWidget):

	def __init__(self, parent=None):
		super(Md,self).__init__(parent)
		self.file = sys.argv[1]
		if os.path.isfile(self.file):
			pass
		else:
			open(self.file, 'w')
		self.filename = '.'.join( self.file.split('.')[:-1] )
		self.initUI()

	def auto_save_(self):
		# self.textedit1.append(open(sys.argv[1]).read())
		while 1:
			# text = unicode( self.textedit1.toPlainText() )
			text = self.textedit1.toPlainText()
			p = re.compile('\n')
			text = p.sub('  \n', text)
			pp = re.compile(' +\n')
			self.text = pp.sub('  \n', text)
			# print(text)
			self.html = markdown.markdown(self.text)
			with open(self.file, 'w', encoding='utf-8') as f:
				f.write(self.text)
			with open(self.filename+'~.html','w',encoding='utf-8') as f:
				f.write(self.html)
			# self.browser.load(QUrl('file:///tmp/md.html'))
			time.sleep(2)
			# self.browser.reload()

	def auto_save(self):
		t = threading.Thread(target=self.auto_save_)
		t.setDaemon(True)
		t.start()

	def collect(self):
		# text = self.textedit1.toPlainText()
		text = BeautifulSoup(self.html).text
		# p_without_white = re.compile('\S')
		# without_white = len( p_without_white.findall(text) )
		all_zh_and_p = len( re.findall('[^A-Za-z0-9|\s]',text) )
		all_zh = ''.join(
			[ i for i in text if 19968 <= ord(i) <= 40869 ] )
		all_zh = len(all_zh)
		all_words = len( re.findall(r'[A-Za-z]+',text) )
		self.show_message( '汉字与标点符号数:{0} 汉字数:{1} 单词数:{2}'.format(all_zh_and_p, all_zh, all_words) )

	def browser_reload(self, i):
		self.browser.reload()

	def output_html(self):
		with open(self.filename+'.html','w',encoding='utf-8') as f:
			f.write(self.html)
		self.show_message('HTML已保存到工作目录')

	def output_pdf(self):
		p = QPrinter()
		p.setOutputFormat(QPrinter.PdfFormat)
		p.setOutputFileName(self.filename+'.pdf')
		self.browser.print(p)
		self.show_message('PDF已保存到工作目录')

	def show_message_(self, string):
		self.message.setText(string)
		time.sleep(4)
		self.message.setText('')

	def show_message(self, string):
		# print(string)
		t = threading.Thread( target=self.show_message_,args=(string,) )
		t.setDaemon(True)
		t.start()		

	def set_textedit(self):
		# self.textedit1 = QTextEdit()
		self.textedit1 = QPlainTextEdit()
		# self.textedit1.zoomIn(2)
		self.textedit1.setFont(QFont('微软雅黑',12))
		# self.textedit1.setTextFormat(QtextEdit.PlainText)
		# self.textedit1.resize(800,600)
		self.textedit1.setMinimumWidth(500)
		try:
			text = open(self.file).read()
		except UnicodeDecodeError:
			text = open(self.file, encoding='utf-8').read()
		print(text)
		self.textedit1.appendPlainText(text)
		self.auto_save()
		# self.textedit2 = QTextEdit()

	def set_brower(self):
		self.browser = QWebView()
		self.browser.showMaximized()
		self.browser.coding = self.browser.settings()
		self.browser.coding.setDefaultTextEncoding('utf-8')
		# self.browser = QWebView()
		# self.browser.resize(100,100)
		self.browser.load( QUrl(self.filename+'~.html') )
		thread = Thread(self)
		thread.trigger.connect(self.browser_reload)
		thread.start()
		# self.browser.load(QUrl('http://h.nimingban.com'))

	def set_find_line(self):
		self.line_edit1 = QLineEdit()
		self.line_edit1.setFixedWidth(200)
		self.line_edit1.hide()

		self.find_next_button = QPushButton('下一个',self)
		self.find_next_button.setFocusPolicy(Qt.NoFocus)
		self.find_next_button.hide()
		self.find_next_button.clicked.connect(self.find_word_next)

		self.find_last_button = QPushButton('上一个',self)
		self.find_last_button.setFocusPolicy(Qt.NoFocus)
		self.find_last_button.hide()
		self.find_last_button.clicked.connect(self.find_word_last)

		self.change_word_button = QPushButton('替换为->',self)
		self.change_word_button.setFocusPolicy(Qt.NoFocus)
		self.change_word_button.hide()
		self.change_word_button.clicked.connect(self.change_word)

		self.line_edit2 = QLineEdit()
		self.line_edit2.setFixedWidth(200)
		self.line_edit2.hide()

		self.close_find = QPushButton('X', self)
		self.close_find.setFixedWidth(25)
		self.close_find.hide()
		self.close_find.clicked.connect(self.hide_find_line)

	def hide_find_line(self):
		self.line_edit1.hide()
		self.find_next_button.hide()
		self.find_last_button.hide()
		self.change_word_button.hide()
		self.line_edit2.hide()
		self.close_find.hide()

	def show_find_line(self):
		self.line_edit1.show()
		self.find_next_button.show()
		self.find_last_button.show()
		self.change_word_button.show()
		self.line_edit2.show()
		self.close_find.show()

	def find_word_next(self):
		text_cursor = self.textedit1.textCursor()
		old_pos = text_cursor.position()
		# new_pos = re.search( self.line_edit1.text(), self.text[old_pos:] ).span()[0]
		# print(new_pos)
		key_word = self.line_edit1.text()
		findall = self.text.split(key_word)
		if len(findall) == 1:
			self.show_message('未找到!')
			return
		else:
			for i,v in enumerate(findall):
				new_pos = len( key_word.join(findall[:i+1]) )
				if new_pos == len(self.text):
					new_pos = len(findall[0])
					break
				elif new_pos > old_pos:
					break
			text_cursor.setPosition(new_pos)
			self.textedit1.setTextCursor(text_cursor)
			self.textedit1.setFocus()

	def find_word_last(self):
		text_cursor = self.textedit1.textCursor()
		old_pos = text_cursor.position()
		# new_pos = re.search( self.line_edit1.text(), self.text[old_pos:] ).span()[0]
		# print(new_pos)
		key_word = self.line_edit1.text()
		findall = self.text.split(key_word)
		if len(findall) == 1:
			self.show_message('未找到!')
			return
		else:
			last_pos = len( key_word.join(findall[:-1]) )
			for i,v in enumerate(findall):
				new_pos = len( key_word.join(findall[:i+1]) )
				if new_pos >= old_pos:
					break
				last_pos = new_pos
			text_cursor.setPosition(last_pos)
			self.textedit1.setTextCursor(text_cursor)
			self.textedit1.setFocus()

	def change_word(self):
		text = self.text
		text = text.replace( self.line_edit1.text(), self.line_edit2.text() )
		self.textedit1.clear()
		self.textedit1.appendPlainText(text)

	def initUI(self):
		# okbutton = QPushButton('Ok')
		# okbutton.clicked.connect(self.print_)
		# cancelbutton = QPushButton('Cancel')


		self.set_textedit()
		self.set_brower()

		self.message = QLabel('')
		self.show_message('v0.2.0 written by BJ')
		# self.message.setText('a')

		hbox = QHBoxLayout()
		# grid = QGridLayout()
		# grid.setSpacing(0)
		hbox.setSpacing(0)
		vbox = QVBoxLayout()
		vbox.setSpacing(0)
		# vbox.addStretch()
		# hbox.addWidget(okbutton)
		hbox.addWidget(self.textedit1)
		hbox.addWidget(self.browser)

		self.set_find_line()
		# self.show_find_line()
		find_box = QHBoxLayout()
		find_box.addWidget(self.line_edit1)
		find_box.addWidget(self.find_next_button)
		find_box.addWidget(self.find_last_button)
		find_box.addWidget(self.change_word_button)
		find_box.addWidget(self.line_edit2)
		find_box.addStretch()
		find_box.addWidget(self.close_find)
		
		vbox.addLayout(hbox)
		vbox.addLayout(find_box)
		vbox.addWidget(self.message)
		# grid.addWidget(self.textedit2, 1, 1, 1, 2)
		# hbox.addLayout(vbox)
		# hbox.addWidget(self.browser)

		# vbox.addStretch()
		# vbox.addLayout(hbox)

		self.setLayout(vbox)
		# self.setLayout(vbox)


class mainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		md = Md()

		findAction = QAction( QIcon(), '查找/替换', self )
		findAction.triggered.connect(md.show_find_line)
		collectAction = QAction( QIcon(), '字数统计', self )
		collectAction.triggered.connect(md.collect)
		outputHtmlAction = QAction( QIcon(), '输出HTML', self )
		outputHtmlAction.triggered.connect(md.output_html)
		outputPdfAction = QAction( QIcon(), '输出PDF', self )
		outputPdfAction.triggered.connect(md.output_pdf)
		self.toolbar = self.addToolBar('output')
		self.toolbar.setMovable(False)
		self.toolbar.addAction(findAction)
		self.toolbar.addAction(collectAction)
		self.toolbar.addAction(outputHtmlAction)
		self.toolbar.addAction(outputPdfAction)


		self.setGeometry(100, 100, 1100, 640)
		self.setWindowTitle('ToYoung')
		self.setCentralWidget(md)
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainwindow = mainWindow()
	app.exec_()
	os.remove( '.'.join( sys.argv[1].split('.')[:-1] ) + '~.html' )
	sys.exit()
