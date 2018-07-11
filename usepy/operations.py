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
import shutil
import inspect

home_dir = os.path.expanduser('~')

class Operations(object):

    def __init__(self):
        pass

    def copy(self, **kwargs):
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
            srcfl_content = ''
            temp_dest_file = dest_file
            for fl in src_files:
                if os.path.islink(src_dir + os.sep + fl):
                    try:
                        os.symlink(src_dir + os.sep + fl, dest_dir + os.sep + fl)
                        print('Copying Symlinks from {} to {}'.format(os.path.realpath(src_dir + os.sep + fl), dest_dir + os.sep + fl))
                    except FileExistsError:
                        pass
                elif os.path.isdir(src_dir + os.sep + fl):
                    if src_dir + os.sep + fl == dest_dir:
                        continue
                    try:
                        os.mkdir(dest_dir + os.sep + fl)
                    except FileExistsError:
                        pass
                    rkwargs = {'src': src_dir + os.sep + fl + '/*', 'dest': dest_dir + os.sep + fl + os.sep}
                    self.copy(**rkwargs)
                else:
                    if os.path.isdir(dest_dir) and os.path.isdir(dest_dir + os.sep + dest_file):
                        dest_file = dest_dir + os.sep + fl
                    elif os.path.isdir(dest_dir) and not os.path.isdir(dest_dir + os.sep + dest_file):
                        dest_file = dest_dir + os.sep + dest_file 
                    res_dest = shutil.copy2(src_dir + os.sep + fl, dest_file)
                    if res_dest == dest_dir + os.sep + fl:
                        print('Copying {} to {}'.format(src_dir + os.sep + fl, res_dest))
                    else:
                        print('Error Copying {} to {}'.format(src_dir + os.sep + fl, res_dest))
                    dest_file = temp_dest_file 
        except IOError as err:
            print(err)

    def rename(self, **kwargs):
        """
        -- Source
            -- File rename 
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory rename
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            rename_text = kwargs['rename_text']
            if src_files:
                for fl in src_files:
                    if os.path.isdir(src_dir) and os.path.isdir(src_dir + os.sep + fl):
                        os.rename(src_dir + os.sep + fl, src_dir + os.sep + rename_text)
                        print('Renaming {} to {}'.format(src_dir + os.sep + fl, src_dir + os.sep + rename_text))
                    else:
                        ext = fl.split('.')[1]
                        os.rename(src_dir + os.sep + fl, src_dir + os.sep + rename_text + '.' + ext)
                        print('Renaming {} to {}'.format(src_dir + os.sep + fl, src_dir + os.sep + rename_text + '.' + ext))
            else:
                base_dir = os.sep.join(src_dir.split(os.sep)[:-1])
                os.rename(src_dir,  base_dir + os.sep + rename_text)
                print('Renaming {} to {}'.format(src_dir, base_dir + os.sep + rename_text))
        except IOError as err:
            print(err)

    def rename_prepend(self, *file_to_rename, **kwargs):
        """
        -- Source
            -- File rename 
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory rename
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            rename_text = kwargs['rename_text']
            separator = '_' if 'separator' not in kwargs else kwargs['separator']
            if src_files:
                for fl in src_files:
                    os.rename(src_dir + os.sep + fl, src_dir + os.sep + rename_text + separator + fl)
                    print('Renaming {} to {}'.format(src_dir + os.sep + fl, src_dir + os.sep + rename_text + separator + fl))
            else:
                base_dir = os.sep.join(src_dir.split(os.sep)[:-1])
                change_dir = src_dir.split(os.sep)[-1]
                os.rename(src_dir,  base_dir + os.sep + rename_text + separator + change_dir)
                print('Renaming {} to {}'.format(src_dir, base_dir + os.sep + rename_text + separator + change_dir))
        except IOError as err:
            print(err)

    def rename_append(self, *file_to_rename, **kwargs):
        """
        -- Source
            -- File rename 
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory rename
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            rename_text = kwargs['rename_text']
            separator = '_' if 'separator' not in kwargs else kwargs['separator']
            if src_files:
                for fl in src_files:
                    if os.path.isdir(src_dir) and os.path.isdir(src_dir + os.sep + fl):
                        os.rename(src_dir + os.sep + fl, src_dir + os.sep + fl + separator + rename_text)
                        print('Renaming {} to {}'.format(src_dir + os.sep + fl, src_dir + os.sep + fl + separator + rename_text))
                    else:
                        filename, ext = fl.split('.')
                        os.rename(src_dir + os.sep + fl, src_dir + os.sep + filename + separator + rename_text + '.' + ext)
                        print('Renaming {} to {}'.format(src_dir + os.sep + fl, src_dir + os.sep + filename + separator + rename_text + '.' + ext))
            else:
                base_dir = os.sep.join(src_dir.split(os.sep)[:-1])
                change_dir = src_dir.split(os.sep)[-1]
                os.rename(src_dir,  base_dir + os.sep + change_dir + separator + rename_text)
                print('Renaming {} to {}'.format(src_dir, base_dir + os.sep + change_dir + separator + rename_text))
        except IOError as err:
            print(err)

    def move(self, **kwargs):
        """
        -- Source
            -- File move
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory move
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 

        -- Destination
            -- Move to destination with new filename
            kwargs['dest'] = '/home/srijan/copyto/test2.txt'
            -- Move to destination folder
            kwargs['dest'] = '/home/srijan/copyto'
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            dest_dir, dest_file = self.is_valid_file(kwargs['dest'], flag='DEST')
            for fl in src_files:
                if dest_file:
                    res_dest = shutil.move(src_dir + os.sep + fl, dest_dir + os.sep + dest_file)
                else:
                    res_dest = shutil.move(src_dir + os.sep + fl, dest_dir)
                if res_dest == dest_dir + os.sep + fl:
                    print('Moving {} to {}'.format(src_dir + os.sep + fl, res_dest))
                else:
                    print('Error Moving {} to {}'.format(src_dir + os.sep + fl, res_dest))
        except IOError as err:
            print(err)

    def delete(self, **kwargs):
        """
        -- Source
            -- File delete 
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory delete 
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 
        """
        try:
            src_dir, src_files = self.is_valid_file(kwargs['src'], flag='SRC')
            if src_files:
                for fl in src_files:
                    if os.path.isdir(src_dir) and os.path.isdir(src_dir + os.sep + fl):
                        shutil.rmtree(src_dir + os.sep + fl)
                        print('Deleting {} '.format(src_dir + os.sep + fl))
                    elif os.path.isdir(src_dir) and not os.path.isdir(src_dir + os.sep + fl):
                        os.remove(src_dir + os.sep + fl)
                        print('Deleting {} '.format(src_dir + os.sep + fl))
            else:
                shutil.rmtree(src_dir)
                print('Deleting {} '.format(src_dir))
        except IOError as err:
            print(err)

    def find(self, **kwargs):
        pass

    def backup(self, **kwargs):
        """
        -- Source
            -- File backup 
            kwargs['src'] = '/home/srijan/test1.txt' 
            kwargs['src'] = '/home/srijan/{test1.txt,test2.txt}' 
            kwargs['src'] = '/home/srijan/*' 
            -- Directory backup 
            kwargs['src'] = '/home/srijan/' 
            kwargs['src'] = '/home/srijan' 

        -- Destination
            -- Backup to destination with new filename
            kwargs['dest'] = '/home/srijan/copyto/test2.txt'
            -- Backup to destination folder
            kwargs['dest'] = '/home/srijan/copyto'
        """
        pass

    def encrypt(self, **kwargs):
        pass

    def decrypt(self, **kwargs):
        pass

    def is_valid_file(self, dirpath, flag='SRC'):
        if flag == 'SRC':
            # Source file Exists
            print()
            if dirpath[-1] == '/': # Directory
                raise IOError('{} File to {} not provided'.format(dirpath, inspect.stack()[1][3]))
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
