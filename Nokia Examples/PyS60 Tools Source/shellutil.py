# Copyright (c) 2005-2009 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import stat
import re
import shutil
import thread
import os.path
from os.path import normpath
from subprocess import *
from threading import Thread
import zipfile
import tarfile


class CommandFailedException(Exception):
    pass


class BuildFailedException(Exception):
    pass


class ConfigureError(Exception):
    pass


def log(str):
    """Prints the log in PyS60 format.
    This must be used in place of "print" to get uniformity in logs
    """
    print "PyS60: " + str


def run_shell_command(cmd, stdin='', mixed_stderr=0, verbose=0,
                      exception_on_error=1):
    """Internal method to execute shell commands"""
    stdout_buf = []
    if mixed_stderr:
        stderr_buf = stdout_buf
    else:
        stderr_buf = []
    if verbose:
        print '- ', cmd
    p = Popen(cmd,
              stdin=PIPE,
              stdout=PIPE,
              stderr=PIPE,
              shell=True)
    p.stdin.write(stdin)
    p.stdin.close()

    def handle_stderr():
        while 1:
            line = p.stderr.readline()
            if len(line) == 0:
                break
            if verbose:
                print " ** " + line
            stderr_buf.append(line)
    stderr_thread = Thread(target=handle_stderr)
    stderr_thread.start()
    while 1:
        line = p.stdout.readline()
        if len(line) == 0:
            break
        if verbose:
            print " -- " + line,
        stdout_buf.append(line)
    retcode = p.wait()
    stderr_thread.join()
    if retcode != 0 and exception_on_error:
        raise CommandFailedException('Command "%s" failed with code "%s"'
                                       % (cmd, retcode))
    if mixed_stderr:
        return {'stdout': ''.join(stdout_buf),
                'return_code': retcode}
    else:
        return {'stdout': ''.join(stdout_buf),
                'stderr': ''.join(stderr_buf),
                'return_code': retcode}


def run_cmd(cmd, verbose=1, exception_on_error=1):
    """Method to execute shell commands.
    Set verbose to 0 to stop logging messages.
    """
    log('Executing command :<%s>' % cmd)
    run_shell_command(cmd, mixed_stderr=1, verbose=verbose,
                      exception_on_error=exception_on_error)


def rename_file(fromfile, tofile):
    if not os.path.exists(fromfile):
        log("shellutil.py: Error: %s File does not exists" % (fromfile))
        return
    fromfile = normpath(fromfile)
    tofile = normpath(tofile)
    delete_file(tofile)
    log("shellutil.py: Renaming: %s -> %s" % (fromfile, tofile))
    os.rename(fromfile, tofile)


def copy_file(fromfile, tofile):
    """Method to copy files"""
    fromfile = normpath(fromfile)
    tofile = normpath(tofile)
    if fromfile == tofile:
        log("shellutil.py: No need to copy, source and target are the same:" +
             "%s -> %s" % (fromfile, tofile))
    else:
        log("shellutil.py: Copying: %s -> %s" % (fromfile, tofile))
        targetdir = os.path.dirname(os.path.abspath(tofile))
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
        content = open(fromfile, 'rb').read()
        open(tofile, 'wb').write(content)


def delete_file(filename):
    """Method to delete a particular file if that exists
    If access is denied will give an error.
    """
    if os.path.exists(filename):
        log("Deleting: %s" % filename)
        os.remove(filename)


def deltree_if_exists(dirname):
    """Delete an entire directory."""
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def files_matching_regex(topdir, regex):
    """Find the matching files in a directory
    Return an empty list if file not found
    """
    files = []
    compiled_regex = re.compile(regex, re.I)
    for path, dirnames, filenames in os.walk(topdir):
        for x in filenames:
            pathname = os.path.join(path, x)
            if compiled_regex.match(pathname):
                files.append(pathname)
    return files


def setcapas(output, capas, compression_type='', verbose=0):
    """Method to apply new capability set & compression type on dlls or exes
    This is used as post linker
    """
    compression_opt = ''
    if compression_type != '':
        compression_opt = '-compressionmethod ' + compression_type
    run_cmd('elftran -capability "%s" %s %s' \
                                           % (capas, compression_opt, output))
    if verbose:
        run_cmd('elftran -dump s %s' % output, exception_on_error=0)


def create_archive_from_directory(archive_name, topdir, archive_dir='',
                                  archive_type='zip'):
    """Creates a compressed archive from the contents of the given directory.
       The archive types supported are tar.gz and zip.
    """
    archive_name = os.path.normpath(archive_name)
    topdir = os.path.normpath(topdir)
    print "Creating archive %s from directory %s..." % (archive_name, topdir)

    if archive_type == 'tar.gz':
        archive = tarfile.open(archive_name, 'w:gz')
    else:
        archive = zipfile.ZipFile(archive_name, 'w')
    abs_topdir = os.path.abspath(topdir)
    for root, dirs, files in os.walk(topdir):
        if '.svn' in dirs:
            dirs.remove('.svn')
        abs_root = os.path.abspath(root)
        # Remove the common part from the directory name,
        # leaving just the relative part
        relative_path = abs_root[len(abs_topdir) + 1:]
        for name in files:
            absolute_filename = os.path.join(abs_root, name)
            archive_filename = os.path.join(relative_path, name)
            archive_filename = os.path.join(archive_dir, archive_filename)
            print "Adding %s as %s" % (absolute_filename, archive_filename)
            if archive_type == 'tar.gz':
                archive.add(absolute_filename, archive_filename)
            else:
                archive.write(absolute_filename, archive_filename,
                                                          zipfile.ZIP_DEFLATED)
    archive.close()
    print "Created: ", archive_name


class tee(object):
    """Class that implements stdout redirection to both file and screen"""

    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self

    def close(self):
        if self.stdout is not None:
            sys.stdout = self.stdout
            self.stdout = None
        if self.file is not None:
            self.file.close()
            self.file = None

    def write(self, data):
        data = data.replace("\r", "")
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()

    def __del__(self):
        self.close()
