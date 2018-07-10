import os
home_dir = os.path.expanduser('~')
from operations import Operations
op = Operations()
kwargs = {'src': home_dir + os.sep + 'temp/123.txt', 'dest': home_dir + os.sep + 'copyto/1234.txt'}
# srcdirpath = home_dir + os.sep + '{test1.txt,test.txt}'
# srcdirpath = home_dir + os.sep + 'temp/*' 
# srcdirpath = home_dir
# op.copy(**kwargs)
# op.move(**kwargs)
op.delete(**kwargs)
