import os

class Session:
	def __init__(self, settings=None):
		self.creation_date = None
		self.search = None
		self.search_history = None
		self.settings = settings

	def do_search(self):
		torrent_directories = self.settings['torrent_directories']
		self.search = Search()
		self.search.torrent_directories = torrent_directories
		torrent_files, torrent_files_concatenated = self.search.torrent_search()
		return torrent_files, torrent_files_concatenated
		
		
class Search:
	def __init__(self):
		self.torrent_directories = None
		self.file_directories = None
		self.torrents = None
		self.files = None
		
	def torrent_search(self):
		return Search.search_torrent_directories(self.torrent_directories)
		
	def search_torrent_directories(directories):
		file_output = []
		concatenated_output = []
		file_counter = 0
		for directory in directories:
			for root, path, files in os.walk(directory):
				for filename in files:
					if filename.endswith(".torrent"):
						file_output.append((root, filename))
						concatenated_output.append(os.path.join(root, filename))
						file_counter += 1
		return file_output, concatenated_output
		

	def search_directory_extension(directory, extension, maximum_files=-1):
		file_output = []
		concatenated_output = []
		file_counter = 0
		for root, directories, files in os.walk(directory):
			for filename in files:
				if filename.endswith(extension):
					file_output.append((root, filename))
					concatenated_output.append(os.path.join(root, filename))
					file_counter += 1
					if maximum_files > 0 and file_counter >= maximum_files:
						return file_output, concatenated_output
		return file_output, concatenated_output

