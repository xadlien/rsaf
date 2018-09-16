Program: rsaf.py
Author: Daniel Martin

Purpose:
  To create archives from files similarly to "tar". RSAF stands for
  "Really Stupid Archive Format". Please keep in mind this was meant as a
  project for me to see how python would compare to a C program I had written
  for a class. This code would be faster written in C. I translated the C
  code into a python equivalent. I was using this program to test out execution
  time. Thanks for your time.

How To Use:
  I have included three test files, test1, test2, and test3.

  To archive them you would run
    "python3 ./rsaf.py -a archive test*"

    In the above case, "archive is the output file"

  To extract the files you would run
    "python3 ./rsaf.py -x archive"

    This will create the files with the same names and data that you archived
    Note, you won't see any difference if you extract the files and you are in
    the same directory as the originals so I would recommend deleting the
    original test1, test2, test3. I will have a directory with the backups for
    you.

  To view a list of files from the archive run
    "python3 ./rsaf.py -l archive"

    This will list all files in the archive.
    You can also put a pattern after the archive and it will list all
    file names that match that pattern.

  For help run
    "python3 ./rsaf.py -h"

    This won't tell you much more than what I said here...
