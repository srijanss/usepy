"""
Operations of the project
-- copy
-- rename
-- rename_prepend
-- rename_append
-- delete
-- move
"""
import subprocess

class Operations(object):

	def __init__(self):
		pass

	def copy(self, *file_to_copy, **kwargs):
		"""
		* - copy all
		test.txt - copy specific
		test.* - copy all that match pattern
		test1, test2, test3 - copy multiple
		-- args
		*file_to_copy -- tuple containing file or files to copy	
		**kwargs -- dict containing source dir, destination dir
		"""
		pass

	def rename(self, *file_to_rename, **kwargs):
		"""
		* - rename all
		test.txt - rename specific
		test.* - rename all that match pattern
		test1, test2, test3 - rename multiple
		-- args
		*file_to_rename -- tuple containing file or files to rename	
		**kwargs -- dict containing source dir, destination dir, 
				texttouse
		"""
		pass

	def rename_prepend(self, *file_to_rename, **kwargs):
		"""
		* - rename_prepend all
		test.txt - rename_prepend specific
		test.* - rename_prepend all that match pattern
		test1, test2, test3 - rename_prepend multiple
		-- args
		*file_to_rename -- tuple containing file or files to rename
		**kwargs -- dict containing source dir, destination dir, 
				texttouse
		"""
		pass

	def rename_append(self, *file_to_rename, **kwargs):
		"""
		* - rename_append all
		test.txt - rename_append specific
		test.* - rename_prepend all that match pattern
		test1, test2, test3 - rename_prepend multiple
		-- args
		*file_to_rename -- tuple containing file or files to rename
		**kwargs -- dict containing source dir, destination dir, 
				texttouse
		"""
		pass

	def move(self, *file_to_move, **src_dest):
		"""
		* - move all
		test.txt - move specific
		test.* - move all that match pattern
		test1, test2, test3 - move multiple
		-- args
		*file_to_move -- tuple containing file or files to move
		**kwargs -- dict containing source dir, destination dir
		"""
		pass

	def delete(self, *file_to_delete, **dir):
		"""
		* - delete all
		test.txt - delete specific
		test.* - delete all that match pattern
		test1, test2, test3 - delete multiple
		-- args
		*file_to_delete -- tuple containing file or files to delete
		**kwargs -- dict containing source dir
		"""
		pass
