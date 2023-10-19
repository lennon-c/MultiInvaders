# -*- coding: utf-8 -*-
"""
Script to package the game into an exe file using PyInstaller.
It creates also a 'Install.vbs' file outside of the packaged game folder.

By clicking on the 'Install.vbs', a shorcut to the game will be created
 in the computer of the user, which can be then copied in other location.


# pyinstaller creates two folders
    => dist  # the exe file is located here
    => build

# pyinstaller also populates the "[name].spec" file
based on the instructions passed in `pyinstall_bat`.


Workflow:
1) call pyinstall_bat()
    => which creates and runs the bat file `[name]_installer.bat` that
     is located in the script folder.

2) Manual check whether the installation worked

If one file, END!

If GUI is packaged in a folder, then:

3) Call CreateInstallFile() to create 'Install.vbs' in the dist folder

4) Zip to share: The zip file including the "install" file is saved in
    => [name].zip in the folder of the main script

5) Copy zip file in folder reserved for sharing

6) Copy and extract zip file in desktop for testing


"""
# %% IMPORTS and CONSTANTS

import os
import winshell
import shutil
from Constants import c

# Constants
# package path
path = c('root')
# name of the main script of the game
script = 'Main.py'
# image.ico to use as icon of the exe file
icon_file = os.path.join(c('images_path'), 'favicon.ico')
#
path_env = 'SET YOUR PATH TO ENV.'  # i.e `C:\Users\a_user\.virtualenvs\my_project`

# %% [PYINSTALLER]

def activate_env(path_env):
    r"""Return the full path to the activate.bat file.

    path_env: path to the environment
        i.e `C:\Users\a_user\.virtualenvs\my_project`.
    """
    activate = os.path.join(path_env, 'Scripts/activate.bat')
    return activate

def pyinstall_bat(
        script, path, path_env,
        onefile=False, windowed=True, name=None, icon_file=None,
        add_data=['images', 'sounds'], other=None,
        run=False, close=False
        ):
    r"""Create a batch file that packages a Python GUI into an `.exe` file.

    The function creates the batch file `[name]_installer.bat`,
    which is located in the same directory as the sript file.
    and which runs the PyInstaller to package the GUI.
    The function can also run the bat file if `run` is set to True.

    Args:
        script (str): The name of the main Python script (i.e. `Main.py`)
        path (str): The path where the main script.py is located.
        path_env (str): The path to the virtual environment.
            Example : `C:\\Users\\a_user\\.virtualenvs\\my_project`.
            this environment will be activated before running PyInstaller.
        onefile (bool, optional): Whether to create a single executable file
            (default is False).
        windowed (bool, optional): Whether to open window as pyinstaller runs
            (default is True).
        name (str, optional): The name of the packaged executable file
            (default is None, which uses the script's name).
        icon_file (str, optional): The path to the icon file
            to be used for the packaged executable (default is None).
        add_data (list[str], optional): A list of relative paths
            to additional data files or directories to include
            (default is ['images', 'sounds']).
        other (str, optional): Additional command-line options
            to pass to PyInstaller (default is None).
        run (bool, optional): Whether to run the generated batch file after
            it is created (default is False).
        close (bool, optional): Close the cmd window after the process
            finishes or fails (default is False).
    """
    if name is None:
        name = script.split('.')[0]

    script_path = os.path.join(path, script)

    # Setting command-line options
    _windowed = '--windowed' if windowed else ''
    _onefile = '--onefile' if onefile else ''
    _icon = f'--icon {icon_file}' if icon_file is not None else ''
    _name = f'--name {name}' if name is not None else ''
    _add_data = ''
    if add_data is not None:
        for file in add_data:
            current_path = os.path.join(path, file)
            _add_data = _add_data + f' --add-data="{current_path};./{file}"'

    _other = other if other else ''

    # Creating the batch file
    bat_file = os.path.join(path, f'{name}_installer.bat')
    with open(bat_file, 'w') as f:
        f.write('@echo off\n')
        f.write(f'call {activate_env(path_env)}{chr(10)}')
        cmd = f'{_windowed} {_onefile} {_icon} {_name} {_add_data} {_other}'
        f.write(f'call pyinstaller {cmd} "{script_path}"{chr(10)}')
        if close:
            f.write('exit')  # it closes in any case.

    with open(bat_file, 'r') as f:
        print(f.read())

    if run:
        os.startfile(bat_file)


