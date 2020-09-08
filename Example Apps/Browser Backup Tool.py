import os
import e32
import appuifw
import stat
import sys
import zipfile
import time
from os.path import abspath

def makeArchive(fileList, archive):
    "\n    'fileList' is a list of file names - full path each name\n    'archive' is the file name for the archive with a full path\n    "
    try:
        a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)
        for f in fileList:
            a.write(f)

        a.close()
        return True
    except:
        return False



def dirEntries(dir_name, subdir, *args):
    """Return a list of file names found in directory 'dir_name'
    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional arguments, if any, are file extensions to match filenames. Matched
        file names are added to the list.
    If there are no additional arguments, all files found in the directory are
        added to the list.
    Example usage: fileList = dirEntries(r'H:\\TEMP', False, 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
    Example usage: fileList = dirEntries(r'H:\\TEMP', True)
        All files and all the files in subdirectories under H:\\TEMP will be added
        to the list.
    """
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if (not args):
                fileList.append(dirfile)
            elif (os.path.splitext(dirfile)[1][1:] in args):
                fileList.append(dirfile)
        elif (os.path.isdir(dirfile) and subdir):
            fileList.extend(dirEntries(dirfile, subdir, *args))

    return fileList



def unzip(path, zfile):
    zip = zipfile.ZipFile(zfile, 'r')
    isdir = os.path.isdir
    join = os.path.join
    norm = os.path.normpath
    split = os.path.split
    for each in zip.namelist():
        if (not each.endswith('/')):
            (root, name,) = split(each)
            directory = norm(join(path, root))
            if (not isdir(directory)):
                os.makedirs(directory)
            file(join(directory, name), 'wb').write(zip.read(each))

    zip.close()


class Error(EnvironmentError):
    __module__ = __name__


def copyfileobj(fsrc, fdst, length = (16 * 1024)):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        if (not buf):
            break
        fdst.write(buf)




def _samefile(src, dst):
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False
    return (os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst)))



def copyfile(src, dst):
    """Copy data from src to dst"""
    if _samefile(src, dst):
        raise Error, ('`%s` and `%s` are the same file' % (src,
         dst))
    fsrc = None
    fdst = None
    try:
        fsrc = open(src, 'rb')
        fdst = open(dst, 'wb')
        copyfileobj(fsrc, fdst)

    finally:
        if fdst:
            fdst.close()
        if fsrc:
            fsrc.close()




def copymode(src, dst):
    """Copy mode bits from src to dst"""
    if hasattr(os, 'chmod'):
        st = os.stat(src)
        mode = stat.S_IMODE(st.st_mode)
        os.chmod(dst, mode)



def copystat(src, dst):
    """Copy all stat info (mode bits, atime and mtime) from src to dst"""
    st = os.stat(src)
    mode = stat.S_IMODE(st.st_mode)
    if hasattr(os, 'utime'):
        os.utime(dst, (st.st_atime,
         st.st_mtime))
    if hasattr(os, 'chmod'):
        os.chmod(dst, mode)



def copy(src, dst):
    """Copy data and mode bits ("cp src dst").

    The destination may be a directory.

    """
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    copymode(src, dst)



def copy3(src, dst):
    """Copy data and all stat info ("cp -p src dst").

    The destination may be a directory.

    """
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    copystat(src, dst)



def copy2(src, dst):
    """Copy data and all stat info ("cp -p src dst").

    The destination may be a directory.

    """
    if (os.path.isdir(dst) == False):
        os.makedirs(dst)
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst)
    copystat(src, dst)



def rmtree(path, ignore_errors = False, onerror = None):
    if ignore_errors:

        def onerror(*args):
            pass

    elif (onerror is None):

        def onerror(*args):
            raise 


    names = []
    try:
        names = os.listdir(path)
    except os.error, err:
        onerror(os.listdir, path, sys.exc_info())
    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = os.lstat(fullname).st_mode
        except os.error:
            mode = 0
        if stat.S_ISDIR(mode):
            rmtree(fullname, ignore_errors, onerror)
        else:
            try:
                os.remove(fullname)
            except os.error, err:
                onerror(os.remove, fullname, sys.exc_info())

    try:
        os.rmdir(path)
    except os.error:
        onerror(os.rmdir, path, sys.exc_info())



def copytree(src, dst):
    names = os.listdir(src)
    if (os.path.isdir(dst) == False):
        os.makedirs(dst)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isdir(srcname):
            copytree(srcname, dstname)
        else:
            copy3(srcname, dstname)

    try:
        copystat(src, dst)
    except WindowsError:
        pass



def RestOfRestore():
    body.add(u'Removing temporary files...\n\n')
    e32.ao_sleep(1)
    rmtree('e:\\MyBrowser_backup\\')
    body.color = (255,
     0,
     0)
    body.add(u'Restoration Complete!')



