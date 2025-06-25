from tkinter import *

from deluvian.gui.mainwindow import ApplicationWindow, SettingsWindow
from deluvian.core.session import Session
from deluvian.utils.directories import search_torrent_directories

DEBUG = True

#TORRENT_DIRECTORY = "F:\\Videos\\Torrent"
#FILE_DIRECTORY = "F:\\Videos\\Movies"
TORRENT_DIRECTORY = "/media/accessory/Extreme SSD/Torrents"
FILE_DIRECTORY = "/media/accessory/Extreme SSD/Videos"
#TORRENT_DIRECTORY = "/media/stewart/Extreme SSD/Torrents"
#FILE_DIRECTORY = "/media/stewart/Extreme SSD/Videos"

class Application:
	application_title = "Deluvian"
		
	def __init__(self):
		self.root = Tk()
		self.root.title(Application.application_title)
		
		self.session = self.load_session()
		self.window = ApplicationWindow(self.root, self, self.session)
		self.settings_window = None		
		#self.settings = self.session.settings
		
		self.root.mainloop()
		
	def load_session(self):
		return Session(settings=self.generate_settings())

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
		
	def generate_session(self):
		session = Session(settings=self.generate_settings())
		
		return session
		
		
	def open_settings_window(self):
		if self.settings_window is None:
			self.settings_window = SettingsWindow(self.root, self)
			
	def do_search(self):
		search = self.session.current_search
		torrent_directories = search.torrent_directories
		torrent_files, torrent_files_concatenated = search_torrent_directories(torrent_directories)
		self.window.torrent_list.set(torrent_files_concatenated)
		#self.droplet_list.clear()
		#for torrent_file in self.torrent_files_concatenated:
		#	 self.droplet_list.append(Droplet(torrent_file, bdecode(torrent_file)))
		