# %% [SHORCUT]

def install_vbs():
    """Create an install.vbs file that runs the game."""
    name = c('name')
    print(f'{name=}')
    app = '.\\' + name + '\\' + f'{name}.exe'
    vbs_file = os.path.join('dist', 'Install.vbs')
    with open(vbs_file, 'w') as f:
        f.write('Set oShell = CreateObject("Wscript.Shell")\n')
        f.write('Dim strArgs\n')
        f.write(f'strArgs = "cmd /c {app}"{chr(10)}')
        f.write('oShell.Run strArgs, 0, false')

def create_shortcut( target, place='desktop', name=None, icon_file=None):
    """Create a shortcut (.lnk file) to a file or folder.

    Parameters:
    - target: str, path to the file or folder to create a shortcut to
    - place: str or path, optional, location to save the shortcut file (default is 'desktop')
    - name: str, optional, name for the shortcut file (default is the name of the target file without extension)
    - icon_file: str, optional, path to the icon file to use for the shortcut
    """
    if name is None:
        name = os.path.basename(target).split('.')[0] # file

    #### shortcut
    if place == 'desktop':
        where = winshell.desktop()
    else:
        where = place

    link_path = os.path.join(where, f'{name}.lnk')
    target_path = os.path.abspath(target)

    if os.path.exists(target_path):
        with winshell.shortcut(link_path) as shortcut:
            shortcut.path = target_path
            if icon_file is not None:
                shortcut.icon_location = icon_file,0
            shortcut.description = f"Shortcut to {name}"
            shortcut.working_directory = os.path.dirname(target_path)
    else:
        raise FileNotFoundError(f"Target file '{target_path}' does not exist")

def first_run_setup(root, splash):
    """Actions taking place when the game is run for the first time by the user.

    This function creates a shorcut in user's computer, the `config.txt` file
    and displays the splash window.
    The shorcut can be then moved by the user to a more convinient place.
    These actions take place only during the first run by the user.
    Thus, it is to be called only when the game runs from the executable.
    This function is meant to be called in the main.py of the game.

    Returns:
        True, if it is the first time that the game is run from the executable
        False, otherwise.
    """
    # Check if the game is running for the first time
    # by checking if the `config.txt` file exists.
    first_time = False
    config = os.path.join(root, 'config.txt')
    if not os.path.exists(config): # if it does not exist
        # => first_time = true
        first_time = True
        # => create a shortcut to the executable
        app = os.path.abspath(os.path.join(root, f'{c("name")}.exe'))
        icon_file = os.path.join(c('ico_path'), 'favicon.ico' )
        create_shortcut( app # target
                        , place = os.path.dirname(root) # one level up from exe file
                        , name  = c('name')
                        , icon_file =  icon_file)
        # = > create configuration file
        with open(config, 'w') as f:
            f.write(f'Shorcut already created in: {os.path.dirname(root)}')

        splash()
        # sys.exit() # did not work here, exits before splash is closed by the user
        return first_time


