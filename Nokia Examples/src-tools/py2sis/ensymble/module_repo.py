#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# module_repo.py - Ensymble command line tool, py2sis command
# Copyright (c) 2009 Nokia Corporation
#
# This file is part of Ensymble developer utilities for Symbian OS(TM).
#
# Ensymble is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ensymble is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ensymble; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
##############################################################################

import sys
import os
import shutil
import modulefinder

module_repo_dir = os.path.abspath('module-repo')
std_modules_dir = os.path.join(module_repo_dir, 'standard-modules')
dev_modules_dir = os.path.join(module_repo_dir, 'dev-modules')

standard_module_dependency = {}
prefix = ""
debug_log = None

# PyS60 supported modules, part of PyS60 base runtime
std_base_module = 'base'
# PyS60 supported modules, not part of base runtime
std_repo_module = 'repo'
# Standard Python modules, not supported by PyS60
std_excluded_module = 'excluded'
# Modules added externally
dev_repo_module = 'dev'
# Unknown modules
unknown_module = 'unknown'

resolved_modules = {std_repo_module: [],
                    dev_repo_module: []}

debug = False
ignore_missing_deps = False
error_count = 0

module_lookup_file = os.path.abspath(os.path.join("module-repo", "dev-modules",
                                                  "module_search_path.cfg"))
appdir = ''
extrasdir = ''
pys60_extension_modules = ['appuifw',
'e32calendar',
'camera',
'contacts',
'e32',
'e32db',
'glcanvas',
'gles',
'globalui',
'gps',
'graphics',
'inbox',
'keycapture',
'location',
'logs',
'messaging',
'audio',
'sensor',
'btsocket',
'sysinfo',
'telephone',
'topwindow',
'scriptext']


def debug_print(msg, print_anyways=False):
    if debug or print_anyways:
        print str(msg)
    debug_log.write(str(msg) + '\n')


def get_module_type(module):
    try:
        # Check if it has a entry in standard modules dependency list
        return standard_module_dependency[module]['type']
    except:
        try:
            # Get the base module, by splitting on '.'
            module = module.split('.')[0]
        except:
            pass
        else:
            try:
                return standard_module_dependency[module]['type']
            except:
                pass

    # Is it a dev module ?
    module_path = os.path.join(dev_modules_dir, module)
    if os.path.isdir(module_path):
        return dev_repo_module

    # unknown module
    return unknown_module


def get_dev_modules():
    dev_modules = []
    for mod in os.listdir(dev_modules_dir):
        if os.path.isdir(os.path.join(dev_modules_dir, mod)):
            dev_modules.append(mod)
    return dev_modules


def find_in_all_devmodules(module):
    dev_modules = get_dev_modules()

    mod_pyd_name = prefix + module + '.pyd'
    found_dev_mod = ''
    for dep_mod in dev_modules:
        mod_path = os.path.join(dev_modules_dir, dep_mod)
        if os.path.isfile(os.path.join(mod_path, module + '.py')) or\
           os.path.isfile(os.path.join(mod_path, module + '.pyc')) or\
           os.path.isfile(os.path.join(mod_path, module + '.pyo')) or\
           os.path.isfile(os.path.join(mod_path, mod_pyd_name)) or\
           os.path.isdir(os.path.join(mod_path, module)):
            found_dev_mod = dep_mod
            break
    return found_dev_mod


def add_to_resolved_std_repo(modules):
    for mod in modules:
        module_type = get_module_type(mod)
        if module_type == std_base_module or \
                                            module_type == std_excluded_module:
            debug_print('Excluding: ' + mod +' module_type:' + \
                                                                   module_type)
        elif mod not in resolved_modules[std_repo_module]:
            debug_print('* Including: ' + mod +' module_type:' + module_type)
            resolved_modules[std_repo_module].append(mod)


