# *
# ?
# []

# *.txt
# file.txt
# test.txt
# log.txt

# file?.txt
# file1.txt
# file2.txt
# fileb.txt
# filea.txt

# file??.txt
# file10.txt
# file11.txt
# file12.txt
# file20.txt


# file[ABC].txt
# fileA.txt < - O
# fileB.txt < - O
# fileC.txt < - O
# fileD.txt < - X


# file[A-F].txt
# fileA.txt < - O
# fileB.txt < - O
# fileF.txt < - O
# fileH.txt < - X
# fileZ.txt < - X

# file[A-Z].txt

# file[!A].txt
# fileA.txt < - X
# fileB.txt < - O
# fileF.txt < - O
# fileH.txt < - O
# fileZ.txt < - O

# file[A-D1-3].txt
# fileA.txt - fileD.txt  <- O
# file1.txt - file3.txt  <- O

# file[!A-D1-3].txt
# fileA.txt - fileD.txt  <- X
# file1.txt - file3.txt  <- X

# case_sensitive
# file[a].txt
# filea.txt <- O
# fileA.txt <- X