def RestOfUCWEBBackup():
    body.add(u'Creating Zipfile for easy export/upload...\n\n')
    makeArchive(dirEntries('e:\\MyBrowser_backup\\', True), 'e:\\Others\\MyUCWEB_Backup.zip')
    e32.ao_sleep(1)
    body.add(u'Removing temporary files...\n\n')
    rmtree('e:\\MyBrowser_backup\\')
    e32.ao_sleep(1)
    body.add(u'Backup file created: \n')
    body.color = (255,
     0,
     0)
    body.add(u'e:\\Others\\MyUCWEB_Backup.zip')



def RestOfOperaBackup():
    body.add(u'Creating Zipfile for easy export/upload...\n\n')
    makeArchive(dirEntries('e:\\MyBrowser_backup\\', True), 'e:\\Others\\MyOpera_Backup.zip')
    e32.ao_sleep(1)
    body.add(u'Removing temporary files...\n\n')
    rmtree('e:\\MyBrowser_backup\\')
    e32.ao_sleep(1)
    body.add(u'Backup file created: \n')
    body.color = (255,
     0,
     0)
    body.add(u'e:\\Others\\MyOpera_Backup.zip')



def Restore():
    L = [u'UCWEB',
     u'Opera']
    index = appuifw.selection_list(L, 0)
    if (index == 0):
        e32.ao_sleep(1)
        body.clear()
        body.add(u'\nChecking for UCWEB backup...\n\n')
        e32.ao_sleep(2)
        if os.path.isfile('e:\\Others\\MyUCWEB_Backup.zip'):
            body.add(u'Backup file found. Extracting contents....\n\n')
            e32.ao_sleep(1)
            unzip('e:\\MyBrowser_Backup\\', 'e:\\others\\MyUCWEB_Backup.zip')
            RestoreUCWEB()
        else:
            appuifw.note(u'Backup file not found!')
    if (index == 1):
        e32.ao_sleep(1)
        body.clear()
        body.add(u'\nChecking for Opera backup...\n\n')
        e32.ao_sleep(2)
        if os.path.isfile('e:\\Others\\MyOpera_Backup.zip'):
            body.add(u'Backup file found. Extracting contents....\n\n')
            e32.ao_sleep(1)
            unzip('e:\\MyBrowser_Backup\\', 'e:\\others\\MyOpera_Backup.zip')
            RestoreOpera()
        else:
            appuifw.note(u'Backup file not found!')