def resolve_unresolved_dep(unresolved_dep_mods):

    global resolved_modules
    global error_count
    processed_modules = []

    debug_print('In resolve_unresolved_dep now:' + str(unresolved_dep_mods))
    while(len(unresolved_dep_mods)):
        current_module = unresolved_dep_mods.pop()
        module_type = get_module_type(current_module)
        debug_print('mod: %s : type: %s' %(current_module, module_type))

        processed_modules.append(current_module)

        if module_type == unknown_module:
            # Unknown module, search in dev modules
            dev_mod = find_in_all_devmodules(current_module)
            if dev_mod != '' and dev_mod not in processed_modules and \
                                 dev_mod not in unresolved_dep_mods:
                debug_print("Found '%s' in '%s'" % (current_module, dev_mod))
                unresolved_dep_mods.append(dev_mod)
            continue
        elif module_type == std_base_module or \
                                    module_type == std_excluded_module:
            debug_print('excluding: ' + current_module + \
                                        ' module type: ' + module_type)
            continue
        elif module_type == std_repo_module:
            add_to_resolved_std_repo([current_module])
            add_to_resolved_std_repo(standard_module_dependency[\
                                                       current_module]['deps'])
            continue

        # If we are here then, it should be a dev-module
        try:
            module_dir = current_module.split('.')[0]
        except:
            module_dir = current_module

        module_path = os.path.join(dev_modules_dir, module_dir)
        mod_config_file = os.path.join(module_path, 'module_config.cfg')
        try:
            module_config = eval(open(mod_config_file, 'rU').read())
        except:
            raise RuntimeError('Error reading config file of dev-module: '
                                                             + current_module)
        if module_config['type'] == 'base':
            debug_print('excluding: ' + current_module + \
                                      ' module type: ' + module_config['type'])
            continue

        # Read the module_config file of this module and validate the
        # mentioned dependencies.
        mod_deps_config = module_config['deps']
        for mod in mod_deps_config:
            mod_type = get_module_type(mod)
            if mod_type == unknown_module:
                debug_print("Unknown dependency: '%s' in '%s'" %\
                                                        (mod, mod_config_file))
            if mod_type == std_base_module:
                mod_deps_config.remove(mod)
                debug_print('removed ' + mod)
                continue
            if mod_type == std_repo_module:
                add_to_resolved_std_repo([current_module])
                add_to_resolved_std_repo(standard_module_dependency[\
                                                    current_module]['deps'])
                mod_deps_config.remove(mod)
                debug_print('removed ' + mod)
                continue
        # Now scan the module to auto-find the dependencies
        module_resolved_deps, module_unresolved_deps = \
                                              find_dep_modules(module_path)
        add_to_resolved_std_repo(module_resolved_deps)

        # The unresolved dependencies should be present in the current
        # dev-modules or in one of the modules in its deps list.
        for mod in module_unresolved_deps:
            if get_module_type(mod) == unknown_module:
                found_mod = find_in_all_devmodules(mod)
                if found_mod == '':
                    if ignore_missing_deps:
                        # If this flag is set then print the missing
                        # dependencies as warnings else print them as errors
                        debug_print(("WARNING: Dependent module '%s' not " +\
                                     "found") % mod, print_anyways=True)
                        continue
                    else:
                        error_count += 1
                        debug_print("ERROR: Dependent module '%s' not found" %
                                    mod, print_anyways=True)
                        continue
                else:
                    debug_print("Found '%s' in '%s'" %(mod, found_mod))
                    mod_deps_config.append(found_mod)
            elif mod not in resolved_modules[std_repo_module] and \
                 mod not in resolved_modules[dev_repo_module] and \
                 mod not in processed_modules:
                    unresolved_dep_mods.append(mod)

        for m in mod_deps_config:
            if m not in resolved_modules[std_repo_module] and \
               m not in resolved_modules[dev_repo_module] and \
               m not in processed_modules:
                unresolved_dep_mods.append(m)

        debug_print('including:' + str(current_module))
        if current_module not in resolved_modules[dev_repo_module]:
            resolved_modules[dev_repo_module].append(current_module)


def get_py_files(arg, dirname, files):
    for f in files:
        entry = os.path.join(dirname, f)
        if os.path.isdir(entry) or not f.endswith('.py'):
            continue
        arg.append(entry)


