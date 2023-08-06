# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import getopt
import os
import shutil
import stat

from pathlib import Path
from toybox.__about__ import __version__
from toybox.boxfile import Boxfile
from toybox.exceptions import ArgumentError
from toybox.version import Version


class Toybox:
    """A Lua and C dependency management system for the Playdate SDK."""

    def __init__(self, args):
        """Initialise toybox based on user configuration."""

        self.box_file = None
        self.dependencies = []
        self.only_update = None
        self.installed_a_local_toybox = False

        try:
            # -- Gather the arguments
            opts, other_arguments = getopt.getopt(args, '')

            if len(other_arguments) == 0:
                raise SyntaxError('Expected a command!  Maybe start with `toybox help`?')

            number_of_arguments = len(other_arguments)

            self.command = None
            self.argument = None
            self.second_argument = None

            i = 0
            argument = other_arguments[i]
            if len(argument):
                self.command = argument
            i += 1

            if i != number_of_arguments:
                argument = other_arguments[i]
                if len(argument):
                    self.argument = other_arguments[i]
                i += 1
                if i != number_of_arguments:
                    argument = other_arguments[i]
                    if len(argument):
                        self.second_argument = other_arguments[i]
                        i += 1

            if i != number_of_arguments:
                raise SyntaxError('Too many commands on command line.')

        except getopt.GetoptError:
            raise ArgumentError('Error reading arguments.')

    def main(self):
        switch = {
            'help': Toybox.printUsage,
            'version': Toybox.printVersion,
            'info': self.printInfo,
            'add': self.addDependency,
            'remove': self.removeDependency,
            'update': self.update,
            'check': self.checkForUpdates,
            'setimport': self.setLuaImport
        }

        if self.command is None:
            print('No command found.\n')
            self.printUsage()
            return

        if self.command not in switch:
            raise ArgumentError('Unknow command \'' + self.command + '\'.')

        switch.get(self.command)()

    def printInfo(self, folder=None):
        if folder is None:
            print('Resolving dependencies...')
            box_file_for_folder = Boxfile(Toybox.boxfileFolder())

            self.box_file = box_file_for_folder

            if self.box_file is None or len(self.box_file.dependencies) == 0:
                print('Boxfile is empty.')
                return
        else:
            box_file_for_folder = Boxfile(folder)

        if box_file_for_folder is None:
            return

        for dep in box_file_for_folder.dependencies:
            info_string = '       - ' + str(dep) + ' -> '

            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            dep_folder_exists = os.path.exists(dep_folder)

            version_installed_as_string = self.box_file.maybeInstalledVersionAsStringForDependency(dep)
            if dep_folder_exists and version_installed_as_string:
                info_string += version_installed_as_string
            elif dep_folder_exists:
                info_string += 'Unknown version.'
            else:
                info_string += 'Not installed.'

            print(info_string)

            if dep_folder_exists:
                self.printInfo(dep_folder)

    def checkForUpdates(self, folder=None):
        if folder is None:
            print('Resolving dependencies...')
            box_file_for_folder = Boxfile(Toybox.boxfileFolder())

            self.box_file = box_file_for_folder

            if self.box_file is None or len(box_file_for_folder.dependencies) == 0:
                print('Boxfile is empty.')
                return
        else:
            box_file_for_folder = Boxfile(folder)

        if box_file_for_folder is None:
            return

        something_needs_updating = False

        for dep in box_file_for_folder.dependencies:
            version_available = dep.resolveVersion()
            if version_available is None:
                continue

            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            if os.path.exists(dep_folder) is False:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
                continue

            version_installed = None
            version_installed_as_string = self.box_file.maybeInstalledVersionAsStringForDependency(dep)
            if version_installed_as_string is None:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
            else:
                version_installed = Version(version_installed_as_string)
                if version_installed != version_available:
                    if version_available.isLocal():
                        print('       - ' + str(dep) + ' -> Local version not installed.')
                    elif version_available.isBranch():
                        print('       - ' + str(dep) + ' -> A more recent commit is available.')
                    else:
                        print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')

                    something_needs_updating = True

            something_needs_updating |= self.checkForUpdates(dep_folder)

        if folder is None and something_needs_updating is False:
            print('You\'re all up to date!!')

        return something_needs_updating

    def addDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'add\' command.')

        self.box_file = Boxfile(Toybox.boxfileFolder())
        self.box_file.addDependencyWithURL(self.argument, self.second_argument)
        self.box_file.saveIfModified()

        print('Added a dependency for \'' + self.argument + '\' at \'' + self.box_file.dependencies[0].originalVersionsAsString() + '\'.')

    def removeDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'remove\' command.')

        self.box_file = Boxfile(Toybox.boxfileFolder())
        self.box_file.removeDependencyWithURLIn(self.argument, Toybox.toyboxesFolder())
        self.box_file.saveIfModified()

        print('Removed a dependency for \'' + self.argument + '\'.')

    def setLuaImport(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'setimport\' command.')

        self.box_file = Boxfile(Toybox.boxfileFolder())
        self.box_file.setLuaImport(self.argument)
        self.box_file.saveIfModified()

        print('Set Lua import file to \'' + self.argument + '\' for this project.')

    def installDependency(self, dep, no_copying=False):
        dependency_is_new = True

        for other_dep in self.dependencies:
            if other_dep.url == dep.url:
                other_dep.versions += dep.versions
                dep = other_dep
                dependency_is_new = False

        should_copy = (self.only_update is not None) and (self.only_update != dep.repo_name) and Toybox.dependencyExistsInBackup(dep)

        if (no_copying is False) and should_copy:
            print('Copying \'' + str(dep) + '.')
            self.copyDependencyFromBackup(dep)
        else:
            version = dep.installIn(Toybox.toyboxesFolder())

            if version is not None:
                installed_version_string = version.original_version

                if version.isBranch():
                    commit_hash = dep.git.getLatestCommitHashForBranch(version.original_version)
                    if commit_hash is None:
                        raise RuntimeError('Could not find latest commit hash for branch ' + version.original_version + '.')

                    installed_version_string += '@' + commit_hash
                else:

                    if version.isLocal():
                        self.installed_a_local_toybox = True

                info_string = 'Installed \'' + str(dep) + '\' -> ' + str(version)

                if should_copy and no_copying:
                    info_string += ' (force-installed by another dependency)'

                print(info_string + '.')

                self.box_file.setInstalledVersionStringForDependency(dep, installed_version_string)

            no_copying = True

        dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
        dep_box_file = Boxfile(dep_folder)
        for child_dep in dep_box_file.dependencies:
            self.installDependency(child_dep, no_copying)

        if dependency_is_new:
            self.dependencies.append(dep)

    def generateLuaIncludeFile(self):
        lua_includes = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())

            maybe_lua_include_path = Boxfile(dep_folder).maybeLuaImportFile()
            if maybe_lua_include_path is not None and maybe_lua_include_path.endswith('.lua'):
                maybe_lua_include_path = maybe_lua_include_path[:-4]

            lua_include_path = Toybox.findLuaIncludeFileIn(dep_folder, dep.repo_name, maybe_lua_include_path)

            if lua_include_path is not None:
                lua_includes.append(os.path.join(dep.subFolder(), lua_include_path))

        if len(lua_includes) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.lua'), 'w') as out_file:
            out_file.write('--\n')
            out_file.write('--  toyboxes.lua - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('--\n')
            out_file.write('\n')

            for lua_include in lua_includes:
                out_file.write('import \'' + lua_include + '.lua\'\n')

            out_file.close()

    def generateMakefile(self):
        makefiles = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            makefile_path = Toybox.findMakefileIn(dep_folder, dep.repo_name)
            if makefile_path is not None:
                makefiles.append([os.path.join(dep.subFolder(), makefile_path), dep.repo_name.upper()])

        if len(makefiles) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.mk'), 'w') as out_file:
            out_file.write('#\n')
            out_file.write('#  toyboxes.mk - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('#\n')
            out_file.write('\n')
            out_file.write('_RELATIVE_FILE_PATH := $(lastword $(MAKEFILE_LIST))\n')
            out_file.write('_RELATIVE_DIR := $(subst /$(notdir $(_RELATIVE_FILE_PATH)),,$(_RELATIVE_FILE_PATH))\n')
            out_file.write('\n')
            out_file.write('uniq = $(if $1,$(firstword $1) $(call uniq,$(filter-out $(firstword $1),$1)))\n')
            out_file.write('UINCDIR := $(call uniq, $(UINCDIR) $(_RELATIVE_DIR))\n')
            out_file.write('\n')

            for makefile in makefiles:
                out_file.write(makefile[1] + '_MAKEFILE := $(_RELATIVE_DIR)/' + makefile[0] + '\n')

            out_file.write('\n')

            for makefile in makefiles:
                out_file.write('include $(' + makefile[1] + '_MAKEFILE)\n')

            out_file.close()

    def generateIncludeFile(self):
        include_files = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            include_file_path = Toybox.findIncludeFileIn(dep_folder, dep.repo_name)
            if include_file_path is not None:
                include_files.append([os.path.join(dep.subFolder(), include_file_path), dep.repo_name])

        if len(include_files) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.h'), 'w') as out_file:
            out_file.write('//\n')
            out_file.write('//  toyboxes.h - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('//\n')
            out_file.write('\n')

            for include in include_files:
                out_file.write('#include "' + include[0] + '"\n')

            out_file.write('\n')

            prefix = ''
            out_file.write('#define REGISTER_TOYBOXES(pd)')
            for include in include_files:
                out_file.write(prefix + '   register_' + include[1] + '(pd);')
                prefix = ' \\\n                             '

            out_file.write('\n')

            out_file.close()

    def update(self):
        if self.argument is not None:
            self.only_update = self.argument

        Toybox.backupToyboxes()

        try:
            self.box_file = Boxfile(Toybox.boxfileFolder())
            for dep in self.box_file.dependencies:
                self.installDependency(dep)

            if os.path.exists(Toybox.toyboxesFolder()):
                Toybox.generateReadMeFile()
                self.generateLuaIncludeFile()
                self.generateMakefile()
                self.generateIncludeFile()

            self.box_file.saveIfModified()

        except Exception:
            Toybox.restoreToyboxesBackup()
            raise

        Toybox.deleteToyboxesBackup()

        Toybox.restorePreCommitFileIfAny()

        if self.installed_a_local_toybox:
            Toybox.generatePreCommitFile()

        print('Finished.')

    @classmethod
    def printVersion(cls):
        print('🧸 toybox.py v' + __version__)

    @classmethod
    def printUsage(cls):
        Toybox.printVersion()
        print('Usage:')
        print('    toybox help                   - Show a help message.')
        print('    toybox version                - Get the Toybox version.')
        print('    toybox info                   - Describe your dependency set.')
        print('    toybox add <url>              - Add a new dependency.')
        print('    toybox add <url> <version>    - Add a new dependency with a specific version.')
        print('    toybox remove <url>           - Remove a dependency.')
        print('    toybox update                 - Update all the dependencies.')
        print('    toybox update <dependency>    - Update a single dependency.')
        print('    toybox check                  - Check for updates.')
        print('    toybox setimport <lua_file>   - Set the name of the lua file to import from this project.')

    @classmethod
    def boxfileFolder(cls):
        return os.getcwd()

    @classmethod
    def toyboxesFolder(cls):
        return os.path.join(Toybox.boxfileFolder(), 'toyboxes')

    @classmethod
    def toyboxesBackupFolder(cls):
        return Toybox.toyboxesFolder() + '.backup'

    @classmethod
    def backupToyboxes(cls):
        toyboxes_folder = Toybox.toyboxesFolder()
        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_folder):
            shutil.move(toyboxes_folder, toyboxes_backup_folder)

    @classmethod
    def restoreToyboxesBackup(cls):
        toyboxes_folder = Toybox.toyboxesFolder()
        if os.path.exists(toyboxes_folder):
            shutil.rmtree(toyboxes_folder)

        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_backup_folder):
            shutil.move(toyboxes_backup_folder, toyboxes_folder)

    @classmethod
    def dependencyExistsInBackup(cls, dep):
        return os.path.exists(os.path.join(Toybox.toyboxesBackupFolder(), dep.subFolder()))

    @classmethod
    def copyDependencyFromBackup(cls, dep):
        source_path = os.path.join(Toybox.toyboxesBackupFolder(), dep.subFolder())
        if not os.path.exists(source_path):
            raise RuntimeError('Backup from ' + dep.subFolder() + ' cannot be found.')

        shutil.copytree(source_path, os.path.join(Toybox.toyboxesFolder(), dep.subFolder()))

    @classmethod
    def deleteToyboxesBackup(cls):
        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_backup_folder):
            shutil.rmtree(toyboxes_backup_folder)

    @classmethod
    def lookInFolderFor(cls, folder, wildcard):
        # -- We use this here instead of just simply os.path.exists()
        # -- because we want the test to be case-sensitive on all platforms,
        # -- so we list what the match are and let glob give us the paths.
        paths_found = []
        looking_in = Path(folder)

        for p in looking_in.glob(wildcard):
            as_string = str(p)
            if len(as_string) > 4:
                as_string = as_string[len(folder) + 1:-4]
                paths_found.append(as_string)

        return paths_found

    @classmethod
    def findLuaIncludeFileIn(cls, folder, repo_name, maybe_additional_path):
        if maybe_additional_path is not None:
            filename = maybe_additional_path + '.lua'
            paths_found = Toybox.lookInFolderFor(folder, filename)
            if len(paths_found) != 0:
                return maybe_additional_path

            print('Warning: Could not find file \'' + filename + '\' to import in \'' + repo_name + '\'.')

        paths_found = Toybox.lookInFolderFor(folder, '**/import.lua')
        paths_found += Toybox.lookInFolderFor(folder, '**/' + repo_name + '.lua')

        correct_names = [repo_name,
                         'import',
                         os.path.join('Source', repo_name),
                         os.path.join('Source', 'import'),
                         os.path.join('source', repo_name),
                         os.path.join('source', 'import')]

        for path_found in paths_found:
            for correct_name in correct_names:
                if path_found == correct_name:
                    return path_found

        return None

    @classmethod
    def findMakefileIn(cls, folder, repo_name):
        potential_names = [repo_name + '.mk',
                           'Makefile',
                           'Makefile.mk']
        for name in potential_names:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return name

        return None

    @classmethod
    def findIncludeFileIn(cls, folder, repo_name):
        potential_names = [os.path.join(repo_name, repo_name + '.h'),
                           os.path.join(repo_name, 'include.h')]
        for name in potential_names:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return name

        return None

    @classmethod
    def generateReadMeFile(cls):
        with open(os.path.join(Toybox.toyboxesFolder(), 'README.md'), 'w') as out_file:
            out_file.write('# toyboxes\n')
            out_file.write('\n')
            out_file.write('This folder contains files auto-generated and managed by [**toybox.py**](https://toyboxpy.io).\n')
            out_file.write('\n')
            out_file.write('**!!! DO NOT MODIFY OR PLACE ANYTHING IN THIS FOLDER !!!**\n')
            out_file.write('\n')
            out_file.write('Please [install](https://github.com/toyboxpy/toybox.py#installing) **toybox.py** in order to modify or update the content of this folder.\n')

    @classmethod
    def preCommitFilePath(cls):
        return os.path.join('.git', 'hooks', 'pre-commit')

    @classmethod
    def preCommitFileBackupPath(cls):
        return Toybox.preCommitFilePath() + '.toyboxes_backup'

    @classmethod
    def preCommitFileNoBackupPath(cls):
        return Toybox.preCommitFilePath() + '.toyboxes_no_backup'

    @classmethod
    def generatePreCommitFile(cls):
        if not os.path.exists('.git'):
            return

        pre_commit_file_path = Toybox.preCommitFilePath()
        if os.path.exists(pre_commit_file_path):
            shutil.move(pre_commit_file_path, Toybox.preCommitFilePathBackup())
        else:
            with open(Toybox.preCommitFileNoBackupPath(), 'w') as out_file:
                out_file.write('#!/bin/sh\n')
                out_file.write('#\n')
                out_file.write('# This file is generated by toybox.py to remember there was no backup to be restored.\n')
                out_file.write('\n')

        with open(pre_commit_file_path, 'w') as out_file:
            out_file.write('#!/bin/sh\n')
            out_file.write('#\n')
            out_file.write('# This file is generated by toybox.py to prevent committing local toyboxes.\n')
            out_file.write('\n')
            out_file.write('echo "You shouldn\'t commit when you have \'local\' toyboxes in your repo."\n')
            out_file.write('exit 1\n')

        if os.path.exists(pre_commit_file_path):
            os.chmod(pre_commit_file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    @classmethod
    def restorePreCommitFileIfAny(cls):
        if not os.path.exists('.git'):
            return

        pre_commit_file_path = Toybox.preCommitFilePath()
        pre_commit_file_backup_path = Toybox.preCommitFileBackupPath()
        pre_commit_file_no_backup_path = Toybox.preCommitFileNoBackupPath()

        if os.path.exists(pre_commit_file_no_backup_path):
            os.remove(pre_commit_file_no_backup_path)
            os.remove(pre_commit_file_path)
        elif os.path.exists(pre_commit_file_backup_path):
            os.remove(pre_commit_file_path)
            shutil.move(pre_commit_file_backup_path, pre_commit_file_path)
