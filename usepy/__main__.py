import os
home_dir = os.path.expanduser('~')
from operations import Operations
op = Operations()
kwargs = {'src': home_dir + os.sep + 'temp/*', 'dest': home_dir + os.sep + 'copyto'}
# srcdirpath = home_dir + os.sep + '{test1.txt,test.txt}'
# srcdirpath = home_dir + os.sep + 'temp/*' 
# srcdirpath = home_dir
op.copy(**kwargs)