# %% [RUNNING - PACKAGING]
if (__name__ == '__main__'):


    working_directory = os.path.dirname(os.path.abspath("__file__"))
    sharing_path = os.path.join(working_directory, 'GameSharing')
    desktop_path = winshell.desktop()
    testing_path = os.path.join(desktop_path, 'Testing')


    def copy_zip_to(dst):
        """copy in a different location for testing or sharing.

        dst (str) : path to copy
        """
        home_path = os.path.dirname(os.path.abspath("__file__"))
        zip_file = os.path.join(home_path, f"{c('name')}.zip")

        if os.path.exists(zip_file):
            shutil.copy(zip_file ,dst)
            print(f'zip file copied to: {dst}')

        else:
            print('zip does not exist')

    """
    copy_zip_to(desktop_path)
    copy_zip_to(testing_path)
    copy_zip_to(sharing_path)
    """

    def unpacking_zip(location):
        """unpackage the zipped `exe` file and folders for testing."""
        from zipfile import ZipFile
        destination = os.path.join(location, c('name'))
        zip_file = os.path.join(location, f"{c('name')}.zip")

        with ZipFile(zip_file, 'r') as f:
            f.extractall(path=destination)

    """
    unpacking_zip(testing_path)
    """

    def del_installations():
        """Delete all information of past installers."""
        current_folder = os.path.dirname(os.path.abspath("__file__"))

        # folders to delete (ckeck first if they exist)
        folders = [x for x in ['dist', 'build'] if os.path.isdir(x)]

        # files to delete .spec, .bat, ,zip files
        extensions = ('.spec', '_installer.bat', '.zip')
        files = [x for x in os.listdir() if x.endswith(extensions)]

        # exit if no files or folders exist
        if len(folders) == 0 and len(files) == 0:  # no folders/files
            print('\nNo file/folder found to delete')
            return

        delete = input(
            f"Do you want to delete the following items?{chr(10)}{chr(10)}folders:{chr(10)}{chr(9)}{', '.join(folders)}{chr(10)}and files: {chr(10)}{chr(9)}{', '.join(files)}{chr(10)}from:{chr(10)}{chr(9)}{current_folder}? {chr(10)}{chr(10)}if YES, write 'y' if NO, write any other character:{chr(10)}")
        if delete == 'y' or delete == 'Y':
            # delete folder created by pyinstaller
            for folder in folders:
                shutil.rmtree(folder)
            for file in files:
                os.remove(file, dir_fd=None)
            print('\nThe folders and files were deleted.')
        else:
            print('\nNo file was deleted.')

    def slim_it(path):
        """Delete unnecessary local data from babel before zipping."""

        keep = "en.dat  en_001.dat  en_US.dat  en_US_POSIX.dat  root.dat"
        keep = keep.split()

        babel = os.path.join(path, 'dist', c('name'), 'babel', 'locale-data')
        # print(os.listdir(babel))
        for file in os.listdir(babel):
            if file not in keep:
                full_path = os.path.join(babel, file)
                os.remove(full_path, dir_fd=None)


    def delete_from(location):
        """Delete copied zip, unzipped folder, and shorcuts from `location`."""
        # print(winshell.desktop())
        # location = winshell.desktop()
        zip_file = os.path.join(location, f"{c('name')}.zip")
        folder =  os.path.join(location, c('name'))
        shortcut = os.path.join(location, f"{c('name')}.lnk")

        # To remove folders, use shutil.rmtree
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f'folder deleted: {folder}')
        else:
            print(f'folder does not exit: {folder}')

        # To remove files, use os.remove
        if os.path.exists(zip_file):
            os.remove(zip_file, dir_fd=None)
            print(f'file deleted: {zip_file}')
        else:
            print(f'file does not exit: {zip_file}')
        if os.path.exists(shortcut):
            os.remove(shortcut, dir_fd=None)
            print(f'file deleted: {shortcut}')
        else:
            print(f'file does not exit: {shortcut}')


    # PERSONAL DATA
    from my_scripts import my_env
    env = 'Multiplications'
    path_env = my_env(env)

    #### RUNNING

    """
    delete_from(desktop_path)
    delete_from(testing_path)
    delete_from(sharing_path)
    del_installations()
    """
    # create bat and run to pack the game
    pyinstall_bat(
        script, path, path_env=path_env,
        name=c('name'), icon_file=icon_file, onefile=c('onefile'),
        # other='--noconfirm',
        run=True)

    # Manually check whether the installation worked

    # if installation has been succsseful then proceed
    if not c('onefile'):

        install_vbs()
        # zip to share
        slim_it(path) # clean unnesseray files
        to_zip = os.path.join(path, 'dist')
        shutil.make_archive(c('name'), 'zip',  to_zip)

        # To desktop
        copy_zip_to(testing_path)
        unpacking_zip(testing_path)

        # For sharing
        copy_zip_to(dst = 'GameSharing')

