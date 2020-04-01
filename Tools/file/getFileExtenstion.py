from extenstionDB import EXTENSIONS

HEADER_BYTES = 262


def get_header(filePath):
	#Need to add checking for file with zero lenght
	try:
		with open(filePath, 'rb') as file:
			return bytearray(file.read(HEADER_BYTES))
	except:
		print('Cant read the file')
		return None


def getFileExtension(filePath):
	header = get_header(filePath)
	if not header:
		exit()

	for extension in EXTENSIONS:
		if extension.check(header):
			return extension
	return 'Extension not found'


print(getFileExtension("Examples/CR2.CR2"))