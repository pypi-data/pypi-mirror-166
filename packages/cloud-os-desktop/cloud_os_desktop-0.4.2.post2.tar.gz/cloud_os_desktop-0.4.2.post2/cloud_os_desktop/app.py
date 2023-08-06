# -*- coding: utf-8 -*-

import asyncio, sys, os, json, threading, time
from os.path import abspath, dirname, join
from threading import Timer
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder

from .AboutDialog import Ui_AboutDialog
from .MainWindow import Ui_MainWindow
from .ConnectDialog import Ui_ConnectDialog
from .EditConnectionDialog import Ui_EditConnectionDialog
from .WebBrowser import Ui_WebBrowser

import PyQt5
from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle, QDialog, QMessageBox, \
	QListWidgetItem, QToolBar, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

main_window = None
app_debug = True


def set_window_center(window):
	
	desktop = QApplication.desktop()
	screen_number = desktop.screenNumber(desktop.cursor().pos())
	center = desktop.screenGeometry(screen_number).center()
	
	window_size = window.size()
	width = window_size.width(); 
	height = window_size.height();
	
	x = center.x() - round(width / 2);
	y = center.y() - round(height / 2);
	
	window.move ( x, y );


class Connection():
	
	def __init__(self):
		self.connection_name = "";
		self.host = "";
		self.local_port = "";
		self.username = "";
		self.password = "";


