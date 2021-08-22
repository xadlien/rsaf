# Really Stupid Archive Format
## Description
To create archives from files similarly to "tar". RSAF stands for
"Really Stupid Archive Format". Please keep in mind this was meant as a
project for me to see how python would compare to a C program I had written
for a class. This code would be faster written in C. I translated the C
code into a python equivalent. I was using this program to test out execution
time.
## Usage
To archive files you would run
`python3 ./rsaf.py -a archive file1 file2 ...`
In the above case, "archive is the output file"
  
To extract the files you would run
`python3 ./rsaf.py -x archive`
    
To view a list of files from the archive run
`python3 ./rsaf.py -l archive`

This will list all files in the archive.
You can also put a pattern after the archive and it will list all
file names that match that pattern.