def Backup():
    body.clear()
    L = [u'UCWEB',
     u'Opera']
    index = appuifw.selection_list(L, 0)
    if (index == 0):
        body.add(u'\nChecking for UCWEB...\n\n')
        e32.ao_sleep(2)
        if os.path.isdir('c:\\private\\A00079AF'):
            body.add(u'UCWEB is installed in drive C!\n\n')
            e32.ao_sleep(2)
            Open = appuifw.query(u'Is your phone Hacked and Open?', 'query')
            if Open:
                appuifw.note(u'Now complete UCWEB app suite will be backed up')
                body.add(u'Copying files. Please wait....\n\n')
                copytree('c:\\private\\A00079AF', 'e:\\MyBrowser_Backup\\UCWEB1')
                copytree('c:\\system\\data\\ucwebconfig', 'e:\\MyBrowser_Backup\\UCWEB2')
                copy2('c:\\sys\\bin\\UCWEB6-EN.exe', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\resource\\apps\\UCWEB6-EN.RSC', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\resource\\apps\\UCWEB6-EN_Caption.RSC', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\resource\\apps\\UCWEB6-EN_aif.mif', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\private\\10003a3f\\import\\apps\\UCWEB6-EN_reg.RSC', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\resource\\apps\\UCWEB6-ENIMAGES.MBM', 'e:\\MyBrowser_Backup\\UCWEB3')
                copy2('c:\\UCDownloaded\\empty_UCWEB6-EN.txt', 'e:\\MyBrowser_Backup\\UCWEB3')
                RestOfUCWEBBackup()
            else:
                appuifw.note(u'Only Bookmarks, Settings and Shortcuts will be backed up')
                e32.ao_sleep(1)
                body.add(u'Copying files. Please wait....\n\n')
                copytree('c:\\system\\data\\ucwebconfig', 'e:\\MyBrowser_Backup\\UCWEB2')
                RestOfUCWEBBackup()
        elif os.path.isdir('e:\\private\\A00079AF'):
            body.add(u'UCWEB is installed in drive E!\n')
            e32.ao_sleep(1)
            Open = appuifw.query(u'Is your phone Hacked and Open?', 'query')
            if Open:
                appuifw.note(u'Now complete UCWEB app suite will be backed up')
                body.add(u'Copying files. Please wait....\n\n')
                copytree('e:\\private\\A00079AF', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB1')
                copytree('e:\\system\\data\\ucwebconfig', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB2')
                copy2('e:\\sys\\bin\\UCWEB6-EN.exe', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\resource\\apps\\UCWEB6-EN.RSC', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\resource\\apps\\UCWEB6-EN_Caption.RSC', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\resource\\apps\\UCWEB6-EN_aif.mif', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\private\\10003a3f\\import\\apps\\UCWEB6-EN_reg.RSC', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\resource\\apps\\UCWEB6-ENIMAGES.MBM', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                copy2('e:\\UCDownloaded\\empty_UCWEB6-EN.txt', 'e:\\MyBrowser_Backup\\UCWEB\\UCWEB3')
                RestOfUCWEBBackup()
            else:
                e32.ao_sleep(1)
                appuifw.note(u'Only Bookmarks, Settings and Shortcuts will be backed up')
                e32.ao_sleep(1)
                appuifw.note(u'Copying Files...\n')
                copytree('e:\\system\\data\\ucwebconfig', 'e:\\MyBrowser_Backup\\UCWEB2')
                RestOfUCWEBBackup()
    if (index == 1):
        body.add(u'\nChecking for Opera...\n\n')
        e32.ao_sleep(2)
        if os.path.isdir('c:\\system\\data\\opera'):
            body.add(u'Opera is installed in drive C!\n\n')
            body.add(u'Copying files. Please wait....\n\n')
            copytree('c:\\system\\data\\opera', 'e:\\MyBrowser_Backup\\OPERA')
            RestOfOperaBackup()
        elif os.path.isdir('e:\\system\\data\\opera'):
            body.add(u'Opera is installed in drive E!\n\n')
            body.add(u'Copying files. Please wait....\n\n')
            copytree('e:\\system\\data\\opera', 'e:\\MyBrowser_Backup\\OPERA')
            RestOfOperaBackup()



def RestoreUCWEB():
    L = [u'Install Drive C',
     u'Install Drive E']
    index = appuifw.selection_list(L, 0)
    if (index == 0):
        body.add(u'Restoring. Please wait...\n\n')
        copytree('e:\\MyBrowser_Backup\\UCWEB2', 'c:\\system\\data\\ucwebconfig')
        if os.path.isdir('e:\\MyBrowser_Backup\\UCWEB1'):
            copytree('e:\\MyBrowser_Backup\\UCWEB1', 'c:\\private\\A00079AF')
        if os.path.isdir('e:\\MyBrowser_Backup\\UCWEB3'):
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN.exe', 'c:\\sys\\bin')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN.RSC', 'c:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_Caption.RSC', 'c:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_aif.mif', 'c:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_reg.RSC', 'c:\\private\\10003a3f\\import\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-ENIMAGES.MBM', 'c:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\empty_UCWEB6-EN.txt', 'c:\\UCDownloaded')
    else:
        body.add(u'Restoring. Please wait...\n\n')
        copytree('e:\\MyBrowser_Backup\\UCWEB2', 'e:\\system\\data\\ucwebconfig')
        if os.path.isdir('e:\\MyBrowser_Backup\\UCWEB1'):
            copytree('e:\\MyBrowser_Backup\\UCWEB1', 'e:\\private\\A00079AF')
        if os.path.isdir('e:\\MyBrowser_Backup\\UCWEB3'):
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN.exe', 'e:\\sys\\bin')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN.RSC', 'e:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_Caption.RSC', 'e:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_aif.mif', 'e:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-EN_reg.RSC', 'e:\\private\\10003a3f\\import\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\UCWEB6-ENIMAGES.MBM', 'e:\\resource\\apps')
            copy2('e:\\MyBrowser_Backup\\UCWEB3\\empty_UCWEB6-EN.txt', 'e:\\UCDownloaded')
    RestOfRestore()



def RestoreOpera():
    L = [u'Install Drive C',
     u'Install Drive E']
    index = appuifw.selection_list(L, 0)
    if (index == 0):
        body.add(u'Restoring. Please wait...\n\n')
        copytree('e:\\MyBrowser_Backup\\OPERA', 'c:\\system\\data\\opera')
    else:
        body.add(u'Restoring. Please wait...\n\n')
        copytree('e:\\MyBrowser_Backup\\OPERA', 'e:\\system\\data\\opera')
    RestOfRestore()



def about():
    appuifw.note(u'MyBrowser Backup v1.1 by jbpseudo ')



def quit():
    app_lock.signal()



def exit():
    appuifw.app.set_exit()


body = appuifw.Text()
body.set(u"---------------------------------\nHi. This simple script backs up the browsers user data to a file on the memory card.\n\nUCWEB features 'Core-Backup'. \nYou dont need to reinstall after restore!! \n\nData backed up for OPERA include Bookmarks, Settings, History, Cache, and Cookies. Core backup will be implemented soon!\n\nPress 'Options' for Backup/Restore")
appuifw.app.screen = 'normal'
appuifw.app.body = body
appuifw.app.exit_key_handler = quit
appuifw.app.title = u'My_Browser Backup'
appuifw.app.menu = [(u'Backup',
  Backup),
 (u'Restore',
  Restore),
 (u'about',
  about),
 (u'Exit',
  exit)]
app_lock = e32.Ao_lock()
app_lock.wait()

