from deluvian.gui.mainwindow import ApplicationWindow

DEBUG = True

class Application:
	def __init__(self):
		self.window = ApplicationWindow()
		self.settings = self.load_settings()
		
	def load_settings(self):
		settings = {}
		if DEBUG:
			settings["maximum_files"] = 25
			settings["maximum_torrents"] = 25
		else:
			settings["maximum_files"] = -1
			settings["maximum_torrents"] = -1
		return settings
		