def find_dep_modules(src):
    dep_mods = []
    unresolved_dep_mods = []
    py_files = []

    if os.path.isdir(src):
        os.path.walk(src, get_py_files, py_files)
    else:
        py_files.append(src)

    for f in py_files:
        mf = modulefinder.ModuleFinder(path=[std_modules_dir])
        mf.run_script(f)
        mod_list = []
        for mod in mf.modules.iteritems():
            mod_list.append(mod[0])

        dep_mods = list(set(dep_mods + mod_list))
        unresolved_dep_mods = list(set(unresolved_dep_mods + mf.any_missing()))

    return (dep_mods, unresolved_dep_mods)


def init_module_repo():
    global standard_module_dependency
    global prefix

    std_deps_file = os.path.join(std_modules_dir, 'module_dependency.cfg')

    try:
        standard_module_dependency = eval(open(std_deps_file, 'rU').read())
    except:
        raise RuntimeError('Reading of module-repo config file failed:',
                                                                 std_deps_file)
    try:
        prefix = open(os.path.join("templates", "prefix_data.txt"), "rU").read()
    except:
        raise RuntimeError('Getting prefix failed')


def get_dependency_list(src, extra_modules):
    '''Process the source and return list of complete set of dependencies.'''

    init_module_repo()

    try:
        extra_modules = extra_modules.split(',')
    except:
        extra_modules = []

    dep_mods, unresolved_dep_mods = find_dep_modules(src)
    add_to_resolved_std_repo(dep_mods)
    resolve_unresolved_dep(list(set(unresolved_dep_mods + extra_modules)))

    debug_print("Final dependency list: " + str(resolved_modules))
    return resolved_modules


def copy_dep_file(dep_file, appdir):
    global extrasdir
    if dep_file.endswith('.pyd'):
        # Move the pyds to extrasdir\sys\bin. If the
        # application does not have extrasdir, then create it
        # and set the 'extrasdir' ensymble option.
        if extrasdir is None:
            extrasdir_path = os.path.join(appdir,
                                    "extras_dir", "sys", "bin")
            if not os.path.exists(extrasdir_path):
                os.makedirs(extrasdir_path)
                extrasdir = 'extras_dir'
        else:
            extrasdir_path = os.path.join(appdir, extrasdir,
                                          "sys", "bin")
            if not os.path.exists(extrasdir_path):
                os.makedirs(extrasdir_path)
        debug_print("Copying '%s' to '%s' " % (dep_file, extrasdir_path))
        shutil.copy(dep_file, extrasdir_path)
    else:
        # It is not a pyd. Copy to application private dir.
        if os.path.basename(dep_file) != 'module_config.cfg':
            debug_print("Copying '%s' to '%s' " % (dep_file, appdir))
            shutil.copy(dep_file, appdir)


