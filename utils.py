import os
import sys
from pathlib import Path

def addFoldersToPath(directory, recursive=True):
	ignore_list=['.git', '__pycache__']
	'''
	Directory has to be pathlib format
	'''
	for item in directory.iterdir():
		#print(str(item))
		for ignored in ignore_list:
			if ignored in str(item):
				pass
			else:
				if item.is_dir():
					sys.path.append(str(item))
					if recursive:
						addFoldersToPath(item)