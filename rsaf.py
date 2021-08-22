#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
#File Name: rsaf
#Author: Daniel Martin
#Date: 05/02/2015
#Purpose: Recreation of rsaf.c in python. This is finished and is about half the lines of the original written
#   in C. Note though that it is noticeably slower, not by much but if you're archiving huge files it will matter

import sys
import os
import struct
import getopt
import fnmatch

signature = "RSAF"

def main():

    #parse command line
    options, args = get_arguments()
    ARCHIVE = False
    EXTRACT = False
    LIST = False
    output_file_name = ""
    verbose = False
    for option in options:
        if option[0] == "-a" or option[0] == "--archive":
            ARCHIVE = True
            output_file_name = option[1]
        elif option[0] == "-l" or option[0] == "--list":
            LIST = True
            output_file_name = option[1]
        elif option[0] == "-x" or option[0] == "--extract":
            EXTRACT = True
            output_file_name = option[1]
        elif option[0] == "-h" or option[0] == "--help":
            print_usage()
            exit()
        elif option[0] == "-v" or option[0] == "--verbose":
            verbose = True

    #make sure options and arguments are acceptable
    ensure_functionality(ARCHIVE, EXTRACT, LIST)
    if EXTRACT:
        extract(args, output_file_name, verbose)
    elif ARCHIVE:
        archive(args, output_file_name, verbose)
    else:
        list(args, output_file_name)
    exit()

def get_arguments():
     return getopt.getopt(sys.argv[1:], 'a:l:x:vh', ['archive=', "list=", "extract=", "help", "verbose"])

def print_usage():
    print("""Usage: rsaf <options> <files>
    \t-a or --archive creates an archive from the list of files.
    \t      The first file listed will be the output archive.
    \t-l or --list    lists the files in a given archive
    \t-x or --extract extracts files from an archive
    \t-v or --verbose list files as they are processed
    \t-h or --help    prints this menu""")

def ensure_functionality(ARCHIVE, EXTRACT, LIST):
    if EXTRACT and LIST:
        print_usage()
        exit()
    elif EXTRACT and ARCHIVE:
        print_usage()
        exit()
    elif ARCHIVE and LIST:
        print_usage()
        exit()

def archive(args, output_file_name, verbose):
    #open output file
    try:
        outfile = os.open(output_file_name, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, int("0666", 8))
        if verbose:
            print("Opening", output_file_name)
    except FileNotFoundError:
        print(output_file_name, "not found")
        exit()
    i = 0
    hit = 0
    for pattern in args:
        #get path to directory
        path = pattern.split('/')
        pattern = path[-1]
        if len(path) == 1:
            path = "./"
        else:
            path = path[0:-1].join("/")
            path = path + "/"
        files = os.listdir(path)
        for file in files:
            #match files in directory
            if fnmatch.fnmatch(file, pattern):
                if verbose:
                    print("Archiving:", file)
                #increment file count
                hit = hit + 1
                infile = os.open(path + file, os.O_RDONLY)
                #while there is data, write to archive
                while True:
                    c = os.read(infile, 1)
                    if c:
                        os.write(outfile, c)
                        i = i + 1
                    else:
                        break
                #write out variables at end of file data
                os.write(outfile, bytes(file, 'ascii'))
                os.write(outfile, struct.pack(">Q", i))
                os.write(outfile, struct.pack(">H", len(file)))
                os.close(infile)
                i = 0
    #if there are files in the archive
    if hit:
        temp = struct.pack(">I", hit)
        os.write(outfile, temp)
    os.write(outfile, bytes(signature, 'ascii'))
    os.close(outfile)

def list(args, output_file_name):
    #open file
    try:
        listfile = os.open(output_file_name, os.O_RDONLY)
    except FileNotFoundError:
        print(output_file_name, " not found")
        exit()

    #if there are not arguments do *
    if len(args) == 0:
        args = ["*"]

    #go to the end of file
    os.lseek(listfile, -4, os.SEEK_END)

    #check for signature
    sigcheck = os.read(listfile, 4).decode('ascii')
    if sigcheck != signature:
        print(output_file_name, " is not an RSAF file")
        exit()

    #read number of files
    os.lseek(listfile, -8, os.SEEK_END)
    number_of_files = struct.unpack(">I", os.read(listfile, 4))

    #set up for loop
    os.lseek(listfile, -4, os.SEEK_CUR)

    #search archive for file names
    while True:
        #get file size
        os.lseek(listfile, -2, os.SEEK_CUR)
        file_name_size = struct.unpack(">H", os.read(listfile, 2))

        #go to file name
        os.lseek(listfile, -1 * (10 + file_name_size[0]), os.SEEK_CUR)

        #get file name
        file_name = os.read(listfile, file_name_size[0]).decode('ascii')

        #print file name if it matches a pattern
        for pattern in args:
            if fnmatch.fnmatch(file_name, pattern):
                print(file_name)
                break

        #get length of file to bypass
        file_size = struct.unpack(">Q", os.read(listfile, 8))

        #bypass file data
        pos = os.lseek(listfile, -1 * (8 + file_name_size[0] + file_size[0]), os.SEEK_CUR)

        #check if we are at beginning at file
        if pos == 0:
            break

def extract(args, output_file_name, verbose):
    #open file
    try:
        listfile = os.open(output_file_name, os.O_RDONLY)
        if verbose:
            print("Opening", output_file_name)
    except FileNotFoundError:
        print(output_file_name, " not found")
        exit()

    #if there are not arguments do *
    if len(args) == 0:
        args = ["*"]

    #go to the end of file
    os.lseek(listfile, -4, os.SEEK_END)

    #check for signature
    sigcheck = os.read(listfile, 4).decode('ascii')
    if sigcheck != signature:
        print(output_file_name, " is not an RSAF file")
        exit()

    #read number of files
    os.lseek(listfile, -8, os.SEEK_END)
    number_of_files = struct.unpack(">I", os.read(listfile, 4))

    #set up for loop
    os.lseek(listfile, -4, os.SEEK_CUR)

    #search archive for file names
    while True:
        #get file size
        os.lseek(listfile, -2, os.SEEK_CUR)
        file_name_size = struct.unpack(">H", os.read(listfile, 2))

        #go to file name
        os.lseek(listfile, -1 * (10 + file_name_size[0]), os.SEEK_CUR)

        #get file name
        file_name = os.read(listfile, file_name_size[0]).decode('ascii')

        #get length of file
        file_size = struct.unpack(">Q", os.read(listfile, 8))

        #go to beginning of file data
        pos = os.lseek(listfile, -1 * (8 + file_name_size[0] + file_size[0]), os.SEEK_CUR)

        #if file name matches an expression recreate file
        for pattern in args:
            if fnmatch.fnmatch(file_name, pattern):
                if verbose:
                    print("Remaking", file_name)
                refile = os.open(file_name, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, int("0666", 8))
                keeper = 0
                while keeper != file_size[0]:
                    char = os.read(listfile, 1)
                    os.write(refile, char)
                    keeper = keeper + 1
                os.close(refile)
                os.lseek(listfile, -1 * file_size[0], os.SEEK_CUR)
                break

        #check if we are at beginning at file
        if pos == 0:
            break

main()