def process_dependent_modules(dep_module_paths):

    def split_and_strip(dep_module_path, repo_dir):
        return dep_module_path.split(repo_dir)[-1].lstrip(os.sep)

    all_dep_mod_paths = []
    all_dep_mod_paths.extend(dep_module_paths['std'])
    all_dep_mod_paths.extend(dep_module_paths['dev'])

    for dep_module_path in all_dep_mod_paths:
        # relative_dir_path will have the path after the module-repo dir -
        # xxx\\module-repo\\standard-modules\\<relative_dir_path>\\<files> or
        # xxx\\module-repo\\dev-modules\\<module>\\<relative_dir_path>\\<files>
        if dep_module_path in dep_module_paths['std']:
            module_repo_dir = std_modules_dir
            relative_dir_path = os.path.dirname(
                             split_and_strip(dep_module_path, module_repo_dir))
        else:
            module_repo_dir = dev_modules_dir
            relative_dir_path = \
                              split_and_strip(dep_module_path, module_repo_dir)
            # Remove the topmost dir as this directory is just a container for
            # dev modules and it should not be created on the phone
            relative_dir_path = os.path.dirname(
                                        relative_dir_path.split(os.sep, 1)[-1])

        debug_print("Relative dir path :" + relative_dir_path)
        # Create the directory hierarchy rooted at appdir, if it doesn't exist.
        if not os.path.exists(os.path.join(appdir, relative_dir_path)):
            debug_print("Create dir" + os.path.join(appdir, relative_dir_path))
            os.makedirs(os.path.join(appdir, relative_dir_path))

        # If the module is a directory, then we loop through all the files at
        # the top level of that directory and then call copy_dep_file to handle
        # the copying of PYDs and .py files.
        if os.path.isdir(dep_module_path):
            debug_print("Dep module '%s' is a Directory" % dep_module_path)

            # if the path contains 'standard-modules' then we directly copy the
            # directory to appdir, else we parse the directory for PYDs and sub
            # directories and then copy them to different directories.
            if dep_module_path in dep_module_paths['std']:
                dest_path = os.path.join(appdir, relative_dir_path,
                                         os.path.basename(dep_module_path))
                if os.path.exists(dest_path):
                    debug_print("Deleting directory: " + dest_path)
                    shutil.rmtree(dest_path)
                debug_print("Copying directory as-is -'%s' to '%s'" % \
                            (dep_module_path, dest_path))
                shutil.copytree(dep_module_path, dest_path)
            else:
                for dep_filename in os.listdir(dep_module_path):
                    dep_file_path = os.path.join(dep_module_path, dep_filename)
                    if os.path.isdir(dep_file_path):
                        # Copy the module's sub-directory as-is
                        dest_path = os.path.join(appdir,
                                             relative_dir_path, dep_filename)
                        if os.path.exists(dest_path):
                            debug_print("Deleting directory: " + dest_path)
                            shutil.rmtree(dest_path)
                        debug_print("Copying directory as-is -'%s' to '%s'" % \
                            (dep_file_path, dest_path))
                        shutil.copytree(dep_file_path, dest_path)
                    else:
                        # PYDs should go to extrasdir rooted at appdir, whereas
                        # .py should go to appdir + relative_dir_path
                        if not dep_file_path.endswith('.pyd'):
                            copy_dep_file(dep_file_path, os.path.join(appdir,
                                   relative_dir_path,
                                   os.path.basename(dep_file_path)))
                        else:
                            copy_dep_file(dep_file_path, appdir)
        else:
            debug_print("Dependent module '%s' is a file" % dep_module_path)
            # If the file is a pyd then we need to move it to extrasdir rooted
            # at appdir, else move it to appdir + relative_dir_path
            if not dep_module_path.endswith('.pyd'):
                copy_dep_file(dep_module_path, os.path.join(appdir,
                            split_and_strip(dep_module_path, module_repo_dir)))
            else:
                copy_dep_file(dep_module_path, appdir)


def handle_dotted_dependencies(module_name, module_repo_dir):
    # module_name is split into <module_root><module_dirs><module_leaf>
    # For a module 'a.b' - module_root = a, module_dirs = '', module_leaf = b
    # for 'a.b.c.d' - module_root = a, module_dirs = b.c and module_leaf = d
    # Also convert all '.' to os.sep('\\' on windows) in module_dirs
    module_root, module_path = module_name.split('.', 1)
    if module_path.find('.') != -1:
        module_dirs, module_leaf = module_path.rsplit('.', 1)
        module_dirs = module_dirs.replace('.', os.sep)
    else:
        module_dirs = ''
        module_leaf = module_path
    debug_print("module_root-module_dirs-module_leaf : " + module_root + "-" +\
              module_dirs + "-" + module_leaf)
    # List the contents of the directory one level above module_leaf, check if
    # module_leaf exists. If there are both .py and .py[c|o], then the .py file
    # will be picked up.
    sub_dir_contents = os.listdir(os.path.join(module_repo_dir, module_root,
                                               module_dirs))
    debug_print("Module dir contains :" + str(sub_dir_contents))

    if module_leaf.lower() in \
                           [(os.path.basename(leaf_node).split('.')[0]).lower()
                            for leaf_node in sub_dir_contents]:
        debug_print("Found sub-module '%s' in module directory" % module_leaf)

        # Extract the full path of module_leaf by filtering out everything in
        # the sub_module dir that does not match module_leaf
        sub_module_paths = [os.path.join(module_repo_dir, module_root,
                                         module_dirs, filename)
                       for filename in os.listdir(os.path.join(module_repo_dir,
                                                   module_root, module_dirs))]
        for sub_module_path in sub_module_paths:
            if os.path.basename(sub_module_path).split('.')[0] == module_leaf:
                break
        debug_print("Returning path to leaf node - " + sub_module_path)

        return sub_module_path


