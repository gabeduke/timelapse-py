#!/usr/bin/env python

import os
from sys import version_info
from cursesmenu import *
from cursesmenu.items import *
from subprocess import call
import pudb

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
direc = os.getcwd()
fps = str(420)
scale_4k = 'scale=-1:2160'
scale_hd = '1920:1080'


def jpgs_list():
    '''List the jpegs in directory to a file, formatted
    for ffmpeg to export.'''

    jpeg_files = list()

    for i in os.listdir(direc):
        file_type = os.path.splitext(i)[1]

        if file_type.lower() in (".jpg", ".jpeg"):
            jpeg_files.append(i)

    if not jpeg_files:
        return

    jpeg_files.sort()
    with open('files.txt', mode='wt') as myfile:
        myfile.write('\n'.join(jpeg_files))


def raws_list():
    '''List the RAW files in directory to a file, formatted
    for ffmpeg to export.'''

    raw_files = list()

    for i in os.listdir(direc):
        file_type = os.path.splitext(i)[1]

        if file_type.lower() == ".cr2":
            raw_files.append(i)

    if not raw_files:
        return

    raw_files.sort()
    with open('files.txt', mode='wt') as myfile:
        myfile.write('\n'.join(raw_files))


def menu():
    """Menu object for running the timelapse"""

    # create the menu object
    this_menu = CursesMenu("Timelapse Helper", "Menu")

    # create the menu items
    default = FunctionItem("Compile Timelapse", run)
    framerate = FunctionItem("Set framerate", set_fps)

    # build the menu
    this_menu.append_item(default)
    this_menu.append_item(framerate)

    # show the menu
    this_menu.show()


def set_fps():
    global fps
    if py3:
        fps = input("Enter new framerate: ")
    else:
        fps = raw_input("Enter new framerate: ")


def run():
    """Compile the timelapse."""

    fps
    scale_hd
    command = 'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=21600000 -o rendered.avi -mf type=jpeg:fps=%s mf://@files.txt -vf scale=%s' % (fps, scale)

    call(command, shell=True)


if __name__ == '__main__':
    """Entry point, scrape the directory for image files
    & save to global variable.
    """
    jpgs_list()
    raws_list()

    menu()
