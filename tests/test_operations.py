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
    files = ['test.txt', 'test.html', 'main.css', 'last.txt']
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
    assert op.parse_files(test_dir) == (os.sep.join(test_dir.split(os.sep)[:-1]), [test_dir.split(os.sep)[-1]])
    test_filepath = test_dir + os.sep + 'test.txt'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), [test_filepath.split(os.sep)[-1]])
    test_filepath = test_dir + os.sep + 'test*'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['test.html', 'test.txt'])
    test_filepath = test_dir + os.sep + '*.css'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['main.css'])
    test_filepath = test_dir + os.sep
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), '')
    test_filepath = test_dir + os.sep + '{test.txt,main.css,test.html}'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['test.txt', 'main.css', 'test.html',])
    test_filepath = test_dir + os.sep + '{test*,*.css}'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['test.html', 'test.txt', 'main.css'])
    test_filepath = test_dir + os.sep + '*'
    test_dir_contents = ['test.txt', 'main.css', 'test.html', 'INNER_DIR', 'NEW_DIR', 'SYMLINK']
    dirpath, files = op.parse_files(test_filepath)
    for fl in test_dir_contents:
        assert fl in files
    test_filepath = test_dir + os.sep + '-'
    assert op.parse_files(test_filepath) == (os.sep.join(test_filepath.split(os.sep)[:-1]), '')

def test_is_valid_file(op):
    assert op.is_valid_file(test_dir, flag='TEST') == []
    test_filepath = test_dir + os.sep
    assert op.is_valid_file(test_filepath, flag='SRC') == (os.sep.join(test_filepath.split(os.sep)[:-1]), ['INNER_DIR', 'last.txt', 'main.css', 'NEW_DIR', 'SYMLINK', 'test.html', 'test.txt'])
    # with raises(IOError):
    #     assert op.is_valid_file(test_filepath, flag='SRC')
    test_filepath = test_dir + os.sep + 'test.txt'
    assert op.is_valid_file(test_filepath, flag='SRC') == (os.sep.join(test_filepath.split(os.sep)[:-1]), [test_filepath.split(os.sep)[-1]])
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

def test_get_md5_checksum(op):
    test_filepath = test_dir + os.sep + 'test.txt'
    test_filepath2 = test_dir + os.sep + 'test.txt'
    test_filepath3 = test_dir + os.sep + 'test.html'
    assert op.get_md5_checksum(test_filepath) == op.get_md5_checksum(test_filepath2)
    assert op.get_md5_checksum(test_filepath) == op.get_md5_checksum(test_filepath3)

def test_get_checksum_dict(op):
    test_filepath = test_dir
    md5 = op.get_checksum_dict(test_filepath)
    for fl in (test_dir + os.sep + fd for fd in os.listdir(test_filepath)):
        if not os.path.isdir(fl):
            assert md5[fl] == 'd41d8cd98f00b204e9800998ecf8427e'
        else:
            assert isinstance(md5[fl], dict)

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