def search_module(modules):
    global error_count
    dep_module_paths = {'std': [], 'dev': []}
    if not os.path.exists(dev_modules_dir) or \
                                           not os.path.exists(std_modules_dir):
        raise RuntimeError("Module Dependency folder does not exist")

    std_module_paths = [os.path.join(std_modules_dir, filename) \
                        for filename in os.listdir(std_modules_dir)]
    std_module_names = [(os.path.basename(
                        std_module).split('.')[0].split(prefix)[-1]).lower()
                                         for std_module in std_module_paths]
    # The module_lookup_file contains a list of paths that should be scanned
    # by the packaging tool when searching for a module before searching the
    # module-repo.
    try:
        module_lookup_paths = eval(open(module_lookup_file, 'rU').read())
    except IOError:
        module_lookup_paths = []
        pass
    else:
        debug_print("Custom lookup paths are :" + str(module_lookup_paths))

    for module_name in modules[std_repo_module]:
        dotted_module = False
        # For a module named 'a.b.c.d', we split it into 'a' and 'b.c.d' to
        # check if 'a' is present in either std-modules or dev-modules. If
        # found, we then call handle_dotted_dependencies to find and return
        # the path of 'b.c.d' which is then added to dep_module_paths['std'].
        if module_name.find('.') != -1:
            module_name, module_leaf = module_name.split('.', 1)
            dotted_module = True
        # Search in standard-modules repo directory. Remove the file extension
        # and check if the module is present
        if module_name.lower() in std_module_names:
            debug_print("Dep module %s found in Std. Library" % module_name)
            if dotted_module:
                module_path = handle_dotted_dependencies(module_name + '.' +
                                                  module_leaf, std_modules_dir)
                if module_path == None:
                    debug_print("WARNING: Module "+ \
                     "'%s' not found in standard module repo" % (module_name +\
                     '.' + module_leaf), print_anyways=True)
                    continue
                debug_print("Adding '%s' to dep_module_paths['std']" %
                            module_path)
                dep_module_paths['std'].append(module_path)
            else:
                # If it is a file then extract the full filename from the list
                # std_module_paths and add it to dep_module_paths['std']
                if not os.path.isdir(os.path.join(std_modules_dir,
                                                  module_name)):
                    for std_module_path in std_module_paths:
                        if os.path.basename(
                           std_module_path).split('.')[0].split(prefix)[-1] ==\
                                                                   module_name:
                            break
                    dep_module_paths['std'].append(std_module_path)
                else:
                    dep_module_paths['std'].append(
                                    os.path.join(std_modules_dir, module_name))
        elif ignore_missing_deps:
            # If this flag is set then print the missing dependencies as
            # warnings else print them as errors
            debug_print("WARNING: Dependent module '%s' not found" %
                            module_name, print_anyways=True)
            continue
        else:
            error_count += 1
            debug_print("ERROR: Dependent module '%s' not found" %
                        module_name, print_anyways=True)
            continue

    for module_name in modules[dev_repo_module]:
        # Dotted dependencies are ignored and the entire dev module is
        # added to dep_module_paths['dev'].
        # If the module is a third party dev module then we check the
        # custom lookup path
        if module_name not in pys60_extension_modules:
            module_found = False
            if module_lookup_paths:
                for module_lookup_path in module_lookup_paths:
                    if os.path.exists(os.path.join(module_lookup_path,
                                      prefix + module_name + '.pyd')):
                        debug_print("Module found in custom lookup path " +
                                    module_lookup_path)
                        copy_dep_file(os.path.join(module_lookup_path,
                                      prefix + module_name + '.pyd'),
                                      appdir)
                        module_found = True
                        break
            if module_found:
                continue
        debug_print("Processing dev module : " + module_name)

        debug_print("Adding '%s' to dep_module_paths['dev']" %
                    os.path.join(dev_modules_dir, module_name))
        dep_module_paths['dev'].append(
                                    os.path.join(dev_modules_dir, module_name))

    return dep_module_paths
