import os
import subprocess
cwd = os.getcwd()
test_dir = os.path.abspath(cwd) + os.sep + 'TEST_DIR' 
inner_dir = test_dir + os.sep + 'INNER_DIR'
new_dir = test_dir + os.sep + 'NEW_DIR'
from pytest import fixture, raises

@fixture
def op():
    from usepy.operations import Operations
    return Operations()

def setup_function():
    try:
        os.mkdir(test_dir)
    except FileExistsError:
        pass
    files = ['test.txt', 'test.html', 'main.css']
    for fl in files:
        cmd = ['touch', test_dir + os.sep + fl]
        subprocess.Popen(cmd).wait()
    try:
        os.mkdir(inner_dir)
    except FileExistsError:
        pass
    for fl in files:
        cmd = ['touch', inner_dir + os.sep + fl]
        subprocess.Popen(cmd).wait()
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass
    cmd = ['touch', new_dir + os.sep + 'symlinked.file']
    subprocess.Popen(cmd).wait()
    try:
        os.symlink(new_dir + os.sep + 'symlinked.file', test_dir + os.sep + 'SYMLINK')
    except FileExistsError:
        pass

def teardown_function():
    cmd = ['rm', '-rf', test_dir]
    subprocess.Popen(cmd).wait()

def test_file_is_dir(op):
    assert op.file_is_dir(test_dir)
    assert op.file_is_dir(inner_dir)
    assert op.file_is_dir(new_dir)
    with raises(SystemExit):
        op.file_is_dir(new_dir + os.sep + 'test.txt')

def test_file_exists(op):
    assert op.file_exists(test_dir)
    assert op.file_exists(inner_dir)
    assert op.file_exists(new_dir)
    assert op.file_exists(test_dir + os.sep + 'test.txt')
    with raises(SystemExit):
        op.file_exists(new_dir + os.sep + 'non_existing')

def test_parse_files(op):
    assert op.parse_files(test_dir) == (os.sep.join(test_dir.split(os.sep)[:-1]), (test_dir.split(os.sep)[-1],))
    test_filepath = test_dir + os.sep + 'test.txt'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), (test_filepath.split(os.sep)[-1],))
    test_filepath = test_dir + os.sep
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), '')
    test_filepath = test_dir + os.sep + '{test.txt,main.css,test.html}'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['test.txt', 'main.css', 'test.html',])
    test_filepath = test_dir + os.sep + '*'
    test_dir_contents = ['test.txt', 'main.css', 'test.html', 'INNER_DIR', 'NEW_DIR', 'SYMLINK']
    dirpath, files = op.parse_files(test_filepath)
    for fl in test_dir_contents:
        assert fl in files
    test_filepath = test_dir + os.sep + '-'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ('-',))

def test_is_valid_file(op):
    assert op.is_valid_file(test_dir, flag='TEST') == []
    test_filepath = test_dir + os.sep
    with raises(IOError):
        assert op.is_valid_file(test_filepath, flag='SRC')
    test_filepath = test_dir + os.sep + 'test.txt'
    assert op.is_valid_file(test_filepath, flag='SRC') == (os.sep.join(test_filepath.split(os.sep)[:-1]), (test_filepath.split(os.sep)[-1],))
    test_filepath = test_dir + os.sep + '{test.txt,main.css,test.html}'
    assert op.is_valid_file(test_filepath, flag='SRC') == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['test.txt', 'main.css', 'test.html',])
    test_filepath = test_dir + os.sep + '*'
    test_dir_contents = ['test.txt', 'main.css', 'test.html', 'INNER_DIR', 'NEW_DIR', 'SYMLINK']
    dirpath, files = op.is_valid_file(test_filepath, flag='SRC')
    for fl in test_dir_contents:
        assert fl in files
    test_filepath = test_dir + os.sep + 'test.txt'
    assert op.is_valid_file(test_filepath, flag='DEST') == (os.sep.join(test_filepath.split(os.sep)[:-1]), test_filepath.split(os.sep)[-1])
    test_filepath = test_dir + os.sep
    assert op.is_valid_file(test_filepath, flag='DEST') == (test_filepath[:-1], '')
    test_filepath = test_dir
    assert op.is_valid_file(test_filepath, flag='DEST') == (test_filepath, '')

def test_copy(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    dest_filepath = new_dir + os.sep + 'test2.txt'
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.copy(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test2.txt' in new_dir_contents
    # Multiple file
    src_filepath = test_dir + os.sep + '{test.txt,main.css,test.html}'
    dest_filepath = new_dir + os.sep
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.copy(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test.txt' in new_dir_contents
    assert 'test.html' in new_dir_contents
    assert 'main.css' in new_dir_contents
    # All file
    src_filepath = test_dir + os.sep + '*'
    dest_filepath = new_dir + os.sep
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.copy(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test.txt' in new_dir_contents 
    assert 'test.html' in new_dir_contents 
    assert 'main.css' in new_dir_contents 
    assert 'INNER_DIR' in new_dir_contents
    assert 'NEW_DIR' not in new_dir_contents