def test_move(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    dest_filepath = new_dir + os.sep + 'test2.txt'
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.move(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test2.txt' in new_dir_contents
    assert 'test.txt' not in os.listdir(test_dir)
    # Multiple file
    src_filepath = test_dir + os.sep + '{main.css,test.html}'
    dest_filepath = new_dir + os.sep
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.move(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test.html' in new_dir_contents
    assert 'main.css' in new_dir_contents
    assert 'test.html' not in os.listdir(test_dir)
    assert 'main.css' not in os.listdir(test_dir)
    # All file
    src_filepath = test_dir + os.sep + '*'
    dest_filepath = new_dir + os.sep
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.move(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test2.txt' in new_dir_contents 
    assert 'test.html' in new_dir_contents 
    assert 'main.css' in new_dir_contents 
    assert 'INNER_DIR' in new_dir_contents
    assert 'NEW_DIR' not in new_dir_contents
    assert 'last.txt' in new_dir_contents
    # Move directory
    src_filepath = new_dir + os.sep + 'INNER_DIR'
    dest_filepath = test_dir
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    op.move(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'INNER_DIR' not in new_dir_contents
    assert 'INNER_DIR' in os.listdir(test_dir)

def test_delete(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    kwargs = {'src': src_filepath}
    op.delete(**kwargs)
    assert 'test2.txt' not in os.listdir(test_dir)
    # Multiple file
    src_filepath = test_dir + os.sep + '{main.css,test.html}'
    kwargs = {'src': src_filepath}
    op.delete(**kwargs)
    new_dir_contents = os.listdir(test_dir)
    assert 'test.html' not in new_dir_contents
    assert 'main.css' not in new_dir_contents
    # All file
    src_filepath = test_dir + os.sep + '*'
    kwargs = {'src': src_filepath}
    op.delete(**kwargs)
    new_dir_contents = os.listdir(test_dir)
    assert 'test.html' not in new_dir_contents 
    assert 'main.css' not in new_dir_contents 
    assert 'INNER_DIR' not in new_dir_contents
    assert 'NEW_DIR' not in new_dir_contents
    assert 'last.txt' not in new_dir_contents
    # Delete directory
    os.mkdir(test_dir + os.sep + 'LAST_DIR')
    src_filepath = test_dir + os.sep + 'LAST_DIR'
    kwargs = {'src': src_filepath}
    op.delete(**kwargs)
    new_dir_contents = os.listdir(test_dir)
    assert 'LAST_DIR' not in new_dir_contents

def test_rename(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    kwargs = {'src': src_filepath, 'rename_text': 'rename'}
    op.rename(**kwargs)
    assert 'test.txt' not in os.listdir(test_dir)
    assert 'rename.txt' in os.listdir(test_dir)
    # rename dir
    src_filepath = test_dir + os.sep + 'INNER_DIR'
    kwargs = {'src': src_filepath, 'rename_text': 'DIR_INNER'}
    op.rename(**kwargs)
    assert 'INNER_DIR' not in os.listdir(test_dir)
    assert 'DIR_INNER' in os.listdir(test_dir)

def test_rename_prepend(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    kwargs = {'src': src_filepath, 'rename_text': 'rename'}
    op.rename_prepend(**kwargs)
    assert 'test.txt' not in os.listdir(test_dir)
    assert 'rename_test.txt' in os.listdir(test_dir)
    # different separator
    src_filepath = test_dir + os.sep + 'test.html'
    kwargs = {'src': src_filepath, 'rename_text': 'rename', 'separator': '%'}
    op.rename_prepend(**kwargs)
    assert 'test.html' not in os.listdir(test_dir)
    assert 'rename%test.html' in os.listdir(test_dir)
    # rename dir
    src_filepath = test_dir + os.sep + 'INNER_DIR'
    kwargs = {'src': src_filepath, 'rename_text': 'RENAME'}
    op.rename_prepend(**kwargs)
    assert 'INNER_DIR' not in os.listdir(test_dir)
    assert 'RENAME_INNER_DIR' in os.listdir(test_dir)

def test_rename_append(op):
    src_filepath = test_dir + os.sep + 'test.txt'
    kwargs = {'src': src_filepath, 'rename_text': 'rename'}
    op.rename_append(**kwargs)
    assert 'test.txt' not in os.listdir(test_dir)
    assert 'test_rename.txt' in os.listdir(test_dir)
    # different separator
    src_filepath = test_dir + os.sep + 'test.html'
    kwargs = {'src': src_filepath, 'rename_text': 'rename', 'separator': '%'}
    op.rename_append(**kwargs)
    assert 'test.html' not in os.listdir(test_dir)
    assert 'test%rename.html' in os.listdir(test_dir)
    # rename dir
    src_filepath = test_dir + os.sep + 'INNER_DIR'
    kwargs = {'src': src_filepath, 'rename_text': 'RENAME'}
    op.rename_append(**kwargs)
    assert 'INNER_DIR' not in os.listdir(test_dir)
    assert 'INNER_DIR_RENAME' in os.listdir(test_dir)

def test_backup(op):
    src_filepath = test_dir + os.sep
    dest_filepath = new_dir + os.sep
    kwargs = {'src': src_filepath, 'dest': dest_filepath}
    kwargs2 = {'src': src_filepath + 'test.html', 'dest': inner_dir}
    op.copy(**kwargs2)
    op.backup(**kwargs)
    new_dir_contents = os.listdir(new_dir)
    assert 'test.txt' in new_dir_contents
    inner_dir_contents = os.listdir(new_dir + os.sep + 'INNER_DIR')
    assert 'test.html' in inner_dir_contents
