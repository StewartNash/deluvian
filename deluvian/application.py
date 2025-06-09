from tkinter import *

from deluvian.gui.mainwindow import ApplicationWindow, SettingsWindow

DEBUG = True

#TORRENT_DIRECTORY = "F:\\Videos\\Torrent"
#FILE_DIRECTORY = "F:\\Videos\\Movies"
#TORRENT_DIRECTORY = "/media/accessory/Extreme SSD/Torrents"
#FILE_DIRECTORY = "/media/accessory/Extreme SSD/Videos"
TORRENT_DIRECTORY = "/media/stewart/Extreme SSD/Torrents"
FILE_DIRECTORY = "/media/stewart/Extreme SSD/Videos"

class Application:
	application_title = "Deluvian"
		
	def __init__(self):
		self.root = Tk()
		self.root.title(Application.application_title)
				
		self.window = ApplicationWindow(self.root, self, self.generate_settings())
		self.settings_window = None
		
		self.settings = self.load_settings()
		
		self.root.mainloop()

	def load_settings(self):
		settings = {}
		if DEBUG:
			settings["maximum_files"] = 25
			settings["maximum_torrents"] = 25
		else:
			settings["maximum_files"] = -1
			settings["maximum_torrents"] = -1
		return settings
		
	def generate_settings(self):
	    settings = {}
	    settings['torrent_directories'] = [TORRENT_DIRECTORY]
	    settings['file_directories'] = [FILE_DIRECTORY]
	    settings['maximum_files'] = 25
	    settings['maximum_torrents'] = 25
	    
	    return settings
	    
	def open_settings_window(self):
	    if self.settings_window is None:
	        self.settings_window = SettingsWindow(self.root, self)
		

