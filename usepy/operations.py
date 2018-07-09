"""
Operations of the project
-- copy
-- rename
-- rename_prepend
-- rename_append
-- delete
-- move
"""
import os
import sys

home_dir = os.path.expanduser('~')

class Operations(object):

    def __init__(self):
        pass

    def copy(self, *file_to_copy, **kwargs):
        """
        -- Source
            -- File copy
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory copy
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 

        -- Destination
            -- Copy to destination with new filename
            kwargs['dest'] = '/home/srijan/copyto/test2.txt'
            -- Copy to destination folder
            kwargs['dest'] = '/home/srijan/copyto'
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            dest_dir, dest_file = self.is_valid_file(kwargs['dest'], flag='DEST')
            # Read from source, Write to destination
            srcfl_content = ''
            temp_dest_file = dest_file
            for fl in src_files:
                if os.path.islink(src_dir + os.sep + fl):
                    print('Skipping symlink {}'.format(src_dir + os.sep + fl))
                elif os.path.isdir(src_dir + os.sep + fl): 
                    # print('{} is a directory'.format(fl))
                    if src_dir + os.sep + fl == dest_dir:
                        continue
                    try:
                        os.mkdir(dest_dir + os.sep + fl)
                    except FileExistsError:
                        pass
                    rkwargs = {'src': src_dir + os.sep + fl + '/*', 'dest': dest_dir + os.sep + fl + os.sep}
                    self.copy(**rkwargs)
                else:
                    # Read file in source
                    with open(src_dir + os.sep + fl, 'r') as srcfl:
                        srcfl_content = srcfl.read()
                    # Write file to destinations
                    if os.path.isdir(dest_dir) and os.path.isdir(dest_dir + os.sep + dest_file):
                        dest_file = dest_dir + os.sep + fl
                    elif os.path.isdir(dest_dir) and not os.path.isdir(dest_dir + os.sep + dest_file):
                        dest_file = dest_dir + os.sep + dest_file 
                    with open(dest_file, 'w') as destfl:
                        print('Copying {} to {}'.format(src_dir + os.sep + fl, dest_file))
                        destfl.write(srcfl_content)
                        dest_file = temp_dest_file 
        except IOError as err:
            print(err)

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

    def is_valid_file(self, dirpath, flag='SRC'):
        if flag == 'SRC':
            # Source file Exists
            if dirpath[-1] == '/': # Directory
                raise IOError('{} File to copy not provided'.format(dirpath))
            elif ('{' in (dirpath[-1][0]) and '}' in dirpath[-1][-1]) or '*' in dirpath[-1]:
                self.file_exists(dirpath[:-1])
            file_dir, dir_file = self.parse_files(dirpath)
            for fl in dir_file:
                self.file_exists(file_dir + os.sep + fl)
        elif flag == 'DEST':
            # Destination directory Exists
            if dirpath[-1] == '/':
                self.file_exists(dirpath)
                dirpath = dirpath[:-1]
            file_dir, dir_file = self.parse_files(dirpath)
            dir_file = dir_file[0] if dir_file else dir_file
            if self.file_exists(file_dir):
                self.file_is_dir(file_dir)
            if os.path.isdir(file_dir + os.sep + dir_file):
                file_dir = file_dir + os.sep + dir_file
                dir_file = ''
        else:
            return []
        return (file_dir, dir_file)

    @staticmethod
    def parse_files(dirpath):
        pathlist = dirpath.split(os.sep)
        path_to_dir = os.sep.join(pathlist[:-1])
        files = pathlist[-1]
        if files:
            if '{' in (files[0]) and '}' in (files[-1]):
                files = files[1:-1].split(',')
            elif files[0] == '*':
                files = os.listdir(path_to_dir)
            else:
                files = (files,)
        return (path_to_dir, files)

    @staticmethod
    def file_exists(dirpath):
        try:
            if os.path.exists(dirpath):
                return True
            raise FileNotFoundError('{} File not Found'.format(dirpath))
        except FileNotFoundError as err:
            print(err)
            sys.exit(0)

    @staticmethod
    def file_is_dir(dirpath):
        try:
            if os.path.isdir(dirpath):
                return True
            raise FileNotFoundError('{} Not a directory'.format(dirpath))
        except FileNotFoundError as err:
            print(err)
            sys.exit(0)