class AboutDialog(QDialog, Ui_AboutDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setFixedSize(self.size())
	

class ConnectDialog(QDialog, Ui_ConnectDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.label.setWordWrap(True)
		self.setFixedSize(self.size())
	

class EditConnectionDialog(QDialog, Ui_EditConnectionDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Edit connection")
		self.setFixedSize(self.size())


class WebBrowser(QMainWindow, Ui_WebBrowser):
	
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		
		self.home_url = ""
		self.connect_data = None
		self.connect_dialog = None
		self.ssh_server = None
		self.thread_connect = None
		self.is_connected = False
		
		self.setupUi(self)
		self.setWindowTitle("Connect to server")
		self.setCentralWidget(self.webBrowser)
		
		# Tool Bar
		self.toolBar = QToolBar()
		self.addToolBar(self.toolBar)
		
		# Buttons
		self.prevButton = QAction('Prev', self)
		self.nextButton = QAction('Next', self)
		self.refreshButton = QAction('Refresh', self)
		self.homeButton = QAction('Home', self)
		self.urlEdit = QLineEdit()
		
		# Add to toolbar
		self.toolBar.addAction(self.prevButton)
		self.toolBar.addAction(self.nextButton)
		self.toolBar.addAction(self.refreshButton)
		#self.toolBar.addAction(self.homeButton)
		self.toolBar.addWidget(self.urlEdit)
		
		# Events
		self.prevButton.triggered.connect(self.onPrevButtonClick)
		self.nextButton.triggered.connect(self.onNextButtonClick)
		self.refreshButton.triggered.connect(self.onRefreshButtonClick)
		self.homeButton.triggered.connect(self.onHomeButtonClick)
		self.urlEdit.returnPressed.connect(self.onUrlEditChange)
		self.webBrowser.urlChanged.connect(self.onWebBrowserUrlChange)
	
	
	def closeEvent(self, event):
		self.sshDisconnect()
		event.accept()
	
	
	def sshConnect(self):
		
		try:
			time.sleep(1)
			
			if self.connect_data == None:
				s = "Error: Connection data is None"
				self.connect_dialog.label.setText(s)
				if app_debug:
					print (s)
				return
			
			# Connect to ssh server
			data:Connection = self.connect_data
			data_url_arr = data.host.split(":")
			data_host = data_url_arr[0]
			data_port = data_url_arr[1] if len(data_url_arr) > 1 else "8022"
			
			try:
				self.ssh_server = SSHTunnelForwarder(
					data_host,
					ssh_port=int(data_port),
					ssh_username=data.username,
					ssh_password=data.password,
					set_keepalive=60*60,
					remote_bind_address=('127.0.0.1', 80),
					local_bind_address=('127.0.0.1', int(data.local_port)),
				)
				self.ssh_server.start()
				
				self.home_url = "http://127.0.0.1:" + str(self.ssh_server.local_bind_port) + "/"
				
			except Exception as e:
				s = "Error: Failed connect to {0}:{1}: {2}".format(data_host, data_port, e)
				if self.connect_dialog != None:
					self.connect_dialog.label.setText(s)
				if app_debug:
					print (s)
				return
			
			self.is_connected = True
			
			if self.connect_dialog != None:
				self.connect_dialog.accept()
				if app_debug:
					print ("Connected")
			
			pass
		
		except Exception as e:
			print (e)
			
	
	def sshDisconnect(self):
		
		if self.thread_connect != None:
			#self.thread_connect.stop()
			self.thread_connect = None
		
		try:
			if self.ssh_server != None:
				self.ssh_server.stop()
		except Exception as e:
			print (e)
			
		self.is_connected = False
		self.ssh_server = None
		
		if app_debug:
			print ("Disconnect")
	
	
	def connectToServer(self, data:Connection):
		
		self.home_url = ""
		
		if app_debug:
			print ("Connect to " + data.host)
		
		# Create connection dialog
		self.connect_dialog = ConnectDialog()
		
		# Setup title
		connect_title = "Connect to {0} ({1})".format(data.connection_name, data.host)
		self.connect_dialog.setWindowTitle(connect_title)
		self.setWindowTitle(connect_title)
		
		# Setup connection
		self.connect_data = data
		
		# Connect to server
		self.thread_connect = threading.Thread(target=self.sshConnect)
		self.thread_connect.start()
		
		# Show connection dialog
		result = 0
		if self.is_connected == False:
			result = self.connect_dialog.exec()
		
		if app_debug:
			print ("Result: ", result)
		
		# Cancel connect
		if result == 0:
			self.sshDisconnect()
		else:
			if self.is_connected == False:
				self.sshDisconnect()
		
		# Success connect
		if self.is_connected:
			
			if app_debug:
				print ("Open web browser")
			
			data:Connection = self.connect_data
			
			if self.home_url != "":
				webBrowser:QWebEngineView = self.webBrowser
				url = QUrl(self.home_url)
				url.setUserName(data.username)
				url.setPassword(data.password)
				webBrowser.setUrl( url )
			
			connect_title = "Connected to {0} ({1})".format(data.connection_name, data.host)
			self.setWindowTitle(connect_title)
			self.show()
			set_window_center(self)
		
		self.connect_dialog = None
		
		pass
		
	
	def onPrevButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.back()
	
	
	def onNextButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.forward()
	
	
	def onRefreshButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		#webBrowser.reload()
		data:Connection = self.connect_data
		url = webBrowser.url()
		url.setUserName(data.username)
		url.setPassword(data.password)
		webBrowser.setUrl( url )
	
	
	def onHomeButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		data:Connection = self.connect_data
		url = QUrl(self.home_url)
		url.setUserName(data.username)
		url.setPassword(data.password)
		webBrowser.setUrl( url )
	
	
	def onUrlEditChange(self):
		url = self.urlEdit.text()
		webBrowser:QWebEngineView = self.webBrowser
		data:Connection = self.connect_data
		url = QUrl(url)
		url.setUserName(data.username)
		url.setPassword(data.password)
		webBrowser.setUrl( url )
	
	
	def onWebBrowserUrlChange(self, url):
		#print( url )
		from urllib.parse import urlparse
		res = urlparse(url.toString())
		url_new = res.scheme + "://"  + res.hostname + ":" + str(res.port) + res.path
		self.urlEdit.setText(url_new)
	

class MainWindow(QMainWindow, Ui_MainWindow):
	
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Set a title
		self.setupUi(self)
		self.setWindowTitle("BAYRELL OS Desktop Client")
		self.listWidget.setSortingEnabled(True)
		
		# Set to center
		self.setFixedSize(self.size())
		set_window_center(self)
		
		# Load items
		self.loadItems()
		
		# Button action
		self.aboutButton.clicked.connect(self.onAboutClick)
		self.addButton.clicked.connect(self.onAddClick)
		self.editButton.clicked.connect(self.onEditClick)
		self.deleteButton.clicked.connect(self.onDeleteClick)
		self.connectButton.clicked.connect(self.onConnectClick)
		#self.exitButton.clicked.connect(self.onExitClick)
		
		pass
	
	
	def show_edit_connection_dialog(self, item:QListWidgetItem = None):
		dlg = EditConnectionDialog()
		
		if item != None:
			data = item.data(1)
			dlg.connectionNameEdit.setText( data.connection_name )
			dlg.hostEdit.setText( data.host )
			dlg.portEdit.setText( data.local_port )
			dlg.usernameEdit.setText( data.username )
			dlg.passwordEdit.setText( data.password )
		
		result = dlg.exec()
		
		if result == 1:
			
			# Create data
			data = Connection()
			data.connection_name = dlg.connectionNameEdit.text()
			data.host = dlg.hostEdit.text()
			data.local_port = dlg.portEdit.text()
			data.username = dlg.usernameEdit.text()
			data.password = dlg.passwordEdit.text()
			
			# Add data to list widget
			if item == None:
				item = QListWidgetItem(data.connection_name)
				item.setData(1, data)
				self.listWidget.addItem(item)
			
			else:
				item.setText(data.connection_name)
				item.setData(1, data)
		
		
	def getSettingsFileName(self):
		path = os.path.expanduser('~')
		path = os.path.join(path, ".config", "bayrell_os")
		os.makedirs(path, exist_ok=True)
		file_name = os.path.join(path, "settings.json")
		return file_name
	
	
	def loadItems(self):
		
		file_name = self.getSettingsFileName()
		file_content = ""
		
		try:
			if os.path.exists(file_name):
				with open(file_name) as file:
					file_content = file.read()
					file.close()
				
				settings = json.loads(file_content)
				connections = settings["connections"]
				for connection in connections:
					
					data = Connection()
					data.connection_name = connection["connection_name"] \
						if "connection_name" in connection else ""
					data.host = connection["host"] \
						if "host" in connection else ""
					data.username = connection["username"] \
						if "username" in connection else ""
					data.password = connection["password"] \
						if "password" in connection else ""
					data.local_port = connection["local_port"] \
						if "local_port" in connection else "8080"
					
					item = QListWidgetItem(data.connection_name)
					item.setData(1, data)
					self.listWidget.addItem(item)
				
		finally:
			pass
		
		pass
	
	
	def saveItems(self):
		
		connections = []
		for row in range(self.listWidget.count()):
			item = self.listWidget.item(row)
			
			data = item.data(1)
			connection = {
				"connection_name": data.connection_name,
				"host": data.host,
				"local_port": data.local_port,
				"username": data.username,
				"password": data.password,
			}
			
			connections.append(connection)
		
		settings = {
			"connections": connections
		}
		
		text = json.dumps(settings, indent=2) 
		
		file_name = self.getSettingsFileName()
		with open(file_name, "w") as file:
			file.write(text)
			file.close()
			
		pass
	
	
	def onAboutClick(self):
		dlg = AboutDialog()
		result = dlg.exec()
	
	
	def onAddClick(self):
		self.show_edit_connection_dialog()
		self.saveItems()
	
	
	def onEditClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			self.show_edit_connection_dialog( self.listWidget.item(items[0].row()) )
			
		self.saveItems()
	
	
	def onDeleteClick(self):
		
		delete_msg = "Are you sure want to delete selected items?"
		result = QMessageBox.question(self, "Delete selected items",
				delete_msg, QMessageBox.Yes, QMessageBox.No)
		
		if result == QMessageBox.Yes:
			items = self.listWidget.selectedIndexes()
			for item in items:
				row = item.row()
				self.listWidget.takeItem(row)
			
			self.saveItems()
	
	
	def onConnectClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			row = items[0].row()
			item = self.listWidget.item(row)
			data = item.data(1)
			
			web_browser = WebBrowser(self)
			web_browser.connectToServer(data)
		
		pass
	
	
	def onExitClick(self):
		
		quit_msg = "Are you sure want to exit from the app?"
		result = QMessageBox.question(self, "Exit from the app",
				quit_msg, QMessageBox.Yes, QMessageBox.No)
		
		if result == QMessageBox.Yes:
			self.close()
	
	
def run():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec())
