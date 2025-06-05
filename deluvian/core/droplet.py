# DICTIONARY_DELIMITER = b'd'
# END_DELIMITER = b'e'
# INTEGER_DELIMITER = b'i'
# LIST_DELIMITER = b'l'
# BYTE_SEPARATOR = b':'


class Droplet:
	"""This class encapsulates a torrent. It contains all the information found in the torrent
	and the associated files that have been found."""
	def __init__(self,
		filename,
		torrent,
		encoding_type="utf-8"):
		self.torrent_filename = filename

		self.encoding_type = encoding_type
		#self.root_index = 0
		#self.filename_index = 1

		self._convert_raw_torrent(torrent)

		self.associated_files = []

	def _convert_raw_torrent(self, torrent):
		self.raw_torrent = torrent
		self.announce = torrent[0][b'announce']
		#self.created_by = torrent[0][b'created by']
		self.creation_date = torrent[0][b'creation date']
		self.created_by = torrent[0].get(b'created by', None)
		if b'encoding' in torrent[0].keys():
			self.encoding = torrent[0][b'encoding']
		else:
			self.encoding = None

		# Dictionary 'info'
		if b'length' in torrent[0][b'info']:
			self.length = torrent[0][b'info'][b'length']
		else:
			self.length = None
		self.name = torrent[0][b'info'][b'name'].decode(self.encoding_type)
		self.piece_length = torrent[0][b'info'][b'piece length']
		self.files = []
		if b'files' in torrent[0][b'info']:
			for x in torrent[0][b'info'][b'files']:
				self.files.append((x[b'path'][0].decode(self.encoding_type), x[b'length'])) #TODO: Is filepath always first and only item in list?
			# print(torrent[0][b'info'][b'files'])

		# Optional
		self.duration = None
		self.encoded_rate = None
		self.height = None
		self.width = None
		self.url_list = None
		if b'duration' in torrent[0].keys():
			self.duration = torrent[0][b'duration']
		if b'encoded rate' in torrent[0].keys():
			self.encoded_rate = torrent[0][b'encoded rate']
		if b'height' in torrent[0].keys():
			self.height = torrent[0][b'height']
		if b'width' in torrent[0].keys():
			self.width = torrent[0][b'width']
		if b'url-list' in torrent[0].keys():
			self.url_list = torrent[0][b'url-list']

	def add_associated_file(self, file_tuple):
		# root = file_tuple[self.root_index]
		# filename = file_tuple[self.filename_index]
		# self.associated_files.append((root, filename))
		self.associated_files.append(file_tuple)

	def clear_associated_file(self):
		self.associated_files.clear()

	def get_associated_file(self):
		return self.associated_files.copy()

	def remove_associated_file(self, index):
		self.associated_files.remove(index)

