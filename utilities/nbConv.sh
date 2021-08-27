#!/bin/bash
# A bash script that converts python scripts in the working directory
# to notebook files in a subdirectory

# In order to use this, navigate to the directory containing the .py
# you wish to convert.
# The output will be in a $HOME subdirectory, which is /home/cdsw
# in most use cases.

# It is advised that you do not change the generated directory's name.
newDir="$HOME/convertedFiles"
echo $GIT_DIR

# Declares a function that converts a single file. If you specify a non-python
# file, the script will just skip it.
p2j_conv () {
  if [ "${1: -3}" == *.py ]; then
    p2j $1
  fi
}

# You can specify a single file or multiple files to convert on the command line.
# If you choose this option, it'll create a stand-in copy of each argument in the same directory.
# OR if you choose to provide a directory, we'll take that.
if [ -f "$1" ]; then
  while [ "$#" ]; do
    p2j_conv $1
    shift
  done
  exit 1;
elif [ -d "$1" ]; then
  dir=${1}
else
  dir=${PWD}
fi

# Otherwise, we'll just go through the di
# If you've run this script before, we don't want to overwrite any
# notebooks you've already edited.
if [ -d $newDir ];then
    for filename in ${dir}/*.py; do
        exists=false
        basename="${filename%.*}"
        basename="${basename##*/}"
        for compname in ${newDir}/*; do
            compbase="${compname##*/}"
            if [  "$basename.ipynb" == "$compbase" ]; then
                exists=true
                break
            fi
        done
        if [ $exists = false ]; then
            p2j $filename
            mv "${basename}.ipynb" $newDir
        fi
    done
# Otherwise, we create a new directory and inject all our new files.
else
    mkdir "${newDir}"
    for filename in ${PWD}/*.py; do
        basename="${filename%.*}"
        p2j $filename
        # chmod ugoa+wx "${basename}.ipynb"
        mv "${basename}.ipynb" $newDir
    done
fi
